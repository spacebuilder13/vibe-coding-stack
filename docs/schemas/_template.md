# Schema: <Product Name>

> Copy this file to `docs/schemas/<product-slug>.md` and fill in. Follows the Bible: [`../crm-template.md`](../crm-template.md).

**Product purpose:** <one-sentence description of what this product does and who its clients are>

**Sink today:** <e.g. Attio (People + a list), HubSpot Contacts, Notion DB>

---

## Schema (machine-readable)

```yaml
product: <product-slug>
version: 1
description: |
  <2-3 sentences. What is this product? Who is the typical client?
  What kind of input do we receive about them?>

input_types:
  - call_transcript
  - whatsapp_export
  - meeting_notes
  # add others as needed: form_submission, voice_memo, video_notes

merge_strategy: most_recent_wins

fields:

  # ── IDENTITY (universal — keep these) ───────────────────────────────────────
  - slug: name
    title: "Name"
    type: text
    block: identity
    required: true
    description: "Client first name, or full name if both given"
    sink_mapping:
      attio: { object: people, attribute: name }

  - slug: phone
    title: "Phone"
    type: phone
    block: identity
    description: "Phone or WhatsApp number if mentioned"
    sink_mapping:
      attio: { object: people, attribute: phone_numbers }

  - slug: source_city
    title: "Source City"
    type: text
    block: identity
    description: "City the client lives in or is from"
    sink_mapping:
      attio: { object: people, attribute: source_city }

  # ── PSYCHOGRAPHIC — what they want and why ──────────────────────────────────
  # Add fields that capture the client's desires, motivations, JTBD,
  # trigger moments, identity goals.
  #
  # Example:
  # - slug: <slug>
  #   title: "<Display name>"
  #   type: text   # text | number | checkbox | select | url | phone | email
  #   block: psychographic
  #   description: "<what the LLM should extract and how>"
  #   sink_mapping:
  #     attio: { object: people, attribute: <attio_slug> }

  # ── BEHAVIORAL — where they are in the journey ──────────────────────────────
  # Add fields that capture state, stage, recent activity, milestones.

  # ── BLOCKERS — what is stopping them ────────────────────────────────────────
  # Add fields for financial / time / belief / circumstance blockers.

  # ── INTELLIGENCE (optional, derived by a second LLM pass) ───────────────────
  # Sentiment, recommended next action, predicted timeline, etc.

sink_targets:
  attio:
    object: people
    list_id: "<attio-list-id-for-this-product>"
    auto_add_to_list: true
```

---

## Notes for the human filling this in

1. **Keep identity block as-is.** It is the same for every product.
2. **Psychographic / Behavioral / Blocker** are the product-specific blocks. Spend time here.
3. **Start small.** 6–10 fields beats 50 broken ones. Add fields after the simpler set proves itself.
4. **Describe fields like you would brief a smart intern.** The LLM reads `description` verbatim.
5. **Use `select` for closed sets**, `text` for open language. Don't shoehorn open language into enums.
6. **Sink mapping is optional** — if a field isn't mapped, it's silently dropped at that sink. Useful for fields you want to extract but not yet write anywhere.
