# Security

## Reporting

If you find a vulnerability (for example a committed secret or unsafe default), open a **private** GitHub advisory or contact the maintainer directly. Do not post exploit details in public issues.

## Scope

This repository is **documentation and configuration only** (no application runtime, no dependencies, no CI secrets). Risk is mainly **accidental disclosure** via:

- Pasting API keys or tokens into `hubs/exports/` or prompts
- Committing `.env` files or private transcripts with PII

## Maintainer checks (last: 2026-04-28)

- [x] No `ghp_`, `gho_`, `github_pat_`, or `sk-` patterns in git history for tracked paths
- [x] `origin` remote is HTTPS without embedded credentials
- [x] No `/Users/` paths or local machine identifiers in tracked content
- [x] `.gitignore` excludes common env/key material and large hub binaries

Re-run before releases: `git grep -iE 'ghp_|gho_|github_pat_|sk-[a-z]' -- . ':!.git'` (should return nothing).
