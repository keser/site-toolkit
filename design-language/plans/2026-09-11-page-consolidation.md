# Page Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Collapse the Water, Sun & Solar, and Zones & Design hub-plus-children page clusters into
three single long-form pages with in-page secondary nav, fold `wind.html` into `climate.html`,
and update all cross-links and site chrome (nav, Home, Sectors) accordingly.

**Architecture:** Each consolidated page keeps its existing filename (`water.html`, `sun-solar.html`,
`zones-design.html`) and existing `<!-- NAV:START/END -->` / `<!-- FOOTER:START/END -->` marker
regions. The hub's thumbnail-card markup is deleted and replaced with N full-width `<section>`
blocks (one per former child page), each holding that child's original header (promoted to
`<h2>`), body content, and source note, wrapped in its own uniquely-prefixed CSS/JS namespace.
A `.badge-row` of anchor-link pills sits under the page header as the secondary nav.

**Tech Stack:** Plain HTML/CSS/vanilla JS, no build step, matching every existing page on this
site (`.viz-root` theming pattern, inline SVG, self-contained `<script>` blocks).

**Spec:** `site-plan/specs/2026-09-11-page-consolidation-design.md`

## Global Constraints

- **Relative links only.** After every task: `grep -rn 'href="/' docs/` and `grep -rn 'src="/' docs/`
  must both return nothing.
- **Nav/footer stamping.** Run `python3 scripts/build_nav.py` from the repo root after any edit
  to `docs/_partials/nav.html` or `docs/_partials/footer.html`, or after adding/removing a page —
  before committing. A second run must report `0 file(s) updated` (idempotent).
- **Tests.** `python3 -m pytest scripts/tests/ -q` must pass (currently 16 tests) after every task.
- **`git add -A` when committing**, never a hand-picked file list — `build_nav.py` re-stamps every
  `docs/*.html` file whenever the shared nav/footer partials change, and a scoped `git add` has
  caused an incomplete commit in an earlier phase of this project.
- **Universal shared identifiers — do not rename these, they already match everywhere they
  appear on this site:** CSS custom properties `--surface-1`, `--page`, `--text-primary`,
  `--text-secondary`, `--text-muted`, `--grid`, `--baseline`, `--border`, `--badge-bg`, `--accent`;
  CSS classes `.viz-root`, `.wrap`, `.subhead`, `.badge-row`, `.badge` (+ `.badge b`), `.panel`,
  `.panel-title`, `.panel-sub`, `svg.chart`, `.tooltip`, `.data-table` (+ its `caption`/`th`/`td`
  descendants), and the nav/footer partial classes (`.site-nav*`, `.site-footer*`, stamped
  separately — never touch these by hand).
- **Blanket rename rule for everything else.** Every source file being merged onto a consolidated
  page gets a short prefix (table below, per task). For that file: every CSS custom property not
  in the universal list, and every CSS class not in the universal list, gets renamed from `--foo`
  / `.foo` to `--{prefix}-foo` / `.{prefix}-foo` — at its declaration (light `.viz-root` rule, the
  `@media (prefers-color-scheme: dark)` block, and the `:root[data-theme="dark"]` block for custom
  properties; the bare selector for classes) and at **every** reference (`var(--foo)` in CSS or
  JS, `class="foo"` in HTML, `className`/`classList`/template-string class assignments in JS).
  Apply this even where two files happen to use the same value today (e.g. `--hard: #5598e7` is
  identical in two water files right now) — rename anyway, since "happens to match today" is not
  a guarantee and the rename costs nothing. Same rule for element `id`s and their matching
  `getElementById("...")` calls — prefix table given per task.
  Do NOT rename `.note` or `.src` into the universal list — they look like shared boilerplate
  (present under the same name in every water file) but their actual CSS rules differ file to
  file (confirmed: `precipitation-by-month.html`'s `.note` is plain text, `water-use-by-season.html`'s
  `.note` is a colored callout box) — they must be prefixed like everything else.
- **Wrap every merged file's entire `<script>` body, verbatim, in `(function(){ ... })();`** — no
  need to rename anything *inside* the closure beyond the id/class/var renames above, since each
  source file is already self-contained (confirmed: no file in this plan calls a function or reads
  a variable defined in a different file).
- **Section anchor ids** (used both by that page's own secondary nav and, for two of them, by
  `docs/sectors.html`'s cross-links) are given per task — use them exactly as written.
- **Per-section source note.** Keep each file's own source/citation text (its `<p class="src">`,
  `<p class="note">` covering sourcing, or `<footer class="notes">` — whichever that file uses)
  inside that file's own `<section>`, renamed per the blanket rule above. Do not create one
  combined bibliography.

---

### Task 1: Consolidate `docs/water.html`

**Files:**
- Modify: `docs/water.html` (hub → 8-section page)
- Delete: `docs/precipitation-by-month.html`, `docs/runoff-by-surface.html`,
  `docs/water-balance.html`, `docs/elevation-sections.html`,
  `docs/site-flow-schematic.html`, `docs/design-storm-frequency.html`,
  `docs/macro-watershed-scale.html`, `docs/water-use-by-season.html`

**Interfaces:**
- Produces: section ids `#precipitation`, `#runoff`, `#water-balance`, `#elevation`,
  `#flow-schematic`, `#design-storm`, `#watershed`, `#water-use` on `water.html` — no other task
  in this plan links to them.

Read each of the 8 files listed above in full before starting — they are the real, currently-shipped
content; copy their body markup and `<script>` content verbatim except for the renames below.

**Per-file prefix and rename table:**

