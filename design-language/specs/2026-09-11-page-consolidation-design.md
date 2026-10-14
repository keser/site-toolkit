# Site Profile Microsite — Page Consolidation Design

Status: draft, pending approval.

## Goal

Collapse four hub-plus-children page clusters into four single long-form pages, each with an
in-page secondary nav that jumps to full-width sections. This removes the extra click through a
thumbnail hub for every visualization on the site, following the pattern `climate.html` already
uses for its own widgets (badges, full-width panels, one continuous scroll).

| Cluster | Today | After |
|---|---|---|
| Water | `water.html` hub + 8 children | one `water.html`, 8 sections |
| Sun & Solar | `sun-solar.html` hub + 3 children | one `sun-solar.html`, 3 sections |
| Climate + Wind | `climate.html` (already inline) + `wind.html` | `climate.html` only, `wind.html` removed |
| Zones & Design | `zones-design.html` hub + 3 children | one `zones-design.html`, 3 sections (reordered) |

15 files are deleted outright: all 14 child pages named in the sections below (8 water + 3 sun +
3 zones) plus `wind.html`. The 3 hub pages (`water.html`, `sun-solar.html`, `zones-design.html`)
are not deleted as files — their filenames and nav links stay; their hub markup is replaced
in place with the consolidated section content. Net: 19 pages today (3 hubs + 14 children +
`wind.html` + `climate.html`) become 4 pages (the 3 former hubs, now full pages, + `climate.html`
with Wind folded in).

## Why now

Andrew's own words: the hub pages exist only to route to a thumbnail grid; the destination
pages are usually short (~180-260 lines) and read better as sections of one continuous page,
the way `climate.html`'s widgets already work. `wind.html` duplicates content already partially
inlined on `climate.html` (see Climate + Wind below) — folding it removes that duplication
rather than creating new duplication elsewhere.

## Shared pattern: secondary nav

Every consolidated page gets a sticky-free (scrolls with the page, not fixed) row of jump-links
right under the page header, reusing the site's existing `.badge` pill component verbatim
(already used for Climate's Köppen/Hardiness/Bioregion badges) — same visual weight, same
`.badge-row` flex-wrap container, but each pill is an `<a href="#section-id">` instead of static
text:

```html
<div class="badge-row" id="section-nav">
  <a class="badge" href="#precipitation">Precipitation by Month</a>
  <a class="badge" href="#runoff">Runoff by Surface</a>
  ...
</div>
```

No new CSS class — `.badge` already renders as a pill; an `<a>` needs only `text-decoration:none`
and `cursor:pointer`, added once to the shared badge rule (a one-line addition, applied to all
pages that use `.badge` since it's a shared, ported style block — pure addition, doesn't change
existing static-badge appearance).

Each jump target is a `<section id="...">` wrapping that visualization's full original content:
its own `<h2>` (promoted from the child page's `<h1>`), its own description paragraph (from the
child's `<p class="subhead">`), then the original chart/table/photo markup unchanged, then a
per-section source note (see below). Sections stack full-width (no side-by-side grid at the
section level — matches "each visualization should be full width").

## Shared pattern: per-section source notes

Not a combined bibliography. Each section keeps its own source line exactly where the source
child page had it (most water children: an inline `<b>Source:</b> ...` sentence near the
bottom of that content block; `climate.html`/`wind.html`-style pages: a `<footer class="notes">`
block). When folding a child's content into a section, that source text moves with it, unchanged
in wording, into a `<p class="section-source">` (new class: same visual treatment as the site's
existing `<footer class="notes">` — `font-size:12px; color:var(--text-muted); line-height:1.6`)
placed at the end of that `<section>`, not collected into one page-level footer. This matches how
diverse the Water page's citations already are (NOAA Atlas 14, USGS 3DEP, Town of Portland water
utility, KHFD station data, etc.) — a single combined bibliography would blur which source backs
which chart.

## Mechanical merge safety (technical note, not user-facing)

Every source page's `<script>` block is self-contained (top-level `const`s + either bare
functions or IIFEs). Concatenating them naively into one page's `<script>` risks two collisions:

1. **Top-level `const`/`let` name collisions** (e.g. two children might each declare
   `const DATA = {...}` with different meanings) — a real `SyntaxError` or silent wrong-value bug
   in classic (non-module) `<script>` tags, which share one global scope.
2. **Container-id collisions** (`document.getElementById("chart-grid")` existing in two children
   pointed at two different divs) — wrong chart renders into wrong section, or a `null` crash.

Fix, applied per source file during the plan/implementation phase:

- Wrap each source file's **entire original `<script>` body, verbatim**, in its own
  `(function(){ ... })();` — this closes over all of that file's top-level consts/functions
  without renaming a single identifier inside, since nothing in the reviewed files reaches across
  file boundaries (each child page is already fully self-contained). Internal same-file
  references (e.g. a builder function calling a same-file helper) keep working because they share
  the enclosing closure.
