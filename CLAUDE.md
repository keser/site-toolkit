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
- **Demo images are checkerboard placeholders** (SVG, gray and white tiles) labeled with the subject
  ("Bioregion map of your project site here"). Real site imagery does not go in this repo. If a
  future demo shows real imagery, use high-resolution source images, added deliberately, never
  screenshots of slides.
- The species page uses one shared placeholder (`docs/assets/species-placeholder.svg`) and no
  remote photo URLs.

## Layout
- `docs/` — demo microsite, GitHub Pages source (`main` / `/docs`). Plain static HTML, no
  generator, no build step at serve time. Must remain `docs/` (Pages only serves root or `/docs`).
- `tools/` — `build_nav.py [site_dir]`, `port_report.py`, and `tests/` (run `python3 -m pytest tools`).
- `design-language/` — docs and history for the shared visual system. Figma is the source of truth.
  **Design-system specs and plans for the permaculture files are authored here** (decided 2026-10-13),
  not in any site repo.
- `template/` — copy into a new private repo for each site.

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
  --baseline --border --badge-bg --accent`, `.viz-root .wrap .subhead .badge-row .badge .panel
  .panel-title .panel-sub svg.chart .tooltip .data-table`.
- Anchor contracts: `sectors.html` links to `sun-solar.html#sun-path-charts` and `climate.html#wind`.
- Demo tasks page (`project-plan.html`) is a hand-ported snapshot of the demo site's task data.

## Working rules
- Abstract only after something has worked on a real site, and only when a second site needs it.
- Reusable tools take a site as input. No site-specific values in shared code.
- Never distinguish meaning by color alone.