| File | prefix | non-universal CSS custom properties to rename | non-universal CSS classes to rename | ids to rename |
|---|---|---|---|---|
| `precipitation-by-month.html` | `precip` | `--band-et`, `--band-et-line`, `--mean-line`, `--series-precip` | `.ax`, `.val`, `.gl`, `.base`, `.mean`, `.mean-lbl`, `.et-band`, `.et-lbl`, `.note`, `.src` | (none) |
| `runoff-by-surface.html` | `runoff` | `--hard`, `--hard-2`, `--perm`, `--perm-2` | `.axt`, `.gl`, `.headline`, `.lbl`, `.lbl-b`, `.legend`, `.seclbl`, `.sw`, `.val`, `.val-m2`, `.src` | `flip`→`runoff-flip`, `bars`→`runoff-bars` |
| `water-balance.html` | `wbal` | `--hard`, `--infil`, `--node`, `--perm`, `--rain`, `--runoff` | `.foot`, `.nlbl`, `.nsub`, `.src` | (none) |
| `elevation-sections.html` | `elev` | `--divide`, `--ground`, `--ground-fill`, `--lot`, `--lot-line` | `.axt`, `.gl`, `.note`, `.note-b`, `.src` | `secA`→`elev-secA`, `secB`→`elev-secB` |
| `site-flow-schematic.html` | `flow` | `--contour`, `--divide`, `--exit`, `--flow`, `--lot`, `--lot-line`, `--pool`, `--struct`, `--struct-line`, `--swale-new`, `--swale-old` | `.cl`, `.lbl`, `.lbl-b`, `.lbl-m`, `.note`, `.num`, `.src` | (none) |
| `design-storm-frequency.html` | `storm` | `--curve`, `--curve-dot`, `--evt`, `--evt-line`, `--rec` | `.axl`, `.axt`, `.dot-lbl`, `.gl`, `.note`, `.src` | (none) |
| `macro-watershed-scale.html` | `shed` | `--land`, `--land-line`, `--river`, `--site`, `--water` | `.axt`, `.maplbl`, `.maplbl-b`, `.note`, `.rd`, `.rn`, `.src` | (none) |
| `water-use-by-season.html` | `wuse` | `--base`, `--excess`, `--excess-line`, `--fall`, `--spring`, `--summer`, `--winter` | `.axl`, `.axt`, `.dot-lbl`, `.gl`, `.legend`, `.note`, `.seclbl`, `.src`, `.sw`, `.val` | (none) |

**Redaction carry-forward:** `water-use-by-season.html` has a real utility account number
redacted per `permaculture-site-plan/CLAUDE.md`'s "Redacted account number" note (a body-text
mention near "four consecutive bills" and the source citation line). Copy that file's content
with the redaction exactly as it already reads in the committed file — do not re-derive it from
`pdc-pro-2026`, and do not restore the real number.

- [ ] **Step 1: Build the new shared `<style>` block for `water.html`**

  Replace `water.html`'s existing `<style>...</style>` block (lines 7-44 of the current file —
  the hub's card-grid CSS) with:
  ```html
  <style>
    .viz-root {
      color-scheme: light;
      --surface-1: #fcfcfb; --page: #f9f9f7; --text-primary: #0b0b0b;
      --text-secondary: #52514e; --text-muted: #898781; --grid: #e1e0d9;
      --baseline: #c3c2b7; --border: rgba(11,11,11,0.10);
      --badge-bg: #eef0ea; --accent: #e07b39;
    }
    @media (prefers-color-scheme: dark) {
      :root:where(:not([data-theme="light"])) .viz-root {
        color-scheme: dark;
        --surface-1: #1a1a19; --page: #0d0d0d; --text-primary: #ffffff;
        --text-secondary: #c3c2b7; --text-muted: #898781; --grid: #2c2c2a;
        --baseline: #383835; --border: rgba(255,255,255,0.10);
        --badge-bg: #23261f; --accent: #e8935a;
      }
    }
    :root[data-theme="dark"] .viz-root {
      color-scheme: dark;
      --surface-1: #1a1a19; --page: #0d0d0d; --text-primary: #ffffff;
      --text-secondary: #c3c2b7; --text-muted: #898781; --grid: #2c2c2a;
      --baseline: #383835; --border: rgba(255,255,255,0.10);
      --badge-bg: #23261f; --accent: #e8935a;
    }
    * { box-sizing: border-box; }
    body { margin: 0; }
    .viz-root {
      font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
      background: var(--page); color: var(--text-primary);
      min-height: 100vh; padding: 32px 20px 60px;
    }
    .wrap { max-width: 900px; margin: 0 auto; }
    .section-title { font-size: 21px; font-weight: 600; margin: 0 0 6px; }
    .subhead { color: var(--text-secondary); font-size: 14px; line-height: 1.5; margin: 0 0 12px; }
    .badge-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
    .badge {
      background: var(--badge-bg); border: 1px solid var(--border); border-radius: 6px;
      padding: 5px 10px; font-size: 12px; color: var(--text-secondary);
      text-decoration: none;
    }
    .badge b { color: var(--text-primary); font-weight: 600; }
    a.badge:hover { border-color: var(--accent); color: var(--text-primary); }
    .panel {
      background: var(--surface-1); border: 1px solid var(--border);
      border-radius: 10px; padding: 16px 16px 10px;
    }
    .panel-title { font-size: 15px; font-weight: 600; margin: 0 0 2px; }
    .panel-sub { font-size: 12px; color: var(--text-muted); margin: 0 0 10px; }
    svg.chart { width: 100%; height: auto; display: block; overflow: visible; }
    section.page-section { margin-bottom: 48px; padding-bottom: 4px; border-bottom: 1px solid var(--border); }
    section.page-section:last-of-type { border-bottom: none; }
    .refs {
      margin-top: 12px; padding-top: 18px; border-top: 1px solid var(--border);
      font-size: 12.5px; color: var(--text-secondary); line-height: 1.7;
    }
    .refs b { color: var(--text-primary); }
    .survey { margin-top: 18px; background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 16px 18px; }
    .survey img { width: 100%; height: auto; border-radius: 8px; border: 1px solid var(--border); display: block; }
    .survey p { font-size: 12.5px; color: var(--text-secondary); line-height: 1.6; margin: 10px 0 0; }
    .survey b { color: var(--text-primary); }
  </style>
  ```
  This is the union of every universal identifier from the Global Constraints list, plus a new
  `.section-title` class for promoted `<h2>`s, a `section.page-section` divider rule, and the
  hub's own pre-existing `.refs`/`.survey` rules (kept verbatim — they style the 1996 site-survey
  block described in Step 3 below).

  Then append, immediately after this block and still inside `<head>`, once per file in the
  table above, that file's own **non-universal** custom-property declarations (light block, dark
  media-query block, dark `[data-theme]` block) and non-universal class rules, each renamed per
  that file's prefix. For example, `precipitation-by-month.html`'s light-mode block becomes:
  ```css
  .viz-root { --precip-band-et: rgba(224,123,57,0.14); --precip-band-et-line: #e07b39; --precip-mean-line: #52514e; --precip-series-precip: #5598e7; }
  ```
  (declared as an *additional* rule targeting `.viz-root`, not replacing the canonical block above
  — CSS rules with the same selector merge) and its class rules become e.g.:
  ```css
  .precip-ax { fill: var(--text-muted); font-size: 11px; }
  .precip-val { fill: var(--text-secondary); font-size: 10.5px; font-weight: 600; }
  .precip-gl { stroke: var(--grid); stroke-width: 1; }
  .precip-base { stroke: var(--baseline); stroke-width: 1.5; }
  .precip-mean { stroke: var(--precip-mean-line); stroke-width: 1.5; stroke-dasharray: 5 4; }
  .precip-mean-lbl { fill: var(--precip-mean-line); font-size: 10.5px; font-weight: 600; }
  .precip-et-band { fill: var(--precip-band-et); }
  .precip-et-lbl { fill: var(--precip-band-et-line); font-size: 10.5px; font-weight: 600; }
  .precip-note { font-size: 12.5px; color: var(--text-secondary); line-height: 1.55; margin: 12px 2px 0; }
  .precip-src { font-size: 11.5px; color: var(--text-muted); margin: 14px 2px 0; }
  ```
  Repeat this — read the source file's own `<style>` block, take every rule not in the universal
  list, rename its selector/custom-properties with that file's prefix — for all 8 files.

