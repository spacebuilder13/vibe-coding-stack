# youtube-top-comments

Bundled in **vibe-coding-stack** at `tools/youtube-top-comments/` (can also exist as a standalone repo).

Fetch YouTube **top** comments via [yt-dlp](https://github.com/yt-dlp/yt-dlp), then **sort by likes** in CSV/MD exports.

**For Cursor agents or automation:** read **[AGENTS.md](./AGENTS.md)** first — setup, one-liner commands, I/O layout, flags, limits.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python fetch_comments.py --urls-file example_urls.txt --insecure --single-md out.md
```

Artifacts: `out/<video_id>/` plus optional combined markdown from `--single-md`.

## Optional sample inputs

- `example_urls.txt` — minimal demo URL  
- `india_insurance_urls.txt` + `india_insurance_all_comments.md` — frozen example corpus from an earlier project (large MD)

## Deno & TLS

Deno improves YouTube JS paths; install from https://deno.land — details in **AGENTS.md**. Use `--insecure` if you hit certificate errors on macOS.
