# Design language

One visual system for maps, diagrams, slides, and report pages.

## Source of truth: Figma
The system lives in Figma, not in this repo. This folder documents it and keeps the history of
how it was built.

- **Library:** Site Design Toolkit (named Site Toolkit Design Language until 2026-10-25, and
  PDC Pro Vision until 2026-10-15; older specs and plans use those names) —
  https://www.figma.com/design/aF9SVeTLwFN8PCEiU2OSBQ/Site-Design-Toolkit
- **Site files**, one per site, using the library. The demo site's is Lot 86 – Site Plan —
  https://www.figma.com/design/iFt6im4itRdGt8UJ44GHyc/Lot-86-%E2%80%93-Site-Plan
- Slides: AKeser-PDCPro-26-Course-Template —
  https://www.figma.com/slides/4HO6wuq75jFhX7OuMpqPNs/AKeser-PDCPro-26-Course-Template?node-id=2463-5803

The slide template is still course-named; generalizing it is a separate job. The library/site
split is recorded in `specs/2026-10-25-figma-library-split-design.md`.

## File layout (since 2026-10-25)
Every page's content sits in labeled sections that use the `doc-header`, `doc-title`,
`doc-section-label`, and `doc-toc-item` components from Components > Documentation. Every page
after the Cover opens with a `Contents` section: a linked list of its sections. Each Cover has a
`Pages` frame beside it that links to every page.

**Library**, pages in order:

1. **Cover:** title, Andrew Keser, andrewkeser.com, Highlands Land Systems Design, the `Pages`
   frame, and Permaculture resources, which frame what the tools are for.
2. **Styles:** one section per collection: color ramps, color roles, fill styles, stroke,
   typography, charts, species, sheet & map display, map semantic, page. Every color token's label
   shows its CSS name (its Figma code syntax). Swatches are bound to the variables; captions are
   static text, so update them by hand when a collection changes.
3. **Components:** Documentation, Map keys & legends (placeholder text), Map samples, Base map
   symbols, and the Sheet template (`00`) that new sheets start from.
4. **Demo – Lot 86:** dated image exports of finished Lot 86 sheets and charts, linking to the
   site file.
5. **Assets:** patterns.

**Site file** (Lot 86 – Site Plan), pages in order: Cover, Components (the site's base map,
site-legend, and sector diagram), Map Set (Regional & overlay, Property – current, Property –
proposed; each sheet is a component), Data Visualizations (Sun, Wind, Climate, Water, Flood,
Elevation, Species), Inspiration, Assets (site imagery and textures), and Course (deleted after the
course ends).

The 2026-10-20 single-file layout is in the library's version history, saved before the split.
The earlier per-topic pages (Keys and its style Inventory, Base Map, Solar Paths, Elevation,
Sector Analysis, Water & Watershed, Soil, Species, Site Data Visualizations) are preserved in
the Figma version "Before reorganization: style inventory and per-map pages". Older specs and
plans refer to those pages by name.

## Pieces
Every color variable aliases a **Ramps** primitive; no other collection holds a raw value.

- **Ramps:** ten hues of nine steps (50 → 800), plus charcoal/900, neutral white and black, and
  translucent `alpha/<hue>-<step>-<percent>` copies. Figma can't alias a color and change its
  alpha, so each alpha entry copies its base step; the check below fails if one drifts.
- **Color Roles and fill styles:** each hue's Tint, Base, and Shade, plus Tint at 50% and 25%. The
  50 paint styles all bind these. History: `specs/2026-09-28-map-design-system-design.md`,
  `specs/2026-10-10-map-tokens-v2-design.md`, and `specs/2026-10-11-map-tokens-v3-design.md`.
- **Charts:** Chart Semantic, Chart Neutral, and Chart Categorical, Light and Dark. History:
  `specs/2026-10-14-chart-tokens-design.md`.
- **Species:** native, naturalized, cultivated, and invasive status colors, plus plant layers.
  History: `specs/2026-10-14-species-palette-design.md`.
- **Map Semantic:** one-mode color scales that a raster and its key share: `sun/*`, `vigor/*`,
  `terrain/*`. History: `plans/2026-10-24-map-semantic-tokens.md`.
- **Page:** microsite chrome and status chips, Light and Dark. Amber is the accent. History:
  `specs/2026-10-25-page-tokens-design.md`.
- **Sheet, Map display, Stroke:** map sheet canvas, panels, text, and marks (Light and Dark); the
  plant-label toggle; stroke weights xs to 2xl.

### Where the code reads them
`tokens/` holds each collection as Ramps steps per mode (`ramps.json`, `chart.json`,
`species.json`, `map.json`, `page.json`). Two consumers read them:

1. **The microsite.** `docs/assets/page-tokens.css` (on `:root`) and `chart-tokens.css` (on
   `.viz-root`) are hand-kept mirrors. `tools/check_chart_tokens.py tokens` resolves every
   variable through `ramps.json` and fails on drift, on a page missing a stylesheet, and on any
   `var()` a page uses that nothing defines.
2. **Python renders.** `tools/tokens.py` returns a token's color, so a raster and its key can't
   drift. `tools/palette_check.py` validates the palette itself.

After any Figma color change, update the matching JSON and CSS and run both checks.

### Microsite
The `.viz-root` pattern (light/dark aware, inline SVG, self-contained pages). See
`microsite-patterns.md`.

## specs/ and plans/
Historical design docs and implementation plans from the demo site's build. They are records,
not instructions: they mention the original repo, the course, and the demo property by name.
