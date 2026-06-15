#!/usr/bin/env python3
"""
Push pre-extracted CRM data to Attio People + add to WHEN Travel list.
Run this locally — no transcripts needed, no Claude call.

Usage:
    ATTIO_API_KEY=<token> python3 tools/attio-ingest/push_to_attio.py

Reads: tools/attio-ingest/crm_extracted.json
"""

import os, sys, json, time, urllib.request, urllib.error

ATTIO_TOKEN   = os.environ.get("ATTIO_API_KEY", "")
if not ATTIO_TOKEN:
    sys.exit("ATTIO_API_KEY not set")

SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_FILE     = os.path.join(SCRIPT_DIR, "crm_extracted.json")
WHEN_LIST_ID  = "4bd161bd-2b58-4c11-9ee5-004257444bb2"

if not os.path.exists(DATA_FILE):
    sys.exit(f"Not found: {DATA_FILE}")

ATTIO_BASE = "https://api.attio.com/v2"

def attio_post(path, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{ATTIO_BASE}{path}", data=body,
        headers={"Authorization": f"Bearer {ATTIO_TOKEN}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def attio_patch(path, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{ATTIO_BASE}{path}", data=body,
        headers={"Authorization": f"Bearer {ATTIO_TOKEN}", "Content-Type": "application/json"},
        method="PATCH"
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def fetch_all_people():
    return attio_post("/objects/people/records/query", {"limit": 500}).get("data", [])

def fetch_list_entry_ids():
    """Return set of record_ids already in the WHEN Travel list."""
    resp = attio_post(f"/lists/{WHEN_LIST_ID}/entries/query", {"limit": 500})
    ids = set()
    for entry in resp.get("data", []):
        try:
            ids.add(entry["record_id"])
        except (KeyError, TypeError):
            pass
    return ids

def add_to_when_list(record_id):
    attio_post(f"/lists/{WHEN_LIST_ID}/entries", {
        "data": {
            "parent_record_id": record_id,
            "parent_object": "people",
            "entry_values": {}
        }
    })

def find_existing(records, name):
    name_lower = (name or "").lower()
    for r in records:
        arr = r.get("values", {}).get("name", [])
        if arr and (arr[0].get("full_name") or "").lower() == name_lower:
            return r
    return None

def txt(v):
    return [{"value": str(v).strip()}] if v and str(v).strip() else None

def build_values(d):
    v = {}
    name = d.get("name", "").strip()
    if name:
        v["name"] = [{"first_name": name.split()[0], "last_name": " ".join(name.split()[1:]), "full_name": name}]

    for slug, val in [
        ("source_city",   d.get("source_city")),
        ("trip_timeline", d.get("time_to_travel")),
        ("trip_budget",   d.get("budget_range")),
        ("pain_points",   d.get("blockers_pain_point")),
        ("value_points",  d.get("jtbd")),
        ("journey_stage", d.get("journey_stage")),
    ]:
        t = txt(val)
        if t:
            v[slug] = t

    phone = d.get("phone")
    if phone and "@" not in str(phone) and str(phone).strip():
        v["phone_numbers"] = [{"phone_number": str(phone).strip(), "country_code": "IN"}]

    return v

# ── Main ───────────────────────────────────────────────────────────────────────

with open(DATA_FILE) as f:
    records = json.load(f)

print(f"→ Loading {len(records)} records from {DATA_FILE}")
print("→ Fetching existing Attio people...")
all_people = fetch_all_people()
print(f"   {len(all_people)} existing record(s)")

print("→ Fetching WHEN Travel list members...")
already_in_list = fetch_list_entry_ids()
print(f"   {len(already_in_list)} already in list\n")

ok = err = 0
for d in records:
    if d.get("error"):
        print(f"   SKIP   {d.get('name')} — extraction failed: {d['error']}")
        continue

    name   = d.get("name", "Unknown").strip()
    values = build_values(d)

    try:
        existing = find_existing(all_people, name)
        if not existing:
            resp = attio_post("/objects/people/records", {"data": {"values": values}})
            rid  = resp["data"]["id"]["record_id"]
            action = "CREATE"
        else:
            rid = existing["id"]["record_id"]
            attio_patch(f"/objects/people/records/{rid}", {"data": {"values": values}})
            action = "UPDATE"

        # Add to WHEN Travel list if not already there
        if rid not in already_in_list:
            try:
                add_to_when_list(rid)
                list_status = "+ list"
            except urllib.error.HTTPError as le:
                body = le.read().decode()
                # 409 = already in list (race condition) — safe to ignore
                list_status = "~ list (already exists)" if le.code == 409 else f"! list err {le.code}"
        else:
            list_status = "~ list (already in)"

        print(f"   {action:<6} {name}  [{list_status}]")
        ok += 1

    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"   ERROR  {name} — HTTP {e.code}: {body[:200]}")
        err += 1

    time.sleep(0.3)

print(f"\n━━━ Done: {ok} written  {err} errors ━━━")
