# site-toolkit

Public toolkit for permaculture site analysis and design: demo microsite (`docs/`), tools
(`tools/`), design language (`design-language/`), and a per-site workspace template
(`template/`). Maintained by Andrew Keser under the `keser` GitHub account; Highlands Land
Systems Design (HLSD) is referenced by name where relevant, and its own structure is not
settled.

## Privacy (public repo — be strict)
- Private by default. The demo property (Lot #86, 58 Freestone Avenue, Portland, CT) is the
  only site whose address and coordinates may appear here.
- Never add another site's address, parcel data, survey scans, photos, or household details.
- Never name neighbors or other private third parties; use roles.
- Never write a utility account number. `docs/water.html` `#water-use` has one redacted on
  purpose; if that section is re-ported from its source, strip the number again and don't quote it.
- Anything committed to a public repo is permanently public. Every file in `docs/assets/` is a
  deliberate decision to publish it.
- **The demo shows real Lot 86 imagery** (owner's decision, 2026-10-23), and only Lot 86. Images
  come from high-resolution sources, added deliberately: Figma map sheets exported at full size,
  CT ECO orthoimagery, the owner's own iNaturalist photos. Never screenshots of slides. Each image
  gets a source credit on its page. Images still missing stay checkerboard placeholders (SVG, gray
  and white tiles) labeled with the subject.
- Lot 86 images are built by `site-plan/data/microsite_assets_build.py` in the Lot 86 repo
  (parcel aerial, species photos) or exported from the Figma map sheets. Species photos live in
  `docs/assets/species/`, resized to 600 px; no remote photo URLs.

## Layout
- `docs/` — demo microsite, GitHub Pages source (`main` / `/docs`). Plain static HTML, no
  generator, no build step at serve time. Must remain `docs/` (Pages only serves root or `/docs`).
- `tools/` — `build_nav.py [site_dir]`, `port_report.py`, `fetch_ct_eco.py` (a Connecticut site's
  CT ECO imagery, lidar, and building layers into the site repo), `sun_arcs.py` (sun positions, a
  top-down sun-path projection, and a Google Earth camera model), `shade.py` (shadow masks, hours
  of direct sun, skyline profiles and roof solar access from a lidar surface), `imagery.py` (NDVI and color-infrared from 4-band imagery), `terrain.py` (hillshade, contours,
  canopy height), `fetch_s2cloudless.py` (regional Sentinel-2 imagery), `tokens.py` (token colors
  for raster renders, resolved through the Ramps), `check_chart_tokens.py` (token CSS against the
  token files, and page wiring), `palette_check.py` (palette validation), and `tests/`.
  The tools are an installable package (`pyproject.toml`, top-level modules). Locally they live in
  the shared environment `~/Code/keser/.venv`, installed editable, so site repos import them
  without path hacks. Run tests with `~/Code/keser/.venv/bin/python -m pytest`. New dependencies go in
  `pyproject.toml`.
- `design-language/` — docs and history for the shared visual system. Figma is the source of truth.
  **Design-system specs and plans for the permaculture files are authored here** (decided 2026-10-13),
  not in any site repo.
- `template/` — copy into a new private repo for each site, at `~/Code/keser/site-plans/<site-name>/`.

## Microsite conventions (docs/)
- Internal links stay **relative** (`climate.html`, not `/climate.html`): project-scoped Pages site.
- Hand-authored pages need `body { margin: 0; }` explicitly.
- Shared nav/footer: `docs/_partials/nav.html` and `footer.html` are the source of truth; pages
  carry `<!-- NAV:START -->…<!-- NAV:END -->` and `<!-- FOOTER:START -->…<!-- FOOTER:END -->` markers.
  Re-run `python3 tools/build_nav.py` after editing a partial or adding a page, before committing.
- Long-form pages (`water`, `sun-solar`, `zones-design`) are sequences of `<section class="page-section" id="…">`
  with a `.badge-row` of anchor pills. Adding a visualization: prefix every non-shared CSS
  property, class, and bare selector uniquely, and wrap scripts in an IIFE. Shared identifiers
  (do not prefix): every variable in `docs/assets/page-tokens.css` (`--surface-1 --page
  --text-* --grid --baseline --border --badge-bg --accent --status-*`), every `--chart-*` token, `.viz-root .wrap .subhead
  .badge-row .badge .panel .panel-title .panel-sub svg.chart .tooltip .data-table`, and the
  `.chart-title .chart-label .chart-value .chart-note` classes.
- **Page chrome colors come from `docs/assets/page-tokens.css`** (on `:root`, so the nav and footer
  use them too). It mirrors the Figma "Page" collection; values live in
  `design-language/tokens/page.json` as Ramps steps. Every page links it; never redefine its
  variables in a page. After renaming any variable, run `check_chart_tokens.py tokens`: it fails on
  a `var()` that nothing defines, which the browser would drop without an error. Amber is the accent; status colors never use it. Spec:
  `design-language/specs/2026-10-25-page-tokens-design.md`.
- **Chart colors and chart text come from `docs/assets/chart-tokens.css`.** It mirrors the chart
  collections in the Site Toolkit Design Language Figma library (formerly PDC Pro Vision); the spec
  is `design-language/specs/2026-10-14-chart-tokens-design.md`. Its `--chart-*` values live in
  `design-language/tokens/chart.json` (Ramps steps per mode), which the check resolves.
  A new chart's prefixed variables reference `--chart-*` tokens, not raw hex, and its SVG text uses
  `font: var(--chart-font-<role>)`. Chart fills and strokes never use the page variables
  (`--grid`, `--baseline`, `--accent`, `--text-*`); the check flags them. Run
  `python3 tools/check_chart_tokens.py page <file> <prefixes…>` before committing a chart page, and
  `python3 tools/check_chart_tokens.py tokens` after any palette change.
- **Species colors come from the `--species-*` tokens** in the same file. Their values live in
  `design-language/tokens/species.json` (Ramps steps per mode); `check_chart_tokens.py tokens`
  fails if the CSS drifts from it, and `tools/palette_check.py` validates the palette itself.
- **Map colors in the microsite come from the `--map-*` tokens** in `chart-tokens.css`, mirroring
  Map Semantic (`design-language/tokens/map.json`). One mode, so they sit in the light block only.
- **Raster renders take colors from tokens, not hex.** A build script that colors a map raster calls
  `tokens.rgb("map" | "species", name)`; the values live in `design-language/tokens/map.json` and
  `species.json`, mirroring Figma's Map Semantic and Species collections. External palettes (USDA
  zones, colors sampled from a photo) stay raw, with their source noted.
- **Three-part structure** (decided 2026-10-25; spec `design-language/specs/2026-10-25-profile-synthesis-proposal-design.md`).
  The audience is designers and engineers proposing work for the owner, so write for them, not a
  course rubric. Nav groups pages as Current state, Synthesis (`synthesis.html`), and Proposal
  (`project-plan.html`).
  Each current-state page ends with a `#findings` block ("Findings for design", `.fd-*` classes,
  inside the page's `.wrap`) sorted as strengths, weaknesses, opportunities, threats. Only write
  findings the page's own content supports; an empty quadrant reads "None identified yet."
  `synthesis.html` rolls up the strongest findings and links each one back to its page.
- Cite original data sources (NOAA, station IDs, lidar, USGS), never course lessons or private
  repo paths.
- Anchor contracts: `sectors.html` links to `sun-solar.html#sun-path-charts` and `climate.html#wind`;
  `synthesis.html` links to each page's `#findings` and to `sectors.html#views`, `#social`,
  `water.html#water-balance`, `#flow-schematic`, `sun-solar.html#sun-path-3d`, `zones-design.html#brainstorm`.
- Demo tasks page (`project-plan.html`) is a hand-ported snapshot of the demo site's task data.
  It is the Proposal part for this lot; on a client site it becomes a design brief with phases.

## Figma (library and site files)
- **Two kinds of file** (split 2026-10-25; spec `design-language/specs/2026-10-25-figma-library-split-design.md`).
  - **Site Toolkit Design Language** (`aF9SVeTLwFN8PCEiU2OSBQ`) is the published library: Cover
    (with Permaculture resources), Styles, Components, Demo – Lot 86, Assets (patterns). It holds
    no site content except the demo page, and never mentions the course.
  - **One site file per site**, which uses the library. Lot 86's is Lot 86 – Site Plan
    (`iFt6im4itRdGt8UJ44GHyc`): its maps, charts, inspiration, imagery, and course work. Its map
    sheets are components, so its decks place them live. It is the upstream source for every Lot 86
    map and chart; check it before using a slide export.
- **Demo – Lot 86 is a snapshot**: dated image exports of finished site-file work, linking to the
  site file. Refresh it on request, like the microsite's project plan page.
- **Map keys & legends ship placeholder text** ("Project site", "Name, address"). A site sheet
  overrides every row. Never type a site's details into a library component.
- **Scripts that edit a site file import library assets by key** (`importVariableByKeyAsync`,
  `importStyleByKeyAsync`, `importComponentByKeyAsync`). A site file has no local variables or
  styles, and the team-library API lists nothing for these files.
- **Two audiences for maps.** Brainstorm and practice maps are course work and live on the site
  file's Course page until the course ends. A property owner gets polished sheets only: current (`NNa`) and
  proposed (`NNb`). That's a default, not a rule (the owner added the resilience brainstorm as
  `23a`). When a new map appears, ask which it is. Sheet spec:
  `design-language/specs/2026-10-15-map-sheet-design.md`.
- **Legend location field stays hidden** unless a map needs it, to limit exposure of the site's
  location.
- **The Styles page is generated documentation.** Swatches are live-bound; captions are static.
  After a Ramps, Color Roles, Species, or text-style change, re-sync it from the plans
  (`plans/2026-10-11-map-tokens-v3.md` Task 5,
  `plans/2026-10-14-species-palette.md` Task 4). Edit frames in place rather than rebuilding them,
  so the owner's manual tweaks survive. The page is now one section per collection (Color ramps, Color roles,
  Fill styles, Stroke, Typography, Charts, Species, Sheet & map display, Map semantic, Page). To add a
  token, clone a sibling row or swatch, rebind its fills, and resize the section to fit. Give a
  translucent (alpha) swatch an explicit backing: white for Light, charcoal/900 for Dark. Hue order in docs: magenta, coral, amber, gold, sage, teal,
  cobalt, violet, slate, charcoal, neutral.
