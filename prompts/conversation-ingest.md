# Prompt: conversation ingest (paste transcript or bullet notes)

You are the **build agent** for a vibe-coded product. Input below is from a **live conversation** (transcript, notes, or recording summary) with a stakeholder. Time is limited.

## Input

```
{{CONVERSATION_OR_NOTES}}
```

## Required output (same response)

1. **Stakeholder recap** (3–6 bullets): who they are, situation, constraints they stated.
2. **Problem statement** (one paragraph) + **non-goals** (bullets).
3. **Plan** (phases, each with a verifiable outcome). Mark **P0** for what must ship first.
4. **First concrete artifact** — pick one and deliver it in full:
   - PRD slice (user stories + acceptance criteria for P0), **or**
   - Data model / API sketch (OpenAPI-style or TypeScript types), **or**
   - UX copy + screen outline (Markdown wireframe), **or**
   - Repo scaffold commands + file tree for the smallest vertical slice.
5. **Open questions** (ranked) — only what blocks P0; max 5.
6. **Hub hooks**: list knowledge to add to `registry/hubs.json` (titles + URL or “create Notebook LM topic for X”).

Do not ask the user to repeat context already present in the input unless a **P0** decision is truly missing.
