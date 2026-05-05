# Skill: apply-design-system

Apply a reference design system (from a URL or GitHub repo) to a project's CSS and config.

**Trigger phrases:** "apply design system", "apply this design system", "use this design system",
"import design tokens from", "port design system from <url>", "make it look like <reference site>".

---

## What this skill does

Extracts design tokens (colors, typography, spacing, motion, radius) from a reference design system
URL or GitHub repo, then applies them to a target project's `index.css`, `tailwind.config.ts`,
and component conventions.

---

## Step 1 — Audit the reference design system

**For a URL:** Use `WebFetch` to fetch the design system page.
Look for:
- Color tokens (CSS variables or named values)
- Font families and scale
- Spacing system
- Motion/animation tokens
- Border radius values
- Component naming conventions

**For a GitHub repo:** Clone/read the repo's CSS files:
```bash
git clone <repo_url> /tmp/<name>
cat /tmp/<name>/src/styles.css
cat /tmp/<name>/src/index.css
cat /tmp/<name>/tailwind.config.ts
```

### What to capture
- [ ] Background / surface color roles
- [ ] Ink / text color hierarchy (primary, soft, faint)
- [ ] Accent / brand color(s)
- [ ] Signal colors (ok, warn, error)
- [ ] Font families and their roles
- [ ] Font size scale and line heights
- [ ] Spacing unit (e.g. 4pt baseline)
- [ ] Border radius vocabulary
- [ ] Motion duration tokens + easing functions
- [ ] Motion principles (narrative: "breathe don't blink", etc.)

---

## Step 2 — Write `src/index.css`

Structure:
```css
/* 1. Font imports */
@import url('...');

/* 2. Tailwind directives */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* 3. CSS custom properties in :root (semantic roles, not raw values) */
@layer base {
  :root {
    /* Surfaces */
    --background: <hsl>;
    --foreground: <hsl>;
    /* ... all roles ... */

    /* Motion */
    --motion-instant: 80ms;
    --motion-quick: 180ms;
    --motion-calm: 420ms;
    /* ... */

    /* Easing */
    --ease-arrive: cubic-bezier(0.22, 1, 0.36, 1);
    /* ... */
  }
}

/* 4. Motion @keyframes */
@keyframes arrive { ... }
@keyframes breath { ... }
/* ... */

/* 5. Utility classes */
@layer utilities {
  .animate-arrive { ... }
  .press-scale { ... }
  /* ... */
}
```

**Key rule:** Use HSL format for all colors (`hsl(H S% L%)`), not hex. This enables opacity modifiers.

---

## Step 3 — Update `tailwind.config.ts`

Map CSS variables to Tailwind utilities:

```typescript
colors: {
  background: "hsl(var(--background))",
  foreground: "hsl(var(--foreground))",
  primary: { DEFAULT: "hsl(var(--primary))", foreground: "hsl(var(--primary-foreground))" },
  // ... all roles
  
  // Also add semantic named colors directly:
  sandy: {
    bg: "hsl(46 33% 96%)",
    gold: "hsl(36 72% 46%)",
    // ...
  },
},
borderRadius: {
  lg: "var(--radius)",
  md: "calc(var(--radius) - 4px)",
  pill: "var(--radius-pill, 9999px)",
  hero: "var(--radius-hero, 1.75rem)",
},
fontFamily: {
  sans:    ["Inter", ...],
  serif:   ["DM Serif Display", ...],
  mono:    ["IBM Plex Mono", ...],
  display: ["DM Serif Display", ...],
},
transitionDuration: {
  instant: "80ms",
  quick:   "180ms",
  calm:    "420ms",
},
transitionTimingFunction: {
  press:   "cubic-bezier(0.34, 1.56, 0.64, 1)",
  arrive:  "cubic-bezier(0.22, 1, 0.36, 1)",
},
animation: {
  arrive:      "arrive 420ms cubic-bezier(0.22, 1, 0.36, 1) both",
  breath:      "breath 900ms cubic-bezier(0.37, 0, 0.63, 1) infinite alternate",
  shimmer:     "shimmer 1.6s linear infinite",
  "page-arrive": "page-arrive 420ms cubic-bezier(0.22, 1, 0.36, 1) both",
},
```

---

