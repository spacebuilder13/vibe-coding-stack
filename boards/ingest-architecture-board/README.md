# Ingest v3 architecture board

**Source of truth** for diagram + blueprint: this folder (`data/`).

## Preview locally

```bash
cd boards/ingest-architecture-board && python3 -m http.server 4173
```

Open `http://localhost:4173`.

## Hosted + comments

- **Pages**: https://spacebuilder13.github.io/ingest-architecture-board/
- **Giscus** in `app.js` targets repo `spacebuilder13/ingest-architecture-board` (install [giscus app](https://github.com/apps/giscus) if comments are blank).

## Keep deploy repo in sync

From the **vibe-coding-stack** repo root (adjust path if your clone differs):

```bash
rsync -av --delete --exclude README.md \
  boards/ingest-architecture-board/ \
  ../ingest-architecture-board/
```

Use `--exclude README.md` so the deploy mirror can keep its own top-level README (Pages + Giscus notes).

Then commit and push `ingest-architecture-board` so GitHub Pages updates.

## Vercel

Import [vibe-coding-stack](https://github.com/spacebuilder13/vibe-coding-stack) and set **Root Directory** to `boards/ingest-architecture-board`, or deploy the standalone repo above.
