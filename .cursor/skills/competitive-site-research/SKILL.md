---
name: competitive-site-research
description: >-
  Builds an Obsidian-ready knowledge graph from a competitor or reference site:
  sitemap-driven HTML crawl to markdown (YAML + body), hub/MOC notes, IA outline,
  and a UX audit pack (browser full-page screenshots + journey notes). Use when
  the user asks for competitive research, site teardown, Obsidian KG from a URL,
  marketing IA capture, or "research [domain] like we did for Ditto".
---

# Competitive site research (Obsidian + UX pack)

## When to use

- Competitive / landscape research on a **public** marketing or content site.
- "Turn this website into notes" / **Obsidian vault** structure for linking and graph view.
- **Design or IA audit** evidence: screenshots + written summaries in one markdown index.

## What to run (this repo)

1. **Crawl → vault** (Python, vendored tool):

   ```bash
   cd tools/competitive-site-research
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   python scripts/crawl_to_obsidian.py --base-url "https://example.com" --vault /path/to/vault
   ```

   Optional: `--posts-sitemap URL`, `--marketing-limit N`, `--articles-limit N`, `--articles-only`, `--insecure` (dev TLS only), `--zen-audit`, `--zen-target-url URL`.

2. **Hubs + IA** (after crawl):

   ```bash
   python scripts/generate_hubs.py --vault /path/to/vault
   ```

3. **UX screenshots** (MCP `cursor-ide-browser`): navigate key URLs, full-page PNGs under `vault/assets/ux-audit/`, document in `vault/UX-AUDIT-PACK.md` (see `prompts/competitive-research-agent.md` for the table + summary pattern).
4. **ZEN design-system audit extension** (new): produce a principle rubric, page-level pass/fail scoring, and tool-level UX logic notes.

   Required docs:
   - `vault/00-meta/ZEN-DESIGN-PRINCIPLES-RUBRIC.md`
   - `vault/00-meta/ZEN-AUDIT-SCORECARD.md`
   - `vault/00-meta/ZEN-AUDIT-FINDINGS.md`

   Recommended scoring model:
   - `PASS` = principle clearly satisfied with source evidence.
   - `PARTIAL` = principle present but inconsistent or fragile.
   - `FAIL` = principle absent, contradictory, or blocked by UX copy/flow.
   - confidence tags: `high | medium | low`.

## Output contract

| Path | Purpose |
|------|---------|
| `vault/03-articles/` | URLs whose path contains `/articles/` (or entire `--posts-sitemap` list) |
| `vault/02-pages/` | Other crawled pages |
| `vault/01-hubs/` | MOC notes + site hub |
| `vault/00-meta/` | `url-inventory.md`, `CRAWL_LOG.md`, `IA-outline.md` |
| `vault/assets/ux-audit/` | Screenshots |
| `vault/UX-AUDIT-PACK.md` | Image index + IA + journeys |
| `vault/00-meta/ZEN-DESIGN-PRINCIPLES-RUBRIC.md` | Principle definitions + evaluation logic |
| `vault/00-meta/ZEN-AUDIT-SCORECARD.md` | URL-by-principle score matrix |
| `vault/00-meta/ZEN-AUDIT-FINDINGS.md` | What is working vs not working + prioritized fixes |

## Rules

- Respect **robots.txt** `Disallow` for `User-agent: *` (parser in script); add `--disallow-prefix` if you must mirror extra exclusions.
- Do not bypass **login**, **paywall**, or **ToS**; gated flows get a stub note + "manual" tag only if the user asks.
- Prefer **evidence** (crawled text, snapshots) over invention; summaries are allowed for UX tables.
- Reference implementation the stack author used: external vault `ditto-obsidian-vault` on the same machine path pattern `~/Projects/ditto-obsidian-vault/vault` — do not require it; the tool is site-agnostic.

## Agent persona

For copy-paste system framing or long jobs, use **`prompts/competitive-research-agent.md`** in this repo.
