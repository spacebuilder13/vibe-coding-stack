# Domain: Coding

When to load: writing code, choosing a stack, setting up a new project.

## Default stack (most apps)

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend | React + Vite + TypeScript | Fast setup, wide ecosystem |
| Styling | Tailwind CSS + Sandy tokens | Utility + design system |
| Components | shadcn/ui + Radix UI | Accessible, composable |
| API | Vercel Functions (Node.js) | Co-located with frontend |
| DB / Auth | Supabase | Postgres + GAuth out of the box |
| Deploy | Vercel | Zero-config, instant preview URLs |

## Alt stack (edge / SSR apps)
- TanStack Start + Cloudflare Workers — for global edge SSR
- Bun as package manager for speed
- `wrangler.jsonc` for Cloudflare config

## API pattern (Vercel Functions)

```
api/
  _lib/
    anthropic.js      ← shared Claude client
    session-kv.js     ← Vercel KV session helper
    token-usage-ledger.js ← cost tracking per session
  chat-generate.js    ← POST /api/chat-generate
  voice-generate.js   ← POST /api/voice-generate (if voice)
  doc-parse.js        ← POST /api/doc-parse (if file upload)
```

## Shared API libs (reuse from project-sandy/project-insurance)

- `api/_lib/anthropic.js` — Anthropic client with model routing
- `api/_lib/session-kv.js` — Vercel KV persistence
- `api/_lib/token-usage-ledger.js` — per-session cost tracking

## File structure (standard app)

```
/
  api/           ← Vercel Functions
  outputs/       ← single-file HTML outputs (frozen UIs)
  src/           ← React source (if SPA)
  public/        ← static assets
  vercel.json    ← routing + rewrites
  CLAUDE.md      ← project-specific agent instructions
  HANDOVER.md    ← current state + next steps
```

## Code rules
- Single-file HTML outputs for frozen UI states (preserves working snapshots)
- `localStorage` for client-side session (7-day TTL)
- No framework overhead when a direct API call works
- Reuse shared libs before writing new ones
- Match existing code style in the target repo
- No speculative abstractions — three similar lines > premature abstraction

## Skills
| Skill | When |
|-------|------|
| `/simplify` | Review changed code for reuse, quality, efficiency |
| `/health` | Code quality dashboard — types, lint, tests, dead code |

## Anti-patterns
- Adding error handling for scenarios that can't happen
- Creating helpers for one-time operations
- Feature flags when you can just change the code
- Comments on self-evident code
- Framework overhead when a direct call works
