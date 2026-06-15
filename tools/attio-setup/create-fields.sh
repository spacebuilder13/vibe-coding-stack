#!/usr/bin/env bash
# Create WHEN Travel CRM fields on the Attio People object (simplified 8-field set).
#
# Usage:
#   ATTIO_API_KEY=<token> bash tools/attio-setup/create-fields.sh
#
# Safe to re-run — already-existing fields (HTTP 409) are silently skipped.

set -e

ATTIO_TOKEN="${ATTIO_API_KEY:?ATTIO_API_KEY must be set}"
ATTIO_BASE="https://api.attio.com/v2"

echo "→ Creating WHEN Travel CRM fields on Attio People object"
echo ""

python3 - "$ATTIO_TOKEN" "$ATTIO_BASE" <<'PYEOF'
import sys, json, time
import urllib.request
import urllib.error

token, base_url = sys.argv[1], sys.argv[2]

# Standard Attio People fields (name, email_addresses, phone_numbers) are skipped —
# they already exist. We only create custom fields.
FIELDS = [
    # title                         api_slug              type
    # ── v1 fields ──────────────────────────────────────────────────────────────
    ("Source City",                 "source_city",        "text"),
    ("Time to Travel",              "trip_timeline",      "text"),
    ("Budget Range",                "trip_budget",        "text"),
    ("JTBD (Functional)",           "value_points",       "text"),
    ("Blockers / Pain Point",       "pain_points",        "text"),
    ("Journey Stage",               "journey_stage",      "text"),
    # ── v2 fields (richer qualitative extraction) ───────────────────────────────
    ("JTBD (Emotional)",            "jtbd_emotional",     "text"),
    ("Blocker Type",                "blocker_type",       "text"),
    ("Memorable Quote",             "memorable_quote",    "text"),
]

created = skipped = failed = 0

for title, slug, ftype in FIELDS:
    payload = json.dumps({
        "data": {
            "title": title,
            "api_slug": slug,
            "type": ftype,
            "is_required": False
        }
    }).encode()

    req = urllib.request.Request(
        f"{base_url}/objects/people/attributes",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req):
            created += 1
            print(f"   ✓  {title} ({slug})")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if e.code == 409 or "already_exists" in body or "already exists" in body.lower():
            skipped += 1
            print(f"   ~  {title} — already exists, skipped")
        else:
            failed += 1
            print(f"   ✗  {title} — HTTP {e.code}: {body[:200]}")

    time.sleep(0.15)

print("")
print(f"━━━ Done: {created} created  {skipped} skipped  {failed} failed ━━━")
PYEOF