- [ ] **Step 2: Replace the body content**

  Replace everything between `<div class="viz-root"><div class="wrap">` and the closing
  `</div></div>` (currently the hub's `<h1>`, `<p class="subhead">`, `<div class="grid" id="grid">`,
  `.refs`, and `.survey` blocks) with:
  ```html
  <div class="viz-root"><div class="wrap">
    <header>
      <h1 class="section-title" style="font-size:23px;">Water</h1>
      <p class="subhead">Eight views of water on the property — rainfall, runoff, the watershed it sits in, and the rainwater-harvesting potential across every surface.</p>
      <div class="badge-row" id="section-nav">
        <a class="badge" href="#precipitation">Precipitation by Month</a>
        <a class="badge" href="#runoff">Runoff by Surface</a>
        <a class="badge" href="#water-balance">Site Water Balance</a>
        <a class="badge" href="#elevation">Elevation Cross-Sections</a>
        <a class="badge" href="#flow-schematic">Site Water-Flow Schematic</a>
        <a class="badge" href="#design-storm">Design-Storm Frequency</a>
        <a class="badge" href="#watershed">Macro Watershed</a>
        <a class="badge" href="#water-use">Household Water Use by Season</a>
      </div>
    </header>

    <section class="page-section" id="precipitation">
      <!-- precipitation-by-month.html's <h1> becomes <h2 class="section-title">, its
           subhead/badge-row/panel/note/src content follows verbatim with the precip- prefix
           renames applied -->
    </section>
    <section class="page-section" id="runoff"> <!-- runoff-by-surface.html, runoff- prefix --> </section>
    <section class="page-section" id="water-balance"> <!-- water-balance.html, wbal- prefix --> </section>
    <section class="page-section" id="elevation"> <!-- elevation-sections.html, elev- prefix --> </section>
    <section class="page-section" id="flow-schematic"> <!-- site-flow-schematic.html, flow- prefix --> </section>
    <section class="page-section" id="design-storm"> <!-- design-storm-frequency.html, storm- prefix --> </section>
    <section class="page-section" id="watershed"> <!-- macro-watershed-scale.html, shed- prefix --> </section>
    <section class="page-section" id="water-use"> <!-- water-use-by-season.html, wuse- prefix --> </section>

    <div class="refs">
      <b>Source drawing:</b> the 1996 zoning-approved Partial Site Plan below (1"&nbsp;=&nbsp;10') — the primary source for the house footprint, driveway, and impermeable-area figures used throughout these reports.
    </div>
    <div class="survey">
      <img src="assets/site-survey-1996.jpg" alt="1996 zoning-approved Partial Site Plan, hand-drawn, scale 1 inch to 10 feet, showing the existing structure, proposed addition, swimming pool, driveway, and property lines" width="1400" height="1050">
      <p><b>Partial Site Plan</b> — approved for zoning compliance 2/26/1996. Existing structure 613&nbsp;ft², proposed addition 312.5&nbsp;ft², frontage on Freestone&nbsp;Ave N&nbsp;51°00'W&nbsp;46.00&nbsp;ft. No additions to the house since.</p>
    </div>
  </div></div>
  ```
  For each `<section>`, replace that file's own `<h1>` with `<h2 class="section-title">` holding
  the same text, keep its `<p class="subhead">` unchanged, then paste the rest of its body content
  (badge-row stat pills, `.panel` chart, `.note`/`.src` paragraphs, any other markup) verbatim
  with that file's prefix renames applied to every class attribute. The 1996 survey block
  (`.refs`/`.survey`) is page-level reference material, not tied to one section — keep it once,
  at the end, exactly as shown above (unchanged from the current hub).

