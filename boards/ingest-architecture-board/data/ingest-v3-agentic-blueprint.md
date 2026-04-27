# /ingest v3 - Agentic Routing Blueprint (Lean)

## Intent

Extend `/ingest` from a deterministic media-to-NotebookLM pipeline into a lean agentic system with:

- deterministic ingest core
- intelligent project/context routing
- optional task creation (Linear MCP or handover)
- structured knowledge updates (individual, market, IP)
- human-in-the-loop checkpoints
- strict token discipline

This is not full autonomy. It is a controlled router workflow with selective agent behavior.

---

## Design Principles (Mapped to Sources)

### From Anthropic: Building Effective Agents

1. Start simple, add complexity only when outcomes improve.
2. Prefer workflows for predictable tasks; use agents for open-ended decisions.
3. Invest heavily in tool/interface clarity (ACI).
4. Keep planning visible and checkpoints explicit.
5. Treat eval as a first-class loop.

### From Vellum: Agentic Workflows Patterns

1. Use router-level decisioning before autonomous process control.
2. Build around planning -> execution -> refinement -> interface.
3. Make observability and replay non-negotiable.
4. Keep humans in loop for high-impact decisions.
5. Use memory stores intentionally (short-term and long-term separation).

---

## Scope: What v3 Adds vs v2

## Keep from v2 (unchanged)

- two mandatory gates
- one compound synthesis query
- `/tmp` offload for long outputs
- direct file writes for deterministic steps
- no unnecessary sub-agent fanout

## Add in v3

- ElevenLabs transcription path (audio + video audio extraction)
- contextual routing layer (project, notebook, confidentiality, knowledge targets)
- confidence-based clarification questions
- optional Linear task compilation and create flow (via MCP)
- structured knowledge updates for person/market/IP files
- replayable run artifacts and scoring fields

---

## Proposed v3 Architecture

1. Ingest Worker (deterministic)
   - normalize media
   - extract audio from video
   - transcribe using ElevenLabs
   - produce raw + cleaned transcript + transcript metadata

2. Context Router (semi-agentic)
   - input: transcript digest + project registry + source metadata
   - output schema: project, notebook, confidential, knowledge targets, task policy, confidence
   - ask user only if confidence below threshold

3. Synthesizer (deterministic prompt)
   - single structured extraction:
     - SUMMARY
     - ITEMS ([ACTION]/[DECISION]/[FACT]/[QUESTION])
     - BRIEF
     - OPEN QUESTIONS
   - write full result to `/tmp` and project meta files

4. Action Compiler
   - convert confirmed items into:
     - `actions_log.md`
     - optional Linear issue payloads
     - handover notes for task management agent

5. Knowledge Updater
   - append/update:
     - `knowledge/individual/*.md`
     - `knowledge/market/*.md`
     - `knowledge/ip/*.md`
   - include source references and confidence annotations

6. Evaluator and HITL gate
   - compact digest to user
   - correction pass
   - keep/delete/confidential decision
   - proceed/skip registry and task push

---

## v3 Data Contracts (Strict JSON First)

## Router output

```json
{
  "project_id": "project-ob",
  "notebook_id_var": "NOTEBOOKLM_TRANSCRIPT2_NOTEBOOK_ID",
  "source_name": "2026_04_26_ob_market_checkin_pending",
  "label": "market_checkin",
  "confidential": false,
  "knowledge_targets": ["individual", "market"],
  "task_policy": "create_from_actions",
  "route_confidence": 0.84,
  "clarification_questions": []
}
```

## Evaluation digest output

```json
{
  "summary_top3": ["...", "...", "..."],
  "counts": {"action": 3, "decision": 2, "fact": 6, "question": 4},
  "top_questions": ["...", "..."],
  "risk_flags": ["speaker_ambiguity_low"]
}
```

## Linear task payload output

```json
{
  "title": "Follow up on supplier pricing variance",
  "description": "Derived from source 2026_04_26_ob_market_checkin...",
  "labels": ["ingest", "auto-extracted"],
  "priority": 2,
  "project": "Operations",
  "assignee_hint": "OB",
  "source_ref": "outputs/source_meta/2026_04_26_ob_market_checkin_meta.md"
}
```

---

## Folder Structure (Contextual Drive Organization)

Per project root:

- `inputs/raw_media/`
- `outputs/transcripts/raw/`
- `outputs/transcripts/clean/`
- `outputs/source_meta/`
- `outputs/actions/`
- `outputs/handovers/`
- `knowledge/individual/`
- `knowledge/market/`
- `knowledge/ip/`
- `logs/ingest_runs/`

Per source bundle:

- `<source_name>.json` (machine metadata and routing decisions)
- `<source_name>_transcript_raw.md`
- `<source_name>_transcript_clean.md`
- `<source_name>_meta.md`
- `<source_name>_digest.json`
- `<source_name>_tasks.md` (optional)

