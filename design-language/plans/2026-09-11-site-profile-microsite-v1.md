# Site Profile Microsite V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a V1 site-profile microsite at `docs/` (GitHub Pages root) covering Home, Climate, Sun & Solar, Wind, and Flood & Hazard — ported from `pdc-pro-2026`'s existing report HTML plus two new pages.

**Architecture:** Plain static HTML/CSS, no generator. Two small standalone Python scripts (no third-party dependencies) do the only "build" work: `port_report.py` wraps a `pdc-pro-2026` `.viz-root` fragment into a full HTML document with empty nav/footer marker regions, and `build_nav.py` stamps the current `docs/_partials/nav.html` / `footer.html` content into every page's marker regions. Both are run locally before committing — GitHub Pages serves the committed output as-is, zero server-side processing (`docs/.nojekyll` disables GitHub's default Jekyll pass).

**Tech Stack:** HTML, CSS (the existing `.viz-root` scoped pattern — light/dark aware via `prefers-color-scheme` + `data-theme`, inline SVG, no external deps), Python 3 (stdlib only) for the two build scripts, pytest for their tests.

**Spec:** `site-plan/specs/2026-09-11-site-profile-microsite-v1-design.md`

## Global Constraints

- No JS framework, no CSS framework, no build tool beyond the two local Python scripts — matches the spec's "plain static HTML, no generator" decision.
- Every `docs/*.html` content page (not partials) must contain exactly one `<!-- NAV:START -->…<!-- NAV:END -->` region and one `<!-- FOOTER:START -->…<!-- FOOTER:END -->` region.
- `build_nav.py` must be re-run (and its output committed) after any edit to `docs/_partials/nav.html` or `docs/_partials/footer.html`, or after adding a new `docs/*.html` page.
- Exact address ("58 Freestone Avenue, Portland, CT 06480") and coordinates (41°34'22"N 72°38'04"W / 41.572814, -72.634377) are permitted per the 2026-09-11 CLAUDE.md privacy policy change — do not genericize them.
- Neighbor / third-party names are never permitted, per the same policy (unchanged). Spot-check every ported page for this before committing.
- GitHub Pages is **not** enabled until Task 10, as an explicit, confirmed action — no earlier task should assume the site is live.

---

### Task 1: Nav/footer partials and the `build_nav.py` stamping script

**Files:**
- Create: `permaculture-site-plan/docs/.nojekyll` (empty file)
- Create: `permaculture-site-plan/docs/_partials/nav.html`
- Create: `permaculture-site-plan/docs/_partials/footer.html`
- Create: `permaculture-site-plan/scripts/build_nav.py`
- Test: `permaculture-site-plan/scripts/tests/test_build_nav.py`

**Interfaces:**
- Produces: `stamp(html: str, name: str, partial_content: str) -> str` in `scripts/build_nav.py` — replaces the content between `<!-- {name}:START -->` and `<!-- {name}:END -->` in `html` with `partial_content`, leaving `html` unchanged if the markers aren't present. Later tasks' pages must use marker names `NAV` and `FOOTER` for this function to find them.
- Produces: `build() -> list[Path]` in `scripts/build_nav.py` — stamps `docs/_partials/nav.html` and `docs/_partials/footer.html` into every `docs/*.html` file (excluding `docs/_partials/*`), returns the list of files it changed. Running the script (`python3 scripts/build_nav.py`) calls this and prints the result.

- [ ] **Step 1: Write the failing tests for `stamp()`**

Create `permaculture-site-plan/scripts/tests/test_build_nav.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from build_nav import stamp


def test_stamp_replaces_marker_region():
    html = (
        "<body>\n"
        "<!-- NAV:START -->\n<!-- NAV:END -->\n"
        "<p>content</p>\n"
        "</body>"
    )
    result = stamp(html, "NAV", "<nav>Home</nav>")
    assert "<nav>Home</nav>" in result
    assert "<p>content</p>" in result


def test_stamp_is_idempotent():
    html = "<!-- NAV:START -->\nold\n<!-- NAV:END -->"
    once = stamp(html, "NAV", "<nav>new</nav>")
    twice = stamp(once, "NAV", "<nav>new</nav>")
    assert once == twice
    assert "old" not in once


def test_stamp_leaves_other_markers_alone():
    html = (
        "<!-- NAV:START -->\nnav\n<!-- NAV:END -->\n"
        "<!-- FOOTER:START -->\nfoot\n<!-- FOOTER:END -->"
    )
    result = stamp(html, "NAV", "<nav>new</nav>")
    assert "foot" in result
    assert "<!-- FOOTER:START -->" in result


def test_stamp_returns_unchanged_when_marker_absent():
    html = "<p>no markers here</p>"
    result = stamp(html, "NAV", "<nav>x</nav>")
    assert result == html
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd permaculture-site-plan && python3 -m pytest scripts/tests/test_build_nav.py -v`
Expected: `ModuleNotFoundError: No module named 'build_nav'` (or all 4 tests erroring the same way) — `scripts/build_nav.py` doesn't exist yet.

- [ ] **Step 3: Write `scripts/build_nav.py`**

```python
#!/usr/bin/env python3
"""Stamp shared nav/footer partials into every docs/*.html page.

Usage: python3 scripts/build_nav.py
Run from the repo root (or anywhere — paths are resolved relative to this
file). Rewrites the content between marker comments in every docs/*.html
file (excluding docs/_partials/*) using the current content of
docs/_partials/nav.html and docs/_partials/footer.html.

Re-run this after editing either partial, or after adding a new
docs/*.html page, before committing.
"""
import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
PARTIALS = DOCS / "_partials"

MARKERS = {
    "NAV": PARTIALS / "nav.html",
    "FOOTER": PARTIALS / "footer.html",
}


def stamp(html: str, name: str, partial_content: str) -> str:
    pattern = re.compile(
        rf"(<!-- {name}:START -->)(.*?)(<!-- {name}:END -->)", re.DOTALL
    )
    if not pattern.search(html):
        return html
    return pattern.sub(
        lambda m: f"{m.group(1)}\n{partial_content.strip()}\n{m.group(3)}", html
    )


def build() -> list[Path]:
    for partial_path in MARKERS.values():
        if not partial_path.exists():
            raise FileNotFoundError(f"missing partial: {partial_path}")
    partial_contents = {name: path.read_text() for name, path in MARKERS.items()}

    changed = []
    for page in sorted(DOCS.glob("*.html")):
        original = page.read_text()
        updated = original
        for name, content in partial_contents.items():
            updated = stamp(updated, name, content)
        if updated != original:
            page.write_text(updated)
            changed.append(page)
    return changed


if __name__ == "__main__":
    changed_files = build()
    for p in changed_files:
        print(f"stamped {p.relative_to(DOCS.parent)}")
    print(f"{len(changed_files)} file(s) updated")
```

Using a lambda (rather than a `\1`/`\3`-style string template) for the replacement
avoids `re.sub` misinterpreting any literal backslash sequence that happens to appear
inside `partial_content`.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd permaculture-site-plan && python3 -m pytest scripts/tests/test_build_nav.py -v`
Expected: 4 passed.

- [ ] **Step 5: Create the nav partial**

Create `permaculture-site-plan/docs/_partials/nav.html`:

```html
<style>
  .site-nav {
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
    gap: 12px; padding: 14px 20px;
    background: #fcfcfb; border-bottom: 1px solid rgba(11,11,11,0.10);
  }
  .site-nav__brand { font-weight: 600; font-size: 14px; color: #0b0b0b; text-decoration: none; }
  .site-nav__links { display: flex; gap: 18px; flex-wrap: wrap; }
  .site-nav__links a { font-size: 13px; color: #52514e; text-decoration: none; }
  .site-nav__links a:hover { color: #0b0b0b; }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) .site-nav { background: #1a1a19; border-bottom-color: rgba(255,255,255,0.10); }
    :root:not([data-theme="light"]) .site-nav__brand { color: #ffffff; }
    :root:not([data-theme="light"]) .site-nav__links a { color: #c3c2b7; }
    :root:not([data-theme="light"]) .site-nav__links a:hover { color: #ffffff; }
  }
  :root[data-theme="dark"] .site-nav { background: #1a1a19; border-bottom-color: rgba(255,255,255,0.10); }
  :root[data-theme="dark"] .site-nav__brand { color: #ffffff; }
  :root[data-theme="dark"] .site-nav__links a { color: #c3c2b7; }
  :root[data-theme="dark"] .site-nav__links a:hover { color: #ffffff; }
</style>
<nav class="site-nav">
  <a class="site-nav__brand" href="/">Lot #86 — Site Profile</a>
  <div class="site-nav__links">
    <a href="/climate.html">Climate</a>
    <a href="/sun-solar.html">Sun &amp; Solar</a>
    <a href="/wind.html">Wind</a>
    <a href="/flood-hazard.html">Flood &amp; Hazard</a>
  </div>
</nav>
```

- [ ] **Step 6: Create the footer partial**

Create `permaculture-site-plan/docs/_partials/footer.html`:

```html
<style>
  .site-footer {
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: 20px; text-align: center;
    font-size: 12px; color: #898781;
  }
  .site-footer a { color: #52514e; }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) .site-footer a { color: #c3c2b7; }
  }
  :root[data-theme="dark"] .site-footer a { color: #c3c2b7; }
</style>
<footer class="site-footer">
  <p>Lot #86, 58 Freestone Avenue, Portland, CT 06480 — part of the
    <a href="https://github.com/keser/permaculture-site-plan">permaculture-site-plan</a>
    project. Data ported from <a href="https://github.com/keser/pdc-pro-2026">pdc-pro-2026</a>
    coursework.</p>
</footer>
```

- [ ] **Step 7: Create the empty `.nojekyll` file**

```bash
mkdir -p permaculture-site-plan/docs
touch permaculture-site-plan/docs/.nojekyll
```

- [ ] **Step 8: Run `build_nav.py` and confirm it reports zero files stamped (no content pages exist yet)**

Run: `cd permaculture-site-plan && python3 scripts/build_nav.py`
Expected: `0 file(s) updated` (only the partials exist so far; `docs/*.html` glob matches nothing else).

- [ ] **Step 9: Commit**

```bash
cd permaculture-site-plan
git add docs/.nojekyll docs/_partials scripts/build_nav.py scripts/tests/test_build_nav.py
git commit -m "Add nav/footer partials and the build_nav.py stamping script"
```

---

### Task 2: `port_report.py` script, applied to Climate (first end-to-end port)

**Files:**
- Create: `permaculture-site-plan/scripts/port_report.py`
- Test: `permaculture-site-plan/scripts/tests/test_port_report.py`
- Create: `permaculture-site-plan/docs/climate.html`

**Interfaces:**
- Consumes: `scripts/build_nav.py`'s `build()` (Task 1) — run as a CLI step after this task's port, not imported.
- Produces: `port(source_text: str) -> str` in `scripts/port_report.py` — splits `source_text` on its first `<div class="viz-root">`, puts everything before it (the `<meta>`/`<title>`/`<style>` block) in a `<head>`, and everything from it onward in a `<body>` alongside empty `NAV`/`FOOTER` marker regions. Raises `ValueError` if no `<div class="viz-root">` is found. Later tasks (3–7) use this same function via the CLI, not by importing it.

- [ ] **Step 1: Write the failing tests for `port()`**

Create `permaculture-site-plan/scripts/tests/test_port_report.py`:

```python
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from port_report import port

FRAGMENT = (
    '<meta charset="utf-8">\n'
    '<title>Example Report</title>\n'
    '<style>.viz-root { color: red; }</style>\n'
    '<div class="viz-root">\n'
    '  <p>hello</p>\n'
    '</div>\n'
)


def test_port_splits_head_and_body():
    result = port(FRAGMENT)
    assert "<title>Example Report</title>" in result
    assert result.index("<head>") < result.index("<title>Example Report</title>") < result.index("</head>")
    assert result.index("</head>") < result.index('<div class="viz-root">')


def test_port_inserts_empty_markers():
    result = port(FRAGMENT)
    assert "<!-- NAV:START -->\n<!-- NAV:END -->" in result
    assert "<!-- FOOTER:START -->\n<!-- FOOTER:END -->" in result


def test_port_preserves_body_content():
    result = port(FRAGMENT)
    assert "<p>hello</p>" in result


def test_port_raises_on_missing_viz_root():
    with pytest.raises(ValueError):
        port("<p>no viz-root div here</p>")
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd permaculture-site-plan && python3 -m pytest scripts/tests/test_port_report.py -v`
Expected: `ModuleNotFoundError: No module named 'port_report'`.

- [ ] **Step 3: Write `scripts/port_report.py`**

```python
#!/usr/bin/env python3
"""Wrap a pdc-pro-2026 .viz-root report fragment into a full HTML document
with empty NAV/FOOTER marker regions, ready for scripts/build_nav.py.

Usage: python3 scripts/port_report.py <source-fragment.html> <dest-in-docs.html>

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
        print("usage: port_report.py <source-fragment.html> <dest-in-docs.html>", file=sys.stderr)
        raise SystemExit(2)
    source_path, dest_path = Path(sys.argv[1]), Path(sys.argv[2])
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(port(source_path.read_text()))
    print(f"wrote {dest_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd permaculture-site-plan && python3 -m pytest scripts/tests/test_port_report.py -v`
Expected: 4 passed.

- [ ] **Step 5: Port the Climate report**

```bash
cd permaculture-site-plan
python3 scripts/port_report.py \
  ../pdc-pro-2026/lesson-01-climate/assets/climate-survey-charts.html \
  docs/climate.html
python3 scripts/build_nav.py
```

Expected `build_nav.py` output includes `stamped docs/climate.html` and `1 file(s) updated`.

- [ ] **Step 6: Verify the ported page**

```bash
grep -c 'class="site-nav"' docs/climate.html   # expect: 1
grep -c 'class="site-footer"' docs/climate.html  # expect: 1
grep -c 'class="viz-root"' docs/climate.html   # expect: 1 (original content intact)
```

Open `docs/climate.html` directly in a browser (`open docs/climate.html` on macOS) and confirm: the nav bar renders at the top with working links, the original chart content renders unchanged below it, the footer renders at the bottom, and toggling the OS/browser color scheme swaps both the nav/footer and the chart colors together.

Read through the page text and confirm no third-party (non-"Andrew Keser") names appear. The exact address/coordinates are expected and fine per the current privacy policy — do not remove them.

- [ ] **Step 7: Commit**

```bash
git add scripts/port_report.py scripts/tests/test_port_report.py docs/climate.html
git commit -m "Add port_report.py; port the Climate report"
```

---

### Task 3: Port Wind

**Files:**
- Create: `permaculture-site-plan/docs/wind.html`

**Interfaces:**
- Consumes: `scripts/port_report.py` CLI and `scripts/build_nav.py` CLI (Tasks 1–2), used as-is — no code changes in this task.

- [ ] **Step 1: Port and stamp**

```bash
cd permaculture-site-plan
python3 scripts/port_report.py \
  ../pdc-pro-2026/lesson-03-site-analysis/assets/wind-roses.html \
  docs/wind.html
python3 scripts/build_nav.py
```

- [ ] **Step 2: Verify**

Same checks as Task 2 Step 6, against `docs/wind.html`: nav/footer/viz-root counts, browser open, light/dark toggle, no third-party names.

- [ ] **Step 3: Commit**

```bash
git add docs/wind.html
git commit -m "Port the Wind report"
```

---

### Task 4: Port Flood & Hazard

**Files:**
- Create: `permaculture-site-plan/docs/flood-hazard.html`

- [ ] **Step 1: Port and stamp**

```bash
cd permaculture-site-plan
python3 scripts/port_report.py \
  ../pdc-pro-2026/lesson-03-site-analysis/assets/flood-risk-report.html \
  docs/flood-hazard.html
python3 scripts/build_nav.py
```

- [ ] **Step 2: Verify**

Same checks as Task 2 Step 6, against `docs/flood-hazard.html`. This source already contains the exact address and decimal coordinates (confirmed while writing this plan) — no addition needed, just confirm they carried through the port unchanged.

- [ ] **Step 3: Commit**

```bash
git add docs/flood-hazard.html
git commit -m "Port the Flood & Hazard report"
```

---

### Task 5: Port Sun Path Charts

**Files:**
- Create: `permaculture-site-plan/docs/sun-path-charts.html`

- [ ] **Step 1: Port and stamp**

```bash
cd permaculture-site-plan
python3 scripts/port_report.py \
  ../pdc-pro-2026/lesson-03-site-analysis/assets/sun-path-charts.html \
  docs/sun-path-charts.html
python3 scripts/build_nav.py
```

- [ ] **Step 2: Verify**

Same checks as Task 2 Step 6, against `docs/sun-path-charts.html`.

- [ ] **Step 3: Commit**

```bash
git add docs/sun-path-charts.html
git commit -m "Port the Sun Path Charts report"
```

---

### Task 6: Port Sun Path 3D

**Files:**
- Create: `permaculture-site-plan/docs/sun-path-3d.html`

- [ ] **Step 1: Port and stamp**

```bash
cd permaculture-site-plan
python3 scripts/port_report.py \
  ../pdc-pro-2026/lesson-03-site-analysis/assets/sun-path-3d.html \
  docs/sun-path-3d.html
python3 scripts/build_nav.py
```

- [ ] **Step 2: Verify**

Same checks as Task 2 Step 6, against `docs/sun-path-3d.html`. This report is larger (~40 KB) and may use inline `<script>` for 3D rendering — confirm any `<script>` tags survived the port intact (the split only looks for `<div class="viz-root">`, so scripts before or after it in the original pass through untouched either way; just eyeball the diff).

- [ ] **Step 3: Commit**

```bash
git add docs/sun-path-3d.html
git commit -m "Port the Sun Path 3D report"
```

---

### Task 7: Port Sun Path Overlay

**Files:**
- Create: `permaculture-site-plan/docs/sun-path-overlay.html`

- [ ] **Step 1: Port and stamp**

```bash
cd permaculture-site-plan
python3 scripts/port_report.py \
  ../pdc-pro-2026/lesson-03-site-analysis/assets/sun-path-overlay.html \
  docs/sun-path-overlay.html
python3 scripts/build_nav.py
```

- [ ] **Step 2: Verify**

Same checks as Task 2 Step 6, against `docs/sun-path-overlay.html` (the largest V1 source file, ~64 KB — this one overlays sun-path data on a base-map image; confirm any embedded/referenced image data survived the port, since a broken image reference would only show up visually, not via grep).

- [ ] **Step 3: Commit**

```bash
git add docs/sun-path-overlay.html
git commit -m "Port the Sun Path Overlay report"
```

---

### Task 8: Build the Sun & Solar hub page

**Files:**
- Create: `permaculture-site-plan/docs/sun-solar.html`

**Interfaces:**
- Consumes: `docs/sun-path-charts.html`, `docs/sun-path-3d.html`, `docs/sun-path-overlay.html` (Tasks 5–7) — links to all three, doesn't embed their content.

This page is new content, not a port — hand-write it directly with markers already in place (no need to run `port_report.py`; `build_nav.py` will still stamp it since it matches `docs/*.html`).

- [ ] **Step 1: Create the hub page**

Create `permaculture-site-plan/docs/sun-solar.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Sun &amp; Solar — Lot #86</title>
<style>
  .viz-root {
    color-scheme: light;
    --surface-1: #fcfcfb; --page: #f9f9f7; --text-primary: #0b0b0b;
    --text-secondary: #52514e; --text-muted: #898781; --border: rgba(11,11,11,0.10);
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) .viz-root {
      color-scheme: dark;
      --surface-1: #1a1a19; --page: #0d0d0d; --text-primary: #ffffff;
      --text-secondary: #c3c2b7; --text-muted: #898781; --border: rgba(255,255,255,0.10);
    }
  }
  :root[data-theme="dark"] .viz-root {
    color-scheme: dark;
    --surface-1: #1a1a19; --page: #0d0d0d; --text-primary: #ffffff;
    --text-secondary: #c3c2b7; --text-muted: #898781; --border: rgba(255,255,255,0.10);
  }
  * { box-sizing: border-box; }
  .viz-root {
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--page); color: var(--text-primary); min-height: 60vh;
    padding: 32px 20px 60px;
  }
  .wrap { max-width: 900px; margin: 0 auto; }
  h1 { font-size: 22px; font-weight: 600; margin: 0 0 6px; }
  .subhead { color: var(--text-secondary); font-size: 14px; line-height: 1.5; margin: 0 0 24px; }
  .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
  .nav-card {
    display: block; background: var(--surface-1); border: 1px solid var(--border);
    border-radius: 12px; padding: 18px 20px; text-decoration: none; color: inherit;
  }
  .nav-card h2 { font-size: 15px; font-weight: 600; margin: 0 0 6px; color: var(--text-primary); }
  .nav-card p { font-size: 13px; color: var(--text-secondary); margin: 0; line-height: 1.5; }
</style>
</head>
<body>
<!-- NAV:START -->
<!-- NAV:END -->
<div class="viz-root">
  <div class="wrap">
    <header>
      <h1>Sun &amp; Solar</h1>
      <p class="subhead">Three views of solar exposure across the property, built from a bioclimatic design study of local weather and sun-position data.</p>
    </header>
    <div class="card-grid">
      <a class="nav-card" href="/sun-path-charts.html">
        <h2>Sun Path Charts</h2>
        <p>Seasonal sun-angle charts — where the sun sits in the sky through the year at this latitude.</p>
      </a>
      <a class="nav-card" href="/sun-path-3d.html">
        <h2>Sun Path 3D</h2>
        <p>An interactive 3D model of the sun's path over the site across the seasons.</p>
      </a>
      <a class="nav-card" href="/sun-path-overlay.html">
        <h2>Sun Path Overlay</h2>
        <p>Sun-path data overlaid directly on the site's base map — shade and exposure by location on the lot.</p>
      </a>
    </div>
  </div>
</div>
<!-- FOOTER:START -->
<!-- FOOTER:END -->
</body>
</html>
```

- [ ] **Step 2: Stamp nav/footer**

```bash
cd permaculture-site-plan
python3 scripts/build_nav.py
```

Expected: `stamped docs/sun-solar.html` in the output.

- [ ] **Step 3: Verify**

```bash
grep -c 'class="site-nav"' docs/sun-solar.html   # expect: 1
grep -c 'class="site-footer"' docs/sun-solar.html  # expect: 1
grep -c 'href="/sun-path' docs/sun-solar.html      # expect: 3
```

Open in a browser: confirm the three cards render and each link opens its target page (from Tasks 5–7).

- [ ] **Step 4: Commit**

```bash
git add docs/sun-solar.html
git commit -m "Add the Sun & Solar hub page"
```

---

### Task 9: Build the Home page

**Files:**
- Create: `permaculture-site-plan/docs/index.html`

**Interfaces:**
- Consumes: `docs/climate.html`, `docs/sun-solar.html`, `docs/wind.html`, `docs/flood-hazard.html` (Tasks 2–8) — links to all four, plus three "coming soon" cards for V2/V3 content that doesn't exist yet.

This is new content — hand-written directly with markers in place, same as Task 8.

- [ ] **Step 1: Create the Home page**

Create `permaculture-site-plan/docs/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Lot #86 — Site Profile</title>
<style>
  .viz-root {
    color-scheme: light;
    --surface-1: #fcfcfb; --page: #f9f9f7; --text-primary: #0b0b0b;
    --text-secondary: #52514e; --text-muted: #898781; --border: rgba(11,11,11,0.10);
    --grid: #e1e0d9;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) .viz-root {
      color-scheme: dark;
      --surface-1: #1a1a19; --page: #0d0d0d; --text-primary: #ffffff;
      --text-secondary: #c3c2b7; --text-muted: #898781; --border: rgba(255,255,255,0.10);
      --grid: #2c2c2a;
    }
  }
  :root[data-theme="dark"] .viz-root {
    color-scheme: dark;
    --surface-1: #1a1a19; --page: #0d0d0d; --text-primary: #ffffff;
    --text-secondary: #c3c2b7; --text-muted: #898781; --border: rgba(255,255,255,0.10);
    --grid: #2c2c2a;
  }
  * { box-sizing: border-box; }
  .viz-root {
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--page); color: var(--text-primary); min-height: 80vh;
    padding: 32px 20px 60px;
  }
  .wrap { max-width: 960px; margin: 0 auto; }
  h1 { font-size: 26px; font-weight: 600; margin: 0 0 6px; }
  .subhead { color: var(--text-secondary); font-size: 15px; line-height: 1.6; margin: 0 0 8px; max-width: 640px; }
  .subhead-muted { color: var(--text-muted); font-size: 12px; margin: 0 0 24px; }

  .fact-row {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 14px; margin: 24px 0 32px;
  }
  .fact {
    background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px;
    padding: 14px 16px;
  }
  .fact-label { font-size: 11px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 6px; }
  .fact-value { font-size: 16px; font-weight: 600; color: var(--text-primary); margin: 0; line-height: 1.3; }

  h2.section-head { font-size: 13px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted); margin: 0 0 12px; }
  .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 32px; }
  .nav-card {
    display: block; background: var(--surface-1); border: 1px solid var(--border);
    border-radius: 12px; padding: 18px 20px; text-decoration: none; color: inherit;
  }
  .nav-card h3 { font-size: 15px; font-weight: 600; margin: 0 0 6px; color: var(--text-primary); }
  .nav-card p { font-size: 13px; color: var(--text-secondary); margin: 0; line-height: 1.5; }
  .nav-card.soon { opacity: 0.5; cursor: default; }
  .nav-card.soon .tag {
    display: inline-block; font-size: 10px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.04em; color: var(--text-muted); border: 1px solid var(--border);
    border-radius: 999px; padding: 2px 8px; margin-top: 8px;
  }
  .divider { height: 1px; background: var(--grid); margin: 8px 0 32px; border: none; }
</style>
</head>
<body>
<!-- NAV:START -->
<!-- NAV:END -->
<div class="viz-root">
  <div class="wrap">
    <header>
      <h1>Lot #86 — Site Profile</h1>
      <p class="subhead">A working reference for designing this 0.43-acre property's permaculture future — climate, solar, wind, and hazard data today, watershed, species, and zone design to follow.</p>
      <p class="subhead-muted">58 Freestone Avenue, Portland, CT 06480 &middot; 41&deg;34&prime;22&Prime;N 72&deg;38&prime;04&Prime;W</p>
    </header>

    <div class="fact-row">
      <div class="fact"><p class="fact-label">Area</p><p class="fact-value">0.43 ac (&asymp;18,730 ft&sup2;)</p></div>
      <div class="fact"><p class="fact-label">Elevation</p><p class="fact-value">106&ndash;114 ft</p></div>
      <div class="fact"><p class="fact-label">Climate</p><p class="fact-value">Dfa &mdash; hot-summer continental</p></div>
      <div class="fact"><p class="fact-label">Hardiness zone</p><p class="fact-value">6b</p></div>
      <div class="fact"><p class="fact-label">Frost-free season</p><p class="fact-value">Apr 14 &ndash; Oct 23</p></div>
      <div class="fact"><p class="fact-label">Flood risk</p><p class="fact-value">FEMA Zone X &mdash; minimal</p></div>
    </div>

    <hr class="divider">

    <h2 class="section-head">Available now</h2>
    <div class="card-grid">
      <a class="nav-card" href="/climate.html">
        <h3>Climate</h3>
        <p>Temperature, precipitation, wind, and frost-free/hardiness data for the site.</p>
      </a>
      <a class="nav-card" href="/sun-solar.html">
        <h3>Sun &amp; Solar</h3>
        <p>Sun-path charts, a 3D seasonal model, and a base-map exposure overlay.</p>
      </a>
      <a class="nav-card" href="/wind.html">
        <h3>Wind</h3>
        <p>10 years of hourly station data as seasonal wind roses.</p>
      </a>
      <a class="nav-card" href="/flood-hazard.html">
        <h3>Flood &amp; Hazard</h3>
        <p>FEMA flood zone and First Street Foundation risk-factor data, checked directly by address.</p>
      </a>
    </div>

    <h2 class="section-head">Coming later</h2>
    <div class="card-grid">
      <div class="nav-card soon">
        <h3>Watersheds &amp; Water</h3>
        <p>Macro watershed, catchment area, rainwater harvesting, and site water flow.</p>
        <span class="tag">V2</span>
      </div>
      <div class="nav-card soon">
        <h3>Species Inventory</h3>
        <p>A georeferenced site map of observed species, from iNaturalist field data.</p>
        <span class="tag">V3</span>
      </div>
      <div class="nav-card soon">
        <h3>Zones &amp; Design</h3>
        <p>Current permaculture zones and the design brainstorm for their future.</p>
        <span class="tag">V3</span>
      </div>
    </div>
  </div>
</div>
<!-- FOOTER:START -->
<!-- FOOTER:END -->
</body>
</html>
```

- [ ] **Step 2: Stamp nav/footer**

```bash
cd permaculture-site-plan
python3 scripts/build_nav.py
```

Expected: `stamped docs/index.html` in the output.

- [ ] **Step 3: Verify**

```bash
grep -c 'class="site-nav"' docs/index.html    # expect: 1
grep -c 'class="site-footer"' docs/index.html   # expect: 1
grep -c 'nav-card' docs/index.html             # expect: > 0
grep -o '58 Freestone Avenue' docs/index.html   # expect: a match
```

Open in a browser: confirm all 6 fact tiles render with correct values, the 4 "Available now" cards link correctly (to pages built in Tasks 2–8), the 3 "Coming later" cards render visibly dimmed/non-clickable, and the light/dark toggle affects the whole page consistently including the nav.

Click through every link on the page once (nav bar's 4 links + the 4 available-now cards) and confirm each resolves to a real page with no 404s and no broken internal links.

- [ ] **Step 4: Commit**

```bash
git add docs/index.html
git commit -m "Add the Home page"
```

---

### Task 10: Final integration check and GitHub Pages enablement

**Files:** none created — verification and one external configuration action only.

**Interfaces:** none — this task consumes the complete output of Tasks 1–9 as a whole.

- [ ] **Step 1: Re-run the full test suite**

```bash
cd permaculture-site-plan
python3 -m pytest scripts/tests/ -v
```

Expected: all 8 tests pass (4 from `test_build_nav.py`, 4 from `test_port_report.py`).

- [ ] **Step 2: Re-run `build_nav.py` one final time and confirm it's a no-op**

```bash
python3 scripts/build_nav.py
```

Expected: `0 file(s) updated` — every page should already be stamped with the current partials from the previous tasks' commits. If it reports any files changed here, something in a partial or a page was edited after its last stamp without re-running the script — investigate before proceeding, and commit the fix.

- [ ] **Step 3: Full link-crawl by hand**

Open `docs/index.html` in a browser and click through every link on every page (Home → each of the 4 sections → Sun & Solar's 3 sub-pages → back via nav) — 8 pages, should be a few minutes. Confirm: no 404s, nav/footer present and consistent on all 8 pages, light/dark toggle works on all 8, no third-party names anywhere, exact address/coordinates present and correct throughout.

- [ ] **Step 4: Confirm before enabling GitHub Pages**

This is the step that makes the site live and publicly reachable at
`https://keser.github.io/permaculture-site-plan/`. **Stop and get an explicit go-ahead
before doing this** — it's the first genuinely external, hard-to-fully-reverse action in
this plan (the repo itself is already public, but a live published URL is a step further:
it'll get crawled/indexed).

- [ ] **Step 5: Enable GitHub Pages**

Once confirmed:

```bash
gh api repos/keser/permaculture-site-plan/pages -X POST -f "source[branch]=main" -f "source[path]=/docs"
```

Verify:

```bash
gh api repos/keser/permaculture-site-plan/pages
```

Expected: JSON response with `"status"` progressing to `"built"` within a few minutes, and a `"html_url"` field. Fetch that URL and confirm the Home page loads.

- [ ] **Step 6: Update CLAUDE.md**

Add a line under "Site Microsite (`docs/`)" recording the live URL and the date Pages was
enabled, so future sessions know the site is live without re-checking.

- [ ] **Step 7: Commit**

```bash
git add CLAUDE.md
git commit -m "Note GitHub Pages is live for the site-profile microsite"
git push origin main
```

---

## Self-Review Notes

- **Spec coverage:** every V1 page in the spec's content table has a task (Home → Task 9, Climate → Task 2, Sun & Solar hub → Task 8, the 3 sun-path reports → Tasks 5–7, Wind → Task 3, Flood & Hazard → Task 4). The nav/footer mechanism → Task 1. `.nojekyll` → Task 1 Step 7. GitHub Pages enablement, called out in the spec as a separate confirmed step → Task 10 Steps 4–5. Non-goals (Water, Species, Zones, Progress page) intentionally have no tasks here — they're future plans per the spec.
- **Placeholder scan:** no TBD/TODO; every step has concrete commands or complete code, not descriptions of code.
- **Type/interface consistency:** `stamp(html, name, partial_content)` and `build()` (Task 1) are used identically by their own tests and by every later task's CLI invocation of `build_nav.py` — no other task imports them directly, so there's no signature drift risk. `port(source_text)` (Task 2) is likewise only ever invoked via the `port_report.py` CLI in Tasks 3–7, with the same two positional file-path arguments each time.
