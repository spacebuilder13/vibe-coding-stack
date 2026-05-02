# Pattern: NotebookLM 360-Degree Query

Multi-advisor knowledge synthesis. Query sequentially, synthesize carefully.

## When to use

- Client-facing coaching or advisory work
- Research question with multiple valid expert perspectives
- Before making a recommendation that has real consequences

## Setup

Each domain of expertise gets its own notebook:
- Client transcripts notebook (raw source material)
- Expert 1 notebook (e.g. Anil Lamba — JMA, manufacturing, India business)
- Expert 2 notebook (e.g. Mike Michalowicz — Profit First, cashflow)
- Expert 3 notebook (e.g. Garrett Gunderson — debt sequencing, cash flow index)
- Expert 4 notebook (e.g. Philip Campbell — 13-week cash flow model)
- Compliance notebook (tax, GST, regulatory)

Register all notebooks in `registry/hubs.json`.

## Query discipline

### Sequential, not parallel
Query one advisor at a time. Do not blend advisors in a single query.
Blending pollutes each voice and makes it impossible to attribute disagreements.

### Per-advisor query format
```
Context: [1-2 lines of the specific situation]
Question: [one clear question]
Constraint: answer only from [Advisor Name]'s framework
```

### Synthesis step (after all advisors queried)
1. List where advisors agree
2. List where they diverge (and why — different frameworks, different assumptions)
3. State the synthesis recommendation with explicit weighting rationale
4. Flag open questions that no advisor resolved

## Source inventory file

Create `<project>_source_index.md` per project:
```
## Notebook 1: Client Transcripts
Sources: [list each file + date added]
Last updated: [date]

## Notebook 2: Anil Lamba
Sources: [list]
Query rules: [any specific constraints for this advisor]
```

## Real usage (project-sandy / project-ob)

**project-sandy:** 5 notebooks (23 client sources + 4 expert advisors + India tax)
**project-ob:** 6 notebooks (50+ sources — OB transcripts + 5 framework advisors)

Query pattern: weekly coaching review → all 5 advisors queried on the week's open questions → synthesis into coaching intervention.

## Anti-patterns
- Querying multiple advisors in one prompt (voices blend, citations become unreliable)
- Not maintaining a source inventory (hard to know what each notebook knows)
- Using NotebookLM for real-time responses (it's for synthesis, not live chat)
- Skipping the synthesis step (individual answers aren't the deliverable)
