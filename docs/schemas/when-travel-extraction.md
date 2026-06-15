# Extraction Intelligence: WHEN Travel

> **This is the brain. Edit this file to evolve what we understand about clients.**
> No code changes needed — the extraction script reads the prompt block below directly.

---

## What this file does

Raw client conversations (Gemini transcripts, WhatsApp exports, call notes) come in as messy text. This file defines how that text becomes structured CRM intelligence. It contains two things:

1. **Human documentation** — field definitions, examples, anti-examples, and emerging segment patterns. For Pooja and the team to read, debate, and refine.
2. **The machine-readable prompt** (the fenced `system_prompt` block at the bottom) — what Claude actually receives. The code reads *only* that block.

---

## How to evolve this file

- **Refine a field's extraction** → update its description inside the `system_prompt` block.
- **Add a new field** → add it to Field Definitions below, then add it to the `system_prompt` JSON, then add it to `tools/attio-setup/create-fields.sh` and re-run that script.
- **Add a segment pattern** → add it to the Segments section. This is for your analysis — it doesn't affect extraction.
- **Never rename a field slug** without also updating `push_to_attio.py` and the Attio attribute slug. They must match.

---

## Field Definitions

### Identity fields
These are factual. Claude finds or returns null.

| Field | What it captures |
|-------|-----------------|
| `name` | First name or full name. Whatever is used most in the conversation. |
| `phone` | Phone / WhatsApp number. Not email. |
| `source_city` | City they live in. Look for "I'm in Mumbai", "based in Bangalore". |

### Psychographic fields
These require inference, not just extraction. The quality of these fields is what makes the CRM intelligent.

---

#### `jtbd_functional` — What they want to DO

The concrete trip outcome. Destination + who is going + rough timing. Think of it as the ticket stub — what would be written on it.

**Good examples:**
- "Solo trip to Japan, October 2026"
- "Family of 3 to Dubai, August 2026, about 2 weeks"
- "Parents' Sri Lanka Buddhist circuit, November 2026, 7 days, private driver"

**What it is NOT:** Why the trip matters to them. That is `jtbd_emotional`.

---

#### `jtbd_emotional` — Why it matters / What they want to FEEL or BECOME

This is the job beneath the job. Not the destination — the identity shift or emotional state the trip represents. This is where the real coaching signal is.

**How to find it:** Ask yourself — if this trip never happened, what would they have lost beyond the holiday itself?

**Signals to look for:** pride, freedom, guilt-free spending, reconnection with someone, proving something to themselves, becoming a certain kind of person, making someone else's dream happen.

**Strong examples from actual clients:**
- *"Prove to herself she can travel debt-free without touching UK savings"* — Baani
- *"Be the daughter who made her parents' honeymoon 2.0 happen"* — Tanya
- *"Feel like someone whose finances are sorted and who can still enjoy life"* — Surej
- *"Recharge before MBA — one last trip as a student, not as a professional"* — Sarthak

**Anti-examples (functional, not emotional — these belong in jtbd_functional):**
- "Go to Switzerland for an anniversary" ← this is the destination
- "Family trip to Dubai" ← this is the ticket

**Return null** if the transcript has no emotional signal — don't invent one.

---

#### `blocker_type` — Category of the primary blocker

Exactly one of five types. Choose the single most dominant one.

| Type | What it means | Signal phrases |
|------|--------------|----------------|
| `financial` | Money is the explicit stated reason | "I don't have enough", "can't afford it right now" |
| `belief` | Has money but feels wrong to spend it | "feel guilty", "seems irresponsible", "should be saving not spending", "what will people think" |
| `timing` | Cannot commit to dates | "job is uncertain", "don't know when I can take leave", "waiting for things to settle", "life is in flux" |
| `circumstance` | External life event is in the way | "new baby", "EMI starting", "job change", "no passport yet", "visa uncertainty" |
| `family` | Requires coordination with someone else | "partner's schedule", "parents' health", "kids' school calendar", "husband won't agree" |

**The distinction that matters most:** `financial` vs `belief`. A client who says "I don't have money" needs a savings plan. A client who says "I feel guilty spending on myself" has money but needs permission. The coaching response is completely different. Get this right.

---

#### `blocker_description` — Their specific words

Not a summary. As close to verbatim as possible. The sentence or phrase they actually used. If they said *"I feel guilty spending on myself when I should be saving for the future"* — write that, not "guilt about spending."

This field is what coaches use to remember the conversation and personalise follow-up.

---

#### `memorable_quote` — The line that would make Pooja remember them

The single most emotionally resonant thing the client said across all sessions. Verbatim. Not Pooja's words — the client's words.

Look for: a moment of vulnerability, excitement, fear, sudden clarity, or self-awareness. Something that reveals who they are beyond the trip.

**Good examples:**
- *"Really grateful to you for helping me make a dream come true"* — Tanya
- *"Until now this trip was a maybe, but I want to make it certain"*
- *"I feel like I've been postponing life"*

**Not:** logistics, numbers, dates. Those are functional.

---

#### `journey_stage` — Where they are in the WHEN Travel journey

The most advanced stage reached across all sessions.

| Stage | Definition | Key signal |
|-------|-----------|------------|
| Discovery Done | First intake call has happened. No plan delivered yet. | Call happened, Pooja is still understanding the client. |
| Plan Delivered | Pooja has shared a savings plan (spreadsheet, WhatsApp message, or mentioned it on the call). | "I've shared the plan", client receives a Google Sheet link. |
| Active Saver | Client has started depositing money toward the trip. | "I did the 5k", "invested this month", "done". |
| Milestone Unlocked | Flights or accommodation actually booked. | "booked the flights", "we have the hotel". |
| Trip Completed | Trip has happened. | Past tense references to the trip. |

