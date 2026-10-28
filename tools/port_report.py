#!/usr/bin/env python3
"""Wrap a .viz-root report fragment into a full HTML document
with empty NAV/FOOTER marker regions, ready for tools/build_nav.py.

Usage: python3 tools/port_report.py <source-fragment.html> <dest-page.html>

Source fragments look like:
    <meta charset="utf-8">
    <title>...</title>
    <style>...</style>
    <div class="viz-root">...</div>

This splits on the first `<div class="viz-root">` and puts everything
before it in <head> (charset/title/style), everything from it onward in
<body>.
"""
import sys
from pathlib import Path

SPLIT_MARKER = '<div class="viz-root">'

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="assets/page-tokens.css">
<style>body {{ margin: 0; }}</style>
{head}
</head>
<body>
<!-- NAV:START -->
<!-- NAV:END -->
{body}
<!-- FOOTER:START -->
<!-- FOOTER:END -->
</body>
</html>
"""


def port(source_text: str) -> str:
    idx = source_text.find(SPLIT_MARKER)
    if idx == -1:
        raise ValueError(f"no {SPLIT_MARKER!r} found in source")
    head = source_text[:idx].strip()
    body = source_text[idx:].strip()
    return TEMPLATE.format(head=head, body=body)


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: port_report.py <source-fragment.html> <dest-page.html>", file=sys.stderr)
        raise SystemExit(2)
    source_path, dest_path = Path(sys.argv[1]), Path(sys.argv[2])
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(port(source_path.read_text()))
    print(f"wrote {dest_path}")


if __name__ == "__main__":
    main()
