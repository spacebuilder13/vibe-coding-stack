# Knowledge hubs

**Hubs** are intentional, citeable knowledge: Notebook LM topics, Magic Patterns boards, architecture HTML, Notion pages, call transcripts, etc. Agents should **read hub manifests** before inventing product history.

## Conventions

- Each hub is an entry in `registry/hubs.json` (or inline in `manifest.yaml` if you prefer a single file—keep one canonical source).
- Prefer **stable URLs** + **last verified date**.
- For **Notebook LM**: store export path (PDF/Markdown) under `hubs/exports/<name>/` *or* link only—never commit secrets.
- For **Magic Patterns**: always record `source_design_url` and optional `repo_sync` path.

## Adding a hub

1. Create `hubs/exports/<slug>/` or document a URL-only hub.
2. Append to `registry/hubs.json`.
3. Note in the **product repo** README: “Knowledge hub: see vibe-coding-stack `registry/hubs.json` entry `<id>`.”