- [ ] **Step 3: Merge the scripts**

  Replace the hub's `<script>...</script>` block (the `CARDS` array + card renderer) with 8
  back-to-back IIFEs, one per file, in section order:
  ```html
  <script>
  (function(){
    // precipitation-by-month.html's entire original <script> body, verbatim,
    // with --precip-*/.precip-* renames applied to every var()/class reference
  })();
  (function(){
    // runoff-by-surface.html's entire original <script> body, verbatim,
    // with --runoff-*/.runoff-* renames and flip→runoff-flip / bars→runoff-bars id renames applied
  })();
  (function(){
    // water-balance.html — wbal- prefix
  })();
  (function(){
    // elevation-sections.html — elev- prefix, secA→elev-secA / secB→elev-secB id renames
  })();
  (function(){
    // site-flow-schematic.html — flow- prefix
  })();
  (function(){
    // design-storm-frequency.html — storm- prefix
  })();
  (function(){
    // macro-watershed-scale.html — shed- prefix
  })();
  (function(){
    // water-use-by-season.html — wuse- prefix
  })();
  </script>
  ```
  Some of these files may already wrap their own script in `(function(){...})();` — if so, that
  becomes the IIFE (don't double-wrap); if a file's script has no wrapper, add one.

- [ ] **Step 4: Delete the 8 source files and verify**

  ```bash
  cd docs
  git rm precipitation-by-month.html runoff-by-surface.html water-balance.html \
    elevation-sections.html site-flow-schematic.html design-storm-frequency.html \
    macro-watershed-scale.html water-use-by-season.html
  ```
  Open `water.html` in a browser (or read it back) and confirm: all 8 secondary-nav badges jump
  to their section; every chart renders (no blank panels — a blank panel usually means an id
  rename was missed in either the DOM or the matching `getElementById` call); light and dark mode
  both look correct (a wrong color usually means a custom-property rename was missed in one of
  the three declaration blocks).

- [ ] **Step 5: Commit**

  ```bash
  git add -A
  git commit -m "Consolidate Water hub + 8 children into one page"
  ```

---

### Task 2: Consolidate `docs/sun-solar.html`

**Files:**
- Modify: `docs/sun-solar.html` (hub → 3-section page)
- Delete: `docs/sun-path-charts.html`, `docs/sun-path-3d.html`, `docs/sun-path-overlay.html`

**Interfaces:**
- Produces: section id `#sun-path-charts` on `sun-solar.html` — **Task 5 links to this exact id**
  from `docs/sectors.html`. Also produces `#sun-path-3d`, `#sun-path-overlay` (no other task
  links to these two).

Read all 3 files in full before starting.

**Per-file prefix and rename table:**

| File | prefix | non-universal CSS custom properties | non-universal CSS classes | ids to rename |
|---|---|---|---|---|
| `sun-path-charts.html` | `spc` | `--series-fall`, `--series-spring`, `--series-summer`, `--series-winter` | `.axis-label`, `.axis-label-strong`, `.baseline`, `.crosshair-line`, `.direct-label`, `.direct-label-strong`, `.grid`, `.grid-line`, `.hit-layer`, `.hour-dot`, `.hover-dot`, `.panel-stats`, `.sun-path`, `.tables` | `chart-grid`→`spc-chart-grid`, `table-grid`→`spc-table-grid` |
| `sun-path-3d.html` | `sp3d` | `--ground`, `--ground-ring`, `--series-fall`, `--series-spring`, `--series-summer`, `--series-winter` | `.legend-row` | `scene-svg`→`sp3d-scene-svg`, `tooltip`→`sp3d-tooltip`, `legend`→`sp3d-legend` |
| `sun-path-overlay.html` | `spo` | `--hour-grid`, `--series-fall`, `--series-spring`, `--series-summer`, `--series-winter` | `.aerial-frame`, `.anchor-dot`, `.compass-label`, `.direct-label`, `.hour-dot`, `.hour-line`, `.hour-line-label`, `.legend-row`, `.month-dot`, `.month-legend`, `.month-line`, `.polar-axis-label`, `.polar-chart-holder`, `.polar-compass-label`, `.polar-wrap`, `.ring-line`, `.season-path` | `aerial-frame`→`spo-aerial-frame`, `overlay-svg`→`spo-overlay-svg`, `overlay-tooltip`→`spo-overlay-tooltip`, `overlay-legend`→`spo-overlay-legend`, `polar-svg`→`spo-polar-svg`, `month-legend`→`spo-month-legend`, `polar-tooltip`→`spo-polar-tooltip` |

Note: `--series-fall/spring/summer/winter` happen to have identical values in all 3 files today —
rename per-file anyway (`--spc-series-winter`, `--sp3d-series-winter`, `--spo-series-winter`, etc.)
per the blanket rule. `.direct-label` and `.hour-dot` appear in both `sun-path-charts.html` and
`sun-path-overlay.html` — rename independently in each (`spc-direct-label` vs `spo-direct-label`,
`spc-hour-dot` vs `spo-hour-dot`). `.legend-row` appears in both `sun-path-3d.html` and
`sun-path-overlay.html` — same treatment (`sp3d-legend-row` vs `spo-legend-row`).
`sun-path-overlay.html` uses `panel-sub`/`panel-title` — these ARE in the universal list, leave
unrenamed.

- [ ] **Step 1: Build the new shared `<style>` block**

  Replace `sun-solar.html`'s existing hub `<style>` block with the same canonical block used in
  Task 1 Step 1 (the universal-identifiers block — `.viz-root`, `.wrap`, `.section-title`,
  `.subhead`, `.badge-row`, `.badge`, `.panel`, `.panel-title`, `.panel-sub`, `svg.chart`,
  `section.page-section`), plus one addition: a shared `.tooltip` rule (all 3 files' `.tooltip`
  rules are near-identical; use the fuller version):
  ```css
  .tooltip {
    position: absolute; pointer-events: none; opacity: 0; transition: opacity .1s;
    background: var(--text-primary); color: var(--surface-1); font-size: 11.5px;
    padding: 5px 8px; border-radius: 6px; white-space: nowrap; transform: translate(-50%, -100%);
    z-index: 5;
  }
  ```
  `sun-solar.html`'s current `.wrap { max-width: 900px; }` and `min-height: 60vh` (vs. Water's
  `100vh`) — use `900px` and `60vh` here to match this page's own prior sizing, not Water's.

  Then append each of the 3 files' non-universal custom-property and class rules, renamed with
  that file's prefix, the same way as Task 1 Step 1 (read the source file, take every
  non-universal rule, rename, append).

