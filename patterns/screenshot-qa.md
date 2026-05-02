# Pattern: Screenshot QA

Visual QA protocol for UI-heavy apps. Establishes baseline, audits, remediates, rescores.

## When to use

- Any app with animation or beat-synced content
- Before shipping a new design direction
- After a major UI change
- When `/qa` passes but something "feels off"

## The 5-step loop

### 1. Fidelity contract
Before QA, define non-negotiables:
- What must work perfectly (beat sync, emotional closure, state reset)
- What is acceptable to be imperfect (minor animation timing)
- What would block ship (broken layout, unreadable text, missing state)

### 2. Baseline score
Score current state 0–10 on 5 axes:

| Axis | What to measure |
|------|----------------|
| **Visual hierarchy** | Clear reading order, one dominant element |
| **Motion fidelity** | Animation communicates, not decorates |
| **Emotional closure** | End states feel complete, not abandoned |
| **Interaction correctness** | Switch, reset, restart work cleanly |
| **Runtime stability** | No layout shift, no memory leak, rAF lifecycle clean |

Document as: `7.4 / 10 — baseline (date)`

### 3. Audit
Use `/browse` or manual screenshots to capture:
- Key interaction moments (load, first action, edge case)
- End states (completion, empty state, error)
- Mobile viewport (375px width minimum)

Rank findings: P0 (blocks ship) / P1 (degrades experience) / P2 (nice-to-fix)

### 4. Remediate
Fix P0s first. Then P1s. Stop before P2s unless trivial.
One fix per commit. Screenshot after each fix.

### 5. Rescore
Score again on the same 5 axes.
Document as: `8.5 / 10 — post-remediation (date). Delta: +1.1`

Residual gaps: list P2s that remain, with rationale for deferral.

## Real example (zen-money-manager-d8a17b9e)

**Woven Stories QA:**
- Baseline: 7.4 / 10
- P0s found: story switch left residual state, end frame blank, rAF not pausing offscreen
- Post-remediation: 8.5 / 10
- Residual: minor beat timing on Story C at 32s mark (P2, deferred)

## Template

```
## Screenshot QA — [App Name] — [Date]

### Baseline
- Visual hierarchy: X/10
- Motion fidelity: X/10
- Emotional closure: X/10
- Interaction correctness: X/10
- Runtime stability: X/10
**Total: X.X / 10**

### P0 findings
1. [finding] — [screenshot ref]

### P1 findings
1. [finding]

### Post-remediation
**Total: X.X / 10 (delta: +X.X)**

### Residual P2s
- [finding] — deferred because [reason]
```
