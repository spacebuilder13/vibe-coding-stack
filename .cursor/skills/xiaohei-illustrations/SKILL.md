---
name: xiaohei-illustrations
description: Generate quirky hand-drawn English article illustrations starring Xiaohei. Use when the user asks for "article illustrations", "body images", "blog illustrations", "illustration suggestions", "shot list", "hand-drawn diagrams", "Xiaohei images", or wants visuals for an English article, post, blog, Notion doc, workflow, methodology, process, structure, state, metaphor, or opinion piece. Default style is the Xiaohei IP — pure white background, black hand-drawn line art, sparse red/orange/blue annotations, clean but wildly imaginative.
---

# Xiaohei Absurdist Article Illustrations

## Core positioning

Design and generate 16:9 landscape body illustrations for English articles. The goal is not commercial illustration, PPT infographics, or cute cartoons — it is turning the article's key judgments, workflows, structures, states, or metaphors into a clean, absurd, creative, readable-but-not-instructional hand-drawn explanatory sketch.

The default visual IP is "Xiaohei" (小黑, "little black"): a solid-black creature with white dot eyes, thin legs, and a blank expression, earnestly doing something absurd but coherent. Xiaohei must participate in the core action of every image — never just stand at the side as decoration.

## Read these references first

Load them per task as needed — do not stuff all of them into context at once:

- `references/style-dna.md` — style DNA, colors, text rules, prohibitions.
- `references/xiaohei-ip.md` — Xiaohei's appearance, personality, action library, and prohibitions.
- `references/composition-patterns.md` — structure types, original-metaphor method, anti-copying rules.
- `references/prompt-template.md` — the single-image generation prompt template.
- `references/qa-checklist.md` — post-generation checks and iteration rules.

## Workflow

### 1. Digest the article

Read the article, link, Notion page, Markdown file, or screenshot content the user provides. Extract:

- What is the core argument?
- Which paragraphs carry cognitive turning points?
- Which content is best explained with an image?
- Which parts work as text only and need no image?

Do not distribute images evenly. Prioritize "cognitive anchors", e.g.: core judgments, two breakpoints, input–output loops, forks, before/after contrasts, one-input-many-outputs, handoff paths, common pitfalls, character state changes.

### 2. Deliver an illustration strategy first

If the user only asks to "analyze what to illustrate / think about where images are needed", produce a shot list first. For each shot specify:

- Which paragraph it follows
- The image's theme
- The core idea
- The structure type
- What Xiaohei is doing in the image
- Suggested elements
- Suggested English annotation words

Default 4–8 shots. Use 1–3 for very short pieces; do not exceed 9 even for long articles. Enough is enough — do not turn the article into a picture book.

### 3. Generate one image at a time

If the user explicitly asks to "generate / output / make the images / create them", do not stop to wait for confirmation. Use Cursor's built-in image generation tool in the agent flow, generating each image individually. Never combine multiple shots into one image.

Each image explains only one core structure. The prompt must include:

- 16:9 horizontal English article illustration
- Pure white background
- Black hand-drawn line art
- Sparse red/orange/blue handwritten English annotations
- Lots of empty white space
- Xiaohei as the subject of the core action
- Prohibitions: PPT style, commercial illustration, childish cuteness, complex architecture, top-left type titles

Do not replicate past examples. Examples only calibrate style density and how Xiaohei participates; never directly reuse known compositions like "conveyor-belt breakpoints / Xiaohei pulling lines / content fish / stamping toolbox / common-pitfalls path" unless the user explicitly asks to replicate a specific image. Invent a fresh, strange-but-coherent metaphor from the current article every time.

**Fallback:** if the built-in image generation tool is unavailable in the current environment, do not fail — output one complete copy-paste-ready prompt block per shot (built from `references/prompt-template.md`) so the user can paste it into any image tool.

### 4. Check and iterate

After generation, check against `references/qa-checklist.md`. Regenerate or locally edit first if any of these appear:

- Xiaohei is only decorative
- The frame is too crowded
- It looks like a flowchart/PPT
- Too much text or serious misspellings
- A title like "Common Pitfalls / Workflow / System Architecture" appears in the top-left corner
- The style is too cute, childish, or stiff
- The background is not clean white

### 5. Save and deliver

When working inside a workspace, copy the final images to:

```text
assets/<article-slug>-illustrations/
```

Named sequentially:

```text
01-topic-name.png
02-topic-name.png
```

Cursor's image tool auto-saves generated images under `assets/`; move/rename them into the folder above. Keep the original generated files and never overwrite existing assets unless the user explicitly asks for replacement.

## Output style

Pre-generation strategy output should be short and precise. Post-generation delivery must include:

- How many images were generated
- Each image's purpose
- Save paths
- Which images are the most reliable, and which are optional

Do not write long essays about style theory; let the images speak.

## Test this skill

Paste this into the Cursor agent to smoke-test the skill end to end:

> Use the xiaohei-illustrations skill. Design and generate 2 illustrations for this paragraph: "Most side projects die between the demo and the deploy. The demo takes a weekend; the deploy needs auth, billing, and error handling — so the project stalls in the gap, waiting for a burst of motivation that never comes."

Expected result:

- 2 PNGs saved in `assets/side-project-gap-illustrations/` (`01-...png`, `02-...png`)
- 16:9, pure white background, black hand-drawn line art
- Xiaohei performing the core action in each image (e.g. stuck in the gap, not watching from the side)
- At most 5–8 short English handwritten labels per image, sparse red/orange/blue only
- No top-left title, no PPT look, two different fresh metaphors (not copied from known examples)