- [ ] **Step 2: Replace the body content**

  ```html
  <div class="viz-root">
    <div class="wrap">
      <header>
        <h1 class="section-title" style="font-size:22px;">Sun &amp; Solar</h1>
        <p class="subhead">Three views of solar exposure across the property, built from a bioclimatic design study of local weather and sun-position data.</p>
        <div class="badge-row" id="section-nav">
          <a class="badge" href="#sun-path-charts">Sun Path Charts</a>
          <a class="badge" href="#sun-path-3d">Sun Path — 3D Site Diagram</a>
          <a class="badge" href="#sun-path-overlay">Sun Path Overlay</a>
        </div>
      </header>

      <section class="page-section" id="sun-path-charts">
        <!-- sun-path-charts.html: h1 -> h2.section-title, rest verbatim with spc- renames -->
      </section>
      <section class="page-section" id="sun-path-3d">
        <!-- sun-path-3d.html: h1 -> h2.section-title, rest verbatim with sp3d- renames -->
      </section>
      <section class="page-section" id="sun-path-overlay">
        <!-- sun-path-overlay.html: h1 -> h2.section-title, rest verbatim with spo- renames -->
      </section>
    </div>
  </div>
  ```

- [ ] **Step 3: Merge the scripts**

  Same pattern as Task 1 Step 3 — 3 back-to-back `(function(){...})();` IIFEs in section order,
  each with that file's original script content and its renames applied.

- [ ] **Step 4: Delete the 3 source files and verify**

  ```bash
  cd docs
  git rm sun-path-charts.html sun-path-3d.html sun-path-overlay.html
  ```
  Verify all 3 secondary-nav badges jump correctly; the 3D diagram and overlay's hover tooltips
  and polar chart all render (these are the most JS-heavy files in this task — check the browser
  console for `getElementById` returning `null`, the tell for a missed id rename).

- [ ] **Step 5: Commit**

  ```bash
  git add -A
  git commit -m "Consolidate Sun & Solar hub + 3 children into one page"
  ```

---

### Task 3: Fold Wind into Climate, delete `docs/wind.html`

**Files:**
- Modify: `docs/climate.html`
- Delete: `docs/wind.html`
- Modify: `docs/_partials/nav.html` (drop the Wind link)

**Interfaces:**
- Produces: `<section id="wind">` on `climate.html`, wrapping the existing Annual + Seasonal Wind
  Rose content — **Task 5 links to `climate.html#wind`** from `docs/sectors.html`.
- Consumes: `climate.html`'s existing `WIND` and `SEASONS` top-level consts (already defined at
  lines 287-306 of the current file) — this task extends `SEASONS`, it does not replace it.

