#!/usr/bin/env python3
"""
Find and remove duplicate People records in Attio where two records share
the same first name — one with only a first name (e.g. 'Azharul') and one
with a full name (e.g. 'Azharul Haque'). The partial-name record is deleted;
the full-name record is kept.

Run this ONCE after push_to_attio.py to clean up pre-existing orphan records.

Usage:
    ATTIO_API_KEY=<token> python3 tools/attio-ingest/cleanup_duplicates.py

Pass --dry-run to preview without deleting anything.
"""

import os, sys, json, time, urllib.request, urllib.error

ATTIO_TOKEN = os.environ.get("ATTIO_API_KEY", "")
if not ATTIO_TOKEN:
    sys.exit("ATTIO_API_KEY not set")

DRY_RUN    = "--dry-run" in sys.argv
ATTIO_BASE = "https://api.attio.com/v2"
WHEN_LIST_ID = "4bd161bd-2b58-4c11-9ee5-004257444bb2"

def attio_post(path, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{ATTIO_BASE}{path}", data=body,
        headers={"Authorization": f"Bearer {ATTIO_TOKEN}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def attio_delete(path):
    req = urllib.request.Request(
        f"{ATTIO_BASE}{path}",
        headers={"Authorization": f"Bearer {ATTIO_TOKEN}"},
        method="DELETE"
    )
    with urllib.request.urlopen(req) as r:
        return r.status

def fetch_all_people():
    return attio_post("/objects/people/records/query", {"limit": 500}).get("data", [])

def get_full_name(record):
    arr = record.get("values", {}).get("name", [])
    if arr and arr[0]:
        return (arr[0].get("full_name") or "").strip()
    return ""

# ── Main ───────────────────────────────────────────────────────────────────────

print("→ Fetching all Attio people...")
people = fetch_all_people()
print(f"   {len(people)} records found\n")

# Group by first name
by_first = {}
for r in people:
    full = get_full_name(r)
    if not full:
        continue
    first = full.split()[0].lower()
    by_first.setdefault(first, []).append(r)

# Find first names with multiple records
duplicates_found = 0
deleted = 0

for first, group in by_first.items():
    if len(group) < 2:
        continue

    # Sort: longer full_name = richer record = KEEP
    group.sort(key=lambda r: len(get_full_name(r)), reverse=True)
    keep   = group[0]
    remove = group[1:]

    keep_name   = get_full_name(keep)
    remove_names = [get_full_name(r) for r in remove]

    print(f"   DUPLICATE first name '{first}':")
    print(f"     KEEP   → '{keep_name}' (id: {keep['id']['record_id']})")
    for r, rname in zip(remove, remove_names):
        rid = r["id"]["record_id"]
        print(f"     DELETE → '{rname}' (id: {rid})")
        duplicates_found += 1

        if DRY_RUN:
            print(f"              [dry-run — not deleting]")
        else:
            try:
                attio_delete(f"/objects/people/records/{rid}")
                print(f"              ✓ deleted")
                deleted += 1
            except urllib.error.HTTPError as e:
                print(f"              ✗ HTTP {e.code}: {e.read().decode()[:100]}")
        time.sleep(0.3)
    print()

if duplicates_found == 0:
    print("✓ No duplicates found — Attio is clean.")
elif DRY_RUN:
    print(f"Dry run complete. {duplicates_found} record(s) would be deleted. Re-run without --dry-run to apply.")
else:
    print(f"━━━ Done: {deleted}/{duplicates_found} duplicate(s) deleted ━━━")
    if deleted > 0:
        print("\nRe-run push_to_attio.py to ensure all records are in the WHEN Travel list.")
