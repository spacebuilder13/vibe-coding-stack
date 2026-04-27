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

### Keep from v2

- two mandatory gates
- one compound synthesis query
- `/tmp` offload for long outputs
- direct file writes for deterministic steps
- no unnecessary sub-agent fanout

### Add in v3

- ElevenLabs transcription path (audio + video audio extraction)
- contextual routing layer (project, notebook, confidentiality, knowledge targets)
- confidence-based clarification questions
- optional Linear task compilation and create flow (via MCP)
- structured knowledge updates for person/market/IP files
- replayable run artifacts and scoring fields

---

## Proposed v3 Architecture

1. Ingest Worker (deterministic)
2. Context Router (semi-agentic)
3. Synthesizer (deterministic prompt)
4. Action Compiler
5. Knowledge Updater
6. Evaluator and HITL gate

---

## Automated eval workflow (explicit)

Add a deterministic evaluator step immediately after synthesis and before Gate 2.

Evaluator checks:

1. schema validity
2. extraction quality
3. routing quality
4. safety/privacy checks

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

## Token Efficiency Rules (Hard Constraints)

1. Never dump full transcript or full synthesis in chat.
2. Keep only digest + counts in active conversation.
3. One extraction call per source (unless confidence retry triggered).
4. Run evaluator call only when risk/confidence conditions trigger.
5. Use deterministic templates for file writes.
6. Use smaller model for routing/classification, larger model only for synthesis.

---

## Phased Rollout

### v3a - Deterministic Expansion

- ElevenLabs transcription path
- transcript artifacts on disk
- attach transcript/meta to NotebookLM
- keep existing two gates

### v3b - Intelligent Router

- strict router JSON
- confidence thresholds
- clarification mini-loop

### v3c - Task + Knowledge Automation

- Linear MCP task creation from confirmed items
- structured knowledge file updates
- handover payload generation

### v3d - Evaluation Hardening

- scoring and replay
- regression checks over 20-50 ingest samples
- prompt/version tracking
