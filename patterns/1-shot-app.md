# Pattern: 1-Shot App Build

From a 2-3 line brief on Android to a deployed web app in a single conversation.

## The pipeline

```
Human types brief (2–3 lines)
        ↓
Fill PROGRAM.md template
        ↓
Route → which domains needed?
        ↓
Load domain docs (only relevant ones)
        ↓
Write BUILD.md → human reviews
        ↓
Visual approval gate (design direction)
        ↓
Build code per BUILD.md
        ↓
/qa → fix loop
        ↓
/ship → Vercel → URL
        ↓
Register in app-store/STORE.md
```

## Step 1: Fill PROGRAM.md

Parse the brief into the PROGRAM.md template sections.
If anything is ambiguous (auth? payments? voice?), ask once before proceeding.
If the brief is clear enough, fill it and confirm with the human before step 2.

## Step 2: Route domains

From PROGRAM.md, determine which domains to load:
- Has auth → `security.md` + `deployment.md` (Supabase)
- Has payments → `payments.md` + `legal.md`
- Has voice → `voice.md`
- Has analytics → `analytics.md`
- Always: `design.md` + `coding.md` + `testing.md` + `deployment.md`

## Step 3: Write BUILD.md

Write the spec. Human reviews before any code is written.
Build.md is a contract — don't deviate from it without flagging the change.

## Step 4: Visual approval gate

Before writing a single line of UI code:
- State the design direction (A/B/C/D or custom)
- Describe the key visual decisions (tokens, font, accent)
- Get explicit human confirmation

## Step 5: Build

Write code per BUILD.md. Reuse shared libs from registry before writing new ones.
For Vercel apps: start with `api/_lib/anthropic.js` + `vercel.json`.

## Step 6: QA

Run `/qa`. Fix what it finds. Rerun until pass.
For visual UIs: screenshot key states, score on the 5 axes (see `domains/testing.md`).

## Step 7: Ship

`/ship` → PR → merge → Vercel deploys automatically.
Confirm URL is live. Add to `app-store/STORE.md`.

## Timing guidance

| Phase | Target |
|-------|--------|
| PROGRAM.md fill | < 2 min |
| BUILD.md write | < 5 min |
| Design approval | 1 round |
| Code write | single conversation |
| QA pass | ≤ 2 iterations |
| Ship + register | < 5 min |

## What makes a 1-shot build succeed

1. Brief is specific enough (struggling moment, not a feature list)
2. Design direction decided upfront (no mid-build pivots)
3. Scope is locked in BUILD.md before code starts
4. No scope creep during build — new ideas go into the next PROGRAM.md
