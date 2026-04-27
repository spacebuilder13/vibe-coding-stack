#!/usr/bin/env python3
"""Generate Obsidian hub / MOC notes and IA outline from crawled markdown."""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


def read_frontmatter_url(p: Path) -> str | None:
    text = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^url:\s*\"([^\"]+)\"", text, re.MULTILINE)
    return m.group(1) if m else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", type=Path, required=True)
    args = ap.parse_args()
    vault: Path = args.vault
    art = vault / "03-articles"
    pages = vault / "02-pages"
    if not art.is_dir():
        print(f"No {art}; skipping article MOC", flush=True)
        return

    by_cat: dict[str, list[str]] = defaultdict(list)
    for md in sorted(art.glob("*.md")):
        if md.name.startswith("_"):
            continue
        url = read_frontmatter_url(md)
        if not url:
            continue
        m = re.search(r"/articles/([^/]+)/", url)
        cat = m.group(1) if m else "other"
        by_cat[cat].append(f"[[03-articles/{md.stem}]]")

    hubs = vault / "01-hubs"
    hubs.mkdir(parents=True, exist_ok=True)

    lines = [
        "# MOC — Articles by category",
        "",
        "Map of content for crawled article-style notes under `03-articles/`.",
        "",
    ]
    for cat in sorted(by_cat.keys()):
        lines.append(f"## {cat.replace('-', ' ').title()}")
        lines.append("")
        for wl in sorted(by_cat[cat], key=str.lower)[:400]:
            lines.append(f"- {wl}")
        if len(by_cat[cat]) > 400:
            lines.append(f"- _…{len(by_cat[cat]) - 400} more_")
        lines.append("")
    (hubs / "MOC - Articles by topic.md").write_text("\n".join(lines), encoding="utf-8")

    prefixes: dict[str, int] = defaultdict(int)
    if pages.is_dir():
        for md in pages.rglob("*.md"):
            rel = md.relative_to(pages).as_posix()
            top = rel.split("/")[0] if "/" in rel else rel
            prefixes[top] += 1

    ia = [
        "# Information architecture (inferred)",
        "",
        "From crawled `02-pages/` paths and article categories.",
        "",
        "## Top clusters (file count)",
        "",
    ]
    for k, v in sorted(prefixes.items(), key=lambda x: -x[1])[:50]:
        ia.append(f"- **{k}** — {v}")
    ia += ["", "## Article categories", ""]
    for cat in sorted(by_cat.keys()):
        ia.append(f"- `articles/{cat}/` — {len(by_cat[cat])} notes")
    (vault / "00-meta" / "IA-outline.md").write_text("\n".join(ia), encoding="utf-8")

    site_tag = vault.name.replace(" ", "-")
    root_hub = [
        "---",
        f'title: "Site research hub — {site_tag}"',
        "tags: [competitive-research, moc, hub]",
        "---",
        "",
        "# Site research hub",
        "",
        "## Meta",
        "- [[00-meta/IA-outline]]",
        "- [[00-meta/url-inventory]]",
        "- [[00-meta/CRAWL_LOG]]",
        "",
        "## Maps of content",
        "- [[01-hubs/MOC - Articles by topic]]",
        "",
        "## UX audit (if filled in)",
        "- [[UX-AUDIT-PACK]]",
        "",
        "## Folders",
        "- `03-articles/` — blog / long-form URLs",
        "- `02-pages/` — marketing and product URLs",
        "",
    ]
    (hubs / "MOC - Research site.md").write_text("\n".join(root_hub), encoding="utf-8")
    print(f"Wrote hubs under {hubs}", flush=True)


if __name__ == "__main__":
    main()
