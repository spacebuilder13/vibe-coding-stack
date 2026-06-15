#!/usr/bin/env bash
# Create all WHEN Travel CRM fields on the Attio People object.
#
# Usage:
#   ATTIO_API_KEY=<token> bash tools/attio-setup/create-fields.sh
#
# Safe to re-run — already-existing fields are detected (HTTP 409) and skipped.

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

# (title, api_slug, type)
# Standard Attio People fields (name, email, phone) are intentionally excluded.
FIELDS = [
    # ── G1 Identity ────────────────────────────────────────────────────────────
    ("Source",                    "source",                "text"),
    ("Latest Conversation",       "latest_conversation",   "text"),

    # ── G2 Travel Preferences ──────────────────────────────────────────────────
    ("Pref: Beach",               "pref_beach",            "checkbox"),
    ("Pref: Mountain",            "pref_mountain",         "checkbox"),
    ("Pref: Culture",             "pref_culture",          "checkbox"),
    ("Pref: Unique / Off-beat",   "pref_unique",           "checkbox"),
    ("Pref: City",                "pref_city",             "checkbox"),
    ("Travel Style",              "travel_style",          "text"),
    ("Trip Budget",               "trip_budget",           "text"),

    # ── G3 Financial ───────────────────────────────────────────────────────────
    ("Monthly Savings Capacity",  "monthly_savings",       "number"),
    ("Already Saving?",           "already_saving",        "checkbox"),
    ("Existing Savings",          "existing_savings",      "text"),
    ("Savings Instruments",       "savings_instruments",   "text"),
    ("Cards Owned",               "cards_owned",           "text"),

    # ── G4 Blockers ────────────────────────────────────────────────────────────
    ("Blocker: No Money",         "blocker_no",            "checkbox"),
    ("Blocker: Unsure",           "blocker_unsure",        "checkbox"),
    ("Blocker: Key Concern",      "blocker_key",           "checkbox"),
    ("Blocker: Date Uncertainty", "blocker_date",          "checkbox"),
    ("Blocker: Already Planned",  "blocker_already",       "checkbox"),
    ("Blocker: Other",            "blocker_other",         "text"),

    # ── G5 Current Trip ────────────────────────────────────────────────────────
    ("Destination (Primary)",     "destination_primary",   "text"),
    ("Destination (Alternative)", "destination_alternative","text"),
    ("Trip Timeline",             "trip_timeline",         "text"),
    ("Trip Type",                 "trip_type",             "text"),
    ("Booking Details",           "booking_details",       "text"),
    ("Calendly Link",             "calendly_link",         "text"),

    # ── G6 Milestones ──────────────────────────────────────────────────────────
    ("M1: Flights Booked",        "m1_flights",            "checkbox"),
    ("M2: Accommodation Booked",  "m2_accommodation",      "checkbox"),
    ("M3: Food Budget Set",       "m3_food",               "checkbox"),
    ("M4: Activities Planned",    "m4_activities",         "checkbox"),
    ("M5: Transport Sorted",      "m5_transport",          "checkbox"),
    ("Miscellaneous Notes",       "miscellaneous",         "text"),
    ("Trigger Moment",            "trigger_moment",        "text"),
    ("Confidence Score",          "confidence_score",      "number"),
    ("Success Visibility",        "success_visibility",    "text"),

    # ── G7 JTBD ────────────────────────────────────────────────────────────────
    ("Value Points (JTBD)",       "value_points",          "text"),
    ("Pain Points",               "pain_points",           "text"),

    # ── G8 Engagement ──────────────────────────────────────────────────────────
    ("Paid?",                     "paid",                  "checkbox"),
    ("Amount Paid",               "amount",                "number"),
    ("Payment Date",              "payment_date",          "text"),
    ("Hot / Cold",                "hot_cold",              "text"),
    ("Journey Stage",             "journey_stage",         "text"),
    ("Persona",                   "persona",               "text"),
    ("Last Contact",              "last_contact",          "text"),
    ("No. of Conversations",      "conversations",         "number"),
    ("Next Action",               "next_action",           "text"),
    ("Action Owner",              "action_owner",          "text"),
    ("Feedback Quote",            "feedback_quote",        "text"),
    ("Key Quotes",                "key_quotes",            "text"),
    ("Link to Conversations",     "link_to_conversations", "text"),

    # ── G9 Actions & Intelligence ──────────────────────────────────────────────
    ("AI Recommendation",         "ai_recommendation",     "text"),
    ("Follow-Up Priority",        "follow_up_priority",    "text"),
    ("Sentiment Score",           "sentiment_score",       "number"),
    ("Objection Type",            "objection_type",        "text"),
    ("Predicted Conversion",      "predicted_timeline",    "text"),
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

    time.sleep(0.15)  # stay well under Attio rate limit

print("")
print(f"━━━ Done: {created} created  {skipped} skipped  {failed} failed ━━━")
PYEOF
