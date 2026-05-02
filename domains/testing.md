# Domain: Testing

When to load: QA pass needed, bug to investigate, performance check, post-deploy monitoring.

## Core principle
Test at system boundaries. Trust internal code and framework guarantees.
Only validate at: user input, external APIs, LLM outputs.

## Skills for testing

| Skill | When |
|-------|------|
| `/qa` | Full QA pass — finds bugs, fixes them, iterates until pass |
| `/qa-only` | Report only — no auto-fixes, structured output with health score |
| `/investigate` | Unknown root cause — 4 phases: investigate, analyze, hypothesize, implement |
| `/health` | Code quality dashboard — types, lint, tests, dead code |
| `/benchmark` | Performance regression — page load, Core Web Vitals, resource sizes |
| `/canary` | Post-deploy monitoring — console errors, perf regressions, page failures |
| `/browse` | Navigate live URL, interact with elements, verify state |

## Screenshot QA protocol (from zen-money-manager-d8a17b9e)

Used for visual/animation-heavy UIs:
1. **Baseline score** — rate current state 0-10 on 5 axes
2. **Audit** — severity-ranked findings (P0/P1/P2)
3. **Remediate** — fix P0s first
4. **Rerun** — screenshot at key interaction points
5. **Delta score** — document improvement (e.g. 7.4 → 8.5)

5 scoring axes:
- Beat sync / timing fidelity
- Visual hierarchy fidelity
- Emotional closure / end states
- Interaction correctness (switch, restart, reset)
- Runtime stability (rAF lifecycle, offscreen pausing)

## Prompt series for quality loops (from audit-report.md)
1. Fidelity contract — define non-negotiables upfront
2. Runtime correctness gate — lifecycle, state reset, edge cases
3. Screenshot QA protocol — frame audits at boundary moments
4. Gap scoring — 0-10 per axis
5. No-excuse completion — implement → verify → compare → output delta

## LLM output validation
- Validate structure (schema), not content
- Use confidence tags for uncertain spans
- Gate on quality score before writing to knowledge base
- Evaluator-optimizer loop: generator LLM + reviewer LLM

## Anti-patterns
- Mocking the database in integration tests
- Validating internal code that can't fail
- Testing without a baseline score to compare against
- Shipping without a `/qa` pass
- Autonomous fix loops without a human gate
