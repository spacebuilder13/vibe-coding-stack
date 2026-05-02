# Domain: Security

When to load: auth setup, secrets management, security audit, or any user data handling.

## Core principle
Never store secrets in code. Validate at system boundaries only.
Minimum viable trust surface.

## Auth patterns

### Google Auth via Supabase (default)
```js
// Client
const { data, error } = await supabase.auth.signInWithOAuth({ provider: 'google' })

// Server (validate session)
const { data: { user } } = await supabase.auth.getUser(token)
```

### Session persistence
- Client-side: `localStorage` with 7-day TTL
- Server-side: Vercel KV (connector: `vercel-kv`)
- Never store raw API keys client-side

## Secrets checklist
- [ ] All API keys in Vercel env vars (never in `.env` committed to git)
- [ ] `.gitignore` covers: `.env`, `.env.local`, `*.pem`, `*.key`
- [ ] No `ghp_`, `gho_`, `github_pat_`, `sk-` patterns in committed code
- [ ] No local file paths in tracked content
- [ ] Service role keys (Supabase) only used server-side

## LLM trust boundaries
- Never pass raw user input directly to LLM without sanitization
- Validate LLM output structure before writing to DB
- Don't let users inject system prompt content via user-facing fields
- Rate limit API routes (Vercel: use KV for simple counters)

## Skills
| Skill | When |
|-------|------|
| `/cso` | Full security audit — secrets, deps, CI/CD, LLM boundaries |
| `/guard` | Combined: destructive command warnings + directory-scoped edits |
| `/careful` | Warns before rm -rf, DROP TABLE, force-push, etc. |

## SECURITY.md baseline
Every project should have `SECURITY.md` covering:
- What data is stored and where
- API key audit checklist
- No-PII-in-logs rule
- Incident response (delete source + stop, from ingest v3 Gate 2)

## Anti-patterns
- `.env` files committed to git
- Service role keys in client-side code
- Passing unsanitized user input to LLM system prompt
- Storing session tokens in localStorage without TTL
- Skipping auth on routes that access user data
