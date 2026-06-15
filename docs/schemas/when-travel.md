# Schema: WHEN Travel

> The concrete CRM schema for WHEN Travel clients. Follows the Bible: [`../crm-template.md`](../crm-template.md).

**Product purpose:** WHEN Travel is a travel savings coaching platform in India. Clients are professionals saving for a dream trip. The CRM tracks their identity, what they want, where they are in the journey, and what is blocking them.

**Sink today:** Attio (People object + `WHEN Travel` list).

---

## Status

| Block          | Fields today | Target |
|----------------|--------------|--------|
| Identity       | 2            | 5      |
| Psychographic  | 3            | 12     |
| Behavioral     | 1            | 14     |
| Blockers       | 1            | 6      |
| Intelligence   | 0            | 18     |
| **Total**      | **7 + name** | **~55** |

Start small. Grow when the simpler set proves itself.

---

## Schema (machine-readable)

```yaml
product: when-travel
version: 1
description: |
  WHEN Travel coaches Indian professionals on saving for dream trips.
  Input is typically a Google Meet transcript (via Gemini Notes) or a
  WhatsApp export. Coach is Pooja Doshi.

input_types:
  - call_transcript
  - whatsapp_export
  - meeting_notes

merge_strategy: most_recent_wins   # multi-session inputs collapse to latest state

fields:

  # ── IDENTITY ────────────────────────────────────────────────────────────────
  - slug: name
    title: "Name"
    type: text
    block: identity
    description: "Client first name, or full name if both given"
    required: true
    sink_mapping:
      attio: { object: people, attribute: name }

  - slug: phone
    title: "Phone"
    type: phone
    block: identity
    description: "WhatsApp or phone number if mentioned; null otherwise"
    sink_mapping:
      attio: { object: people, attribute: phone_numbers }

  - slug: source_city
    title: "Source City"
    type: text
    block: identity
    description: "City the client lives in or is from"
    sink_mapping:
      attio: { object: people, attribute: source_city }

  # ── PSYCHOGRAPHIC — what they want ──────────────────────────────────────────
  - slug: time_to_travel
    title: "Time to Travel"
    type: text
    block: psychographic
    description: |
      When they want to travel. Free-form e.g. 'March 2026', 'in 6 months',
      'late April or early May'. Most recent mention wins.
    sink_mapping:
      attio: { object: people, attribute: trip_timeline }

  - slug: budget_range
    title: "Budget Range"
    type: text
    block: psychographic
    description: |
      Total trip budget as a string e.g. '1.5L', '80000', '3-5L'.
      Keep the client's own phrasing — do not convert units.
    sink_mapping:
      attio: { object: people, attribute: trip_budget }

  - slug: jtbd
    title: "JTBD"
    type: text
    block: psychographic
    description: |
      The transformation or value they want from this trip.
      Not the destination — the underlying job. E.g. 'recharge before MBA',
      'first international trip with family', 'guilt-free luxury'.
    sink_mapping:
      attio: { object: people, attribute: value_points }

  # ── BEHAVIORAL — where they are in the journey ──────────────────────────────
  - slug: journey_stage
    title: "Journey Stage"
    type: select
    block: behavioral
    description: "Most advanced stage reached"
    options:
      - "Discovery Done"     # first intake, no plan yet
      - "Plan Delivered"     # coach has sent a savings plan
      - "Active Saver"       # client actively tracking savings
      - "Milestone Unlocked" # flights or accommodation booked
      - "Trip Completed"     # trip has happened
    sink_mapping:
      attio: { object: people, attribute: journey_stage }

  # ── BLOCKERS — what is stopping them ────────────────────────────────────────
  - slug: blockers_pain_point
    title: "Blockers / Pain Point"
    type: text
    block: blocker
    description: |
      Main financial or emotional blocker(s). Synthesise across sessions
      — concise, one sentence, named blocker not vague feeling.
    sink_mapping:
      attio: { object: people, attribute: pain_points }

sink_targets:
  attio:
    object: people
    list_id: "4bd161bd-2b58-4c11-9ee5-004257444bb2"   # WHEN Travel
    auto_add_to_list: true
```

---

## Growth path (v2 → v3)

When the v1 set proves itself, expand toward the full 55-field map. Order of expansion:

1. **Psychographic depth** — travel preferences (beach / mountain / culture / city / off-beat), travel style (budget / mid / luxury), trigger moment, success visibility.
2. **Behavioral richness** — destination primary + alternative, trip type (solo / couple / family / group), milestones M1–M5 (flights / accommodation / food / activities / transport), booking details, calendly link, last contact, conversations count, next action.
3. **Financial state** — monthly savings capacity (number), already saving (bool), existing savings, savings instruments, cards owned.
4. **Engagement layer** — hot/cold, persona archetype, feedback quotes, key quotes, paid/amount/payment date.
5. **AI intelligence layer** — sentiment score, confidence score, follow-up priority, objection type, predicted booking timeline, AI coaching recommendation.

When adding fields: edit the YAML above and re-run `tools/attio-setup/create-fields.sh`. Code does not change.

---

## Worked example

Input: an 18k-char Gemini Notes transcript of Abhishek's discovery call.

Canonical output:
```json
{
  "name": "Abhishek Shankhdhar",
  "phone": null,
  "source_city": null,
  "time_to_travel": "October or November (end of year)",
  "budget_range": "2L",
  "jtbd": "Take a trip within 12 months by building disciplined savings through equity funds",
  "journey_stage": "Plan Delivered",
  "blockers_pain_point": "Fear of not taking trips; needs structured savings plan to make travel happen"
}
```

Sink action: upsert Attio People record → add to WHEN Travel list.
