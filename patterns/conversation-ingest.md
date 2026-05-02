# Pattern: Conversation Ingest

Turn a live conversation (call, meeting, WhatsApp thread) into a structured plan + first artifact.

## When to use

- After a client call where you need to deliver something
- At the end of a product conversation that produced ideas
- When handing off to a new Claude session with no prior context

## The intake prompt

Drop the conversation transcript or notes into Claude with this structure:

```
## Source
[Paste transcript, notes, or rough bullet points here]

## What I need
- Stakeholder recap (who was in the room, their perspective)
- Problem statement + explicit non-goals
- Plan with P0 milestone marked
- First concrete artifact (choose one: PRD / API sketch / wireframe copy / repo scaffold)
- Open questions (max 5, ranked by blocking-ness)
- Hub hooks (what knowledge to register in registry/hubs.json)
```

## Output format

Agent produces six sections:

### 1. Stakeholder recap
Who was in the call, what they care about, what they confirmed, what they're uncertain about.

### 2. Problem statement
One paragraph. What is broken, for whom, why the current solution fails.
Non-goals listed explicitly — what this does NOT solve.

### 3. Plan
Milestones with P0 marked. P0 = the one thing that must happen before anything else.

### 4. First artifact
**Choose exactly one:**
- PRD (if goal is ambiguous and needs alignment)
- API sketch (if backend shape is the open question)
- Wireframe copy (if UI flow is the open question)
- Repo scaffold (if setup is the blocker)

### 5. Open questions
Max 5. Ranked by: does this block P0? If yes, it's top of list.

### 6. Hub hooks
What needs to be registered:
- New NotebookLM source to add
- New Magic Patterns board to store
- New document to add to hubs/

## Sanity check (2 min, human does this)
- Is P0 actually the most important thing?
- Is the persona/struggling moment correct?
- Are the constraints real (not assumed)?

## Register hubs
After sanity check, add new hub entries to `registry/hubs.json`.

## Success criterion
Stakeholder can answer "what's next?" without re-explaining the context.
