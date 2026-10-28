#!/usr/bin/env python3
"""Stamp shared nav/footer partials into every docs/*.html page.

Usage: python3 tools/build_nav.py [site_dir]
site_dir is the folder holding the *.html pages and a _partials/ folder with
nav.html and footer.html. Defaults to <repo>/docs. Rewrites the content between
marker comments in every *.html page (excluding _partials/*) using the current
content of _partials/nav.html and _partials/footer.html.

Re-run this after editing either partial, or after adding a new page, before
committing.
"""
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"


def stamp(html: str, name: str, partial_content: str) -> str:
    pattern = re.compile(
        rf"(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)", re.DOTALL
    )
    if not pattern.search(html):
        return html
    return pattern.sub(
        lambda m: f"{m.group(1)}\n{partial_content.strip()}\n{m.group(3)}", html
    )


def build(docs_dir: Path = DOCS) -> list[Path]:
    partials_dir = docs_dir / "_partials"
    markers = {
        "NAV": partials_dir / "nav.html",
        "FOOTER": partials_dir / "footer.html",
    }
    for partial_path in markers.values():
        if not partial_path.exists():
            raise FileNotFoundError(f"missing partial: {partial_path}")
    partial_contents = {name: path.read_text() for name, path in markers.items()}

    changed = []
    for page in sorted(docs_dir.glob("*.html")):
        original = page.read_text()
        for name in partial_contents:
            if f"<!-- {name}:START -->" not in original:
                print(f"warning: {page.name} has no {name} markers", file=sys.stderr)
        updated = original
        for name, content in partial_contents.items():
            updated = stamp(updated, name, content)
        if updated != original:
            page.write_text(updated)
            changed.append(page)
    return changed


if __name__ == "__main__":
    import sys

    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DOCS
    changed_files = build(target)
    for p in changed_files:
        print(f"stamped {p.relative_to(target.parent)}")
    print(f"{len(changed_files)} file(s) updated")
