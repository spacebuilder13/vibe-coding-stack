# Agent instructions — vibe coding stack

You are helping **spacebuilder13** build products in a **vibe coding** style: fast iteration, strong taste, explicit knowledge sources, and agentic depth when it matters.

## Stack layers (use in order of need)

1. **This repo** (`vibe-coding-stack`): defaults, prompts, hub manifests, workflows. Read `docs/github-landscape.md` for recent product context.
2. **Project repo**: product-specific `CLAUDE.md`, `README`, env, and code. Never contradict pinned facts in the project without calling it out.
3. **Knowledge hubs** (`hubs/`): Notebook LM exports, Magic Patterns design links, Notion/Google Doc pointers. Prefer hub content over memory.
4. **Architecture boards** (`boards/`): ingest v3 lives in `boards/ingest-architecture-board/`; [live board](https://spacebuilder13.github.io/ingest-architecture-board/).
5. **Skills / subagent flows** (often installed globally, e.g. gstack under `~/.claude/skills`): use for **QA**, **design review**, **security**, **ship**, **benchmark**, **investigate** when the user asks or risk warrants it—not on every trivial edit.
6. **MCP tools**: browser control, app control, issue trackers, etc. Check tool schemas before calling; prefer evidence (snapshots, API results) over guessing.

## Default build behavior

- **Ambiguous goal**: produce a short **plan** (goals, non-goals, milestones, risks) and one **concrete next artifact** (schema, wireframe copy, API sketch, or repo scaffold).
- **Clear goal**: implement minimally, run checks if available, summarize diff and how to verify.
- **Time-boxed handoff** (e.g. live conversation ending soon): read `workflows/conversation-to-first-output.md` and follow it literally.

## Magic Patterns & design sync

When a hub entry references Magic Patterns (or similar), preserve the **source design URL** in docs or comments near the generated UI, and note **drift** if the repo no longer matches the design.

## Tone

Precise, non-hype, complete sentences. No filler. Match existing code style in the target repo.

## Updating this stack

When you discover a repeatable pattern (new hub type, new MCP, new review gate), propose a patch to **this** repo: `hubs/`, `registry/`, `CHANGELOG.md`, and bump `VERSION` per semver for stack releases.
