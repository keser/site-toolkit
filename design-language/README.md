# Design language

One visual system for maps, diagrams, slides, and report pages.

## Source of truth: Figma
The system lives in Figma, not in this repo. This folder documents it and keeps the history of
how it was built.

- Maps and keys: Site Toolkit Design Language (design file; named PDC Pro Vision until
  2026-10-15, which is the name older specs and plans use) —
  https://www.figma.com/design/aF9SVeTLwFN8PCEiU2OSBQ/Site-Toolkit-Design-Language?node-id=168-3180
- Slides: AKeser-PDCPro-26-Course-Template —
  https://www.figma.com/slides/4HO6wuq75jFhX7OuMpqPNs/AKeser-PDCPro-26-Course-Template?node-id=2463-5803

Both files are course-named and were built for course deliverables. The map system and slide
template are intended to be generalized into library files that any site file can consume.
That hasn't been done yet.

## Pieces
- **Map system:** "Map Overlay" color variables (aliased to a "Ramps" primitive collection), Shade/Base/Tint
  variables, fill styles, stroke weights, dash patterns, marker shapes, and a componentized
  Keys/Legends page. History: `specs/2026-09-28-map-design-system-design.md` and
  `specs/2026-10-10-map-tokens-v2-design.md`, with matching plans in `plans/`.
- **Charts:** "Chart Semantic" and "Chart Neutral" collections, mirrored for the microsite in
  `docs/assets/chart-tokens.css` and checked by `tools/check_chart_tokens.py`. History:
  `specs/2026-10-14-chart-tokens-design.md` and its plan.
- **Microsite:** the `.viz-root` pattern (light/dark aware, inline SVG, self-contained pages).
  See `microsite-patterns.md`.

## Known gap
The microsite's CSS variables (`--surface-1`, `--accent`, …) don't yet match the map tokens.
Plan: aim both at one tokens file when the microsite is aligned to the map styles. Not built yet.

## specs/ and plans/
Historical design docs and implementation plans from the demo site's build. They are records,
not instructions: they mention the original repo, the course, and the demo property by name.
