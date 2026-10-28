---
paths:
  - "docs/**"
---

# Microsite conventions (docs/)

Moved from the root CLAUDE.md (2026-10-27) so it loads only when working on the microsite.

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
  collections in the Site Design Toolkit Figma library (named Site Toolkit Design Language until
  2026-10-25, and PDC Pro Vision before that); the spec
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
- **Three-part structure** (decided 2026-10-25; spec `design-language/specs/2026-10-25-profile-synthesis-proposal-design.md`).
  The audience is designers and engineers proposing work for the owner, so write for them, not a
  course rubric. Nav groups pages as Current state, Synthesis (`synthesis.html`), and Proposal
  (`project-plan.html`).
  Each current-state page ends with a `#findings` block ("Findings for design", `.fd-*` classes,
  inside the page's `.wrap`) sorted as strengths, weaknesses, opportunities, threats. Only write
  findings the page's own content supports; an empty quadrant reads "None identified yet."
  `synthesis.html` rolls up the strongest findings and links each one back to its page.
- Anchor contracts: `sectors.html` links to `sun-solar.html#sun-path-charts` and `climate.html#wind`;
  `synthesis.html` links to each page's `#findings` and to `sectors.html#views`, `#social`,
  `water.html#water-balance`, `#flow-schematic`, `sun-solar.html#sun-path-3d`, `zones-design.html#brainstorm`.
- Demo tasks page (`project-plan.html`) is a hand-ported snapshot of the demo site's task data.
  It is the Proposal part for this lot; on a client site it becomes a design brief with phases.
