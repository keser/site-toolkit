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
  canopy height), `tokens.py` (token colors for raster renders, resolved through the Ramps), and `tests/` (run `python3 -m pytest tools`).
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
  (do not prefix): `--surface-1 --page --text-primary --text-secondary --text-muted --grid
  --baseline --border --badge-bg --accent`, every `--chart-*` token, `.viz-root .wrap .subhead
  .badge-row .badge .panel .panel-title .panel-sub svg.chart .tooltip .data-table`, and the
  `.chart-title .chart-label .chart-value .chart-note` classes.
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
- Anchor contracts: `sectors.html` links to `sun-solar.html#sun-path-charts` and `climate.html#wind`.
- Demo tasks page (`project-plan.html`) is a hand-ported snapshot of the demo site's task data.

## Working rules
- Sections first, tools later (see README, "How work flows"). Once a lesson has worked on a real
  site, add its structure to `template/`: headings, questions, data to collect. Generalize tools and
  pages only when a second site actually needs them.
- Reusable tools take a site as input. No site-specific values in shared code.
- Never distinguish meaning by color alone.
