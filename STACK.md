# Stack

Environment index for vibe-coding-stack v0.2.0.
This file is a map, not a manual. Follow pointers to find detail.

## What exists

| Type | File |
|------|------|
| API connectors | `registry/connectors.json` |
| CLI tools + MCP servers | `registry/tools.json` |
| Skills (/slash commands) | `registry/skills.json` |
| Design systems | `registry/design-systems.json` |
| Knowledge hubs | `registry/hubs.json` |

## Domains (load when routing determines relevance)

**Build**
`planning` · `design` · `coding` · `testing`

**Infrastructure**
`deployment` · `analytics` · `security`

**Intelligence**
`llm` · `knowledge` · `voice`

**Go-to-Market**
`distribution` · `payments` · `legal`

Each domain doc lives at `domains/<name>.md`.

Domain scope:
- `distribution` — SEO, email (Resend), content, AEO, social — everything that gets the app to users
- `payments` — Stripe, Razorpay, billing, subscriptions, invoicing
- `legal` — terms, privacy policy, GDPR, India compliance, cookie consent
- `security` — auth patterns, secrets management, /cso, /guard, threat model
- `analytics` — PostHog, token ledger, observability, eval scoring
- `voice` — ElevenLabs TTS/STT, voice IDs, call webhooks
- `knowledge` — NotebookLM, RAG, crawled vaults, ingest pipeline
- `llm` — Claude API, model routing, prompt caching, cost tracking

## Build flow

```
PROGRAM.md  ← human writes the 2–3 line brief
AGENTS.md   ← agent routes, plans, writes spec
BUILD.md    ← agent-written spec; human reviews before code starts
```

## App store

- Catalog: `app-store/STORE.md`
- Publish workflow: `app-store/publish.md`

## Architecture boards

- Ingest v3: `boards/ingest-architecture-board/` · [live](https://spacebuilder13.github.io/ingest-architecture-board/)

## Product context

- GitHub landscape: `docs/github-landscape.md`