Read `docs/wind.html` and `docs/climate.html` in full before starting (both already read during
planning — see the design spec's Climate + Wind section for the full comparison).

- [ ] **Step 1: Wrap the existing wind content in a `<section>`**

  In `climate.html`, find:
  ```html
    <div class="grid" id="chart-grid-1"></div>
    <div id="wind-annual-wrap"></div>

    <div style="margin: 4px 0 12px;">
      <div class="panel-title">Seasonal Wind Roses</div>
      <div class="panel-sub">10-year hourly METAR observations, Hartford-Brainard Airport (KHFD, ~16&nbsp;km from site), 2016–2025 — reused from the Lesson 3 Sector Analysis report. See the <a href="wind.html">full Wind report</a> for the full picture.</div>
      <div class="panel-stats" id="season-summary-line"></div>
    </div>
    <div class="grid" id="chart-grid-seasons"></div>

    <div class="panel" id="frost-panel"></div>
  ```
  Replace it with (note: `#frost-panel` moves outside the new `<section id="wind">` — it is
  climate data, not wind data, and stays where it is in the page flow):
  ```html
    <div class="grid" id="chart-grid-1"></div>

    <section id="wind">
      <div id="wind-annual-wrap"></div>

      <div style="margin: 4px 0 12px;">
        <div class="panel-title">Seasonal Wind Roses</div>
        <div class="panel-sub">10-year hourly METAR observations, Hartford-Brainard Airport (KHFD, ~16&nbsp;km from site), 2016–2025. Winter prevails from the N; spring, summer, and fall all trend S (summer most strongly, at 23.7%).</div>
        <div class="panel-stats" id="season-summary-line"></div>
      </div>
      <div class="grid" id="chart-grid-seasons"></div>
    </section>

    <div class="panel" id="frost-panel"></div>
  ```
  The dangling "See the full Wind report" link is removed since `wind.html` no longer exists;
  the factual sentence about the seasonal N/S split moves up into the panel-sub in its place.

- [ ] **Step 2: Add the monthly wind table and seasonal direction×speed matrix tables**

  In `climate.html`'s script, `WIND_DATA`'s equivalent content from `wind.html` needs to land as
  two additions. First, add a new top-level const right after the existing `SEASONS` array
  (climate.html line ~306, after the closing `];` of `SEASONS` and before `const KT_TO_MPH`):
  ```js
  const WIND_MONTHLY = [
    {"month":"January","n_obs":7250,"mean_speed_kt":6.02,"max_speed_kt":23.0,"calm_pct":18.58,"prevailing_direction":"N","prevailing_pct":15.53},
    {"month":"February","n_obs":6614,"mean_speed_kt":6.1,"max_speed_kt":28.0,"calm_pct":18.28,"prevailing_direction":"N","prevailing_pct":16.21},
    {"month":"March","n_obs":7172,"mean_speed_kt":7.05,"max_speed_kt":67.0,"calm_pct":14.78,"prevailing_direction":"S","prevailing_pct":13.94},
    {"month":"April","n_obs":6909,"mean_speed_kt":6.64,"max_speed_kt":24.0,"calm_pct":15.4,"prevailing_direction":"S","prevailing_pct":18.09},
    {"month":"May","n_obs":7045,"mean_speed_kt":5.82,"max_speed_kt":21.0,"calm_pct":17.29,"prevailing_direction":"S","prevailing_pct":21.62},
    {"month":"June","n_obs":6806,"mean_speed_kt":5.36,"max_speed_kt":19.0,"calm_pct":18.92,"prevailing_direction":"S","prevailing_pct":26.54},
    {"month":"July","n_obs":6954,"mean_speed_kt":4.92,"max_speed_kt":20.0,"calm_pct":20.05,"prevailing_direction":"S","prevailing_pct":24.62},
    {"month":"August","n_obs":6957,"mean_speed_kt":4.56,"max_speed_kt":30.0,"calm_pct":24.36,"prevailing_direction":"S","prevailing_pct":19.99},
    {"month":"September","n_obs":6815,"mean_speed_kt":4.63,"max_speed_kt":20.0,"calm_pct":25.8,"prevailing_direction":"N","prevailing_pct":16.45},
    {"month":"October","n_obs":7172,"mean_speed_kt":4.89,"max_speed_kt":21.0,"calm_pct":27.41,"prevailing_direction":"N","prevailing_pct":15.53},
    {"month":"November","n_obs":6984,"mean_speed_kt":5.32,"max_speed_kt":36.0,"calm_pct":24.89,"prevailing_direction":"S","prevailing_pct":13.46},
    {"month":"December","n_obs":7220,"mean_speed_kt":5.26,"max_speed_kt":25.0,"calm_pct":23.31,"prevailing_direction":"N","prevailing_pct":13.12}
  ];
  const WIND_SPEED_BINS = ["1-3","4-7","8-12","13-18","19+"];
  const WIND_SPEED_LABELS = { "1-3": "1–3 kt", "4-7": "4–7 kt", "8-12": "8–12 kt", "13-18": "13–18 kt", "19+": "19+ kt" };
  ```
  This is `wind.html`'s `WIND_DATA.monthly_table` array, copied verbatim (values transcribed
  exactly as they appear in `wind.html` lines 254 and 265) under a new name that doesn't collide
  with `climate.html`'s existing `WIND` const.

  Then extend each of `SEASONS`' four objects (in place, in `climate.html`'s existing `SEASONS`
  array) with a `matrixPct` field holding that season's per-sector, per-speed-bin breakdown from
  `wind.html`'s `WIND_DATA.seasons[key].matrix_pct` (read `wind.html`'s `WIND_DATA` object,
  lines 254, to get the exact values for each of the 4 seasons' `matrix_pct`) — e.g. Winter's
  object gains:
  ```js
  matrixPct: {"N":{"1-3":1.47,"4-7":8.386,"8-12":4.197,"13-18":0.825,"19+":0.038},"NNE":{"1-3":0.835,"4-7":2.419,"8-12":0.749,"13-18":0.104,"19+":0.009},"NE":{"1-3":0.341,"4-7":0.545,"8-12":0.175,"13-18":0.062,"19+":0.0},"ENE":{"1-3":0.19,"4-7":0.346,"8-12":0.085,"13-18":0.009,"19+":0.0},"E":{"1-3":0.275,"4-7":0.204,"8-12":0.043,"13-18":0.005,"19+":0.0},"ESE":{"1-3":0.308,"4-7":0.161,"8-12":0.028,"13-18":0.005,"19+":0.0},"SE":{"1-3":0.564,"4-7":0.384,"8-12":0.047,"13-18":0.014,"19+":0.009},"SSE":{"1-3":1.186,"4-7":1.717,"8-12":0.304,"13-18":0.071,"19+":0.033},"S":{"1-3":1.935,"4-7":7.404,"8-12":2.794,"13-18":0.645,"19+":0.057},"SSW":{"1-3":0.503,"4-7":2.371,"8-12":1.252,"13-18":0.242,"19+":0.009},"SW":{"1-3":0.341,"4-7":1.257,"8-12":0.427,"13-18":0.047,"19+":0.0},"WSW":{"1-3":0.327,"4-7":1.684,"8-12":1.043,"13-18":0.19,"19+":0.0},"W":{"1-3":0.678,"4-7":2.405,"8-12":1.688,"13-18":0.47,"19+":0.033},"WNW":{"1-3":0.379,"4-7":1.992,"8-12":2.296,"13-18":0.93,"19+":0.09},"NW":{"1-3":0.341,"4-7":3.154,"8-12":4.876,"13-18":2.115,"19+":0.204},"NNW":{"1-3":0.422,"4-7":3.913,"8-12":4.017,"13-18":1.134,"19+":0.081}}
  ```
  and similarly Spring/Summer/Fall each gain their own `matrixPct` object copied verbatim from
  `wind.html`'s `WIND_DATA.seasons["Spring (MAM)"].matrix_pct` etc.

  Then, inside the existing `(function(){ ... })()` that builds `#table-grid` (climate.html
  lines ~683-727), after the existing `t4` (Seasonal wind summary) table and before the closing
  `})();`, add:
  ```js
  const t5 = document.createElement("table");
  t5.className = "data-table";
  t5.innerHTML = `
    <caption>Monthly wind summary — KHFD, 2016–2025</caption>
    <thead><tr><th>Month</th><th>Mean speed</th><th>Max gust</th><th>Calm %</th><th>Prevailing dir.</th><th>Prevailing %</th></tr></thead>
    <tbody>${WIND_MONTHLY.map(m => `<tr><td>${m.month}</td><td>${(m.mean_speed_kt * KT_TO_MPH).toFixed(1)} mph</td><td>${(m.max_speed_kt * KT_TO_MPH).toFixed(1)} mph</td><td>${m.calm_pct}%</td><td>${m.prevailing_direction}</td><td>${m.prevailing_pct}%</td></tr>`).join("")}</tbody>
  `;
  tableGrid.appendChild(t5);

  SEASONS.forEach(season => {
    const t = document.createElement("table");
    t.className = "data-table";
    const rows = SECTORS_16.map(sec => {
      const cells = WIND_SPEED_BINS.map(b => `<td>${(season.matrixPct[sec][b] || 0).toFixed(1)}%</td>`).join("");
      return `<tr><td>${sec}</td>${cells}<td><b>${season.pct[SECTORS_16.indexOf(sec)].toFixed(1)}%</b></td></tr>`;
    }).join("");
    t.innerHTML = `
      <caption>${season.label} — direction × speed (KHFD, 2016–2025)</caption>
      <thead><tr><th style="text-align:left;">Dir.</th>${WIND_SPEED_BINS.map(b => `<th>${WIND_SPEED_LABELS[b]}</th>`).join("")}<th>Total</th></tr></thead>
      <tbody>${rows}</tbody>
    `;
    tableGrid.appendChild(t);
  });
  ```
  `climate.html` already speaks mph in its own tables (`t4` converts `meanKt * KT_TO_MPH`), so
  `t5` converts wind.html's kt-native monthly figures to mph for consistency with the rest of the
  page — `wind.html` itself displayed these in kt.

