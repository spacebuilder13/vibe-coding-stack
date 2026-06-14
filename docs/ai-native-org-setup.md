# AI-native org setup

Zen Money Studio operating model. vibe-coding-stack is the **meta harness** — the org OS, not any single client repo.

## Layers

| Layer | Who | What | Repo |
|-------|-----|------|------|
| **Meta** | Utsav | Harness design, stack evolution, model routing | `vibe-coding-stack` |
| **Harness** | Shared | AGENTS.md, BUILD gates, MCP registry, workflows | Per-repo + stack |
| **Pod** | Utsav + cofounder | Client delivery, polished surfaces | `project-{client}` |
| **Client** | External POC | Shared decks, no internals | Separate repo when needed |

## Repo ↔ deploy mental model

Read `docs/repo-deploy-mental-model.md`. Summary: **repo = kitchen, Vercel = window, audience first.**

OSF reference: 2 repos (`project-om-shanti`, `findow-phase-1`), 3 windows (workshop, pod, client).

## Feed-back loop (non-negotiable)

Every client pod should **improve the org harness**, not fork silently.

After each engagement sprint:

1. Extract one pattern → `vibe-coding-stack/patterns/` or `workflows/`
2. Update `registry/hubs.json` phase + URLs
3. Append `CHANGELOG.md` if stack behavior changed
4. If learnings are substantial → update `docs/harness-learnings-from-osf.md` or hub-specific doc

## Two-person pod (OSF)

- Utsav: harness architect, enforcement, stack feed-back
- Pooja: tone, campaign copy review, visual “does this feel like OSF?”
- No third role in Phase 1 execution — org-design content in learn hub is general ZMS, scrubbed for OSF pod banner

## Spar ritual

When `PROGRAM.md` is empty and harness learnings have unchecked rollout items, run spar mode — see `HEARTBEAT.md` § Spar ritual.
