# Harness learnings from OSF (Om Shanti Finserv)

Distilled from OSF Phase 1 sprint (Jun 2026). Roll out org-wide via spar ritual — see `HEARTBEAT.md`.

## Patterns that worked

| Pattern | OSF implementation | Roll out to |
|---------|-------------------|-------------|
| **DSS knowledge router** | `knowledge/dss.md` → SSOT sections only | All B2B hubs with demand-side copy |
| **Learn hub field guide** | Static HTML + `/learn` on pod Vercel | Pods with non-technical cofounders |
| **Storyboard trace (§12)** | Emotional beats default; tech trace toggle for builder | Pooja-friendly observability |
| **Agent vs human routing** | Agents Read markdown; humans browse `/cases` | Every hub with visual galleries |
| **copy-learn prebuild** | `docs/learn-src/` → `public/learn/` in-repo | Any hub hosting static learn pages |
| **Audience map** | 2 repos, 3 Vercel windows | Document in every hub `STACK.md` |
| **Tier 0 harness** | `SOUL.md` + `STACK.md` every session | All client pods |
| **WABA ultracaution** | `compliance/WABA_HEALTH.md` pause rules | Any WhatsApp engagement |

## Rollout checklist (spar with Utsav before implementing)

- [ ] DSS router template in `patterns/dss-knowledge-router.md`
- [ ] Learn hub template in `patterns/learn-hub-field-guide.md`
- [ ] `b2b-client-bootstrap.md` updated with audience table + SOUL/STACK
- [ ] Per-hub `SOUL.md` + `STACK.md` audit (max-spare, janata-masala, om-shanti)
- [ ] Registry URLs: workshop + pod where applicable
- [ ] Compliance scaffold minimum before any WA send
- [ ] Spar-produced `docs/rollout-plan-YYYY-MM-DD.md` approved by Utsav

## Anti-patterns observed

- Deploy paths outside repo (sibling `agent-harness-learning/`) — breaks CI
- Hardcoded client passwords in source — use env vars + Vercel protection
- Third repo for pod when `apps/phase1` folder already exists
- Treating `/cases` UI as agent memory

## Source

- Pod: https://zms-osf-phase-1.vercel.app/learn/osf
- Repo: `spacebuilder13/project-om-shanti`
- Harness architect: `docs/HARNESS_ARCHITECT.md`