- [ ] **Step 3: Update the footer notes**

  `climate.html`'s existing `<footer class="notes">` (lines 265-268) gets one more sentence
  appended, attributing the KHFD source data (currently only attributed by name, not by archive):
  ```html
      Wind data: Iowa Environmental Mesonet ASOS archive for station HFD (Hartford-Brainard Airport), via mesonet.agron.iastate.edu — real hourly wind observations, not a forecast model. Seasons are meteorological (Winter = Dec/Jan/Feb, etc). Direction bins are 16-point compass (22.5° sectors).
  ```

- [ ] **Step 4: Delete `wind.html`, update nav, verify**

  ```bash
  cd docs
  git rm wind.html
  ```
  In `docs/_partials/nav.html`, delete the line `<a href="wind.html">Wind</a>` (8 links remain:
  Climate, Water, Sun & Solar, Flood & Hazard, Species Inventory, Zones & Design, Base Map,
  Sectors).

  Run `python3 scripts/build_nav.py` from the repo root, then re-run it once more and confirm it
  reports `0 file(s) updated`.

  Open `climate.html` and confirm: the wind section still renders both wind roses; the raw-data
  toggle now shows 9 tables (the original 4 plus the new monthly table and 4 seasonal matrix
  tables); no console errors.

- [ ] **Step 5: Commit**

  ```bash
  git add -A
  git commit -m "Fold Wind report into Climate page, remove wind.html"
  ```

---

### Task 4: Consolidate `docs/zones-design.html`

**Files:**
- Modify: `docs/zones-design.html` (hub → 3-section page)
- Delete: `docs/current-zones.html`, `docs/microclimates.html`, `docs/zones-brainstorm.html`

**Interfaces:**
- Produces: section ids `#current-zones`, `#microclimates`, `#brainstorm` on `zones-design.html`
  (no other task links to these).

Read all 3 files in full before starting. This task has **no JS and no page-specific CSS custom
properties to rename** (confirmed: none of the 3 files declare a `<script>` or a non-universal
`--variable`) — the only prefixing needed is for CSS classes, and even those are mostly already
shared verbatim across the 3 files (confirmed via diff: identical `<style>` blocks except
`current-zones.html` alone additionally defines `.swot-label`/`.swot-list`, and
`microclimates.html` has one harmless duplicate `.q` rule that current-zones.html scopes more
specifically as `.qa-block .q` — same visual result either way).

