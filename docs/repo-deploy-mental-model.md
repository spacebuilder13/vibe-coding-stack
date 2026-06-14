# Repo ↔ deploy mental model

Canonical reference for ZMS org deploy decisions. Builder workspace rule: `.cursor/rules/repo-deploy-model.mdc`.

## Analogies

| Concept | Analogy | What it is |
|---------|---------|------------|
| GitHub repo | Kitchen | Source of truth. Version control. Experiments OK. |
| App folder | Station | `apps/web`, `apps/phase1` — one repo, many stations |
| Vercel project | Restaurant window | Deploy config: repo + folder + branch → URL |
| Production URL | Door address | `*.vercel.app` — not code |

**findow** = food truck at the client's office — separate kitchen. Client never sees the main kitchen.

## First principles

1. Repo = kitchen. URL ≠ repo.
2. One repo, many Vercel windows is fine.
3. Audience before architecture — "who sees this?" first.
4. Client surfaces = isolated repos. No harness internals.
5. Pod surfaces = polished only. Promote from workshop when ready.
6. Promote, don't fork — avoid a third repo unless hard isolation is required.

## OSF reference layout (2 repos, 3 windows)

| Audience | Who | Repo | Folder | URL |
|----------|-----|------|--------|-----|
| Client | External | `findow-phase-1` | root | `findow-phase-1.vercel.app` |
| Workshop | Utsav | `project-om-shanti` | `apps/web` | `project-om-shanti.vercel.app` |
| Pod | Utsav + Pooja | `project-om-shanti` | `apps/phase1` | `zms-osf-phase-1.vercel.app` |

Pod bookmark for cofounder: `/learn` on zms-osf.

## Anti-patterns

- Naming a Vercel project like a repo and assuming 1:1 mapping
- Putting client decks in the same repo as `AGENTS.md` / learn hub
- Creating a third repo for pod when `apps/phase1` already exists
- Deploying from paths outside the repo (e.g. sibling `agent-harness-learning/` — vendor into repo)

## New hub checklist

- [ ] Who is the audience? (client / workshop / pod / public)
- [ ] One repo or separate client repo?
- [ ] Which folder does each Vercel project build from?
- [ ] Document in hub `STACK.md` § Audiences
- [ ] Register URLs in `vibe-coding-stack/registry/hubs.json`
- [ ] Add row to `app-store/STORE.md` when live

## Related

- `domains/deployment.md` — Vercel/Supabase/Pages how-to
- `workflows/b2b-client-bootstrap.md` — client pod onboarding
- `app-store/publish.md` — post-deploy registration