---

## Emerging Segments

*Update this section as patterns appear. Use it to identify which JTBDs convert fastest, which segments need different coaching, and where to focus.*

### Observed so far — v1, 14 clients (June 2026)

**The Guilt-Free Seeker**
Has the money. Blocked by belief ("feels irresponsible to spend on myself"). Needs a permission slip + financial proof that this is responsible. Once they have it, they move fast.
Clients: Baani, Urvashi, possibly Surej.

**The Family Enabler**
Doesn't travel primarily for themselves — travels to give someone else an experience (parents, partner, child). High emotional stake. The trip is an act of love, not self-care.
Clients: Tanya (parents), Deepak (wife + baby), Rakesh (parents).

**The Milestone Chaser**
Triggered by a life transition (MBA, new job, wedding, turning 30). Clear deadline. Urgency is built-in. Converts fast because the window is finite.
Clients: Sarthak (pre-MBA), Akanksha (honeymoon).

**The Serial Planner**
Already thinking about 3+ destinations simultaneously. High engagement, long decision cycle. Needs help narrowing and sequencing, not inspiration.
Clients: Paarth.

**The Anxious Executor**
Wants to travel, has started saving, but keeps second-guessing — dates, instruments, allocation, "what if". Needs reassurance and structure more than information.
Clients: Shruthi, Urvashi.

---
<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- CODE READS ONLY THIS BLOCK — edit the prompt here, not in any script  -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->

```system_prompt
You are processing coaching call transcripts and WhatsApp conversations for WHEN Travel, a travel savings coaching platform in India. The coach is Pooja Doshi.

Multiple sessions may be provided — synthesise across all of them and return the MOST CURRENT state of each field. Most recent mention wins for factual fields. For qualitative fields, synthesise the richest signal across all sessions.

Return ONLY a valid JSON object. No markdown. No preamble. No explanation outside the JSON.

{
  "name": "Client first name or full name. Use whatever is used most consistently across the conversation.",

  "phone": "Phone or WhatsApp number if explicitly mentioned. NOT email. null if not found.",

  "source_city": "City they live in or are from. Look for phrases like 'I am in Mumbai', 'based in Bangalore', 'I live in Gurgaon'. null if not mentioned.",

  "time_to_travel": "When they want to travel. Keep their phrasing exactly — 'March 2026', 'end of year', 'in 6 months', 'late April or early May'. Most recent mention wins. null if not mentioned.",

  "budget_range": "Total trip budget. Keep their phrasing and units — '1.5L', '80,000', '3 to 5L', '1,11,000'. Do not convert or round. null if not mentioned.",

  "jtbd_functional": "What they want to DO: the concrete trip. Include destination, who is going, and rough timing. Think of it as what would be on a ticket stub. E.g. 'Solo trip to Japan, October 2026' or 'Family of 3 to Dubai, August 2026' or 'Parents to Sri Lanka, November 2026, 7 days with private driver'. Do not include why it matters — that goes in jtbd_emotional.",

  "jtbd_emotional": "What they want to FEEL or BECOME through this trip. The identity shift or emotional state the trip represents — not the destination. Ask yourself: if this trip never happened, what would they have lost beyond the holiday? Look for signals of pride, freedom, guilt-free spending, reconnection, proving something to themselves, making someone else's dream happen, or becoming a certain kind of person. Write it as a statement about them: 'Prove to herself she can travel debt-free', 'Be the daughter who made her parents dream come true', 'Feel like someone whose finances are sorted and who still enjoys life'. Return null if no emotional signal is present in the transcript — do not invent.",

  "blocker_type": "The single primary category of what is blocking them. Exactly one of: financial | belief | timing | circumstance | family. financial = money is the explicit stated reason. belief = has money but feels guilty or irresponsible spending it — the blocker is internal not factual. timing = cannot commit to dates due to job or life uncertainty. circumstance = a specific external event is blocking (new baby, EMI starting, no passport, visa issue, job change). family = requires coordination with someone else whose schedule or agreement is not in place. Choose the one that best describes the ROOT cause, not the symptom.",

  "blocker_description": "Their specific words about the blocker — as close to verbatim as possible. Not a summary or paraphrase. If they said 'I feel guilty spending on myself when I should be saving for the future', write exactly that. null if no blocker is present in the transcript.",

  "memorable_quote": "The single most emotionally resonant thing the CLIENT said across all sessions. Copy the exact words from the transcript — do not paraphrase, summarise, or rewrite. Not Pooja's words — only the client's own words. Look for vulnerability, excitement, fear, sudden self-awareness, or a moment of clarity. If no verbatim client quote stands out, return null — do not invent or summarise.",

  "journey_stage": "The MOST ADVANCED stage reached across all sessions. Exactly one of: Discovery Done | Plan Delivered | Active Saver | Milestone Unlocked | Trip Completed. Discovery Done = first intake call completed, no plan yet shared. Plan Delivered = Pooja has shared a savings plan (spreadsheet link, WhatsApp plan message, or confirmed on call). Active Saver = client has actually deposited money toward the trip fund (they confirmed a transfer or Pooja confirmed receipt). Milestone Unlocked = flights or accommodation are actually booked and confirmed. Trip Completed = trip has happened, spoken about in past tense."
}
```

<!-- ═══════════════════════════════════════════════════════════════════════ -->
<!-- END PROMPT                                                             -->
<!-- ═══════════════════════════════════════════════════════════════════════ -->
