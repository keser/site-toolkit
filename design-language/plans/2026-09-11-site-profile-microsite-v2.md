# Site Profile Microsite V2 Implementation Plan (Water Suite)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Water section (8 reports + hub) to the live microsite, reachable from the shared nav and the Home page.

**Architecture:** No new tooling — reuses `scripts/port_report.py` and `scripts/build_nav.py` from V1 unchanged. Content-only change: 8 ported reports, one ported-and-hand-fixed hub page, one nav edit, one Home page edit.

**Tech Stack:** Same as V1 — plain HTML/CSS, the two existing Python scripts (no changes to either).

**Spec:** `site-plan/specs/2026-09-11-site-profile-microsite-v2-design.md`

## Global Constraints

- No new scripts, no changes to `port_report.py` or `build_nav.py` — if a task thinks it needs to change either, stop and report BLOCKED rather than doing it; that would be an architecture change out of this plan's scope.
- Every internal link must be relative (e.g. `water.html`), never root-absolute (`/water.html`) — this is the exact Critical defect V1's final review caught. Verify with `grep -rn 'href="/' docs/` returning nothing, every task.
- Exact address/coordinates permitted; third-party names never permitted — same privacy bar as V1.
- `build_nav.py` must be re-run (and its output committed) after any partial edit or new page.

---

### Task 1: Port the 8 Water reports

**Files:**
- Create: `docs/precipitation-by-month.html`
- Create: `docs/runoff-by-surface.html`
- Create: `docs/water-balance.html`
- Create: `docs/elevation-sections.html`
- Create: `docs/site-flow-schematic.html`
- Create: `docs/design-storm-frequency.html`
- Create: `docs/macro-watershed-scale.html`
- Create: `docs/water-use-by-season.html`

**Interfaces:**
- Consumes: `scripts/port_report.py` CLI (`python3 scripts/port_report.py <source> <dest>`) and `scripts/build_nav.py` CLI (`python3 scripts/build_nav.py`, no args) — both unchanged from V1, invoke as-is.

- [ ] **Step 1: Port all 8 reports**

Source directory: `/Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/`

```bash
cd /path/to/permaculture-site-plan
python3 scripts/port_report.py /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/precipitation-by-month.html docs/precipitation-by-month.html
python3 scripts/port_report.py /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/runoff-by-surface.html docs/runoff-by-surface.html
python3 scripts/port_report.py /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/water-balance.html docs/water-balance.html
python3 scripts/port_report.py /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/elevation-sections.html docs/elevation-sections.html
python3 scripts/port_report.py /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/site-flow-schematic.html docs/site-flow-schematic.html
python3 scripts/port_report.py /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/design-storm-frequency.html docs/design-storm-frequency.html
python3 scripts/port_report.py /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/macro-watershed-scale.html docs/macro-watershed-scale.html
python3 scripts/port_report.py /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/water-use-by-season.html docs/water-use-by-season.html
python3 scripts/build_nav.py
```

Expected: `build_nav.py` reports all 8 new files stamped.

- [ ] **Step 2: Verify each of the 8 files**

