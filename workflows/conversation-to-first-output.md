# Workflow: conversation → plan + first output (before goodbye)

**Goal**: By end of a call, the stakeholder sees **clarity** (plan) and **momentum** (one real artifact), without a second “download meeting.”

## Inputs (minimum)

- Audio recording **or** transcript **or** structured notes (who, pain, current tools, success criteria).
- Optional: Magic Patterns link, existing repo, or Notebook LM export path.

## Steps (human + agent)

1. **Capture** (during call): rough notes or transcript tool; note exact **names**, **numbers**, **integrations** they mention.
2. **Drop into agent** using `prompts/conversation-ingest.md` with the raw text in the fenced block.
3. **Agent produces** the six sections in that prompt; artifact must be **copy-pasteable** (Markdown in chat or a linked gist/repo branch).
4. **Human sanity check** (2 minutes): wrong persona? wrong P0? Fix in thread once.
5. **Register hubs**: add any cited URLs/docs to `registry/hubs.json` so the next session does not lose context.
6. **Optional async**: run design or eng review skills on the plan if stakes are high.

## Success criteria

- Stakeholder can answer “what happens next?” without re-explaining the problem.
- P0 scope fits in one small milestone (days, not months).

## Failure modes to avoid

- Generic advice with no artifact.
- Plan that ignores stated constraints.
- Hub left implicit (“I’ll send that doc later”) with no manifest entry.
