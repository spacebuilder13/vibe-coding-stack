#!/usr/bin/env python3
"""
Sitemap-driven crawl → Obsidian-flavored markdown (YAML + body).
Honors robots.txt Disallow for User-agent: *; optional extra post sitemap.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import requests
import trafilatura

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

SKIP_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".svg",
    ".ico",
    ".pdf",
    ".xml",
    ".xsl",
)


def session_for(insecure: bool) -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": "VibeStackCompetitiveResearch/1.0 (+local research)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    if insecure:
        import urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        s.verify = False
    return s


def fetch_text(sess: requests.Session, url: str, timeout: int = 25) -> str:
    r = sess.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text


def parse_robots_disallows(robots_txt: str) -> list[str]:
    """Collect Disallow paths under the first User-agent: * block."""
    out: list[str] = []
    active = False
    for raw in robots_txt.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        low = line.lower()
        if low.startswith("user-agent:"):
            ua = line.split(":", 1)[1].strip()
            if ua == "*":
                active = True
            elif active:
                break
        elif active and low.startswith("disallow:"):
            p = line.split(":", 1)[1].strip()
            if p and p != "/":
                if not p.startswith("/"):
                    p = "/" + p
                out.append(p)
    return out


def parse_sitemap_index(xml_text: str) -> list[str]:
    root = ET.fromstring(xml_text)
    return [loc.text for loc in root.findall(".//sm:loc", NS) if loc.text]


def parse_urlset(xml_text: str) -> list[str]:
    root = ET.fromstring(xml_text)
    return [loc.text for loc in root.findall(".//sm:loc", NS) if loc.text]


def collect_all_sitemap_urls(sess: requests.Session, base: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    sm_url = f"{base}/sitemap.xml"
    try:
        idx = fetch_text(sess, sm_url)
    except Exception:
        return out
    for child in parse_sitemap_index(idx):
        try:
            body = fetch_text(sess, child)
        except Exception:
            continue
        for u in parse_urlset(body):
            if u and u not in seen:
                seen.add(u)
                out.append(u)
    return out


def collect_post_urls(sess: requests.Session, base: str, posts_sitemap: str | None) -> list[str]:
    candidates: list[str] = []
    if posts_sitemap:
        candidates.append(posts_sitemap)
    else:
        candidates.extend(
            [
                f"{base}/articles/sitemap-posts.xml",
                f"{base}/post-sitemap.xml",
                f"{base}/sitemap-posts.xml",
            ]
        )
    for u in candidates:
        try:
            return parse_urlset(fetch_text(sess, u))
        except Exception:
            continue
    return []


def is_disallowed(url: str, prefixes: tuple[str, ...]) -> bool:
    p = urlparse(url).path or "/"
    return any(p.startswith(d) for d in prefixes)


def is_skippable_asset(url: str) -> bool:
    low = url.lower().split("?")[0]
    return any(low.endswith(ext) for ext in SKIP_EXTENSIONS)


def url_to_vault_path(url: str, base: str, vault: Path) -> Path:
    p = urlparse(url).path.strip("/")
    if not p:
        return vault / "02-pages" / "index.md"
    parts = [x for x in p.split("/") if x]
    if "/articles/" in url:
        rel = "/".join(parts[parts.index("articles") + 1 :])
        safe = rel.replace("/", "__") or "index"
        if len(safe) > 180:
            safe = hashlib.sha256(rel.encode()).hexdigest()[:20] + "__" + (parts[-1][:60] if parts else "post")
        return vault / "03-articles" / f"{safe}.md"
    safe_path = "/".join(parts)
    if len(safe_path) > 200:
        safe_path = hashlib.sha256(safe_path.encode()).hexdigest()[:24] + "__" + (parts[-1][:80] if parts else "page")
    return vault / "02-pages" / f"{safe_path}.md"


def fetch_page_md(url: str) -> tuple[str, dict, str | None]:
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return "", {}, "empty_download"
        meta = trafilatura.extract_metadata(downloaded)
        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True,
            favor_precision=True,
        )
        title = (meta.title if meta and meta.title else None) or ""
        if not text:
            return "", {"title": title, "url": url}, "no_main_text"
        d = {
            "title": title or url,
            "url": url,
            "sitename": meta.sitename if meta else "",
            "date": meta.date if meta else "",
        }
        return text.strip(), d, None
    except Exception as e:  # noqa: BLE001
        return "", {"title": "", "url": url}, str(e)


def build_frontmatter(meta: dict, error: str | None, word_count: int, tag_site: str) -> str:
    lines = ["---"]
    for k in ("title", "url", "date", "sitename"):
        v = meta.get(k) or ""
        if v:
            lines.append(f'{k}: "{str(v).replace(chr(34), chr(39))}"')
    lines.append(f"fetched_at: \"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\"")
    lines.append(f"word_count: {word_count}")
    if error:
        lines.append(f'crawl_error: "{error[:200].replace(chr(34), chr(39))}"')
    lines.append(f"tags: [competitive-research, site-{tag_site}]")
    lines.append("---\n")
    return "\n".join(lines)


def worker(args: tuple[str, Path, str]) -> tuple[str, bool, str]:
    url, dest, tag_site = args
    body, meta, err = fetch_page_md(url)
    wc = len(body.split()) if body else 0
    fm = build_frontmatter(meta, err, wc, tag_site)
    content = fm + (f"# {meta.get('title') or 'Untitled'}\n\n" if meta.get("title") else "# Page\n\n")
    content += f"Source: <{url}>\n\n---\n\n"
    content += body or f"_Extraction issue: {err}_\n"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    return url, err is None, err or "ok"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True, help="Origin, e.g. https://example.com")
    ap.add_argument("--vault", type=Path, required=True)
    ap.add_argument("--posts-sitemap", default=None, help="Full URL to posts urlset (optional)")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--articles-only", action="store_true")
    ap.add_argument("--marketing-limit", type=int, default=400)
    ap.add_argument("--articles-limit", type=int, default=0)
    ap.add_argument("--insecure", action="store_true")
    ap.add_argument(
        "--disallow-prefix",
        action="append",
        default=[],
        help="Extra path prefix to treat as disallowed (repeatable)",
    )
    args = ap.parse_args()

    base = args.base_url.rstrip("/")
    netloc = urlparse(base).netloc.replace(".", "-")
    vault: Path = args.vault
    sess = session_for(args.insecure)

    disallow: list[str] = []
    try:
        robots = fetch_text(sess, f"{base}/robots.txt")
        disallow.extend(parse_robots_disallows(robots))
    except Exception:
        pass
    disallow.extend(args.disallow_prefix or [])
    disallow_t = tuple(sorted(set(disallow)))

    vault.mkdir(parents=True, exist_ok=True)
    (vault / "00-meta").mkdir(parents=True, exist_ok=True)
    (vault / "01-hubs").mkdir(parents=True, exist_ok=True)
    (vault / "02-pages").mkdir(parents=True, exist_ok=True)
    (vault / "03-articles").mkdir(parents=True, exist_ok=True)
    (vault / "assets" / "ux-audit").mkdir(parents=True, exist_ok=True)

    print("Collecting URLs…", file=sys.stderr)
    article_urls = [
        u
        for u in collect_post_urls(sess, base, args.posts_sitemap)
        if u.startswith(base) and not is_disallowed(u, disallow_t)
    ]
    if args.articles_limit > 0:
        article_urls = article_urls[: args.articles_limit]

    marketing: list[str] = []
    if not args.articles_only:
        raw = [
            u
            for u in collect_all_sitemap_urls(sess, base)
            if u.startswith(base)
            and not is_disallowed(u, disallow_t)
            and not is_skippable_asset(u)
            and "/articles/" not in u
        ]
        marketing = raw[: args.marketing_limit]

    def norm_key(u: str) -> str:
        u = u.strip().split("#")[0]
        return u.rstrip("/").lower()

    seen: set[str] = set()
    ordered: list[str] = []
    for u in article_urls + marketing:
        k = norm_key(u)
        if k in seen:
            continue
        seen.add(k)
        ordered.append(u.strip())

    inv = vault / "00-meta" / "url-inventory.md"
    inv.write_text(
        "\n".join(
            [
                f"# Crawl URL inventory — {netloc}",
                "",
                f"- **Post / article URLs:** {len(article_urls)}",
                f"- **Other sitemap URLs (capped):** {len(marketing)}",
                f"- **Total queued (deduped):** {len(ordered)}",
                f"- **Disallow prefixes used:** `{disallow_t}`",
                "",
                "## Sample",
                "",
                *[f"- `{u}`" for u in ordered[:40]],
                "",
            ]
        ),
        encoding="utf-8",
    )

    tasks: list[tuple[str, Path, str]] = []
    for url in ordered:
        dest = url_to_vault_path(url, base, vault)
        tasks.append((url, dest, netloc))

    ok = fail = 0
    log_lines: list[str] = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(worker, t): t[0] for t in tasks}
        for i, fut in enumerate(as_completed(futs), 1):
            url = futs[fut]
            try:
                u, success, msg = fut.result()
                if success:
                    ok += 1
                else:
                    fail += 1
                log_lines.append(f"- {'OK' if success else 'FAIL'} | {msg} | `{u}`")
            except Exception as e:  # noqa: BLE001
                fail += 1
                log_lines.append(f"- EXC | {e} | `{url}`")
            if i % 50 == 0:
                print(f"… {i}/{len(tasks)} ({ok} ok, {fail} fail)", file=sys.stderr)

    (vault / "00-meta" / "CRAWL_LOG.md").write_text(
        "\n".join(
            [
                "# Crawl run log",
                "",
                f"- base: `{base}`",
                f"- finished: `{time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}`",
                f"- ok: **{ok}**  fail: **{fail}**",
                "",
                "## Details",
                "",
                *log_lines[:500],
                *(["", f"_… truncated; {len(log_lines) - 500} more lines omitted_"] if len(log_lines) > 500 else []),
            ]
        ),
        encoding="utf-8",
    )
    print(f"Done. ok={ok} fail={fail} vault={vault}", file=sys.stderr)


if __name__ == "__main__":
    main()
