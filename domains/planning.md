# Domain: Planning

When to load: brief is ambiguous, goal needs scoping, milestones needed, or sprint review.

## Core principle
Plan before pixels for ambiguous goals. Ship a thin vertical slice for clear goals.
Never plan more than you need to execute the next concrete step.

## Skills for planning

| Skill | When |
|-------|------|
| `/plan-eng-review` | Lock architecture + execution plan — milestones, risks, data flow |
| `/plan-ceo-review` | Challenge problem framing — is this the right thing to build? |
| `/autoplan` | Full CEO + design + eng + DX review in sequence — high-stakes only |
| `/office-hours` | YC-style forcing questions on demand, wedge, desperation |
| `/retro` | Weekly retrospective — commit history, patterns, quality metrics |
| `/document-release` | Post-ship docs update |

## Build workflow gates

**Before writing code:**
1. PROGRAM.md filled → brief is clear, constraints locked
2. BUILD.md written → spec approved by human
3. Design direction confirmed → visual gate passed

**Before shipping:**
4. `/qa` passed
5. URL confirmed working
6. `app-store/STORE.md` updated

## Plan artifacts
- `PROGRAM.md` — the brief (human-written, one per project)
- `BUILD.md` — the spec (agent-written, human-reviewed)
- `boards/` — architecture diagrams for complex systems

## Connectors
- `linear` — task creation via MCP (registry/connectors.json)
- `github` — issues + PRs for milestone tracking

## Anti-patterns
- Planning without a PROGRAM.md (no anchor for the brief)
- Writing BUILD.md without human review
- Skipping the gate between spec and code
- Producing a plan with no concrete next artifact
