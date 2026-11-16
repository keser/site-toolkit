# Toolkit usage audit (after Lesson 9)

Date: 2026-11-15. Scope mode: personal project, opinionated. Read-only audit of how the Site
Design Toolkit library is applied in the Lot 86 site file, the PDC deck (last 70 slides) and the
microsite. Outcome: the toolkit floor in `2026-10-15-map-sheet-design.md` ("Toolkit floor") and
the Phase 0 sweep below.

## What holds up
- Every color variable aliases a Ramps step; the JSON mirrors and `check_chart_tokens.py` catch drift.
- Current sheets (`NNa`): 440 paints bind `Sheet`, and nearly every text node has a style.
- All 59 sheet borders bind `Sheet / panel/border` at 6 px.
- The site file has no local styles or variables.

## Findings

### Property – proposed (Lesson 9 concept sheets)
- Raw paints: 32b 28 of 69 fills and 25 of 110 strokes; 34b 14 of 18 fills; 36b 18 of 22 strokes.
  Values are Figma defaults (`#262626`, `#e6e6e6`, `#d9d9d9`) and translucent hues that match no
  Ramps step (`#61c3b7` at 25%, `#e748c1` at 25%).
- 24 distinct stroke weights, about 95% unbound to `Stroke`; scaled values (5.33, 10.67, 13.33)
  on detail sheets. Over 40 dash patterns.
- Template file still in use: `Pill` ×20 (the `zones` groups on 32b, 34b and their details);
  `TEMPLATE: PDC PRO / Black` and `Yellow 100` ×34 (22b's posts, gates and nursery bed, then
  copied with the rotation tunnel into 31b, 32b, 37b and details); `Custom Style / Color 1` on 14a.
- The six detail sheets replace the `content` layer with a view instance.
- All 12 concept sheets use local keys. Allowed for concept maps since 2026-11-15.

### Regional & overlay
- 449 paints bind Ramps directly. Allowed by the floor.
- 69 unstyled text nodes, including 24 in Inter 7.2.

### Site Profile
- About 700 unstyled text nodes in about 50 fractional sizes, mostly Inter. The microsite's
  charts use JetBrains Mono through four `--chart-font-*` tokens; Figma has no matching styles.
- 1,391 of 2,154 solid paints raw (65%).

### Deck (last 70 slides)
- 334 of 1,401 text nodes unstyled (Inter 16, 20, Italic 16).
- 2,129 color bindings to local `TEMPLATE: PDC PRO` collections (three duplicate copies of 18
  variables) against about 300 to the toolkit.
- 22 local text styles, including `Mono/16/Bold` three times and Caption and Label families the
  toolkit lacks.

### Library
- 33 text styles, all slide-sized. 23 are a JetBrains Mono size × weight × case grid, named by
  size. Mono line heights are `auto`.
- Inter body styles track −4% at every size, 16 px included (Inter's guidance is about −1% at
  16 px). Caps labels have 0 tracking. Body LG is 40/40.
- No tier below slide size, so the doc components use raw Inter 13/18/36.
- No spacing, radius or size variables. `Map display / plant-labels` uses `ALL_SCOPES`.

### Microsite
- Page text is `system-ui`. About 220 raw `font-size` declarations. No typography JSON, so the
  check can't see type drift.

## Phase 0 sweep log (2026-11-15)

**Property – proposed** (16 sheets) swept to the floor:
- Raw paints were bound to the nearest Ramps step when ΔE < 5. Most were exact Ramps hex pasted
  in. `#262626` → charcoal/800, `#e6e6e6` and `#d9d9d9` → charcoal/100, `#cccccc` → charcoal/200.
  Compost `#d9bf8c` → gold/100 (ΔE 12, Andrew's call).
- Template variables were rebound to toolkit targets: `Black` → neutral/Black, `Neutral 500`
  (an alias of charcoal/800) → charcoal/800.
- `Pill` ×8 → toolkit `caption` (Black, LG). Their template main component no longer resolved,
  so they rendered empty.
- Stroke weights were bound to `Stroke`. Detail sheets use Option A (Andrew): each stroke takes
  its overview counterpart's token, matched by layer path, so a token means the same width on
  every sheet. Dot rows are exempt.
- Raw JetBrains Mono Bold 16 labels → `Mono/16/Bold`.

**Library:**
- New `alpha/violet-500-25` and `alpha/white-85`.
- `caption` fills and text bound (the White style uses `alpha/white-85`). `roof-panel` strokes
  bound.

**Base-map symbols** default to grayscale (see the base-map component spec, amended 2026-11-15).

**Deck** (Option A, Andrew): 5,454 template-neutral bindings on all 269 slides were rebound to
Ramps: `Neutral 500` → charcoal/800, `Neutral 400` → charcoal/700, `Neutral 50` (cream) →
charcoal/50 (nearest, ΔE 2.9; pure white is the alternative), White and Black → neutral, `Accent 2`
→ sage/50. The template values were not aliases, so submitted slides shift by up to ΔE 5.1.
**Left for Phase 2:** the template accents, about 740 bindings (`Green 100` ×402, `Blue 100` ×300,
Yellow, Red, Green 500, Magenta). Retire them, or graduate them as slide accents. The three
duplicate `TEMPLATE: PDC PRO` collections stay until then.

**Finding:** a fill bound to a variable doesn't keep a manual paint opacity; it reads back at
100%. Any translucent color needs an `alpha/*` copy. This settles the Phase 1 alpha question.

**Gotcha:** instances inside a hidden frame don't load their children through the Plugin API.
Edit a clone in a visible frame, then move it in.

## Plan (Andrew, 2026-11-15)
Maps and slides first; the microsite and charts align later.

- **Phase 0 (now):** write the floor; sweep Property – proposed to it (one sheet first, with a
  mapping table approved before any change); rebind the deck's template colors to toolkit
  variables with the same values.
- **Phase 1:** inventory reusable map views and their keys; run the graduation routine; test
  whether a variable-bound fill keeps a manual opacity before adding `alpha/*` copies; a
  form-only drawing kit (weights, dashes, markers).
- **Phase 2 (after the course):** role-based type restructure. Renames are safe now; value
  changes wait, because Canvas submissions link to live deck sections and would re-render.
- **Phase 3:** align Site Profile chart text and microsite type tokens with four shared chart roles.
