# Changelog

## 0.3.0 — 2026-07-30

New skill family: article illustrations.

- `.cursor/skills/xiaohei-illustrations/` — English port of Ian's Xiaohei illustration skill
  (source: helloianneo/ian-xiaohei-illustrations, MIT). SKILL.md + 5 references
  (style-dna, xiaohei-ip, composition-patterns, prompt-template, qa-checklist) + NOTICE.md
  attribution. Generates 16:9 white-background hand-drawn article illustrations via
  Cursor's built-in image generation (2.4+), with a prompt-only fallback and a built-in
  smoke-test command.
- `registry/skills.json` — `/xiaohei-illustrations` entry (domain: design, cost: medium).
- `README.md` — repo map row for the new skill.

## 0.2.2 — 2026-06-17

OSF deck housekeeping.

- `apps/paul-deck/` — archived reference deck moved from `project-om-shanti`
- `app-store/STORE.md` — OSF client deck URL → `findow-phase1.vercel.app`
- `registry/hubs.json` + `hubs/manifest.yaml` — om-shanti client deck path + URLs

## 0.2.1 — 2026-06-15

OSF harness learnings + repo/deploy mental model.

- `docs/repo-deploy-mental-model.md` — kitchen/window analogy, audience-first deploy
- `docs/harness-learnings-from-osf.md` — DSS router, learn hub, rollout checklist
- `docs/ai-native-org-setup.md` — Meta/Harness/Pod/Client layers
- `docs/SPAR_RITUAL.md` — org-wide rollout spar with Utsav
- `HEARTBEAT.md` — spar ritual trigger
- `registry/hubs.json` + `hubs/manifest.yaml` — om-shanti Phase1 URLs, awag sync
- `app-store/STORE.md` — OSF pod, client deck, Max Spare rows
- `workflows/b2b-client-bootstrap.md` — SOUL/STACK + audience table

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

## 0.1.5 — 2026-04-28

- **competitive-site-research**: vendored `tools/competitive-site-research/` (sitemap crawl → Obsidian markdown vault; robots `Disallow`; optional posts sitemap); `scripts/generate_hubs.py` for MOC + IA outline.
- Cursor skill **`.cursor/skills/competitive-site-research/SKILL.md`** and persona **`prompts/competitive-research-agent.md`** (competitive research agent framing + UX audit pack contract).
- `registry/tools.json`, `tools/README.md`, root `AGENTS.md` + `README.md`.

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
