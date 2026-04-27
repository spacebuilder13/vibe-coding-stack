#!/usr/bin/env python3
"""YouTube top comments via yt-dlp; re-rank by like_count in exports. See AGENTS.md."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse, parse_qs

from yt_dlp import YoutubeDL

WATCH_RE = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/)([0-9A-Za-z_-]{6,})",
    re.I,
)


def resolve_deno_path(explicit: str | None) -> str | None:
    """Return path to deno binary for yt-dlp js_runtimes (EJS / n challenge)."""
    if explicit:
        p = Path(explicit).expanduser()
        return str(p) if p.is_file() else None
    env = os.environ.get("DENO_PATH") or os.environ.get("YT_DLP_DENO")
    if env:
        p = Path(env).expanduser()
        if p.is_file():
            return str(p)
    which = shutil.which("deno")
    if which:
        return which
    home = Path.home() / ".deno/bin/deno"
    if home.is_file():
        return str(home)
    return None


def ydl_base_opts(
    *,
    insecure: bool,
    deno_path: str | None,
    remote_ejs: bool,
) -> dict[str, Any]:
    opts: dict[str, Any] = {
        "quiet": True,
        "nocheckcertificate": insecure,
        "extractor_retries": 8,
    }
    if deno_path:
        opts["js_runtimes"] = {"deno": {"path": deno_path}}
        if remote_ejs:
            # Player / n-challenge helpers (see https://github.com/yt-dlp/yt-dlp/wiki/EJS )
            opts["remote_components"] = {"ejs:github", "ejs:npm"}
    return opts


def _video_id_from_url(url: str) -> str | None:
    u = url.strip()
    m = WATCH_RE.search(u)
    if m:
        return m.group(1)
    parsed = urlparse(u)
    if "youtube.com" in (parsed.netloc or "").lower():
        qs = parse_qs(parsed.query)
        v = qs.get("v", [None])[0]
        if v and re.fullmatch(r"[0-9A-Za-z_-]{6,}", v):
            return v
    return None


def expand_to_video_urls(
    seed: str,
    *,
    insecure: bool,
    deno_path: str | None,
    remote_ejs: bool,
) -> list[str]:
    """Return canonical watch URLs for a single video or all entries in a playlist."""
    seed = seed.strip()
    if not seed or seed.startswith("#"):
        return []

    flat_opts: dict[str, Any] = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "nocheckcertificate": insecure,
        "ignoreerrors": True,
    }
    flat_opts.update(ydl_base_opts(insecure=insecure, deno_path=deno_path, remote_ejs=remote_ejs))
    with YoutubeDL(flat_opts) as ydl:
        info = ydl.extract_info(seed, download=False)

    if not info:
        return []

    if info.get("_type") == "playlist":
        out: list[str] = []
        for ent in info.get("entries") or []:
            if not ent:
                continue
            vid = ent.get("id")
            if vid and re.fullmatch(r"[0-9A-Za-z_-]{6,}", str(vid)):
                out.append(f"https://www.youtube.com/watch?v={vid}")
        return out

    vid = info.get("id")
    if vid:
        return [f"https://www.youtube.com/watch?v={vid}"]
    return []


def read_urls_file(path: Path) -> list[str]:
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)
    return lines


def sort_by_likes(comments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def key(c: dict[str, Any]) -> tuple[int, str]:
        likes = c.get("like_count")
        try:
            li = int(likes) if likes is not None else 0
        except (TypeError, ValueError):
            li = 0
        cid = str(c.get("id") or "")
        return (li, cid)

    return sorted(comments, key=key, reverse=True)


def write_csv(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    fieldnames = [
        "rank_by_likes",
        "id",
        "author",
        "like_count",
        "is_pinned",
        "parent",
        "text",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for i, row in enumerate(rows, start=1):
            flat = {
                "rank_by_likes": i,
                "id": row.get("id"),
                "author": row.get("author"),
                "like_count": row.get("like_count"),
                "is_pinned": row.get("is_pinned"),
                "parent": row.get("parent"),
                "text": (row.get("text") or "").replace("\r\n", "\n").replace("\r", "\n"),
            }
            w.writerow(flat)


def video_section_markdown(
    rows: list[dict[str, Any]],
    meta: dict[str, Any],
    *,
    section_index: int,
    table_rows: int = 120,
) -> str:
    """One video’s block for a combined document (H2 spine)."""
    title = meta.get("title") or meta.get("id")
    lines = [
        f"## {section_index}. {title}",
        "",
        f"- **Video ID:** `{meta.get('id')}`",
        f"- **URL:** {meta.get('webpage_url') or ''}",
        f"- **Channel:** {meta.get('channel') or ''}",
        f"- **YouTube comment_count (reported):** {meta.get('comment_count_reported')}",
        f"- **Rows fetched (this run):** {meta.get('fetched_comment_rows')}",
        f"- **Fetch budget used:** {meta.get('fetch_budget')}",
    ]
    if meta.get("note"):
        lines.append(f"- **Note:** {meta['note']}")
    lines.extend(
        [
            "",
            "Sorted **top comments** from the extractor, then **by like_count** here.",
            "",
            "| # | likes | author | excerpt |",
            "|---|------:|--------|---------|",
        ]
    )
    for i, row in enumerate(rows[:table_rows], start=1):
        text = (row.get("text") or "").replace("\n", " ").strip()
        excerpt = text[:120] + ("…" if len(text) > 120 else "")
        excerpt = excerpt.replace("|", "\\|")
        author = str(row.get("author") or "").replace("|", "\\|")
        likes = row.get("like_count") if row.get("like_count") is not None else ""
        lines.append(f"| {i} | {likes} | {author} | {excerpt} |")

    lines.extend(["", "### Full text (same order: by likes)", ""])
    for i, row in enumerate(rows, start=1):
        parent = row.get("parent")
        pin = " (pinned)" if row.get("is_pinned") else ""
        thread = f" — **reply to** `{parent}`" if parent else ""
        lines.append(
            f"#### {i}. {row.get('author') or 'unknown'}{pin} — {row.get('like_count') or 0} likes{thread}"
        )
        lines.append("")
        lines.append(row.get("text") or "")
        lines.append("")
    return "\n".join(lines)


def write_markdown(path: Path, rows: list[dict[str, Any]], meta: dict[str, Any]) -> None:
    title = meta.get("title") or meta.get("id")
    lines = [
        f"# Comments: {title}",
        "",
        f"- **Video:** {meta.get('webpage_url') or ''}",
        f"- **Fetched:** {meta.get('fetched_comment_rows')} rows (top sort, then ranked by likes here)",
        f"- **Target min:** {meta.get('target_min_comments')}",
        "",
        "| # | likes | author | excerpt |",
        "|---|------:|--------|---------|",
    ]
    for i, row in enumerate(rows[:80], start=1):
        text = (row.get("text") or "").replace("\n", " ").strip()
        excerpt = text[:120] + ("…" if len(text) > 120 else "")
        excerpt = excerpt.replace("|", "\\|")
        author = str(row.get("author") or "").replace("|", "\\|")
        likes = row.get("like_count") if row.get("like_count") is not None else ""
        lines.append(f"| {i} | {likes} | {author} | {excerpt} |")

    lines.extend(["", "## Full text (top by likes)", ""])
    for i, row in enumerate(rows, start=1):
        lines.append(f"### {i}. {row.get('author') or 'unknown'} — {row.get('like_count') or 0} likes")
        lines.append("")
        lines.append(row.get("text") or "")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def build_combined_markdown(
    blocks: list[tuple[dict[str, Any], list[dict[str, Any]]]],
    *,
    title: str,
    source_file: str | None,
) -> str:
    toc: list[str] = ["## Table of contents", ""]
    for i, (meta, _) in enumerate(blocks, start=1):
        t = meta.get("title") or meta.get("id")
        vid = meta.get("id")
        toc.append(f"{i}. [{t}](#{vid})")
    toc.append("")

    header = [
        f"# {title}",
        "",
        "_Generated by `fetch_comments.py`. Comments: YouTube **top** sort via yt-dlp, then ordered by **likes** in this file._",
        "",
    ]
    if source_file:
        header.append(f"- **URL list:** `{source_file}`")
    header.append(f"- **Videos:** {len(blocks)}")
    header.append("")

    body_chunks: list[str] = []
    for i, (meta, ranked) in enumerate(blocks, start=1):
        vid = str(meta.get("id") or i)
        inner_meta = {**meta, "fetched_comment_rows": len(ranked)}
        body_chunks.append(
            f'<a id="{vid}"></a>\n\n{video_section_markdown(ranked, inner_meta, section_index=i)}'
        )

    return (
        "\n".join(header)
        + "\n"
        + "\n".join(toc)
        + "\n---\n\n"
        + "\n\n---\n\n".join(body_chunks)
        + "\n"
    )


def fetch_one(
    url: str,
    *,
    fetch_budget: int,
    min_comments: int,
    insecure: bool,
    deno_path: str | None,
    remote_ejs: bool,
    out_root: Path,
) -> dict[str, Any]:
    opts: dict[str, Any] = {
        "skip_download": True,
        "quiet": True,
        "nocheckcertificate": insecure,
        "getcomments": True,
        "extractor_args": {
            "youtube": {
                "comment_sort": ["top"],
                "max_comments": [str(fetch_budget)],
            }
        },
    }
    opts.update(ydl_base_opts(insecure=insecure, deno_path=deno_path, remote_ejs=remote_ejs))
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

    vid = info.get("id") or _video_id_from_url(url)
    if not vid:
        raise RuntimeError(f"Could not resolve video id for {url!r}")

    comments: list[dict[str, Any]] = list(info.get("comments") or [])
    ranked = sort_by_likes(comments)

    meta = {
        "id": vid,
        "title": info.get("title"),
        "webpage_url": info.get("webpage_url") or url,
        "channel": info.get("channel") or info.get("uploader"),
        "comment_count_reported": info.get("comment_count"),
        "fetched_comment_rows": len(comments),
        "target_min_comments": min_comments,
        "fetch_budget": fetch_budget,
        "meets_min": len(comments) >= min_comments,
        "note": None
        if len(comments) >= min_comments
        else f"Only {len(comments)} comments returned; video may have fewer, or comments disabled/partial.",
    }

    d = out_root / vid
    d.mkdir(parents=True, exist_ok=True)
    (d / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (d / "comments.json").write_text(
        json.dumps(comments, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    write_csv(d / "comments_top_by_likes.csv", ranked)
    write_markdown(d / "comments_top_by_likes.md", ranked, {**meta, "fetched_comment_rows": len(comments)})

    return meta, ranked


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch top YouTube comments (then sort by likes).")
    ap.add_argument("urls", nargs="*", help="Video or playlist URLs")
    ap.add_argument(
        "--urls-file",
        type=Path,
        help="File with one URL per line (# comments allowed)",
    )
    ap.add_argument(
        "--min-comments",
        type=int,
        default=120,
        help="Warn in meta if fewer than this many comment rows were fetched (default: 120)",
    )
    ap.add_argument(
        "--fetch-budget",
        type=int,
        default=None,
        help="yt-dlp max_comments ceiling (default: max(250, min-comments + 80))",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path("out"),
        help="Output directory (default: ./out)",
    )
    ap.add_argument(
        "--insecure",
        action="store_true",
        help="Skip TLS certificate verification (use if you hit CERTIFICATE_VERIFY_FAILED)",
    )
    ap.add_argument(
        "--deno-path",
        default=None,
        help="Path to deno binary (default: $DENO_PATH, PATH, or ~/.deno/bin/deno)",
    )
    ap.add_argument(
        "--no-remote-ejs",
        action="store_true",
        help="Do not allow yt-dlp to fetch EJS challenge helpers from GitHub (not recommended)",
    )
    ap.add_argument(
        "--single-md",
        type=Path,
        default=None,
        help="Write one markdown file containing all videos (TOC + full comments)",
    )
    args = ap.parse_args()

    seeds: list[str] = []
    seeds.extend(args.urls)
    if args.urls_file:
        seeds.extend(read_urls_file(args.urls_file))

    if not seeds:
        print("No URLs: pass URLs as args and/or --urls-file", file=sys.stderr)
        return 2

    fetch_budget = args.fetch_budget or max(250, args.min_comments + 80)

    deno_path = resolve_deno_path(args.deno_path)
    remote_ejs = not args.no_remote_ejs
    if deno_path:
        print(f"[deno] Using JS runtime: {deno_path}", file=sys.stderr)
    else:
        print(
            "[deno] No deno binary found — install: curl -fsSL https://deno.land/install.sh | sh",
            file=sys.stderr,
        )
    if remote_ejs and deno_path:
        print("[deno] remote_components: ejs:github, ejs:npm (EJS challenge solver)", file=sys.stderr)

    out_root: Path = args.out
    out_root.mkdir(parents=True, exist_ok=True)

    seen: set[str] = set()
    video_urls: list[str] = []
    for seed in seeds:
        for vu in expand_to_video_urls(
            seed,
            insecure=args.insecure,
            deno_path=deno_path,
            remote_ejs=remote_ejs,
        ):
            vid = _video_id_from_url(vu)
            if vid and vid not in seen:
                seen.add(vid)
                video_urls.append(vu)

    if not video_urls:
        print("No video URLs after expanding inputs.", file=sys.stderr)
        return 2

    summary: list[dict[str, Any]] = []
    blocks: list[tuple[dict[str, Any], list[dict[str, Any]]]] = []
    for vu in video_urls:
        try:
            meta, ranked = fetch_one(
                vu,
                fetch_budget=fetch_budget,
                min_comments=args.min_comments,
                insecure=args.insecure,
                deno_path=deno_path,
                remote_ejs=remote_ejs,
                out_root=out_root,
            )
            summary.append(meta)
            blocks.append((meta, ranked))
            flag = "OK" if meta["meets_min"] else "SHORT"
            print(f"[{flag}] {meta['id']}: {meta['fetched_comment_rows']} comments -> {out_root / meta['id']}")
        except Exception as e:  # noqa: BLE001 — surface per-URL failures
            print(f"[ERR] {vu!r}: {e}", file=sys.stderr)
            summary.append({"webpage_url": vu, "error": str(e)})

    (out_root / "_run_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if args.single_md and blocks:
        src = str(args.urls_file) if args.urls_file else "CLI args"
        doc = build_combined_markdown(
            blocks,
            title="YouTube comments — India / insurance corpus",
            source_file=src,
        )
        args.single_md.parent.mkdir(parents=True, exist_ok=True)
        args.single_md.write_text(doc, encoding="utf-8")
        print(f"[MD] Wrote combined file -> {args.single_md.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