- Rename only each file's own container element `id`s (and the matching `getElementById` calls
  inside that same file's script) with a short section-specific prefix (e.g. `precip-`,
  `runoff-`, `secA-` → `precip-secA-`), enumerated exactly, file by file, in the implementation
  plan — no placeholders, no "similar to the above."
- CSS is not a collision risk (duplicate `.panel`/`.viz-root` rules across concatenated `<style>`
  blocks simply cascade, last-wins, without erroring) — dedupe to one canonical `.viz-root` +
  shared-component block for file cleanliness, but any page-specific CSS class unique to one
  child (e.g. `.matrix-table`, `.two-col`, `.photo-block` on the Zones pages) is kept, since those
  aren't part of the common boilerplate.

This is a copy/merge of already-approved, already-shipped content — not new authoring — so the
plan specifies exact before/after per file rather than re-deriving chart logic from scratch.

---

## Water (`docs/water.html`)

Section order matches the hub's existing card order (the hub's own ordering is not being
second-guessed here):

1. Precipitation by Month — from `precipitation-by-month.html`
2. Runoff by Surface — from `runoff-by-surface.html`
3. Site Water Balance — from `water-balance.html`
4. Elevation Cross-Sections — from `elevation-sections.html`
5. Site Water-Flow Schematic — from `site-flow-schematic.html`
6. Design-Storm Frequency — from `design-storm-frequency.html`
7. Macro Watershed — from `macro-watershed-scale.html`
8. Household Water Use by Season — from `water-use-by-season.html`

`water.html`'s own hub markup (the `CARDS` JS array + thumbnail-card renderer, already stripped
of course-slide tags per the prior site-consistency fix) is deleted entirely and replaced by the
8 sections above under one `<h1>Water</h1>` header, followed by the section-nav badge row.
Page-level subhead becomes a short one-liner describing the consolidated page (adapted from the
hub's own intro sentence: "Eight views of water on the property — rainfall, runoff, the
watershed it sits in, and the rainwater-harvesting potential across every surface."), dropping
the hub-specific "click any card" instruction since there's no longer a card grid.

**Redacted account number carry-forward:** `water-use-by-season.html` has a documented
redaction (real utility account number stripped per `CLAUDE.md`'s explicit note). When this
section's content moves into `water.html`, the redaction moves with it unchanged — re-verify
the redacted line survived the merge intact, don't re-derive it from the coursework source.

Delete after merge: `precipitation-by-month.html`, `runoff-by-surface.html`, `water-balance.html`,
`elevation-sections.html`, `site-flow-schematic.html`, `design-storm-frequency.html`,
`macro-watershed-scale.html`, `water-use-by-season.html`.

## Sun & Solar (`docs/sun-solar.html`)

Section order matches the hub's existing card order:

1. Sun Path Charts — from `sun-path-charts.html`
2. Sun Path — 3D Site Diagram — from `sun-path-3d.html`
3. Sun Path Overlay — from `sun-path-overlay.html`

Same treatment as Water: hub markup replaced by 3 full-width sections + section-nav badge row,
page subhead adapted from the hub's existing "Three views of solar exposure across the property,
built from a bioclimatic design study of local weather and sun-position data."

Delete after merge: `sun-path-charts.html`, `sun-path-3d.html`, `sun-path-overlay.html`.

**Sectors cross-link:** `docs/sectors.html`'s existing link to `sun-path-charts.html` (in its
Sun/Solar section) is repointed to `sun-solar.html#sun-path-charts` (the new section's anchor id).

## Climate + Wind (fold into `docs/climate.html`, delete `docs/wind.html`)

`climate.html` already inlines an **approximate** annual wind rose (Lesson 1 Figma
reconstruction) and the **real** 4 seasonal wind roses (KHFD station data) — but its seasonal
roses use a simplified single-color-per-sector design (total % only), not `wind.html`'s full
5-speed-bin stacked/colored version, and its "raw data" toggle has only a 4-row seasonal summary
table, not `wind.html`'s full monthly table or its per-season 16-sector × 5-speed-bin detail
tables. Confirmed by reading both files in full — this is genuinely a partial duplicate, not a
full one.

**Decision: keep climate.html's existing rose diagrams unchanged, add wind.html's two missing
data tables.** Rationale: replacing the working, already-shipped simplified roses with the
full speed-stacked version would put two different visual treatments of the same 4 seasons
back-to-back on one page (the existing simple rose, right next to a re-rendered detailed one) —
confusing, not clarifying. The two tables `wind.html` has that `climate.html` doesn't are pure
data-completeness additions with no such visual overlap, and they already belong in
`climate.html`'s existing "View raw data tables" `<details class="table-toggle">` alongside its
current 4 tables — same UI pattern, no new component needed.

Changes to `climate.html`:

- Add `wind.html`'s `WIND_DATA.monthly_table` (12-row month-by-month mean speed / max gust /
  calm % / prevailing direction / prevailing %) as a 5th table inside the existing
  `#table-grid` raw-data toggle.
- Add `wind.html`'s per-season 16-sector × 5-speed-bin matrix tables (4 tables, one per season,
  the ones wind.html placed in its own nested `<details>`) as 4 more tables in the same
  `#table-grid` toggle — dropping wind.html's separate nested `<details>` wrapper since they now
  live inside climate's own single toggle.
