# Site Profile Microsite — Base Map & Sectors Design

Status: approved, pending implementation.

## Goal

Add two new sections to the live microsite, both sourced from Figma (`PDC-Pro-Vision`,
`aF9SVeTLwFN8PCEiU2OSBQ`) rather than an existing HTML report or markdown file — this is the
first phase whose primary source is finished Figma artwork:

- **`docs/base-map.html`** — the polished, hand-drawn full-color site-plan drawing (parcel
  boundary, structures, vegetation types, all labeled), plus a plain-language legend.
- **`docs/sectors.html`** — the Sector Compass diagram (directional forces arriving at the site:
  sun, wind, noise, wildlife corridor, etc., overlaid on real aerial imagery) plus the full
  written sector-by-sector analysis from `pdc-pro-2026/lesson-03-site-analysis/work/
  sector-analysis-report.md` (10 sectors: Sun/Solar, Wind, Fire, Pollutants, Crime, Ice, Wildlife
  Corridors, Noise, Views, Human/Social).

Both are real course deliverables — not aspirational or draft content — matching the site's
established "authoritative source over illustration" standard.

## Why Figma export, not the local SVG

`sector-analysis-report.md` documents that the integrated diagram (arcs + arrows + base map,
already aligned to true north) lives in Figma; the repo's own
`lesson-03-site-analysis/assets/sector-compass-overlay.svg` is the overlay layer *alone*, in a
centered coordinate system never aligned to `docs/assets/parcel-aerial.jpg`'s pixel space.
Recreating that alignment by hand would be real, error-prone design work redoing what Andrew
already did visually in Figma — exporting the finished composite is more accurate and much
cheaper. (Same reasoning applies to the base map: it's finished artwork, not raw data to
re-derive.)

## Source assets (Figma, file `aF9SVeTLwFN8PCEiU2OSBQ`)

| Node | Frame | Use |
|---|---|---|
| `155:3976` | Full Color + Detail Base Map | `docs/base-map.html` hero image |
| `37:5426` | Legend | Reference only — decode into plain-language captions, not embedded as an image (see below) |
| `129:1019` | Sector Compass Diagram – Neighborhood Satellite Imagery - North Up | `docs/sectors.html` hero image |

Only the light-mode satellite variant ships. The Figma file also has a "[Dark]" variant of the
same frame (`155:2782`) and two other base options (Community Satellite, hand-drawn Base Map,
each also light/dark) — investigated and intentionally not used: the "dark" variant only
recolors the compass arcs, it doesn't invert or dim the aerial photo or the legend box (which
stays white-backgrounded in both), so it isn't a real dark-mode companion image. This ships as
one static image, matching every other embedded real photo on this site (`parcel-aerial.jpg`,
`site-survey-1996.jpg`, the Zones & Design photos) — none of which swap per site theme.

Export both source images at a higher resolution than the default 1024px screenshot preview
(target ~2000-2400px on the long edge) before compressing, since the base map in particular
carries small legend-code text that needs to stay legible.

## `docs/base-map.html`

- Hero image: the full-color base map (`155:3976`), compressed via `sips` per this repo's
  established recipe (resize + JPEG quality ~65-72) — but test legibility of the small on-map
  labels (VG, WM, EC, etc.) before committing to a width; this image is denser than prior
  photo embeds and may need to ship wider than the usual 1200px if compression blurs the text.
- **Legend**, decoded into a real HTML key (not just the raw Figma legend screenshot, which is
  an unfinished component-kit page with several unlabeled swatches) — built from the on-map
  codes plus what Andrew supplied for the three the legend didn't resolve:
  - VG = Vegetable Garden, WM = Water Meter, EC = Electric Connection, WD = Wooden Deck,
    WW = Walkway (pool deck to back door), SP = Swimming Pool, FP = Fire Pit,
    TS = Tool Shed, BO = Brick Oven, UP = Utility Pole, CC = Chicken Coop, CAMPER = camper.
  - Tree/planting symbols: DT = Deciduous Tree, CT = Coniferous Tree, HR = Hedgerow,
    SH = Shrub, P = Perennial.
  - The "85" / "86" building labels mark this lot (86) and the second house further back on
    the subdivided lot behind it (85) — already-documented site history (see Home page's Site
    History section); phrase generically here too, no neighbor name.