- **Navigation is generated too, in both files.** Each page (except Cover) has a `Contents` section left of its
  content: a linked list of the page's top-level sections, built from `doc-toc-item` instances
  (Components › Documentation). Each entry's summary is the first sentence
  of that section's `doc-title` body. The Cover has a `Pages` frame beside the cover with one
  linked card per page. These are snapshots: after adding, renaming, or moving a section, or
  adding a page, rebuild that page's `Contents` and the `Pages` frame. Delete the old one by name,
  then build fresh; nothing else references them.
- **Translucent colors are copies.** Figma can't alias a color and change its alpha, so each
  `alpha/<hue>-<step>-<percent>` Ramps variable copies its base step. After changing a Ramps value
  or a hue's Tint step: update the matching `alpha/*` copies in Figma (the Tint/25 and /50 fill
  styles reach them through Color Roles `<hue>/Tint/<25|50>`), mirror them in
  `design-language/tokens/ramps.json`, and run `tools/check_chart_tokens.py tokens`, which fails
  on any copy that no longer matches. Don't run map-tokens v2 Task 3; it would unbind the styles.
- **Plugin API gotchas.**
  - Binding a paint to a variable writes the variable's alpha into the paint's opacity, so an opaque
    variable resets it to 1. A translucent style binds a Color Roles variable (`<hue>/Tint/50`)
    that aliases an `alpha/*` Ramps copy.
  - JetBrains Mono has no SemiBold; use Bold.
  - Scripts see fonts installed only on the owner's machine as missing. Swap them with
    `setRangeFontName`, then bind, and skip `hasMissingFont` nodes.
  - Heavy sheets drop the MCP connection. Render one at a time, never in parallel; warming at
    960 px before 1920 px sometimes helps.
  - Don't call `setCurrentPageAsync` on an image-heavy page; it drops the connection. Use
    `page.loadAsync()` and `getNodeByIdAsync`.
  - A dropped response doesn't mean the script failed. Read the canvas before retrying.

## Working rules
- The course rubric is a floor, not the scope. Track every site view and dataset that makes the
  design better.
- Sections first, tools later (see README, "How work flows"). Once a lesson has worked on a real
  site, add its structure to `template/`: headings, questions, data to collect. Generalize tools and
  pages only when a second site actually needs them.
- Reusable tools take a site as input. No site-specific values in shared code.
- Never distinguish meaning by color alone.
