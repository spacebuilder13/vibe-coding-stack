# B2B Client Bootstrap Workflow

Checklist for onboarding a new B2B client engagement pod (derived from project-om-shanti, 2026-05-24).

## Phase 0 — Kickoff

- [ ] Create `project-{client-slug}` under Builder
- [ ] Write `PROGRAM.md` (2–3 line brief)
- [ ] Init `docs/STACK_DELTA.md` for vibe-coding-stack feedback
- [ ] Private GitHub repo + `.gitignore` + `.env.example`

## Phase 1 — Knowledge

- [ ] Register NLM notebook in `.env` as `NOTEBOOKLM_TRANSCRIPT_NOTEBOOK_ID`
- [ ] Verify auth: `notebooklm list`
- [ ] Run meta-query protocol (Brief → Overview → Open questions)
- [ ] Run synthesis batch (Q1–Q6 style) — **sequential only**
- [ ] Write `knowledge/{client}_source_index.md`
- [ ] Write `knowledge/stakeholder_brief.md`
- [ ] Register hub in `vibe-coding-stack/registry/hubs.json`

## Phase 2 — Design

- [ ] Capture design inspiration (Mobbin via browser MCP, or Magic Patterns URL)
- [ ] Write `knowledge/brand_guidelines.md`
- [ ] Human visual approval gate before production code

## Phase 3 — Build

- [ ] Write `BUILD.md` (routes, stack, env)
- [ ] Scaffold app (Vite + React recommended for deck-ready projects)
- [ ] Transcript-backed copy only; label inferences

## Phase 4 — Deploy

- [ ] `npm run build` passes
- [ ] Vercel deploy
- [ ] Register in `app-store/STORE.md`
- [ ] `scripts/context_test.sh` passes

## Phase 5 — Handoff

- [ ] `AGENTS.md` + `CLAUDE.md` with first-reads order
- [ ] Batch-merge `STACK_DELTA.md` to vibe-coding-stack

## Confidentiality

Never commit raw client transcripts to public vibe-coding-stack. Hub entry points to private repo only.
