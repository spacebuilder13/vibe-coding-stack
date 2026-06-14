# Spar ritual

Run when vibe-coding-stack session starts, `PROGRAM.md` has no active brief, and `docs/harness-learnings-from-osf.md` has unchecked rollout items.

## Steps

1. Read `docs/harness-learnings-from-osf.md` + `docs/ai-native-org-setup.md`
2. **Do not write code first.** Open with: *"Spar mode: OSF harness learnings ready to roll out org-wide."*
3. Ask Utsav **one question at a time:**
   - Which pattern ships to ALL hubs first? (DSS router / learn hub / compliance scaffold / observability)
   - Which hubs are in scope this quarter? (list from `registry/hubs.json`)
   - What is the enforcement level? (docs-only / cursor rules / CI gates)
4. Produce `docs/rollout-plan-YYYY-MM-DD.md` with per-hub checklist
5. Human approves plan before any registry `VERSION` bump or cross-repo changes

## Exit

When plan is approved, move items from harness-learnings checklist into the rollout plan and mark spar complete in SESSION notes.
