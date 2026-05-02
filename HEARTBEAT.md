# Heartbeat
# Tier 0 — prompt-cached. Quick-check list to run at session start.

## On every session start
- [ ] Read SOUL.md — identity loaded
- [ ] Read STACK.md — environment indexed
- [ ] Check if PROGRAM.md has an active brief
- [ ] Check if BUILD.md has an in-progress spec
- [ ] Check app-store/STORE.md — any apps missing URLs?

## On every ship
- [ ] URL added to BUILD.md checklist
- [ ] App registered in app-store/STORE.md
- [ ] VERSION bumped if stack files changed
- [ ] CHANGELOG.md updated

## Red lines (never proceed past these without human confirmation)
- Do not write production code before design is approved
- Do not deploy without a passing /qa run
- Do not merge registry changes without bumping VERSION