- Update the existing sentence "See the full Wind report for the full picture" (in the
  panel-sub under "Seasonal Wind Roses") — remove the dangling link/reference to `wind.html`
  since there's no longer a separate report to point to; keep the rest of that sentence's factual
  content (winter-vs-rest-of-year seasonal split) as-is.
- Update `climate.html`'s own footer notes to add wind.html's attribution
  ("Iowa Environmental Mesonet ASOS archive for station HFD ... via mesonet.agron.iastate.edu")
  since that source is now backing tables that live on this page.
- No id-prefix/IIFE-wrap merge risk here in the general sense (this is hand-integration into an
  existing script, not a multi-file concatenation) — but the new `WIND_DATA` monthly/matrix data
  must be added under names that don't collide with `climate.html`'s existing top-level `WIND`
  and `SEASONS` consts (e.g. a new `const WIND_MONTHLY = [...]` and extending each `SEASONS[i]`
  object with a `matrixPct` field rather than introducing a second parallel seasons array).

Delete after merge: `wind.html`.

Nav (`docs/_partials/nav.html`): remove the `<a href="wind.html">Wind</a>` link entirely (8 links
remain: Climate, Water, Sun & Solar, Flood & Hazard, Species Inventory, Zones & Design, Base Map,
Sectors).

**Sectors cross-link:** `docs/sectors.html`'s existing link to `wind.html` (in its Wind section)
is repointed to `climate.html#chart-grid-seasons` (or a more specific new anchor id added to the
seasonal-wind-roses block, e.g. wrapping that block in `<section id="wind">` — implementation
plan picks the exact id, consistent with the id-prefix scheme above).

## Zones & Design (`docs/zones-design.html`)

Section order, per explicit instruction — **not** the hub's current card order:

1. Current Zones — from `current-zones.html`
2. Microclimates — from `microclimates.html`, **reordered internally**: drop its first content
   block (the `microclimates-aerial.jpg` drone photo + caption/credit, immediately after the
   header), promote its map photo block (`microclimates-map.jpg`, currently the *second*
   photo-block, appearing after the "Microclimate Types" table) to run **immediately after the
   section header**, then "Microclimate Types" table, then "Known Plant Species", then
   "Observations & Ideas" — matching the site's established title-then-map convention (Species
   Inventory, Base Map, Sectors all lead with their hero image right under the header).
3. Zones Brainstorm — from `zones-brainstorm.html`

Same hub-replacement treatment as Water/Sun & Solar otherwise. Page subhead adapted from the
hub's own framing.

Delete after merge: `current-zones.html`, `microclimates.html`, `zones-brainstorm.html`.

The dropped microclimates aerial photo (`assets/zones-design/microclimates-aerial.jpg`) stays
on disk (not referenced elsewhere, but this site's convention throughout has been to leave
superseded assets in place rather than delete them — matches how the Journal's spec/plan docs
were kept after the feature itself was removed).

## Site integration (all four pages)

- **Nav** (`docs/_partials/nav.html`): drop the Wind link (see above); Water, Sun & Solar,
  Zones & Design links stay pointed at the same filenames (now single pages, not hubs) —
  no nav text changes needed for those three.
- **Home** (`docs/index.html`): the nav-cards for Water, Sun & Solar, Zones & Design currently
  describe hub/multi-page content ("eight views," "three views," etc.) — reword each card's
  description to drop any "click through to see each" hub framing while keeping the substance
  (still "eight views of water," etc. — the count of visualizations hasn't changed, only the
  navigation mechanic). No card exists for Wind specifically (confirm during implementation; if
  one does, remove it).
- **Relative links:** same bar as every prior phase — `grep -rn 'href="/' docs/` and
  `grep -rn 'src="/' docs/` must both return nothing after this change.
- **`build_nav.py`:** run after all nav/footer edits, before committing; verify idempotent
  (`0 file(s) updated`) on a second run.
- **Tests:** `python3 -m pytest scripts/tests/ -q` must still show all tests passing.

## Out of scope (explicitly deferred)

- Redesigning `climate.html`'s seasonal wind roses to the fuller speed-stacked style — considered
  and rejected above (would duplicate visual treatment on one page); can be revisited later as
  its own scoped change if wanted.
- Any change to `flood-hazard.html`, `species-inventory.html`, `base-map.html`, or `index.html`'s
  structure beyond the card-copy edits and cross-link updates named above.
- Re-evaluating the hub-vs-single-page pattern for any cluster not named in this spec.
