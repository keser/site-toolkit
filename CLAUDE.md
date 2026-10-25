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
  canopy height), `tokens.py` (token colors for raster renders, resolved through the Ramps), and `tests/`.
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
  variables in a page. Amber is the accent; status colors never use it. Spec:
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

## Figma (Site Toolkit Design Language file)
- It is the upstream source for every map, key, and data visualization. Check it before using a
  slide export.
- **Two audiences for maps.** Brainstorm and practice maps are course work and live in the "Course
  maps – remove after PDC" section. A property owner gets polished sheets only: current (`NNa`) and
  proposed (`NNb`). That's a default, not a rule (the owner added the resilience brainstorm as
  `23a`). When a new map appears, ask which it is. Sheet spec:
  `design-language/specs/2026-10-15-map-sheet-design.md`.
- **Legend location field stays hidden** unless a map needs it, to limit exposure of the site's
  location.
- **The Styles page is generated documentation.** Swatches are live-bound; captions are static.
  After a Ramps, Color Roles, Species, or text-style change, re-sync it from the plans
  (`plans/2026-10-10-map-tokens-v2.md` Task 3, `plans/2026-10-11-map-tokens-v3.md` Task 5,
  `plans/2026-10-14-species-palette.md` Task 4). Edit frames in place rather than rebuilding them,
  so the owner's manual tweaks survive. Hue order in docs: magenta, coral, amber, gold, sage, teal,
  cobalt, violet, slate, charcoal, neutral.
- **Plugin API gotchas.**
  - Binding a paint to a variable resets its opacity to 1; restore it afterward.
  - JetBrains Mono has no SemiBold; use Bold.
  - Scripts see fonts installed only on the owner's machine as missing. Swap them with
    `setRangeFontName`, then bind, and skip `hasMissingFont` nodes.
  - Heavy sheets drop the MCP connection. Render one at a time, never in parallel; warming at
    960 px before 1920 px sometimes helps.

## Working rules
- The course rubric is a floor, not the scope. Track every site view and dataset that makes the
  design better.
- Sections first, tools later (see README, "How work flows"). Once a lesson has worked on a real
  site, add its structure to `template/`: headings, questions, data to collect. Generalize tools and
  pages only when a second site actually needs them.
- Reusable tools take a site as input. No site-specific values in shared code.
- Never distinguish meaning by color alone.
