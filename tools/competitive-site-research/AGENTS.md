# competitive-site-research — agent entry

Bundled CLI + conventions for **competitive / reference site** capture into an **Obsidian-flavored vault** (markdown + hubs + optional UX screenshots documented elsewhere).

## Quick start

```bash
cd tools/competitive-site-research
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Example: generic marketing site
python scripts/crawl_to_obsidian.py \
  --base-url "https://example.com" \
  --vault "$HOME/Projects/research-vaults/example-com/vault" \
  --marketing-limit 300 \
  --zen-audit

# Optional: explicit blog/posts sitemap (gzip OK)
python scripts/crawl_to_obsidian.py \
  --base-url "https://joinditto.in" \
  --vault "$HOME/Projects/research-vaults/joinditto/vault" \
  --posts-sitemap "https://joinditto.in/articles/sitemap-posts.xml" \
  --marketing-limit 650

python scripts/generate_hubs.py --vault "$HOME/Projects/research-vaults/example-com/vault"
```

## Flags

| Flag | Meaning |
|------|---------|
| `--base-url` | Origin only, e.g. `https://joinditto.in` |
| `--vault` | Output vault root (creates `00-meta`, `01-hubs`, …) |
| `--posts-sitemap` | Full URL to extra urlset (e.g. posts); if omitted, tries common paths then skips |
| `--marketing-limit` | Cap non-`/articles/` URLs from main sitemaps |
| `--articles-limit` | Cap post URLs (0 = all fetched) |
| `--articles-only` | Skip main sitemap marketing wave |
| `--workers` | Thread pool size (default 6) |
| `--insecure` | Disable TLS verify — **local dev only** |
| `--disallow-prefix` | Repeatable; merged with robots.txt `Disallow` for `User-agent: *` |
| `--zen-audit` | Auto-generate ZEN audit docs in `00-meta/` |
| `--zen-target-url` | Seed scorecard with a specific URL (default first queued URL) |

## UX audit pack

The crawler creates `vault/assets/ux-audit/`. Fill **`vault/UX-AUDIT-PACK.md`** using the pattern in **`prompts/competitive-research-agent.md`** at repo root, with browser MCP screenshots (full page). Cursor may save PNGs under a temp dir first — **copy** into `vault/assets/ux-audit/` if needed.

## Cursor skill

Project skill: **`.cursor/skills/competitive-site-research/SKILL.md`** — when to invoke this workflow.

## Reference run

Author’s full run on Ditto lived under `~/Projects/ditto-obsidian-vault/` (separate folder); this tool generalizes that pipeline.
