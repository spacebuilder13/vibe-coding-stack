# Skill: new-repo-setup

Bootstrap a new project repo with vibe-coding-stack standards in one pass.

**Trigger phrases:** "set up a new repo", "create a new project", "bootstrap this project",
"new repo for <name>", "initialize project repo".

---

## What this skill does

Creates a fully wired project repository: git init, GitHub repo, CLAUDE.md/AGENTS.md,
design system tokens, Vercel config, and vibe-coding-stack hub registration — all in
one session.

---

## Pre-flight checklist

Before starting, gather:

| Item | Why |
|------|-----|
| Project name | Repo name, branding |
| GitHub org/user | Where to push |
| Starting point | Blank / clone existing repo / Lovable export |
| Design system | URL or repo (e.g. Sandy lab URL) |
| Backend | Supabase / Firebase / none |
| Deployment target | Vercel / Fly.io / other |
| Context sources | Claude project URL, NotebookLM URL |
| Stack preference | React/Vite / Next.js / other |

---

## Steps

### 1 — Clone or scaffold

**From existing GitHub repo (Lovable export, etc):**
```bash
cd /Users/jarvis/Projects
git clone <github_url> <project-slug>
```

**From scratch:**
Use `cursor-app-control` MCP → `create_project` tool with path and name.

### 2 — Apply design system

Follow the `apply-design-system` skill (`.cursor/skills/apply-design-system/SKILL.md`).

For Sandy (TQI projects):
- Update `src/index.css` with Sandy CSS tokens (see skill for full token set)
- Update `tailwind.config.ts` with Sandy fonts, colors, motion, radius
- Apply mobile-first AppLayout with bottom tab bar

### 3 — Wire context

Follow the `cloud-chat-context` skill (`.cursor/skills/cloud-chat-context/SKILL.md`).

Create in the new repo:
- `CLAUDE.md` — stack, design system, conventions, context URLs
- `AGENTS.md` — agent layer instructions
- `README.md` — project identity, stack, dev/deploy instructions

### 4 — Add deployment config

**Vercel (Vite/React SPA):**
```json
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

**Vercel (Next.js):** no config needed; Vercel auto-detects.

### 5 — Initial commit and push

```bash
git add -A
git commit -m "Bootstrap: <project name> with Sandy design system + vibe-stack conventions"
git push origin main
```

### 6 — Register in vibe-coding-stack

Update `hubs/manifest.yaml`:
```yaml
hubs:
  - id: <project-slug>
    name: <Project Name>
    repo: https://github.com/<org>/<repo>
    design_system: <design system URL>
    stack: react-vite / nextjs / other
    deployment: vercel / flyio / other
    claude_project: <url or null>
    notebooklm: <url or null>
    created: <YYYY-MM-DD>
    notes: <one-line description>
```

Also update `registry/hubs.json`.

### 7 — Move agent workspace (optional)

To make Cursor work natively in the new repo:
Use `cursor-app-control` MCP → `move_agent_to_root` with the new project path.

---

## Output checklist

- [ ] Repo cloned or created
- [ ] Design system applied (tokens, fonts, motion)
- [ ] `CLAUDE.md` written with full context
- [ ] `AGENTS.md` written with agent instructions
- [ ] `README.md` updated with project identity
- [ ] `vercel.json` (or equivalent) added
- [ ] Build passes (`npm run build` exits 0)
- [ ] TypeScript passes (`npx tsc --noEmit` exits 0)
- [ ] Committed and pushed to GitHub
- [ ] Registered in `hubs/manifest.yaml` + `registry/hubs.json`

---

## Template file locations

After running this skill, the vibe-coding-stack has these templates you can copy-paste:

- **Sandy design tokens** — see `apply-design-system` skill
- **CLAUDE.md** — see `cloud-chat-context` skill
- **vercel.json** — `{"buildCommand":"npm run build","outputDirectory":"dist","framework":"vite","rewrites":[{"source":"/(.*)","destination":"/index.html"}]}`
- **Mobile-first AppLayout** — see `apply-design-system` skill

---

## Reference implementation

**Space Ships and Atoms (TQI)** is the canonical reference for all new TQI projects:
- Repo: `https://github.com/spacebuilder13/sparkle-space-vault`
- Local: `/Users/jarvis/Projects/sparkle-space-vault`
- Full Sandy implementation: `src/index.css`, `tailwind.config.ts`
- Mobile-first AppLayout with bottom tab bar: `src/components/layout/AppLayout.tsx`
- Auth flow: `src/contexts/AuthContext.tsx` + `src/components/auth/AuthForm.tsx`
- Supabase integration: `src/integrations/supabase/`
- Code-split routes with Suspense fallback: `src/App.tsx`

### When starting from a Lovable export

Lovable exports come with a generic Tailwind theme (shadcn defaults). After cloning:
1. Replace `src/index.css` with Sandy tokens (see `apply-design-system`)
2. Replace `tailwind.config.ts` with Sandy config
3. Update `CLAUDE.md` with project identity and context URLs
4. Run the `apply-design-system` polish checklist
5. `npm run build` — must pass with zero warnings before proceeding