For each file: exactly one NAV region + one FOOTER region, both stamped (matching `docs/_partials/nav.html`/`footer.html`); content fidelity against its source (diff the post-split body against the source's content from `<div class="viz-root">` onward); no third-party names; no root-absolute internal links (none expected — these are standalone reports with no internal nav of their own beyond the stamped partials).

You likely don't have a browser tool — substitute reading each finished file and confirming structurally: markers present and stamped, `.viz-root` content intact, well-formed HTML.

- [ ] **Step 3: Commit**

```bash
git add docs/precipitation-by-month.html docs/runoff-by-surface.html docs/water-balance.html docs/elevation-sections.html docs/site-flow-schematic.html docs/design-storm-frequency.html docs/macro-watershed-scale.html docs/water-use-by-season.html
git commit -m "Port the 8 Water suite reports"
```

---

### Task 2: Port the Water hub, fix the missing 8th card, copy thumbnails

**Files:**
- Create: `docs/water.html`
- Create: `docs/assets/thumb-precipitation-by-month.png`
- Create: `docs/assets/thumb-runoff-by-surface.png`
- Create: `docs/assets/thumb-water-balance.png`
- Create: `docs/assets/thumb-elevation-sections.png`
- Create: `docs/assets/thumb-site-flow-schematic.png`
- Create: `docs/assets/thumb-design-storm-frequency.png`
- Create: `docs/assets/thumb-macro-watershed-scale.png`

**Interfaces:**
- Consumes: the 8 files created in Task 1 (the hub's card `href`s must point to their exact filenames, all already relative/flat in `docs/`).

- [ ] **Step 1: Port the hub**

```bash
python3 scripts/port_report.py /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/index.html docs/water.html
```

- [ ] **Step 2: Copy the 7 existing thumbnails**

```bash
mkdir -p docs/assets
cp /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/thumb-precipitation-by-month.png docs/assets/
cp /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/thumb-runoff-by-surface.png docs/assets/
cp /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/thumb-water-balance.png docs/assets/
cp /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/thumb-elevation-sections.png docs/assets/
cp /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/thumb-site-flow-schematic.png docs/assets/
cp /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/thumb-design-storm-frequency.png docs/assets/
cp /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-05-water/assets/thumb-macro-watershed-scale.png docs/assets/
```

Verify: `ls docs/assets/thumb-*.png | wc -l` → 7. Confirm each copy is byte-identical to its source (`diff` or size comparison).

- [ ] **Step 3: Fix the thumbnail paths in `docs/water.html`**

In the ported file, every `img: "thumb-X.png"` entry in the `CARDS` JS array needs its value
changed to `"assets/thumb-X.png"` (7 occurrences, one per existing card). Find the `CARDS=[`
array (search for `img:"thumb-` or `img: "thumb-`) and update each `img` field's string value
to prepend `assets/`. Do not change anything else in the array yet — that's Step 4.

- [ ] **Step 4: Add the missing 8th card and its no-thumbnail fallback**

The `CARDS` array is missing an entry for `water-use-by-season.html`. Add one, following the
exact shape of the existing entries but with no `img` field (there is no thumbnail for this
report):

```js
{f:"water-use-by-season.html", t:"Household Water Use by Season",
 d:"Metered water bills broken into a seasonal bar chart — winter baseline vs. the summer outdoor-use bump.", slide:"Supporting Data"}
```

Place it wherever in the array reads best relative to the others (end of the array is fine
and simplest).

The card-rendering code currently assumes every card has an `img` and unconditionally
renders a `.thumb` div with an `<img>` inside it. Find that rendering code (the function
building each card's `innerHTML`, look for the line containing
`'<div class="thumb"><img src="'`) and make the thumb div conditional on `c.img` being set:
when `c.img` is present, render the thumb div exactly as before; when it's absent, render
nothing in its place (the card's `.body` section — title, description, footer — still
renders normally, it just has no image at the top). Keep the change minimal — this is a
small conditional around existing markup-building code, not a rewrite of the render function.

- [ ] **Step 5: Verify**

```bash
grep -c '"assets/thumb-' docs/water.html   # expect: 7
grep -c 'water-use-by-season' docs/water.html   # expect: >= 1 (the new CARDS entry)
```

Read the finished file and confirm: the CARDS array now has 8 entries, the 8th has no `img`
field, the render function's thumb-div logic is conditional (won't throw or render a broken
`<img src="undefined">` for the 8th card). Re-run `python3 scripts/build_nav.py` — expect
`docs/water.html` reported as stamped (NAV/FOOTER markers, same as every other page).

Confirm no root-absolute links: `grep 'href="/' docs/water.html` → no matches (the `CARDS`
array's `f:` values are bare filenames like `"precipitation-by-month.html"`, used as
`a.href=c.f` — already relative, just confirm no root slash crept in anywhere else in the
file).

- [ ] **Step 6: Commit**

```bash
git add docs/water.html docs/assets/thumb-*.png
git commit -m "Port the Water hub; add the missing 8th card and its thumbnails"
```

---

### Task 3: Add Water to the shared nav and move its Home page card to "Available now"

**Files:**
- Modify: `docs/_partials/nav.html`
- Modify: `docs/index.html`

**Interfaces:**
- Consumes: `docs/water.html` (Task 2) — both edits in this task link to it.

- [ ] **Step 1: Add Water to the nav partial**

In `docs/_partials/nav.html`, the `.site-nav__links` div currently reads:

```html
  <div class="site-nav__links">
    <a href="climate.html">Climate</a>
    <a href="sun-solar.html">Sun &amp; Solar</a>
    <a href="wind.html">Wind</a>
    <a href="flood-hazard.html">Flood &amp; Hazard</a>
  </div>
```

Add a `<a href="water.html">Water</a>` link. Placement: after Climate, before Sun & Solar —
matches the site's content order (Lesson 1 Climate, Lesson 3 Sun/Wind/Flood, Lesson 5
Water) better than appending at the end. Result:

