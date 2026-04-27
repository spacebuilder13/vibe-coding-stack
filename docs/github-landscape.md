# GitHub landscape — spacebuilder13

Snapshot date: **2026-04-28**. Source: `gh repo list spacebuilder13` (push dates, languages, descriptions). Use this to infer **how vibe coding evolved**; it is not exhaustive of private or org repos.

## Account

- **Login**: spacebuilder13  
- **Account created**: 2025-11-14 (GitHub API `created_at`)

## Timeline (public activity, newest first)

| Last push | Language | Repo | Notes |
|-----------|-----------|------|--------|
| 2026-04-27 | HTML | project-insurance | Client/workspace-style static site |
| 2026-04-27 | HTML | project-sandy | Desc: Sandy Menon / Fat Monk Productions — VEM engagement workspace |
| 2026-04-26 | — | Zen-Design-System | Desc: Personal design system — humane, principle-first, built for vibe coders |
| 2026-04-26 | TypeScript | Zen-Money-v1 | **Magic Patterns** — README cites generated Vite template + source design URL |
| 2026-04-26 | JavaScript | ingest-architecture-board | Mermaid board + Giscus on Discussions; static hosting |
| 2026-04-26 | HTML | project-ob | Workspace site |
| 2026-04-18 | TypeScript | Kansou-Library | App/library shape |
| 2026-04-15 | TypeScript | bps-compass, bps-ffplan | Paired TS projects (naming suggests planning/compass metaphors) |
| 2026-04-12 | TypeScript | supperclubbing | Social/dining angle |
| 2026-04-03 | JavaScript | acme-financial-clarity | Demo/financial narrative |
| 2026-03-15 | HTML | explorations | Lightweight HTML experiments |
| 2026-03-15 | — | conductor-playground | Tooling/playground (no README via API at snapshot time) |
| 2026-02-25 | TypeScript | dream-trip-architect | Travel planning product shape |
| 2026-02-05 | TypeScript | gamma-mirror | README: **WHEN Money — Credit Card Concierge**; Next.js 15, MDX, PostHog, Resend, SEO/AEO framing |
| 2026-02-02 | TypeScript | credit-card-coach | Continuation of fintech/cards theme in TS |
| 2025-12-18 | JavaScript | whenmoney, scout | Early **JS** generation: scout = Indian credit card rewards MVP; financial clarity thread |

## Interpretation (v1, opinionated)

1. **Theme**: Strong through-line on **personal finance / credit cards / benefits**, moving from **JavaScript (Dec 2025)** toward **TypeScript + Next-level stacks (Feb–Apr 2026)**.
2. **Vibe infra**: **Zen-Design-System** + **Magic Patterns–synced** repos show investment in **design source of truth** and generator-first UI—not only hand-coded pages.
3. **Knowledge & review**: **ingest-architecture-board** is a pattern you seem proud of: **visible architecture**, **comments via Giscus**, low ceremony—fits “hub + board + async feedback.”
4. **Workspace explosion (Apr 2026)**: Multiple **HTML `project-*`** repos suggest **parallel engagements** or client pods—your stack should support **fast context swap** via hubs, not one monolithic doc.
5. **NLM / external brains**: Not visible in Git metadata; treat **Notebook LM** (and similar) as **hubs** with exports or links in `hubs/manifest.yaml` so agents do not rely on chat memory alone.

## Gaps / next instrumentation

- Add hub entries per repo with **one-line intent**, **Magic Patterns link** if any, and **deploy target**.
- Optionally automate refresh of this doc with `gh repo list` in CI or a monthly local script.
