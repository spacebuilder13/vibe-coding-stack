# Vibe coding stack (v1)

A **personal, versioned control plane** for how you build with agents: skills, prompts, MCP tools, knowledge hubs, and review loops. This repo is the **source of truth** you extend over time—not a frozen template.

## What this is for

- **Every build**: clone or submodule this repo, point Cursor/Claude at `AGENTS.md` and `.cursor/rules`, and inherit defaults.
- **Evolving stack**: bump `VERSION`, append `CHANGELOG.md`, add hubs and prompts as you discover better patterns.
- **North star**: ingest a **recorded conversation** (or transcript) with someone about their problem; the agent produces a **plan plus first concrete output** before the conversation ends—without you re-explaining context manually.

## Repo map

| Path | Role |
|------|------|
| `AGENTS.md` | Agent entry: priorities, stack layers, when to use what |
| `.cursor/rules/vibe-stack.mdc` | Cursor-native reinforcement of the same |
| `boards/` | **Architecture boards** (SSOT for ingest v3 diagram + blueprint + local preview) |
| `docs/github-landscape.md` | Dated snapshot of how your public GitHub work evolved (context, not prescription) |
| `hubs/` | **Knowledge hubs**: manifests + conventions for Notebook LM, docs, design sources, Magic Patterns links, etc. |
| `prompts/` | Reusable prompt shells (handoff, plan-first, ship loop) |
| `workflows/` | Human + agent procedures (e.g. conversation → plan → artifact) |
| `registry/` | Machine-readable indexes (`tools.json`, `hubs.json`) for agents or scripts |
| `tools/` | Vendored one-off CLIs (e.g. YouTube comment export); each tool has its own `AGENTS.md` |

## Principles (v1)

1. **Plan before pixels** when the problem is ambiguous; **ship a thin vertical slice** when the problem is clear.
2. **Ground in hubs**: cite or load hub entries instead of inventing product history.
3. **Subagents / skills are tactics**: invoke deep reviews, QA, security, or design passes when cost is justified—not by default on every keystroke.
4. **Magic Patterns and similar** are first-class inputs: store the design URL and sync notes in `hubs/`.
5. **This repo updates** after meaningful stack changes (new MCP, new skill family, new hub type).

## Quick start (new machine)

```bash
git clone https://github.com/spacebuilder13/vibe-coding-stack.git
# Point your editor/agent at this folder or copy AGENTS.md + .cursor into a product repo
```

## Remote

Live repo: [github.com/spacebuilder13/vibe-coding-stack](https://github.com/spacebuilder13/vibe-coding-stack).

To add `origin` on another clone: `gh repo clone spacebuilder13/vibe-coding-stack`.

## Visibility and license

This repo is **public** on GitHub (clone-friendly stack defaults). It must not contain private credentials or raw client transcripts—use private repos or encrypted storage for those.

Add a `LICENSE` file when you pick a license; until then, all rights reserved unless you state otherwise in `LICENSE`.