## Step 4 — Component conventions

After tokens are in, establish component-level conventions:

### Typography classes
- `font-serif text-headline` → display headings (DM Serif)
- `font-sans text-body` → body copy (Inter)
- `font-mono text-micro` → metadata, numbers (IBM Plex Mono)

### Motion classes
- `animate-arrive` + `stagger-{1-5}` → staggered enter animations
- `press-scale` → on all tappable elements (scale 0.97 on :active)
- `animate-breath` → idle/ambient animations
- `animate-shimmer` → loading/parsing states

### Layout
- Mobile-first: design for 375px
- Max content width: `max-w-2xl mx-auto`
- Primary nav: bottom tab bar on mobile, top bar on desktop
- Spacing: 4pt baseline (Tailwind default)

### Cards
- `rounded-lg` (16px) for cards
- `rounded-hero` (28px) for hero sections
- `rounded-pill` for chips/badges
- Shadows: `shadow-card` (soft), `shadow-elevated` (floating)

---

## Sandy design system (TQI projects) — full reference

Source: `https://zen-design-pal.lovable.app/sandy-lab/`
GitHub: `https://github.com/spacebuilder13/zen-money-manager-d8a17b9e.git`

**Colors:**
```
--background:  46 33% 96%   sandy warm off-white
--primary:     36 72% 46%   sandy gold (warm amber)
--secondary:   192 28% 38%  sandy tea (cool slate)
--muted:       40 12% 90%
--accent:      44 100% 95%  gold wash
--border:      40 18% 86%   hairline
```

**Fonts:**
- DM Serif Display — emotional weight, display/heading
- Inter — body, clarity
- IBM Plex Mono — instrumentation, metadata

**Motion tokens:**
```
--motion-instant:   80ms   press ack
--motion-quick:     180ms  chip select
--motion-calm:      420ms  screen reveal
--motion-breath:    900ms  mandala pulse
--motion-cinematic: 1400ms section bloom
```

**Motion principles:**
1. Breathe, don't blink — loops are slow and continuous
2. Arrive, don't pop — elements ease in from slight offset
3. Reveal, don't replace — old content gives way
4. Calm under failure — errors settle, no shake, no loud red

**Full CSS token set:** See reference implementation at
`/Users/jarvis/Projects/sparkle-space-vault/src/index.css`

**Full Tailwind config:** See reference implementation at
`/Users/jarvis/Projects/sparkle-space-vault/tailwind.config.ts`

---

## Step 5 — Polish checklist (from real-world use)

After the design system is applied, audit these common issues:

### Tailwind class warnings
- `duration-[var(--motion-quick)]` → use `duration-quick` (already mapped in config)
- `duration-[var(--motion-calm)]` → use `duration-calm`
- Any `duration-[var(--motion-*)]` → replace with the token name directly

### Motion consistency
- Loading states: use `animate-breath` (not `animate-pulse` — that's not Sandy)
- Cards: add `press-scale` class to all tappable/clickable elements
- List reveals: add `animate-arrive` + inline `style={{ animationDelay: \`\${Math.min(i, 5) * 50}ms\` }}`

### Page headers
- Remove inline icons from `<h1>` text — use `text-headline font-serif` only
- Subtitle: `text-caption text-muted-foreground` (not `text-muted-foreground` alone)
- Keep headers to 2 lines max on mobile

### Card grids (mobile-first)
- Default: single column, full width
- Tablet+: `sm:grid-cols-2` maximum (avoid `lg:grid-cols-3` — too dense on tablet)
- Gap: `gap-3` (not `gap-4` — slightly tighter feels more considered)

### Code splitting (large pages)
- Lazy load routes that import images or have heavy dependencies:
  ```tsx
  const MentalModels = lazy(() => import("./pages/MentalModels"));
  // Wrap routes in <Suspense fallback={<PageLoader />}>
  ```
- Image-heavy pages (like mental model cards): add `loading="lazy"` to `<img>` tags

---

## Verification

After applying:
1. `npm run build` — must exit 0, **zero warnings**
2. `npx tsc --noEmit` — must exit 0
3. Visual check: load the app and verify font families, colors, card radius, bottom nav
4. Check for `duration-[var(--motion-*)]` warnings — replace with token names
