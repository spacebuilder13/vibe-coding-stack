# Skill: cloud-chat-context

Pull artifacts and context from a Claude project into a new project repo.

**Trigger phrases:** "bring in context from Claude project", "pull Claude project context",
"import from Claude", "use Claude project as context", "sync from cloud chat".

---

## What this skill does

Claude project links (e.g. `https://claude.ai/project/<uuid>`) are authenticated web apps —
they cannot be fetched directly. This skill defines the **workflow** for extracting context
from cloud AI chat history (Claude, ChatGPT, NotebookLM) and wiring it into a project repo
so every future agent session starts fully informed.

---

## Workflow

### Step 1 — Identify context sources

Ask the user for:
- **Claude project URL** (if any): `https://claude.ai/project/<uuid>`
- **NotebookLM URL** (if any): `https://notebooklm.google.com/notebook/<id>`
- **Other chat exports** (PDF, transcript, JSON)

### Step 2 — Fetch what can be fetched automatically

Try `WebFetch` on the URLs. Claude projects require auth → will return a blank shell.
NotebookLM notebooks may be partially fetchable if the notebook is public.

For anything that requires auth, proceed to Step 3.

### Step 3 — User-assisted export (when auto-fetch fails)

Ask the user to manually export from the cloud tool:

**From Claude projects:**
1. Open the project in the browser
2. For each key conversation: open → ⋯ → "Export" (or manually copy key artifacts)
3. Paste the exported text or drag the file into Cursor

**From NotebookLM:**
1. Open the notebook
2. Use "Share" → copy the sharing link (if public) OR export to PDF
3. Copy key source summaries from the sidebar

**From ChatGPT:**
1. Settings → Data controls → Export data (delivers ZIP via email)
2. Or: open conversation → select all → copy

### Step 4 — Scaffold context files in the repo

Once context is available, create:

```
CLAUDE.md          — stack + design system + conventions (full agent context)
AGENTS.md          — agent instructions (layer priorities, coding style)
hubs/              — knowledge hub manifests pointing to live sources
docs/context.md    — narrative summary: what was built, why, decisions made
```

**CLAUDE.md template:**
```markdown
# <Project Name> — CLAUDE.md

## What this is
<1-paragraph summary from cloud chat context>

## Key decisions made
<bullet list of architectural/product decisions>

## Context sources
- Claude project: <url>
- NotebookLM: <url>
- Design system: <url>

## Stack
<fill in>

## Conventions
<fill in>
```

### Step 5 — Register in hubs manifest

Add an entry to `hubs/manifest.yaml` in this vibe-coding-stack repo:

```yaml
hubs:
  - id: <project-slug>
    name: <Project Name>
    claude_project: https://claude.ai/project/<uuid>
    notebooklm: https://notebooklm.google.com/notebook/<id>
    repo: https://github.com/<org>/<repo>
    created: <date>
```

Also update `registry/hubs.json` to keep in sync.

### Step 6 — Verify

Run a quick sanity check: ask the agent "What is this project about?" and verify it answers
correctly from the newly created context files.

---

## NotebookLM integration

NotebookLM doesn't have a public API (as of May 2026). Access patterns:
- **Public notebooks**: fetchable via `WebFetch` on the share link
- **Private notebooks**: user must export or paste content manually

When a NotebookLM URL is provided:
1. Try `WebFetch` first
2. If it returns a login wall, note it in the project's `CLAUDE.md` under "Context sources"
   and ask the user to paste the key source summaries

---

## Claude project integration

Claude projects also require auth. Standard pattern:
1. The human agent (user) reads the key artifacts from the Claude project
2. Pastes them into Cursor chat → agent extracts and structures into `CLAUDE.md` / `docs/`
3. Future sessions use the local files, not the live project URL

The project URL is still recorded in `CLAUDE.md` as the canonical reference.

---

## Output checklist

- [ ] `CLAUDE.md` created with context, stack, decisions, and source URLs
- [ ] `AGENTS.md` created with agent layer priority and coding conventions
- [ ] `hubs/manifest.yaml` updated in vibe-coding-stack
- [ ] `registry/hubs.json` updated in vibe-coding-stack
- [ ] Key artifacts saved in `docs/` of the project repo
