# Changelog

## 0.2.0 — 2026-05-03

Breaking restructure. Vibe coding stack redesigned as a universal agent environment
for 1-shot HQ app builds, applying OpenClaw tiered context + Anthropic agent principles
+ Karpathy 3-file minimalism.

**New files:**
- `SOUL.md` — Tier 0 identity anchor (prompt-cached, ~250 tokens)
- `HEARTBEAT.md` — Tier 0 session checklist (prompt-cached, ~150 tokens)
- `STACK.md` — Tier 0 environment index (~200 tokens, pointers only)
- `PROGRAM.md` — human-written brief template (one per project)
- `BUILD.md` — agent-written spec template (one per project)
- `domains/` — 13 capability domain docs: planning, design, coding, testing,
  deployment, analytics, security, llm, knowledge, voice, distribution, payments, legal
- `registry/connectors.json` — 14 API integrations with cost tiers + env vars
- `registry/skills.json` — 23 skills with domain tags, cost, trigger conditions
- `registry/design-systems.json` — Zen DS, Sandy tokens, shadcn, Magic Patterns
- `patterns/` — 5 reusable workflow templates: 1-shot-app, demand-side, screenshot-qa,
  notebooklm-360, conversation-ingest
- `app-store/STORE.md` — app catalog (Sandy, Supperclubbing, Project OB registered)
- `app-store/publish.md` — publish workflow including PWA setup

**Modified:**
- `AGENTS.md` — rewritten: model routing table, domain routing table, skill routing table,
  simplified 9-step build workflow
- `boards/ingest-architecture-board/app.js` — fix Mermaid rendering (render() not run())

**Token efficiency:**
- Tier 0 (always loaded): ~650 tokens total, prompt-cacheable → ~65 effective tokens
- Domain docs load on-demand only when routing determines relevance
- Registry JSONs fetched JIT when executing, not upfront
- Model routing (Haiku/Sonnet/Opus) → ~51% cost reduction vs uniform Sonnet

## 0.1.4 — 2026-04-28

- Ingest board cleanup: full blueprint synced into `boards/ingest-architecture-board/data/`; shorter `boards/README.md` + board README with `rsync` deploy note; `docs/github-landscape.md` + `AGENTS.md` clarify SSOT vs Pages repo.

## 0.1.3 — 2026-04-28

- Added `boards/ingest-architecture-board/` (Mermaid + blueprint + Giscus) as the in-repo copy of the ingest v3 review board; `boards/README.md`, root `README.md` + `AGENTS.md`.

## 0.1.2 — 2026-04-28

- Vendored **youtube-top-comments** into `tools/youtube-top-comments/` (yt-dlp → JSON/CSV/MD; agent entry `tools/youtube-top-comments/AGENTS.md`).
- `tools/README.md`, `registry/tools.json`, root `AGENTS.md` + `README.md`; `.gitignore` patterns for tool venv/out/cache.

## 0.1.1 — 2026-04-28

- Security pass: `SECURITY.md`, expanded `.gitignore` for env/keys/hub binaries, README visibility note aligned with public repo.

## 0.1.0 — 2026-04-28

- Initial v1 scaffold: `AGENTS.md`, Cursor rules, `hubs/`, `prompts/`, `workflows/`, `registry/`, GitHub landscape doc.
- Documented north-star workflow: conversation ingest → plan + first artifact under time pressure.
