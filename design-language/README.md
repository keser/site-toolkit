# Design language

One visual system for maps, diagrams, slides, and report pages.

## Source of truth: Figma
The system lives in Figma, not in this repo. This folder documents it and keeps the history of
how it was built.

- Maps and keys: Site Toolkit Design Language (design file; named PDC Pro Vision until
  2026-10-15, which is the name older specs and plans use) —
  https://www.figma.com/design/aF9SVeTLwFN8PCEiU2OSBQ/Site-Toolkit-Design-Language
- Slides: AKeser-PDCPro-26-Course-Template —
  https://www.figma.com/slides/4HO6wuq75jFhX7OuMpqPNs/AKeser-PDCPro-26-Course-Template?node-id=2463-5803

Both files are course-named and were built for course deliverables. The map system and slide
template are intended to be generalized into library files that any site file can consume.
That hasn't been done yet.

## File layout (since 2026-10-20)
Pages, in order. Every page's content sits in labeled sections that use the `doc-header`,
`doc-title`, and `doc-section-label` components from Components > Documentation.

1. **Cover:** title, Andrew Keser, andrewkeser.com, Highlands Land Systems Design.
2. **Styles:** one section per doc: color ramps, color roles, fill styles, stroke, typography,
   charts, species, sheet & map display.
3. **Components:** Documentation, Map keys & legends, Map samples, Base map symbols, Lot 86.
4. **Map Set – Lot 86:** Template, Regional & overlay, Property – current, Property – proposed,
   Course maps – remove after PDC.
5. **Data Visualizations:** Sun, Wind, Climate, Water, Flood, Elevation, Species.
6. **Mood Board**, 7. **Permaculture Resources**, 8. **Assets** (images, textures, patterns).

The earlier per-topic pages (Keys and its style Inventory, Base Map, Solar Paths, Elevation,
Sector Analysis, Water & Watershed, Soil, Species, Site Data Visualizations) are preserved in
the Figma version "Before reorganization: style inventory and per-map pages". Older specs and
plans refer to those pages by name.

## Pieces
- **Map system:** "Map Overlay" color variables (aliased to a "Ramps" primitive collection), Shade/Base/Tint
  variables, fill styles, stroke weights, dash patterns, marker shapes, and key, legend, and
  sample components on the Components page. History: `specs/2026-09-28-map-design-system-design.md` and
  `specs/2026-10-10-map-tokens-v2-design.md`, with matching plans in `plans/`.
- **Charts:** "Chart Semantic" and "Chart Neutral" collections, mirrored for the microsite in
  `docs/assets/chart-tokens.css` and checked by `tools/check_chart_tokens.py`. History:
  `specs/2026-10-14-chart-tokens-design.md` and its plan.
- **Map Semantic:** single-mode aliases to the Ramps for the map color scales that rasters and keys
  share: `sun/*` (sun hours, roof solar), `vigor/*` (vegetation index), `terrain/*` (elevation tint,
  contours). Mirrored in `tokens/map.json`; Python renders read it through `tools/tokens.py`, so a
  raster and its key can't drift. History: `plans/2026-10-24-map-semantic-tokens.md`.
- **Microsite:** the `.viz-root` pattern (light/dark aware, inline SVG, self-contained pages).
  See `microsite-patterns.md`.

## Known gap
The microsite's CSS variables (`--surface-1`, `--accent`, …) don't yet match the map tokens.
Plan: aim both at one tokens file when the microsite is aligned to the map styles. Not built yet.

## specs/ and plans/
Historical design docs and implementation plans from the demo site's build. They are records,
not instructions: they mention the original repo, the course, and the demo property by name.
