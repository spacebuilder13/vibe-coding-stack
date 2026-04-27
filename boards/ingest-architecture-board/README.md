# Ingest v3 Architecture Board

A lightweight review board for:

- Mermaid architecture visualization
- Blueprint markdown side panel
- Persistent comments and Q&A via GitHub Discussions (Giscus)

## Local preview

From this folder, run:

```bash
python3 -m http.server 4173
```

Open `http://localhost:4173`.

## GitHub hosting

1. Push this folder to a GitHub repo.
2. Enable GitHub Discussions in repo settings.
3. Install [Giscus app](https://github.com/apps/giscus) on the repo.
4. Create a Discussions category named `Architecture Feedback`.
5. Go to [giscus.app](https://giscus.app) to generate:
   - `data-repo-id`
   - `data-category-id`
6. Update those IDs in `app.js`.

## Vercel hosting

After the repo is on GitHub:

1. Open [Vercel New Project](https://vercel.com/new)
2. Import this repo
3. Deploy with default static settings (no build command required)

Or one-click (replace with your final repo URL):

`https://vercel.com/new/clone?repository-url=https://github.com/<you>/<repo>`
