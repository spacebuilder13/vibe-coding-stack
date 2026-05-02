# Domain: Design

When to load: PROGRAM.md mentions UI, visual design, layout, tokens, or a design direction.

## Core principle
Principle-first design. No AI slop. Every visual decision must pass the 7 tests.
Greyscale first — earn your colour. One accent maximum.

## The 7 tests (Zen Design System)
1. Does it communicate without colour?
2. Does the motion mean something?
3. Is there one clear hierarchy?
4. Does every element earn its space?
5. Would a professional be proud to ship this?
6. Does it work at arms-length on a phone?
7. Is there one red (accent) — and only one?

## Design systems available

### Sandy Tokens (production — use by default)
Source: `registry/design-systems.json` → `sandy-tokens`
- **Colors:** bg `#FBFAF6`, ink `#1B1A17`, gold `#C4983A`, tea `#5C7C6E`
- **Fonts:** DM Serif Display (display) / Inter (body) / IBM Plex Mono (mono)
- **Easing:** `--ease-calm`, `--ease-arrive`, `--ease-breath`
- **Directions:** A (Quiet Mandala) · B (Editorial) · C (Spatial) · D (Living)

### Zen Design System (principles — reference)
Source: `registry/design-systems.json` → `zen-ds`
Philosophy + principles complete. Components partial. Use for principle guidance, not components.

### shadcn/ui + Radix (components)
`npx shadcn@latest add <component>` — 25+ primitives.
Use for interactive components (dialog, select, tabs). Sandy tokens override visual layer.

### Magic Patterns (prototyping)
MCP server: `magic-patterns`. Create board → store URL → generate code → track drift.
Known boards: `registry/design-systems.json` → `known_boards`

## Skills for design

| Skill | When |
|-------|------|
| `/design-shotgun` | Need variants to compare — generates multiple directions |
| `/design-html` | Direction locked — generates production HTML/CSS |
| `/design-review` | Visual QA — spacing, hierarchy, consistency, slop check |
| `/design-consultation` | Need a full design system from scratch |

## Workflow
1. Magic Patterns brief → generate prototype
2. Store board URL in `registry/design-systems.json`
3. Human approves direction (A/B/C/D or custom)
4. `/design-html` → production code with Sandy tokens applied
5. `/design-review` → QA pass
6. Track drift: if repo diverges from design URL, flag it

## Animation patterns (from zen-money-manager-d8a17b9e)
- **Graph paper effects:** breathing, gravity wells, mandala bloom, folded paper
- **Living lines:** marching ants, dot-matrix wave, electric arc, breathing dashes
- **Woven Stories:** beat-synced narrative with side-panel citations
- **Sacred geometry mandala:** CSS-animated circular loader

## Anti-patterns
- Colour before greyscale hierarchy is working
- Animation that doesn't communicate anything
- More than one accent colour
- Building UI before design direction is approved
- Ignoring the 7 tests
