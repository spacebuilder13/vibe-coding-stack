# Mobbin Design Capture Pattern

Browser-based and MCP-based design inspiration workflow.

## Option A — Official Mobbin MCP (preferred)

1. Add to project `.cursor/mcp.json`:
   ```json
   { "mcpServers": { "Mobbin": { "type": "http", "url": "https://api.mobbin.com/mcp", "headers": {} } } }
   ```
2. Cursor → Settings → Tools & MCP → **Connect** Mobbin (OAuth)
3. Query tools: `mobbin_quick_search`, `mobbin_get_site_sections`, `mobbin_search_screens`, `mobbin_get_screen_detail`

Requires paid Mobbin plan.

## Option B — Browser capture (fallback)

- Client wants MVP UI inspired by a Mobbin reference
- Magic Patterns board not yet available
- Need layout anatomy before committing to tokens

## Steps

1. **Navigate** — browser MCP to Mobbin preview URL (user must be logged in)
2. **Capture** — mobile viewport screenshot; hero, nav, cards, CTA
3. **Document** — save to `{project}/outputs/design-captures/mobbin-{name}/NOTES.md`:
   - Layout anatomy (not pixel-copy)
   - Typography scale
   - Color mood (adapt, don't clone)
   - What NOT to copy (competitor-specific UI)
4. **Adapt** — write `knowledge/brand_guidelines.md` for client context
5. **Assets** — optional Gemini generation via user's Comet browser; log in `outputs/design-captures/gemini/LOG.md`

## Fallback

User drops screenshots manually into `outputs/design-captures/`.

## Skill routing

Invoke `/design-capture` when Mobbin + Gemini asset pipeline is needed.

## Source

First used: project-om-shanti (2026-05-24), Titan fintech reference.
