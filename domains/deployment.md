# Domain: Deployment

When to load: choosing a deploy target, writing vercel.json, setting env vars, CI/CD.

## Default: Vercel

Use Vercel for all apps unless there's a specific reason not to.

```json
// vercel.json — standard pattern
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/outputs/$1.html" }
  ],
  "functions": {
    "api/*.js": { "maxDuration": 30 }
  }
}
```

**Env vars to set in Vercel dashboard (never in code):**
- `ANTHROPIC_API_KEY`
- `ELEVENLABS_API_KEY` (if voice)
- `KV_REST_API_URL` + `KV_REST_API_TOKEN` (if session persistence)
- All connector env_vars from `registry/connectors.json`

## Supabase (for auth + database)

Use when app needs: GAuth login, PostgreSQL, realtime, edge functions.

```
SUPABASE_URL=https://<project>.supabase.co
SUPABASE_ANON_KEY=<anon-key>
SUPABASE_SERVICE_ROLE_KEY=<service-role-key> (server-side only)
```

GAuth setup: Supabase dashboard → Auth → Providers → Google → add client ID + secret.

## Cloudflare Workers (alt — edge SSR)

Use for TanStack Start apps needing global low-latency SSR.

```jsonc
// wrangler.jsonc
{
  "name": "app-name",
  "compatibility_date": "2025-09-24",
  "compatibility_flags": ["nodejs_compat"]
}
```

Build: `vite build` → deploy: `wrangler deploy`

## GitHub Pages (for static boards)

Use for architecture boards and static docs only.
Deploy via: push to `main` → Pages auto-deploys from root or `/docs`.

## App store publish flow

After deploy:
1. Confirm URL is live and `/qa` passes
2. Add entry to `app-store/STORE.md`
3. Full workflow: `app-store/publish.md`

## Skills

| Skill | When |
|-------|------|
| `/ship` | Full ship workflow — merge, version bump, changelog, PR |
| `/land-and-deploy` | After PR created — merge, wait for CI, verify prod |
| `/setup-deploy` | Configure deploy settings for a new project |
| `/canary` | Post-deploy health monitoring |

## Anti-patterns
- Env vars in code or committed to git
- Deploying without a passing `/qa`
- Not registering in `app-store/STORE.md` after deploy
- Using Cloudflare when Vercel is sufficient
