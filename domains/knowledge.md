# Domain: Knowledge

When to load: using NotebookLM, building a RAG system, running the ingest pipeline, crawled vaults.

## Core principle
Knowledge hubs as SSOT. Never invent history — always cite source.
Prefer hub content over agent memory.

## NotebookLM — 360-degree query protocol

Used across: project-sandy (5 notebooks), project-insurance, project-ob (6 notebooks).

**Query discipline:**
1. Query each advisor notebook sequentially (not in parallel — avoids polluting context)
2. Compare outputs across advisors before synthesizing
3. Note where advisors agree vs. diverge
4. Cite the notebook + source in the final answer
5. Never blend advisors — keep voices distinct until final synthesis

**Notebook types:**
- **Transcript notebooks** — client sessions, calls, WhatsApp exports
- **Framework notebooks** — expert advisors (Anil Lamba, Mike Michalowicz, Garrett Gunderson, Philip Campbell, Tax)
- **Research notebooks** — crawled articles, YouTube intelligence

**Source inventory file:** `sandy_source_index.md` (pattern — create per project)

## Ingest v3 pipeline

Architecture: `boards/ingest-architecture-board/` · [live board](https://spacebuilder13.github.io/ingest-architecture-board/)

Stages:
1. **Gate 1** — confirm project + identity
2. **Normalize** — ffmpeg audio extract + sample rate standardize
3. **Transcribe** — ElevenLabs STT → raw + clean transcript + JSON
4. **Route** — rules-first context router → project ID, notebook target, confidentiality
5. **Synthesize** — one structured extraction: SUMMARY, ITEMS, BRIEF, OPEN QUESTIONS
6. **Gate 2** — human confirm or delete
7. **Write** — parallel writers: source index, registry, actions log, handover note, knowledge updater, NotebookLM attach

Observability: run manifest, decision trace, metrics, eval scores.

## Crawled vaults
- **Ditto vault** — 1,693 articles from joinditto.in (306 life + 179 term insurance)
- **YouTube comments** — `tools/youtube-top-comments/` CLI for top comments export

## Knowledge hub manifest
Register all hubs in `registry/hubs.json`:
- NotebookLM notebook URLs
- Magic Patterns board URLs
- Crawled vault locations
- Notion/Google Doc pointers

## Skills
| Skill | When |
|-------|------|
| `/ingest` | Process audio/video/conversation into structured knowledge |
| `/learn` | Review, search, prune project learnings |

## Anti-patterns
- Querying all notebooks in parallel (context bleed)
- Inventing facts not in a hub source
- No source inventory file for a multi-notebook project
- Writing to NotebookLM without Gate 2 confirmation