---

## ElevenLabs Integration Plan

1. Normalize input
   - if video: `ffmpeg` extract audio track
   - standardize sample rate/channels

2. Transcription call
   - use ElevenLabs STT endpoint
   - capture timestamps + speaker hints where available
   - store raw API response JSON

3. Post-process
   - produce clean transcript markdown
   - map speaker aliases from project config
   - confidence tags for unclear spans

4. Fallback strategy
   - if ElevenLabs fails: fail closed with actionable error
   - optional fallback provider can be added later, not in v3a

---

## Human-in-the-Loop Policy

## Gate 1 (before processing)

Confirm:

- project
- speaker identity
- context
- source name
- notebook
- confidentiality

## Gate 2 (after synthesis)

Confirm:

- corrections
- which items to log
- keep/delete/confidential override
- proceed with registry and task creation

---

## Token Efficiency Rules (Hard Constraints)

1. Never dump full transcript or full synthesis in chat.
2. Keep only digest + counts in active conversation.
3. One extraction call per source (unless confidence retry triggered).
4. Run evaluator call only when risk/confidence conditions trigger.
5. Use deterministic templates for file writes; avoid creative generation there.
6. Use smaller model for routing/classification, larger model only for synthesis.

---

## Intelligent Routing Policy (Simple First)

Routing tiers:

1. Rule-first routing
   - file path patterns
   - known speaker -> project map
   - explicit user selections

2. LLM router (only when ambiguous)
   - classify project/notebook/knowledge targets
   - return strict JSON

3. Clarification (only when low confidence)
   - ask at most 2 questions
   - then continue deterministically

---

## Linear and Agent Handover Strategy

When to create Linear tasks:

- `[ACTION]` includes owner + concrete deliverable
- or user confirms "all actions"

When to hand over instead:

- strategic or ambiguous items
- multi-step items needing planning agent

Handover outputs:

- concise task brief markdown
- source references
- rationale and confidence

---

## Evaluation and Learning Loop

Each run writes:

- run manifest (`logs/ingest_runs/<timestamp>_<source>.json`)
- decision trace (routing, confidence, clarifications)
- post-run metrics:
  - ingest duration
  - token estimate
  - items extracted count
  - accepted/rejected item ratio
  - user corrections count

Use these metrics weekly to tune prompts and thresholds.

## Automated eval workflow (explicit)

Add a deterministic evaluator step immediately after synthesis and before Gate 2.

Evaluator checks:

1. schema validity
   - all four required sections present
   - item labels strictly in allowed set

2. extraction quality
   - no empty SUMMARY/ITEMS/BRIEF/OPEN QUESTIONS
   - minimum item density threshold for non-trivial recordings
   - speaker attribution completeness score

3. routing quality
   - project and notebook confidence score
   - knowledge target confidence score

4. safety/privacy checks
   - confidential keywords and entities detected
   - enforce "no auto-task push" if privacy risk score is high

Evaluator output contract:

```json
{
  "schema_pass": true,
  "quality_score": 0.81,
  "routing_score": 0.86,
  "privacy_risk": "low",
  "requires_human_review": true,
  "reasons": ["speaker attribution below threshold"],
  "retry_recommended": false
}
```

Auto actions based on evaluator:

- if `schema_pass` is false -> one automatic synthesis retry, then hard stop
- if `quality_score < 0.70` -> request user clarification before any task creation
- if `privacy_risk != low` -> force confidential mode and disable auto Linear push
- if `routing_score < 0.75` -> ask routing clarification question set

---

## Human-in-the-loop escalation policy (explicit)

Gate 1 and Gate 2 are mandatory for all runs.
Additional HITL triggers are mandatory when:

- evaluator flags `requires_human_review = true`
- detected contradiction across `[DECISION]` items
- unknown speaker aliases above threshold
- task creation would impact external stakeholders
- source appears confidential but user selected non-confidential

Human decision options should always include:

- approve as is
- approve with corrections
- approve but skip task creation
- mark confidential and continue
- abort and archive artifacts

---

## Phased Rollout

## v3a - Deterministic Expansion (now)

- ElevenLabs transcription path
- transcript artifacts on disk
- attach transcript/meta to NotebookLM
- keep existing two gates

## v3b - Intelligent Router

- strict router JSON
- confidence thresholds
- clarification mini-loop

## v3c - Task + Knowledge Automation

- Linear MCP task creation from confirmed items
- structured knowledge file updates
- handover payload generation

## v3d - Evaluation Hardening

- scoring and replay
- regression checks over 20-50 ingest samples
- prompt/version tracking

---

## Why This is the Right Complexity

This architecture keeps the ingest backbone deterministic, introduces agentic behavior only at uncertainty points, preserves human control at high-impact checkpoints, and minimizes token burn by moving all heavy artifacts to disk.