- Keep the image's own baked-in scale bar, north arrow, coordinates, elevation range, and
  "Map created by Andrew Keser, July 2026" credit as part of the image — don't recaption those.
- Short intro paragraph (new, brief) framing this as the base layer every other spatial page
  (Species Inventory, Zones & Design, Sectors) implicitly works from.

## `docs/sectors.html`

- Hero image: the Sector Compass diagram over satellite imagery (`129:1019`), same compression
  treatment.
- Intro paragraph adapted from the report's own opening (sectors = forces arriving from outside
  the site, distinct from zones which organize what happens inside) plus the bearing-sourcing
  note (sun angles from exact coordinates, wind from 10 years of real KHFD station data,
  noise/wildlife bearings computed to Arrigoni Bridge and Brownstone Park).
- One real `<h2 class="section-head">` section per sector, in the report's own order: Sun /
  Solar, Wind, Fire, Pollutants, Crime, Ice, Wildlife Corridors, Noise, Views, Human / Social.
  Each section carries, verbatim in substance (see task-code exception below):
  - The factual/data paragraph(s) for that sector.
  - A **Response** badge (Use / Deflect / Use, secondary Deflect / etc., matching the report's
    own wording per sector — don't force a binary that isn't there).
  - The **Design implication** paragraph.
- **Task-code exception to verbatim policy:** replace internal phase-file references (R3, R8,
  R16, R17, S5, D1, D3, D4, D5, C4, C5) with the plain-language description of what that task
  actually is, since a public reader has no way to resolve an opaque code — same treatment the
  Journal gives them, though this page is otherwise held to the site's normal verbatim-content
  standard (unlike the Journal, which is deliberately curated). Examples: "**R3** (limbing lower
  branches on the pines and oaks)" → "the planned pine/oak limbing"; "**R17** (raised beds and
  new plantings)" → "the planned raised beds and new plantings." Keep every other word of the
  surrounding sentence unchanged — this is a targeted substitution, not a rewrite.
- Drop the `## Sources` section's citation-link list from the page body — the report already
  hyperlinks its sources inline in the prose (e.g. "NWS Boston/Norton," "CT DEEP Forestry,"
  linked where the report links them); a trailing bibliography duplicates those links without
  adding public-facing value. (This mirrors how `progress-log.md`'s own bookkeeping isn't
  ported to the Journal — trimming a source-file section that serves the author, not the
  reader, is different from the verbatim-policy exception above, which only covers the
  task-code substitution.)
- No neighbor names anywhere in the source text (checked) — only generic "a neighbor's house"
  language and named public entities (Arrigoni Bridge, Brownstone Park, CT DEEP, NWS, Portland
  town government), all of which are already-established as fine to name per this site's
  privacy policy.

## Site integration

- Nav (`docs/_partials/nav.html`): add both new links, appended at the end in this order —
  Base Map, then Sectors (base map first since sectors are computed relative to it).
- Home (`docs/index.html`): add both as new `.nav-card`s in the "Available now" grid, same
  order, same visual weight as every other direct-content card.
- Standard boilerplate: `.viz-root` CSS pattern, `body { margin: 0; }`, title/H1 convention
  (`{Name} — Lot #86` / `<h1>{Name}</h1>`), `<!-- NAV:START/END -->` /
  `<!-- FOOTER:START/END -->` markers stamped via `python3 scripts/build_nav.py`.

## Relative links

Same bar as every prior phase: `grep -rn 'href="/' docs/` and `grep -rn 'src="/' docs/` must
both return nothing after this change.

## Out of scope (explicitly deferred)

- The Community Satellite and hand-drawn-base-map Sector Compass variants, and all dark-mode
  compass variants — investigated, not used (see above).
- The Vegetation component set (`195:1769`) and other raw Figma component-kit frames — not
  publication-ready assets, not pulled in.
- The four seasonal sun-path charts and wind-rose data the report references — already live on
  the site (`sun-path-charts.html`, `wind-roses.html` folded into `wind.html`) via a separate,
  earlier port; not re-ported here.
- The three previously-deferred site-consistency findings (hub-design unification, Home
  depth-signaling, semantic headings on the *ported* pages) — unrelated to this phase, though
  this phase's `<h2>` sections on `sectors.html` continue the semantic-heading pattern V3b
  started rather than repeating the ported-page gap.
