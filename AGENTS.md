# Agents

Rules, workflow, and routing for vibe-coding-stack v0.2.0.
Read SOUL.md + STACK.md first. This file is Tier 1 — load at session start.

---

## Model routing

| Task | Model | Why |
|------|-------|-----|
| Routing, classification, quick edits | Haiku | Cheap, fast |
| Most work — code, analysis, writing | Sonnet | Default |
| Deep architecture, hard planning | Opus | Only when necessary |

Default to Sonnet. Escalate to Opus only when the problem genuinely requires it.

---

## Build workflow

```
1. Read SOUL.md + STACK.md          — environment loaded
2. Read PROGRAM.md                  — understand the brief
3. Route: which domains are needed? — load only those from domains/
4. Write BUILD.md                   — lock the spec, human reviews
5. Visual approval gate             — design direction confirmed?
6. Build per BUILD.md               — write code
7. /qa → fix loop                   — iterate until pass
8. /ship                            — deploy, get URL
9. Append to app-store/STORE.md     — register the app
```

Do not write production code before step 5 is confirmed.

---

## Skill routing

Invoke skills when the cost is justified — not on every edit.

| Situation | Skill | Cost |
|-----------|-------|------|
| Goal is ambiguous, need to align on scope | `/plan-eng-review` | medium |
| Need multiple design directions to compare | `/design-shotgun` | high |
| Design direction locked, need production HTML | `/design-html` | medium |
| Need QA pass before shipping | `/qa` | medium |
| Ready to deploy | `/ship` | low |
| Bug with unknown root cause | `/investigate` | medium |
| Security concern or audit needed | `/cso` | high — use rarely |
| Performance regression | `/benchmark` | medium |
| Post-ship monitoring | `/canary` | low |

Full skill list: `registry/skills.json`.

---

## Domain routing

When reading PROGRAM.md, determine which domains are needed and load only those files.

| If the brief involves... | Load domain |
|--------------------------|-------------|
| Unclear goal, milestones, non-goals | `domains/planning.md` |
| UI, visual design, tokens, layout | `domains/design.md` |
| Stack choice, code patterns, boilerplate | `domains/coding.md` |
| QA, evals, screenshot audits | `domains/testing.md` |
| Hosting, env vars, CI | `domains/deployment.md` |
| Claude API, model selection, cost | `domains/llm.md` |
| NotebookLM, RAG, ingest pipeline | `domains/knowledge.md` |
| ElevenLabs, voice input/output | `domains/voice.md` |
| SEO, email, content, social | `domains/distribution.md` |
| Stripe, Razorpay, billing | `domains/payments.md` |
| PostHog, token ledger, observability | `domains/analytics.md` |
| Auth, secrets, threat model | `domains/security.md` |
| T&C, privacy, compliance | `domains/legal.md` |

Do not load domains that are not relevant to the current brief.

---

## Stack layers (priority order)

1. `SOUL.md` + `STACK.md` — environment and identity
2. `PROGRAM.md` — the brief (human-written)
3. `domains/` — capability docs (load on demand)
4. `registry/` — machine-readable indexes (fetch JIT when executing)
5. Skills (`~/.claude/skills/`) — invoke when cost-justified
6. MCP tools — check schema before calling; prefer evidence over guessing

---

## Updating this stack

When you discover a repeatable pattern — new connector, new skill, new domain — propose a patch:
- Add to the relevant `registry/` JSON
- Add or update the relevant `domains/` file
- Append to `CHANGELOG.md`
- Bump `VERSION` per semver
