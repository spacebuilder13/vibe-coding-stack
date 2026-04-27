# AGENTS — youtube-top-comments

Small tool: **fetch YouTube comments** (yt-dlp, “Top comments”), **re-sort by likes**, write **JSON/CSV/MD** per video and optional **one combined MD**.

---

## When to use this repo

- You have **watch URLs or a playlist URL** and need **exported comments** for analysis, RAG, or a design/research bundle.
- You do **not** need the video file — metadata + comments only.

---

## Setup (once per machine)

```bash
cd <this-repo>
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

**Deno (recommended):** `curl -fsSL https://deno.land/install.sh | sh`  
The script resolves `~/.deno/bin/deno`, `deno` on `PATH`, or `$DENO_PATH`. Without Deno, YouTube extraction is weaker; still often works for comments.

**TLS errors on macOS:** add `--insecure` to the command below.

---

## Default task (copy-paste)

Replace `urls.txt` with your list (one URL per line; `#` comments allowed).

```bash
cd <this-repo> && source .venv/bin/activate
python fetch_comments.py --urls-file urls.txt --fetch-budget 1000 --insecure \
  --single-md ALL_COMMENTS.md
```

- **`out/<video_id>/`** — per-video artifacts (see below).
- **`ALL_COMMENTS.md`** — optional single doc with TOC + all videos (only if `--single-md` is set).
- **`out/_run_summary.json`** — one-line-per-video outcome.

---

## Inputs

| Input | Notes |
|--------|--------|
| Positional args | One or more watch or playlist URLs. |
| `--urls-file PATH` | One URL per line; lines starting with `#` ignored. |
| Playlists | Flattened to individual videos; IDs deduped. |

---

## Outputs

| Path | Content |
|------|---------|
| `out/<id>/meta.json` | Title, channel, URLs, rows fetched vs `--min-comments`, notes |
| `out/<id>/comments.json` | Raw yt-dlp comment list |
| `out/<id>/comments_top_by_likes.csv` | Same data, sorted by `like_count` |
| `out/<id>/comments_top_by_likes.md` | Table + full text |
| `out/_run_summary.json` | Array of per-URL results |

`out/` is gitignored except when you intentionally commit snapshots.

---

## Useful flags

| Flag | Effect |
|------|--------|
| `--single-md FILE` | One markdown for all videos in the run. |
| `--fetch-budget N` | yt-dlp `max_comments` ceiling (default scales with `--min-comments`). |
| `--min-comments N` | Soft target; `meta.json` gets `meets_min: false` if fewer rows. |
| `--out DIR` | Output root (default `./out`). |
| `--insecure` | Skip TLS verify (common on stock macOS Python). |
| `--deno-path PATH` | Force Deno binary; else auto-resolve. |
| `--no-remote-ejs` | Do not fetch EJS helper assets from GitHub/npm (offline / policy). |

With Deno, the script sets `remote_components` to **`ejs:github`** and **`ejs:npm`** unless `--no-remote-ejs`. It also sets **`extractor_retries: 8`**.

---

## Expectations (do not over-promise)

- **Row count ≠ “all comments on YouTube.”** API limits, disabled comments, and “Incomplete data” from YouTube cap what returns.
- **“Top”** is extractor order; exports **re-rank by likes** for `*_top_by_likes.*`.
- **Members-only / age-gated** content needs cookies — this script does not handle auth unless you extend yt-dlp options yourself.

---

## What not to do

- Do not commit `.venv/` or bulk `out/` unless the user explicitly wants an archived snapshot.
- Do not parse `stderr` as JSON; JSON is only from written files or you must capture stdout from a custom wrapper (this CLI writes to disk).

---

## Entry point

**Single script:** `fetch_comments.py` — read `--help` for the full flag list.

**Dependencies:** `requirements.txt` (only `yt-dlp`).