```html
  <div class="site-nav__links">
    <a href="climate.html">Climate</a>
    <a href="water.html">Water</a>
    <a href="sun-solar.html">Sun &amp; Solar</a>
    <a href="wind.html">Wind</a>
    <a href="flood-hazard.html">Flood &amp; Hazard</a>
  </div>
```

- [ ] **Step 2: Move the Water card on the Home page**

In `docs/index.html`, the "Available now" card grid currently ends with the Flood & Hazard
card, and the "Coming later" grid starts with this Watersheds & Water card:

```html
      <div class="nav-card soon">
        <h3>Watersheds &amp; Water</h3>
        <p>Macro watershed, catchment area, rainwater harvesting, and site water flow.</p>
        <span class="tag">V2</span>
      </div>
```

Remove that block from "Coming later", and add a real card for it to "Available now" (after
Climate, matching the nav's new ordering), in the same style as the other real cards:

```html
      <a class="nav-card" href="climate.html">
        <h3>Climate</h3>
        <p>Temperature, precipitation, wind, and frost-free/hardiness data for the site.</p>
      </a>
      <a class="nav-card" href="water.html">
        <h3>Watersheds &amp; Water</h3>
        <p>Macro watershed, catchment area, rainwater harvesting, and site water flow.</p>
      </a>
      <a class="nav-card" href="sun-solar.html">
```

(i.e. insert the new `<a>` card between the existing Climate and Sun & Solar cards; the rest
of the "Available now" grid — Wind, Flood & Hazard — stays where it is.) The "Coming later"
grid should now have only 2 cards left: Species Inventory (V3) and Zones & Design (V3).

- [ ] **Step 3: Re-stamp and verify**

```bash
python3 scripts/build_nav.py
```

Expected: every `docs/*.html` page reports stamped (the nav partial changed, so all pages
that include it get re-stamped — this is expected and correct, not a bug).

```bash
grep -c 'water.html' docs/_partials/nav.html   # expect: 1
grep -c 'nav-card soon' docs/index.html   # expect: 2 (only Species Inventory + Zones & Design left)
grep -rn 'href="/' docs/   # expect: no output anywhere
```

- [ ] **Step 4: Commit**

```bash
git add docs/_partials/nav.html docs/index.html
git commit -m "Add Water to the nav and move its Home page card to Available now"
```

Note: this commit's diff will show every `docs/*.html` file changed (re-stamped nav), not
just `docs/_partials/nav.html` and `docs/index.html` — that's expected given the stamping
mechanism, not a mistake. Stage and commit all of it together.

---

### Task 4: Final verification

**Files:** none created — verification only.

**Interfaces:** none — consumes the complete output of Tasks 1-3.

- [ ] **Step 1: Re-run the test suite**

```bash
python3 -m pytest scripts/tests/ -v
```

Expected: 16/16 pass (unchanged from V1 — no script code changed in this plan).

- [ ] **Step 2: Re-run `build_nav.py`, confirm no-op**

```bash
python3 scripts/build_nav.py
```

Expected: `0 file(s) updated`.

- [ ] **Step 3: Site-wide link crawl**

For every `docs/*.html` file (now 15: the 8 from V1 + the 8 new Water pages + the water
hub... note that's 17 total content pages minus overlap — count them: `ls docs/*.html | wc -l`
and confirm it matches 8 (V1) + 8 (Task 1) + 1 (Task 2 hub) = 17), extract every internal
`href` and confirm it resolves to a real file in `docs/`. Build one link-graph table like
V1's Task 10 did. Confirm zero root-absolute links anywhere (`grep -rn 'href="/' docs/`).

Also confirm reachability: every one of the 8 new Water reports must be linked from
somewhere (the hub `docs/water.html`, per Task 2's fix) — no orphans, matching the standard
V1's final review set.

- [ ] **Step 4: Commit if anything changed**

If Step 3 found and you fixed anything, commit it with a clear message. If nothing needed
fixing, this task produces no commit — just report the clean verification result.

## Self-Review Notes

- **Spec coverage:** all 8 reports (Task 1), the hub + missing-card fix + thumbnails (Task
  2), nav + Home page (Task 3), final verification (Task 4) — every spec section has a task.
- **Placeholder scan:** no TBD/TODO; every step has concrete commands or exact text to
  find/replace.
- **Consistency:** Task 3's nav/Home edits use the exact current file content (captured
  while writing this plan) as the "before" text to match against — if either file has
  changed since, the task's implementer should treat a non-matching "before" block as a
  signal to stop and report BLOCKED rather than guessing.
