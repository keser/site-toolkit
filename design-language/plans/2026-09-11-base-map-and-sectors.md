# Base Map & Sectors Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two new pages to the microsite — `docs/base-map.html` (the full-color hand-drawn
site-plan drawing, plus a plain-language legend) and `docs/sectors.html` (the Sector Compass
diagram plus the full 10-sector written analysis) — both sourced from Figma exports and a course
report, wired into nav/Home.

**Architecture:** Two new static pages following the site's existing `.viz-root` hand-authored
pattern. No hub/sub-page split for either — each is a single scrolling page. Image assets were
already exported from Figma and compressed during planning (see Pre-staged Assets below).

**Tech Stack:** Plain static HTML/CSS, no JS beyond what's already used elsewhere on the site
(none needed for these two pages — no dynamic data, unlike Species Inventory).

**Spec:** `site-plan/specs/2026-09-11-base-map-and-sectors-design.md`

## Pre-staged Assets

Already exported from Figma (file `aF9SVeTLwFN8PCEiU2OSBQ`, "PDC-Pro-Vision") and compressed via
`sips` during planning — both already exist at these paths, do not re-fetch or re-compress them:

- `docs/assets/base-map-full-color.jpg` (1200×675, from Figma node `155:3976`, "Full Color +
  Detail Base Map") — legibility-checked at this width (cropped and visually verified both the
  house-cluster labels and the shed-cluster labels read clearly).