**Section order (per spec, differs from the hub's current card order):** Current Zones →
Microclimates → Brainstorm.

- [ ] **Step 1: Build the shared `<style>` block**

  Replace `zones-design.html`'s existing hub `<style>` block with the canonical universal block
  (same as Task 1 Step 1: `.viz-root`, `.wrap`, `.section-title`, `.subhead`, `.badge-row`,
  `.badge`, `.panel`, `section.page-section`), plus the zones-cluster's own shared component
  classes — read from `current-zones.html`'s `<style>` block (it is the superset of the 3) and
  copy verbatim: `.photo-block`, `.photo-caption`, `.photo-credit`, `.qa-block`, `.qa-block .q`,
  `.species-list`, `.swot-label`, `.swot-list`, `.table-scroll`, `.two-col`, and (element+class
  selectors) `table.matrix-table`, `table.matrix-table th`, `table.matrix-table td`,
  `table.matrix-table th:first-child`-style variants if present. All of these are byte-identical
  across all 3 source files (confirmed) and none collide with Water's, Sun & Solar's, or
  Climate's identifiers (this is a separate page) — no per-file prefixing needed anywhere in this
  task.

- [ ] **Step 2: Replace the body content**

  ```html
  <div class="viz-root">
    <div class="wrap">
      <header>
        <h1 class="section-title" style="font-size:22px;">Zones &amp; Design</h1>
        <p class="subhead">The property's permaculture zones — current conditions, the microclimates within them, and a brainstorm of proposed changes for the future.</p>
        <div class="badge-row" id="section-nav">
          <a class="badge" href="#current-zones">Current Zones</a>
          <a class="badge" href="#microclimates">Microclimates</a>
          <a class="badge" href="#brainstorm">Zones Brainstorm</a>
        </div>
      </header>

      <section class="page-section" id="current-zones">
        <!-- current-zones.html: h1 -> h2.section-title, rest of body verbatim, no renames needed -->
      </section>

      <section class="page-section" id="microclimates">
        <!-- microclimates.html, REORDERED (see Step 3) -->
      </section>

      <section class="page-section" id="brainstorm">
        <!-- zones-brainstorm.html: h1 -> h2.section-title, rest of body verbatim, no renames needed -->
      </section>
    </div>
  </div>
  ```

- [ ] **Step 3: Reorder the Microclimates section internally**

  `microclimates.html`'s current body order (after its header) is: (a) a `.photo-block` with
  `assets/zones-design/microclimates-aerial.jpg` (drone photo), (b) `<h2 class="section-head">
  Microclimate Types</h2>` + its table, (c) a `.photo-block` with
  `assets/zones-design/microclimates-map.jpg` (the map), (d) `<h2 class="section-head">Known
  Plant Species</h2>` + its two-column list, (e) `<h2 class="section-head">Observations &amp;
  Ideas</h2>` + its content.

  For this section, drop (a) entirely (the aerial drone photo and its caption/credit paragraphs)
  and move (c) — the map `.photo-block` — to run immediately after this section's own `<h2
  id="microclimates">Microclimates</h2>` and `<p class="subhead">` (i.e., first, before
  "Microclimate Types"). Final order inside `<section id="microclimates">`: header → map
  photo-block → Microclimate Types table → Known Plant Species → Observations & Ideas. This
  matches the site's title-then-map convention used on Species Inventory, Base Map, and Sectors.
  The dropped aerial image file (`docs/assets/zones-design/microclimates-aerial.jpg`) stays on
  disk, unreferenced — matches this site's convention of not deleting superseded assets.

- [ ] **Step 4: Delete the 3 source files and verify**

  ```bash
  cd docs
  git rm current-zones.html microclimates.html zones-brainstorm.html
  ```
  Open `zones-design.html` and confirm: 3 secondary-nav badges jump correctly; the Microclimates
  section leads with the map image (not the aerial drone photo, which no longer appears anywhere
  on the page); the SWOT list and species tables from Current Zones still render.

- [ ] **Step 5: Commit**

  ```bash
  git add -A
  git commit -m "Consolidate Zones & Design hub + 3 children, reorder and lead Microclimates with its map"
  ```

---

### Task 5: Site integration — Sectors cross-links, Home cards, final verification

**Files:**
- Modify: `docs/sectors.html`
- Modify: `docs/index.html`

**Interfaces:**
- Consumes: `sun-solar.html#sun-path-charts` (from Task 2) and `climate.html#wind` (from Task 3) —
  this task must run after both.

- [ ] **Step 1: Update `docs/sectors.html`'s two cross-links**

  Find the Sun/Solar section's existing link to `sun-path-charts.html` and change its `href` to
  `sun-solar.html#sun-path-charts`, keeping its link text unchanged.

  Find the Wind section's existing link to `wind.html` and change its `href` to
  `climate.html#wind`, keeping its link text unchanged.

- [ ] **Step 2: Reword the Home page's cards for the now-single-page sections**

  In `docs/index.html`, find the nav-cards for Water, Sun & Solar, and Zones & Design. Their
  current descriptions reference "click any card" / hub-style browsing language inherited from
  when these were multi-page hubs — reword each to describe the page directly, keeping the same
  factual content (visualization count, topics covered) and card visual treatment (same markup
  pattern as every other card on the grid, only the description text changes). If a separate
  "Wind" card exists on the Home grid (check `docs/index.html` for a `wind.html` link), remove it
  — Wind is now reached via Climate.

- [ ] **Step 3: Full-site verification**

  ```bash
  cd /Users/andrewkeser/Code/keser/permaculture-site-plan
  grep -rn 'href="/' docs/    # must be empty
  grep -rn 'src="/' docs/     # must be empty
  python3 scripts/build_nav.py   # stamps any remaining nav/footer drift
  python3 scripts/build_nav.py   # second run — must report "0 file(s) updated"
  python3 -m pytest scripts/tests/ -q   # must pass, 16 tests
  ```
  Also manually confirm, by opening each: `water.html`, `sun-solar.html`, `zones-design.html`,
  `climate.html`, `sectors.html`, `index.html`, and the nav bar on any page (should show 8 links,
  no Wind) — every internal link resolves, no 404s, no leftover reference to a deleted filename
  (`grep -rn 'sun-path-charts.html\|sun-path-3d.html\|sun-path-overlay.html\|wind.html\|precipitation-by-month.html\|runoff-by-surface.html\|water-balance.html\|elevation-sections.html\|site-flow-schematic.html\|design-storm-frequency.html\|macro-watershed-scale.html\|water-use-by-season.html\|current-zones.html\|microclimates.html\|zones-brainstorm.html' docs/` should return nothing — these 14 filenames should not appear anywhere in `docs/` anymore, including in nav/footer partials or other pages' links).

- [ ] **Step 4: Commit**

  ```bash
  git add -A
  git commit -m "Update Sectors cross-links and Home cards for consolidated pages"
  ```
