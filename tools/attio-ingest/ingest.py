#!/usr/bin/env python3
"""
WHEN Travel — Transcript → Attio ingest (direct, no n8n)

Usage:
    ANTHROPIC_API_KEY=sk-ant-...  ATTIO_API_KEY=103...  python3 tools/attio-ingest/ingest.py <folder>

<folder> should contain plain-text transcript files (.txt).
Export Google Docs as plain text from Drive: File → Download → Plain text (.txt)

Fields extracted (8):
    name, phone, source_city, time_to_travel, budget_range,
    blockers_pain_point, jtbd, journey_stage
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ATTIO_TOKEN   = os.environ.get("ATTIO_API_KEY", "")

if not ANTHROPIC_KEY:
    sys.exit("ANTHROPIC_API_KEY not set")
if not ATTIO_TOKEN:
    sys.exit("ATTIO_API_KEY not set")

ATTIO_BASE    = "https://api.attio.com/v2"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"

SYSTEM_PROMPT = """\
You are processing call transcripts and WhatsApp exports for WHEN Travel, \
a travel savings coaching platform based in India. \
Return ONLY a valid JSON object — no markdown, no preamble.

{
  "name": "client first name",
  "phone": "phone/WhatsApp number if mentioned, else null",
  "source_city": "city they are from if mentioned, else null",
  "time_to_travel": "when they want to travel e.g. 'March 2026' or '6 months', else null",
  "budget_range": "total trip budget as a string e.g. '1.5L' or '80000', else null",
  "blockers_pain_point": "their main financial or emotional blocker, else null",
  "jtbd": "the transformation or value they want from this trip, else null",
  "journey_stage": "one of: Discovery Done | Plan Delivered | Active Saver | Milestone Unlocked | Trip Completed"
}

Journey stage rules:
- Discovery Done: first intake call, no plan delivered yet
- Plan Delivered: coach mentioned or sent a savings plan
- Active Saver: client actively tracking savings
- Milestone Unlocked: flights or accommodation booked
- Trip Completed: trip has already happened\
"""


def call_claude(text: str) -> dict:
    body = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 512,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": text[:6000]}]
    }).encode()

    req = urllib.request.Request(
        ANTHROPIC_URL,
        data=body,
        headers={
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        result = json.load(resp)

    raw = result["content"][0]["text"].strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def attio_get(path: str) -> dict:
    req = urllib.request.Request(
        f"{ATTIO_BASE}{path}",
        headers={"Authorization": f"Bearer {ATTIO_TOKEN}"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def attio_post(path: str, payload: dict) -> dict:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{ATTIO_BASE}{path}",
        data=body,
        headers={
            "Authorization": f"Bearer {ATTIO_TOKEN}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def attio_patch(path: str, payload: dict) -> dict:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{ATTIO_BASE}{path}",
        data=body,
        headers={
            "Authorization": f"Bearer {ATTIO_TOKEN}",
            "Content-Type": "application/json"
        },
        method="PATCH"
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def build_attio_values(d: dict, person_name: str) -> dict:
    def txt(v):
        return [{"value": str(v).strip()}] if v and str(v).strip() else None

    values = {}
    if person_name:
        values["name"] = [{"first_name": person_name, "last_name": "", "full_name": person_name}]

    for slug, val in [
        ("source_city",        d.get("source_city")),
        ("trip_timeline",      d.get("time_to_travel")),
        ("trip_budget",        d.get("budget_range")),
        ("pain_points",        d.get("blockers_pain_point")),
        ("value_points",       d.get("jtbd")),
        ("journey_stage",      d.get("journey_stage")),
    ]:
        t = txt(val)
        if t:
            values[slug] = t

    # phone goes on the standard email_addresses / phone_numbers attribute
    phone = d.get("phone")
    if phone and str(phone).strip():
        values["phone_numbers"] = [{"phone_number": str(phone).strip(), "country_code": "IN"}]

    return values


def fetch_all_people() -> list:
    result = attio_post("/objects/people/records/query", {"limit": 500})
    return result.get("data", [])


def find_existing(records: list, name: str) -> dict | None:
    name_lower = (name or "").lower()
    for r in records:
        arr = r.get("values", {}).get("name", [])
        if arr and (arr[0].get("full_name") or "").lower() == name_lower:
            return r
    return None


def process_file(filepath: str, all_people: list) -> str:
    filename = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    if len(text.strip()) < 50:
        return f"   SKIP  {filename} (too short)"

    extracted = call_claude(text)
    fallback  = filename.split("_Session")[0].replace("_", " ").strip()
    name      = (extracted.get("name") or fallback or "").strip()

    values  = build_attio_values(extracted, name)
    payload = {"data": {"values": values}}

    existing = find_existing(all_people, name)

    if not existing:
        resp = attio_post("/objects/people/records", payload)
        record_id = resp["data"]["id"]["record_id"]
        return f"   CREATE {filename} → {name} (id: {record_id})"
    else:
        record_id = existing["id"]["record_id"]
        attio_patch(f"/objects/people/records/{record_id}", payload)
        return f"   UPDATE {filename} → {name} (id: {record_id})"


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 ingest.py <transcripts-folder>")

    folder = sys.argv[1]
    if not os.path.isdir(folder):
        sys.exit(f"Not a directory: {folder}")

    files = sorted(
        f for f in os.listdir(folder)
        if f.lower().endswith(".txt") and not f.startswith(".")
    )

    if not files:
        sys.exit(f"No .txt files found in {folder}")

    print(f"→ Found {len(files)} transcript(s) in {folder}")
    print("→ Fetching existing Attio people...")
    all_people = fetch_all_people()
    print(f"   {len(all_people)} existing record(s)")
    print("")

    ok = err = 0
    for fname in files:
        fpath = os.path.join(folder, fname)
        try:
            msg = process_file(fpath, all_people)
            print(msg)
            ok += 1
        except Exception as e:
            print(f"   ERROR {fname}: {e}")
            err += 1
        time.sleep(0.5)  # rate limit courtesy

    print("")
    print(f"━━━ Done: {ok} processed  {err} errors ━━━")


if __name__ == "__main__":
    main()