- `docs/assets/sectors-compass-diagram.jpg` (1400×787, from Figma node `129:1019`, "Sector
  Compass Diagram – Neighborhood Satellite Imagery - North Up") — legibility-checked at this
  width (arc labels read clearly against the aerial photo).

## Global Constraints

- No root-absolute links: `grep -rn 'href="/' docs/` and `grep -rn 'src="/' docs/` must both
  return nothing after every task.
- `body { margin: 0; }` required in both new pages' `<style>` blocks.
- Title/H1 convention: `<title>{Name} — Lot #86</title>`, `<h1>{Name}</h1>`.
- Nav/footer content lives only in `docs/_partials/nav.html` / `footer.html`; every page's
  `<!-- NAV:START/END -->` and `<!-- FOOTER:START/END -->` regions are stamped via
  `python3 scripts/build_nav.py`, never hand-edited directly.
- No neighbor / private-third-party names anywhere (checked during planning: the source report
  uses only generic "a neighbor's house" language and named public entities — Arrigoni Bridge,
  Brownstone Park, CT DEEP, NWS, Portland town government — all already established as fine to
  name).
- **Task-code substitution (this phase's verbatim-policy exception):** every internal phase-file
  reference (R2, R3, R8, R16, R17, R19, S5, D1, D3, D4, D5, C4, C5, and bare "Phase 4" labels) is
  replaced with plain language describing the same task, exactly as spelled out per-instance in
  Task 2 below. Every other word of `sector-analysis-report.md`'s prose is preserved as closely
  as sense allows — this is a targeted substitution, not a rewrite.
- **Additional adaptation (discovered during planning, extending the spec's intent):** the source
  report also references the Figma design file and private repo file paths for its supporting
  sun-path-chart and wind-rose visualizations (e.g. "built out in Figma on the Sector Analysis
  page... offline copy at `lesson-03-site-analysis/assets/wind-roses.html`") — both inaccessible
  to a public reader. These are replaced with links to this site's own already-live pages that
  host that exact data (`sun-path-charts.html`, `wind.html`), per Task 2's exact text. This is the
  same "don't point a public reader at something they can't reach" logic behind the task-code
  rule, just not called out by name in the spec.
- Citations that were plain text in the source (with their real URL only in the report's own
  bottom `## Sources` list, which this phase drops per the spec) are converted to inline links
  using that same URL, so dropping the trailing list doesn't strand any citation. Exact link
  targets are given per-instance in Task 2. One exception: the Ice section's "1998 storm" mention
  has no matching URL in the source's own Sources list (a mismatch already present in the
  original report — the list's ice-storm link is about the 1973 storm, a different event) — leave
  that specific mention as plain text rather than linking it to the wrong event.

---

## File Structure

- **Create:** `docs/base-map.html`
- **Create:** `docs/sectors.html`
- **Modify:** `docs/_partials/nav.html` — add both links.
- **Modify:** `docs/index.html` — add both `.nav-card`s.
- Assets already staged (see above) — no asset work in this plan's tasks.

---

### Task 1: Author `docs/base-map.html`

**Files:**
- Create: `docs/base-map.html`

**Interfaces:**
- Consumes: `docs/assets/base-map-full-color.jpg` (already staged).
- Produces: a complete, valid HTML page with empty NAV/FOOTER marker regions for Task 3 to stamp.

- [ ] **Step 1: Write the file**

Create `docs/base-map.html` with exactly this content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Base Map — Lot #86</title>
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
  body { margin: 0; }
  .viz-root {
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--page); color: var(--text-primary);
    padding: 32px 20px 60px;
  }
  .wrap { max-width: 900px; margin: 0 auto; }
  h1 { font-size: 24px; font-weight: 600; margin: 0 0 6px; }
  .subhead { color: var(--text-secondary); font-size: 14px; line-height: 1.5; margin: 0 0 24px; }
  h2.section-head { font-size: 13px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted); margin: 28px 0 12px; }
  .hero { margin-bottom: 8px; }
  .hero img { width: 100%; height: auto; border-radius: 12px; border: 1px solid var(--border); display: block; }
  .hero-caption { font-size: 12.5px; color: var(--text-secondary); margin: 8px 0 0; line-height: 1.5; }
  .legend-intro { font-size: 13.5px; color: var(--text-secondary); line-height: 1.6; margin: 0 0 16px; }
  .legend-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px 20px; }
  .legend-item { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }
  .legend-code { display: inline-block; min-width: 30px; padding: 1px 6px; margin-right: 6px; background: var(--surface-1); border: 1px solid var(--border); border-radius: 5px; font-weight: 600; font-size: 11.5px; color: var(--text-primary); text-align: center; }
</style>
</head>
<body>
<!-- NAV:START -->
<!-- NAV:END -->
<div class="viz-root"><div class="wrap">
  <h1>Base Map</h1>
  <p class="subhead">The site's full-color base map — parcel boundary, structures, and vegetation, hand-drawn to scale. Every other spatial page on this site (Species Inventory, Zones &amp; Design, Sectors) works from this same layout.</p>

  <div class="hero">
    <img src="assets/base-map-full-color.jpg" alt="Full-color hand-drawn base map of the 0.43-acre parcel, showing the parcel boundary, house, outbuildings, driveway, and all vegetation, with a scale bar, north arrow, coordinates, and elevation range" width="1200" height="675">
    <p class="hero-caption">Scale 1"&nbsp;=&nbsp;20', true north at &minus;65.43&deg; from the drawing's own up direction, 41&deg;34'22.04"N 72&deg;38'03.90"W, elevation 106&ndash;114&nbsp;ft. Map created by Andrew Keser, July 2026.</p>
  </div>

  <h2 class="section-head">Map Key</h2>
  <p class="legend-intro">Letter codes label structures and utilities directly on the map; single-letter codes label vegetation type.</p>
  <div class="legend-grid">
    <div class="legend-item"><span class="legend-code">86</span>This house</div>
    <div class="legend-item"><span class="legend-code">85</span>The second house further back on the subdivided lot behind it</div>
    <div class="legend-item"><span class="legend-code">VG</span>Vegetable Garden (shed)</div>
    <div class="legend-item"><span class="legend-code">WM</span>Water Meter</div>
    <div class="legend-item"><span class="legend-code">EC</span>Electric Connection</div>
    <div class="legend-item"><span class="legend-code">WD</span>Wooden Deck</div>
    <div class="legend-item"><span class="legend-code">WW</span>Walkway (pool deck to back door)</div>
    <div class="legend-item"><span class="legend-code">SP</span>Swimming Pool</div>
    <div class="legend-item"><span class="legend-code">FP</span>Fire Pit</div>
    <div class="legend-item"><span class="legend-code">TS</span>Tool Shed</div>
    <div class="legend-item"><span class="legend-code">BO</span>Brick Oven</div>
    <div class="legend-item"><span class="legend-code">UP</span>Utility Pole</div>
    <div class="legend-item"><span class="legend-code">CC</span>Chicken Coop</div>
    <div class="legend-item"><span class="legend-code">DT</span>Deciduous Tree</div>
    <div class="legend-item"><span class="legend-code">CT</span>Coniferous Tree</div>
    <div class="legend-item"><span class="legend-code">HR</span>Hedgerow</div>
    <div class="legend-item"><span class="legend-code">SH</span>Shrub</div>
    <div class="legend-item"><span class="legend-code">P</span>Perennial</div>
  </div>
</div></div>
<!-- FOOTER:START -->
<!-- FOOTER:END -->
</body>
</html>
```

- [ ] **Step 2: Verify the file is well-formed**

Run: `python3 -c "import pathlib; s = pathlib.Path('docs/base-map.html').read_text(); print('OK - has markers and image ref:', '<!-- NAV:START -->' in s and '<!-- FOOTER:START -->' in s and 'assets/base-map-full-color.jpg' in s)"`

Expected: `OK - has markers and image ref: True`

- [ ] **Step 3: Commit**

```bash
git add docs/base-map.html docs/assets/base-map-full-color.jpg
git commit -m "Add Base Map page with full-color site plan and legend"
```

(The image asset was staged during planning but not yet committed — this step commits it
alongside the page that uses it.)

---

### Task 2: Author `docs/sectors.html`

**Files:**
- Create: `docs/sectors.html`

**Interfaces:**
- Consumes: `docs/assets/sectors-compass-diagram.jpg` (already staged).
- Produces: a complete, valid HTML page with empty NAV/FOOTER marker regions for Task 3 to stamp.

- [ ] **Step 1: Write the file**

Create `docs/sectors.html` with exactly this content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sectors — Lot #86</title>
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
  body { margin: 0; }
  .viz-root {
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--page); color: var(--text-primary);
    padding: 32px 20px 60px;
  }
  .wrap { max-width: 780px; margin: 0 auto; }
  h1 { font-size: 24px; font-weight: 600; margin: 0 0 6px; }
  .subhead { color: var(--text-secondary); font-size: 14px; line-height: 1.5; margin: 0 0 24px; }
  .hero { margin-bottom: 8px; }
  .hero img { width: 100%; height: auto; border-radius: 12px; border: 1px solid var(--border); display: block; }
  .hero-caption { font-size: 12.5px; color: var(--text-secondary); margin: 8px 0 24px; line-height: 1.5; }
  .intro p { font-size: 13.5px; color: var(--text-secondary); line-height: 1.65; margin: 0 0 14px; }
  h2.section-head { font-size: 15px; font-weight: 600; margin: 30px 0 12px; padding-top: 20px; border-top: 1px solid var(--border); }
  h2.section-head:first-of-type { border-top: none; padding-top: 0; }
  .sector-block p { font-size: 13.5px; color: var(--text-secondary); line-height: 1.65; margin: 0 0 12px; }
  .sector-block a { color: inherit; }
  table.sun-table { width: 100%; border-collapse: collapse; font-size: 12.5px; margin: 0 0 14px; }
  table.sun-table th, table.sun-table td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--grid); vertical-align: top; }
  table.sun-table th { color: var(--text-muted); font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.03em; }
  .table-scroll { overflow-x: auto; }
</style>
</head>
<body>
<!-- NAV:START -->
<!-- NAV:END -->
<div class="viz-root"><div class="wrap">
  <h1>Sectors</h1>
  <p class="subhead">Directional forces that arrive at the site from outside its boundary — sun, wind, fire, pollution, noise, crime, ice, wildlife movement — mapped and matched with a response. Distinct from zones, which organize what happens inside the site.</p>

  <div class="hero">
    <img src="assets/sectors-compass-diagram.jpg" alt="Sector Compass diagram overlaid on satellite imagery of the site and neighborhood, showing color-coded arcs for sun path, wind, noise, and wildlife-corridor sectors, with a legend" width="1400" height="787">
    <p class="hero-caption">Sun and wind arcs, noise and wildlife-corridor arrows, all rotated to true north and overlaid on real satellite imagery of the site and its neighborhood. Bearings are computed, not estimated: sun angles from the site's exact coordinates, wind from 10 years of real KHFD station data, noise and wildlife-corridor bearings from the site's exact bearing to Arrigoni Bridge (Rt 17/66, 251&deg;) and Brownstone Park (286&deg;).</p>
  </div>

  <div class="intro">
    <p>A permaculture design doesn't fight these forces; it maps where they come from, how strong and how frequent they are, and then places elements — windbreaks, buffers, corridors, defensible space — to block, filter, channel, or capture each one on purpose. This analysis walks the sector categories from the <a href="https://open.oregonstate.education/permaculture/chapter/sectors/" target="_blank" rel="noopener">OSU <i>Introduction to Permaculture</i> "Sectors" chapter</a>, plus the Solar Angle Analysis the Lesson 3 assignment requires alongside it, applied to this specific 0.43-acre site.</p>
    <p>Most of the data below is county- or state-level rather than parcel-level — normal for a residential lot this size, since national/state datasets don't resolve to individual half-acre parcels. Where that's the case, it's called out explicitly, and the regional data is used as the best available proxy.</p>
  </div>

  <h2 class="section-head">Sun / Solar</h2>
  <div class="sector-block">
    <p>Correction from an earlier draft of this report: the OSU textbook does treat solar aspect as its own later chapter, but the actual Lesson 3 assignment (Sector Compass) explicitly requires a Solar Angle Analysis as part of this deliverable — summer/winter sun angles, used later for the site cross-section's shading and solar-gain analysis. It belongs here, not deferred.</p>
    <p>Using <a href="https://www.suncalc.org/#/41.5728,-72.6344,17/2026.06.21/13:00/1/3" target="_blank" rel="noopener">SunCalc</a> (one of the three sun-path tools the assignment itself recommends) for the site's exact coordinates (41.5728&deg;N, 72.6344&deg;W):</p>
    <div class="table-scroll">
      <table class="sun-table">
        <thead><tr><th></th><th>Sunrise</th><th>Solar Noon</th><th>Sunset</th><th>Solar Noon Altitude</th><th>Daylight</th></tr></thead>
        <tbody>
          <tr><td><b>Summer solstice</b> (Jun 21)</td><td>5:16 AM, azimuth 57&deg; (ENE)</td><td>12:52 PM</td><td>8:29 PM, azimuth 303&deg; (WNW)</td><td><b>71.8&deg;</b> (near-overhead)</td><td>15h 12m</td></tr>
          <tr><td><b>Winter solstice</b> (Dec 21)</td><td>7:13 AM, azimuth 121&deg; (ESE)</td><td>11:49 AM</td><td>4:24 PM, azimuth 239&deg; (WSW)</td><td><b>25.0&deg;</b> (low, skimming the southern sky)</td><td>9h 10m</td></tr>
        </tbody>
      </table>
    </div>
    <p>Four full sun path charts (winter solstice, spring equinox, summer solstice, fall equinox — altitude vs. azimuth, hour-by-hour) are on this site's own <a href="sun-path-charts.html">Sun Path Charts</a> page.</p>
    <p>That's a 46.8&deg; swing in solar noon altitude and over 6 hours of daylight between solstices — expected for this latitude, but worth stating in numbers since it drives every shade/orientation call on the property.</p>
    <p><b>Response: Use.</b> The energy itself — seasonal sun angle — is accepted and worked with, not fought; canopy limbing and bed placement are tuned to capture available low-angle winter sun rather than blocking or intensifying it.</p>
    <p><b>Design implication:</b> the low winter sun (25&deg;) travels a short, low arc through the southern sky, so anything on the south side of a bed — a structure, an evergreen, a neighbor's house — casts a long winter shadow; any spot counted on for winter solar gain needs a genuinely clear southern sightline, not just "faces south." The near-overhead summer sun (71.8&deg;), by contrast, rises/sets far north of due east/west, so east- and west-facing beds still get real low-angle sun in early morning and evening through summer even if they're shaded at midday. Two concrete ties to the master plan: the planned pine/oak limbing raises the effective canopy line, letting more low-angle winter sun reach the ground beneath those trees — relevant if any bed ends up in their winter shadow line. The planned raised beds and new plantings, on a 0.43-acre in-town lot with houses close on both sides, mean a spot that reads as full sun in July can still be shaded by a neighbor's roofline or a deciduous tree (once leafed out, or even bare in winter) at the 25&deg; winter sun angle. Worth an on-the-ground shadow check near the December solstice specifically, not just judging placement off current summer canopy.</p>
  </div>

  <h2 class="section-head">Wind</h2>
  <div class="sector-block">
    <p>Central Connecticut sits in the mid-latitude prevailing westerlies, with a clear seasonal split: northwest-to-north winds dominate the colder months, while southwest-to-south winds predominate from roughly April through September (<a href="https://www.weather.gov/box/prevailing_winds" target="_blank" rel="noopener">NWS Boston/Norton, "Prevailing Winds"</a>).</p>
    <p>Station-level data confirms and sharpens this: 10 years (2016&ndash;2025) of hourly METAR observations from Hartford-Brainard Airport (KHFD, 16 km away — the nearest station with an actual historical record; Windfinder's own "Cromwell" spot turned out to be a forecast-model point with no real station behind it) show winter prevailing from the N (14.9% of hours), and spring, summer, and fall all prevailing from the S — most strongly in summer (23.7% of hours from S, only 21% calm). Winter is notably bimodal (both N and S show up as real petals, not just N), which the regional NWS generalization doesn't capture. Four seasonal wind roses and a monthly summary table are on this site's own <a href="wind.html">Wind</a> page.</p>
    <p><b>Response: Deflect</b> (primary), with a secondary Use. Winter NW wind is blocked via windbreak density to cut heating load; the same summer S/SW airflow deflected for pollutant-load reasons could alternately be used for passive cooling if a design element is positioned to catch it — a secondary opportunity, not the primary response.</p>
    <p><b>Design implication:</b> the site's exposed side to winter wind is the NW quadrant — this is the side to prioritize for windbreak density before mini-split/heating-load decisions (ties to the planned electrical panel upgrade that will carry that load) and is worth factoring into where the pollard willow row gets planted if it's meant to double as a windbreak rather than just a material crop and screen. Summer's SW airflow is also the same direction Middlesex County's ozone problem arrives from (see Pollutants, below) — the two sectors compound on that side of the property.</p>
  </div>

  <h2 class="section-head">Fire</h2>
  <div class="sector-block">
    <p>Connecticut's local wildfire risk is low relative to the western US — elevated humidity keeps fuel moisture stable most of the year (<a href="https://portal.ct.gov/deep/forestry/forest-fire/fire-danger-weather-and-reporting" target="_blank" rel="noopener">CT DEEP Forestry, "Fire Danger, Weather, and Reporting"</a>). That said, the risk isn't zero: in dry autumn stretches the state has seen real elevated fire weather, and in a notable November 2025 episode Connecticut and the rest of the Northeast experienced smoke transport and elevated fire danger from over 800 active wildfires in Canada, carried in on persistent northwest winds (<a href="https://www.nbcnews.com/news/us-news/150-homes-evacuated-wildfire-risk-persists-historically-dry-northeast-rcna180587" target="_blank" rel="noopener">NBC News, Nov 2025</a>).</p>
    <p><b>Response: Deflect</b> (low-intensity). Risk is low but not zero; existing low-effort fuel-reduction tasks are a passive deflection, not an active defensible-space campaign.</p>
    <p><b>Design implication:</b> low priority for defensible-space design (no need for aggressive brush-clearing setbacks the way a western-US site would), but the existing clearing tasks (deadwood/branch removal, wood-pile reorganization) already reduce accumulated dry fuel near structures, which is the practical, low-effort version of fire-sector design for a site at this risk level.</p>
  </div>

  <h2 class="section-head">Pollutants</h2>
  <div class="sector-block">
    <p>Middlesex County (Portland's county) currently carries an <a href="https://www.lung.org/research/sota/city-rankings/states/connecticut/middlesex" target="_blank" rel="noopener">F grade for ozone from the American Lung Association's <i>State of the Air</i> report</a>, averaging about 7.2 unhealthy ozone days per year — and CT DEEP anticipates Middlesex being reclassified toward "severe" nonattainment under the 2008 ozone standard. Ozone pollution is a regional transport problem, not a local point-source one — it forms from precursor pollutants carried up the Northeast corridor, arriving predominantly on the same summer SW wind identified in the Wind sector above.</p>
    <p>The site has no known active local point-source pollution: Portland's brownstone quarries (a National Historic Landmark since 2000) were an industrial pollution source historically but have been inactive for decades and are now largely a recreational/historic site, not an emissions source.</p>
    <p><b>Response: Deflect.</b> Dense planting on the SW-facing edge filters incoming ozone-precursor-laden summer air rather than doing nothing or trying to amplify airflow through that side.</p>
    <p><b>Design implication:</b> on the design's SW-facing edge, dense planting (trees/shrubs) provides some real particulate/ozone-precursor filtering, which is a reasonable added justification (not the primary one) for native tree diversity on that side of the property. Practically, this also means scheduling strenuous outdoor work for mornings on summer high-ozone days rather than midafternoon peak.</p>
  </div>

  <h2 class="section-head">Crime</h2>
  <div class="sector-block">
    <p>Portland, CT ranks in the <a href="https://www.areavibes.com/ct/safest-cities/" target="_blank" rel="noopener">98th percentile for safety among US cities and is the #2 safest city in Connecticut</a>, with a violent crime rate of roughly 1 per 1,000 residents/year and an overall <a href="https://www.city-data.com/crime/crime-Portland-Connecticut.html" target="_blank" rel="noopener">crime rate about 8x lower than the US average</a>.</p>
    <p><b>Response: Use.</b> The sector is genuinely favorable; the correct response is to accept that baseline as-is rather than over-designing security features the site doesn't need.</p>
    <p><b>Design implication:</b> essentially none needed — this sector doesn't justify security-driven design choices (defensive fencing, lighting-for-safety, sightline control against intruders). Fence and layout decisions (garden-fence removal, raised-bed fencing) can be driven entirely by function (deer, aesthetics — see Wildlife, below) rather than security.</p>
  </div>

  <h2 class="section-head">Ice</h2>
  <div class="sector-block">
    <p>The Northeast sees a major, damaging ice storm roughly every 15&ndash;25 years (most recently 2008, with the 1998 storm — ~1.5"+ accretion — being the region's worst on record, causing roughly $1B in damage). Ice accumulation of just 1/4"&ndash;1/2" is enough to snap small branches and weak limbs; 1/2"&ndash;1" takes down larger branches (<a href="https://northernwoodlands.org/outside_story/article/ice-storms" target="_blank" rel="noopener">Northern Woodlands</a>; NWS Taunton storm reports).</p>
    <p><b>Response: Deflect.</b> Proactive limbing reduces weak-limb ice-load failure risk over paths and structures before it happens.</p>
    <p><b>Design implication:</b> this is a direct, practical reinforcement of two tasks already planned — the planned pine/oak limbing and cutting back the maples aren't just about tick habitat and reuse value, they also reduce the weak-limb load that snaps first in an ice event, particularly over access paths and near structures. Worth keeping in mind when deciding which branches to prioritize removing: weak, low-angle, or overextended limbs over walkways and the shed site first.</p>
  </div>

  <h2 class="section-head">Wildlife Corridors</h2>
  <div class="sector-block">
    <p>The site sits close to the lower Connecticut River corridor, which is a significant regional habitat feature — it's documented as important stopover and breeding habitat for neo-tropical migrant songbirds and supports one of the largest concentrations of migratory waterfowl in southern New England (CT DEEP / regional habitat conservation sources). Deer are locally confirmed near Portland specifically: in fall 2017, Connecticut's <a href="https://portal.ct.gov/deep/news-releases/news-releases---2017/october/deep-reports-small-die-off-in-local-white-tailed-deer-herd" target="_blank" rel="noopener">first-ever confirmed cases of Epizootic Hemorrhagic Disease (EHDV-6) in white-tailed deer</a> began with dead deer found along a small waterbody adjacent to the Connecticut River in Portland; DEEP went on to document 50+ symptomatic deer, primarily in Middletown and Portland, with an estimated 70+ deaths along the Cromwell-to-Old-Lyme stretch of the river that year — direct evidence of an active local deer population using that corridor.</p>
    <p><b>Response: Use</b> (primary), with a targeted Deflect. The regional habitat/corridor value is embraced and leaned into; the deer-browse pressure that comes with it is selectively deflected via fencing/species choice on vulnerable new plantings rather than accepted wholesale.</p>
    <p><b>Design implication:</b> this is a genuinely favorable sector for the property's existing habitat goals (native trees/shrubs, chicken-coop and evergreen habitat cleanup) — the site can meaningfully contribute to a real regional bird/pollinator corridor, not just an isolated garden. It's also the practical reason to expect real deer browse pressure on new plantings: raised beds and any new perennials/shrubs should assume deer will test them, and fencing or species selection (deer-resistant choices, or accepting some loss during establishment — consistent with the phased-planting approach already preferred for this project) should account for that from the start rather than being a reactive fix later.</p>
  </div>

  <h2 class="section-head">Noise</h2>
  <div class="sector-block">
    <p>Two real, verifiable noise sources sit within the town's small footprint. The Arrigoni Bridge carries <a href="https://en.wikipedia.org/wiki/Connecticut_Route_17" target="_blank" rel="noopener">CT Route 17</a>/<a href="https://en.wikipedia.org/wiki/Connecticut_Route_66" target="_blank" rel="noopener">Route 66</a> across the Connecticut River into Portland, becoming a four-lane road before splitting into Marlborough Street and Gospel Lane — a real traffic corridor, though not a highway-scale one. More distinctively, the former brownstone quarries (161 Brownstone Ave) are now <a href="https://brownstonepark.com/park-rules-faq/" target="_blank" rel="noopener">Brownstone Exploration &amp; Discovery Park</a>, an active outdoor adventure park running its own sound system across the site for water sports, cliff jumping, and group activities in-season. It's in the same small town as the site — Portland's built-up area is compact — though the exact distance from Freestone Avenue wasn't confirmed. The <a href="https://en.wikipedia.org/wiki/Middletown%E2%80%93Portland_railroad_bridge" target="_blank" rel="noopener">Providence &amp; Worcester Railroad also runs an active freight line across the Middletown–Portland railroad bridge</a> — freight, not passenger, so infrequent rather than a steady background source. General aviation airports (Goodspeed in East Haddam, Skylark in East Windsor) are both several miles out and not a meaningful factor here.</p>
    <p><b>Response: Deflect.</b> None of this rises to a dominant sector — no major highway, no passenger rail, no nearby airport — but it's enough to be a mild, real deflect case rather than a non-issue.</p>
    <p><b>Design implication:</b> the plantings already justified for wind and pollutant buffering (the pollard willow row, native tree/shrub diversity) can pull double duty as sound buffering on whichever site edge faces the Route 17/66 corridor or town center, without adding a dedicated noise-buffer planting scheme.</p>
  </div>

  <h2 class="section-head">Views</h2>
  <div class="sector-block">
    <p>Portland sits in the lower Connecticut River Valley, with the <a href="https://en.wikipedia.org/wiki/Portland_(CDP),_Connecticut" target="_blank" rel="noopener">Portland CDP</a> bordered by the river to the west and south and a <a href="https://en.wikipedia.org/wiki/Portland,_Connecticut" target="_blank" rel="noopener">town elevation around 157 ft (52 m)</a> — modest relief, not dramatic topography. That's regional context, not parcel-specific fact: nothing in available mapping data confirms whether this site itself has a genuine river sightline, is screened by neighboring structures or tree canopy, or sits on a lot with any real topographic distinction. Consistent with how this report treats other parcel-scale unknowns, that's flagged here rather than guessed at — it needs an on-the-ground check, ideally at both leaf-on and leaf-off, before it factors into design. What the Sun/Solar sector already established with more confidence is directly relevant here too: houses sit close on both sides of this 0.43-acre in-town lot, which makes privacy the more defensible design driver until a real view line is confirmed.</p>
    <p><b>Response: Deflect</b> (pending on-site confirmation). Close neighbor proximity is the confirmed, defensible constraint; a genuine view line hasn't been confirmed yet, so it can't be labeled Use in good faith.</p>
    <p><b>Design implication:</b> default to treating close neighbor proximity as the operating constraint and let any screening/hedge plantings serve double duty as privacy buffers on the sides facing neighboring houses. If an on-site check during the Design phase (the planned pine/oak limbing, which already opens sightlines while raising the canopy line, is a natural moment to look) turns up a genuine river or landscape view, that specific sightline shifts to Use — worth keeping open rather than screened.</p>
  </div>

  <h2 class="section-head">Human / Social</h2>
  <div class="sector-block">
    <p>Two real regulatory threads matter for this design, both confirmed to exist though not fully verified in detail. First, <a href="https://portal.ct.gov/DOAG/Commissioner/Commissioner/The-Right-to-Farm-Law" target="_blank" rel="noopener">Connecticut's Right to Farm Act</a> (Conn. Gen. Stat. &sect; 19a-341) protects generally-accepted agricultural practices — including livestock noise, odor, and normal farm equipment use — from being treated as a nuisance, provided the operation follows accepted practices. That's a real statewide baseline protection once local rules are met. Second, Portland's own municipal code has a dedicated <a href="https://library.municode.com/ct/portland/codes/code_of_ordinances?nodeId=PTIICOOR_CH5AN" target="_blank" rel="noopener">Animals chapter</a> governing exactly this — confirmed to exist, but its page blocked automated fetching, so the specific numbers (minimum lot size, coop setbacks, flock size caps, rooster restrictions — Connecticut towns commonly ban or restrict roosters in residential zones) weren't retrievable and shouldn't be assumed. No HOA turned up in searches for this address or street, consistent with an older, established CT residential neighborhood rather than a planned community with deed restrictions — but that's an absence-of-evidence finding, not a confirmed absence.</p>
    <p><b>Response: Use.</b> Work within the existing regulatory environment (Right to Farm Act, Portland's animal ordinance) rather than around it — verify and comply, then rely on the statutory protection it provides.</p>
    <p><b>Design implication:</b> this directly gates the planned chicken coop / evergreen habitat cleanup — before finalizing coop placement, flock size, or committing design effort to that task, confirm Portland's actual chicken/livestock ordinance (lot-size minimum, setback from property lines, flock cap, rooster restriction) directly with the Town's Planning &amp; Zoning Department or a verified read of Municode Chapter 5, rather than assuming a generic CT small-town allowance applies as-is. Once locally compliant, the Right to Farm Act is a genuine protective backstop against neighbor nuisance complaints down the line.</p>
  </div>
</div></div>
<!-- FOOTER:START -->
<!-- FOOTER:END -->
</body>
</html>
```

- [ ] **Step 2: Verify the file is well-formed**

Run: `python3 -c "import pathlib; s = pathlib.Path('docs/sectors.html').read_text(); import re; codes = re.findall(r'\bR\d+\b|\bD\d+\b|\bS\d+\b|\bC\d+\b', s); print('OK - no task codes:', codes == []); print('OK - has markers and image ref:', '<!-- NAV:START -->' in s and '<!-- FOOTER:START -->' in s and 'assets/sectors-compass-diagram.jpg' in s)"`

Expected: `OK - no task codes: True` and `OK - has markers and image ref: True`

- [ ] **Step 3: Commit**

```bash
git add docs/sectors.html docs/assets/sectors-compass-diagram.jpg
git commit -m "Add Sectors page with compass diagram and 10-sector analysis"
```

---

### Task 3: Site integration — nav links, Home cards, stamp partials

**Files:**
- Modify: `docs/_partials/nav.html`
- Modify: `docs/index.html`
- Run (no file created): `scripts/build_nav.py`

**Interfaces:**
- Consumes: `docs/base-map.html` and `docs/sectors.html` from Tasks 1-2 (must exist with empty
  NAV/FOOTER markers before running `build_nav.py`).
- Produces: every page in `docs/*.html` with the updated nav bar (two new links) stamped into
  its `<!-- NAV:START/END -->` region, and the two new pages additionally getting the footer
  stamped into their `<!-- FOOTER:START/END -->` regions.

- [ ] **Step 1: Add the nav links**

In `docs/_partials/nav.html`, change:

```html
    <a href="zones-design.html">Zones &amp; Design</a>
  </div>
```

to:

```html
    <a href="zones-design.html">Zones &amp; Design</a>
    <a href="base-map.html">Base Map</a>
    <a href="sectors.html">Sectors</a>
  </div>
```

- [ ] **Step 2: Add the Home page cards**

In `docs/index.html`, change:

```html
      <a class="nav-card" href="zones-design.html">
        <h3>Zones &amp; Design</h3>
        <p>Current permaculture zones, microclimates, and the design brainstorm for their future.</p>
      </a>
    </div>
```

to:

```html
      <a class="nav-card" href="zones-design.html">
        <h3>Zones &amp; Design</h3>
        <p>Current permaculture zones, microclimates, and the design brainstorm for their future.</p>
      </a>
      <a class="nav-card" href="base-map.html">
        <h3>Base Map</h3>
        <p>The full-color hand-drawn site plan every other spatial page works from, with a legend.</p>
      </a>
      <a class="nav-card" href="sectors.html">
        <h3>Sectors</h3>
        <p>Sun, wind, fire, noise, and other outside forces mapped and matched with a design response.</p>
      </a>
    </div>
```

- [ ] **Step 3: Stamp nav/footer across every page**

Run: `python3 scripts/build_nav.py`

Expected: output lists every `docs/*.html` file as updated (nav changed on all of them because
`nav.html` changed), including `docs/base-map.html` and `docs/sectors.html` gaining both their
nav bar and footer for the first time.

- [ ] **Step 4: Verify no root-absolute links were introduced**

Run: `grep -rn 'href="/' docs/ ; grep -rn 'src="/' docs/`

Expected: no output (empty) from both.

- [ ] **Step 5: Run the existing script test suite (regression check)**

Run: `python3 -m pytest scripts/tests/ -q`

Expected: `16 passed` (this task doesn't touch the scripts, this just confirms nothing broke).

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "Wire Base Map and Sectors into site nav and Home page"
```

(Using `git add -A` here, not a specific file list — Step 3's `build_nav.py` run touches every
`docs/*.html` file, not just the ones this task's steps named directly.)

---

## Final Verification (after all 3 tasks)

- [ ] `grep -rn 'href="/' docs/` → empty
- [ ] `grep -rn 'src="/' docs/` → empty
- [ ] `python3 -m pytest scripts/tests/ -q` → `16 passed`
- [ ] `python3 scripts/build_nav.py` → `0 file(s) updated` (idempotent — Task 3 already stamped
  everything, so a second run should be a no-op)
- [ ] No task codes (R\d+, D\d+, S\d+, C\d+) anywhere in `docs/sectors.html`
- [ ] Manually confirm in a browser (or via `curl` after push) that both new pages render with a
  nav bar, footer, and their hero image in both light and dark mode, and that Home's two new
  cards and the nav's two new links both work.
