# Chart tokens: one palette and type for deck and microsite charts

**Date:** 2026-10-14
**Status:** Shipped 2026-10-14 (Tasks 1–9 plus a final-review fix pass, pushed at `4488966`). Parked for the repo restructure; see **Pickup** at the end. Plan: `site-plan/plans/2026-10-14-chart-tokens.md`.
**Scope:** personal project, so there's latitude to be opinionated.

## Goal

Charts in the course slide deck and on the microsite (`docs/`) should share one chart palette and
one set of chart type rules, both defined in the PDC Pro Vision library. Each place still builds
its own charts:

- The deck uses native Figma charts.
- The site uses hand-written SVG built by inline scripts.

Alignment means the same meaning gets the same color and the same text role gets the same
treatment, not pixel-identical output.

What Andrew decided (2026-10-14):

- **Alignment:** shared tokens plus chart type. There's no export step between the deck and the
  site.
- **Fonts:** the site loads JetBrains Mono for chart text only. Page text stays on the system font
  stack.
- **Delivery:** a shared stylesheet, `docs/assets/chart-tokens.css`, with values copied by hand
  from the library. The mapping table below is the check.
- **Token structure:**
  - `Chart Categorical` stays as is.
  - Two new collections: `Chart Semantic` and `Chart Neutral`.
  - Per-chart CSS variables point at the shared ones.
- **Palette:** as tabled below, including the water-use recolor and the emphasis-as-band rule.

## Where things stand

| | Microsite | Course deck | Library |
|---|---|---|---|
| Colors | Hex per chart, in prefixed CSS variables (`--wuse-*`, `--spc-series-*`), light and dark | Raw hex. Nothing is bound to variables or styles. | `Chart Categorical`: 7 slots aliasing Ramps, Light and Dark, ordered for color-vision-deficiency (CVD) safety. Nothing uses it. |
| Type | `system-ui` everywhere | JetBrains Mono, 12–21px, in the native charts | Mono, Mono Caps and Body styles; no chart roles |
| Lineage | Ported from the `pdc-pro-2026` reports | Slides 48 and 50 copy the site's sun-chart hex. Slides 96–101 were rebuilt in Figma with their own blue, `#2e59b8`. | — |

The same meanings get different colors in different charts. Winter is `#2a78d6` in the sun chart,
`#5598e7` in water use, and `#2e59b8` in the deck. Water-use summer and fall are gold `#d9a441`
and tan `#b8925f`. Those two nearly merge for deuteranopes against the orange "above baseline"
band.

Chart pages on the site:

- `sun-solar.html`: `spc`, `sp3d` and `spo`.
- `water.html`: `wuse`, `precip`, `runoff`, `wbal`, `elev`, `flow`, `storm` and `shed`.
- `climate.html`: `wind`.
- `species-inventory.html` and `zones-design.html` reference chart markup and get audited in
  phase 2.

## Token structure

The library has three chart collections. Each has `Light` and `Dark` modes, and every value
aliases a Ramps primitive.

1. **`Chart Categorical` (unchanged).** Seven ordered slots for series with no fixed meaning.
   - The earlier out-of-scope item "point Chart Categorical at Color Roles" is **closed, not
     doing it**.
   - Color Roles has a single mode, so pointing the slots there would lose the Dark variants.
     The slots already alias the Ramps.
2. **`Chart Semantic` (new).** These are recurring meanings, so a meaning keeps one color in
   every chart.
3. **`Chart Neutral` (new).** Grids, axes, reference lines and chart text.

Scopes: `ALL_FILLS` and `STROKE_COLOR` for the semantic tokens. Neutral label tokens also get
`TEXT_FILL`.

On the site, `chart-tokens.css` exposes each token as `--chart-<group>-<name>`, for example
`--chart-season-winter`. Each chart's prefixed variables become references:
`--wuse-winter: var(--chart-season-winter)`. The chart scripts and the merge-safety prefix rule in
CLAUDE.md don't change. Only the values move.

## Palette

### Chart Semantic

| Token | Light | Dark | Replaces on the site |
|---|---|---|---|
| `season/winter` | cobalt/500 | cobalt/400 | `--spc/sp3d/spo-series-winter`, `--wuse-winter` |
| `season/spring` | sage/500 | sage/400 | `…-series-spring`, `--wuse-spring` |
| `season/summer` | magenta/400 | magenta/400 | `…-series-summer`, `--wuse-summer` (gold → magenta) |
| `season/fall` | gold/400 | gold/300 | `…-series-fall`, `--wuse-fall` (tan → gold) |
| `water/rain` | cobalt/400 | cobalt/300 | `--precip-series-precip`, `--wbal-rain`, `--flow-pool`, `--shed-water`, `--storm-curve-dot` |
| `water/flow` | cobalt/600 | cobalt/400 | `--flow-flow`, `--shed-river`, `--storm-curve`, `--runoff-hard-2` |
| `water/body` | cobalt/200 | cobalt/700 | `--runoff-hard`, `--wbal-hard` |
| `land/permeable` | sage/500 | sage/400 | `--runoff-perm`, `--wbal-infil`, `--wbal-perm`, `--flow-lot-line`, `--flow-swale-old` |
| `land/ground` | charcoal/500 | charcoal/400 | `--elev-ground`, `--shed-land-line`, `--flow-struct-line` |
| `emphasis` | amber/500 | amber/400 | `--accent` in charts: `--wuse-excess-line`, `--precip-band-et-line`, `--storm-evt-line`, `--elev-divide`, `--shed-site`, `--flow-swale-new`, `--wbal-runoff` |
| `emphasis/fill` | amber/100 | amber/800 | the translucent orange bands: `--wuse-excess`, `--precip-band-et`, `--storm-evt` |
| `alert` | coral/600 | coral/300 | `--storm-rec`, `--flow-exit` |

### Chart Neutral

| Token | Light | Dark | Use |
|---|---|---|---|
| `grid` | charcoal/100 | charcoal/700 | gridlines, `--spo-hour-grid` |
| `axis` | charcoal/300 | charcoal/600 | axis lines, ticks, contours (`--flow-contour`) |
| `reference` | charcoal/600 | charcoal/300 | mean and baseline lines (`--precip-mean-line`, `--wuse-base`), nodes (`--wbal-node`) |
| `label` | charcoal/800 | charcoal/100 | chart text |
| `label/muted` | charcoal/600 | charcoal/400 | secondary chart text |
| `surface` | charcoal/50 | charcoal/800 | ground planes and fills (`--sp3d-ground`, `--shed-land`, `--flow-struct`, `--elev-ground-fill`). *Added while writing the spec, not in the chat palette. Flagged for review.* |

The table maps each site variable to a token. The phase 2 audit confirms every `--<prefix>-*`
variable is accounted for. Any leftover gets a token here or is noted as chart-specific.

### Validation

These results come from a redmean and CIELAB ΔE check of simulated deuteranopia, protanopia and
tritanopia (Machado matrices). Contrast is measured against the site's chart surfaces: `#fcfcfb`
in light and `#1a1a19` in dark. The script is in the session scratchpad and is reproducible from
the Ramps values.

- **Seasons alone:** every pair is at least ΔE 18.5 under all three deficiency types, in both
  modes. Every season meets 3:1 graphical contrast; light-mode fall is the lowest at 3.0.
- **Rejected:** the old water-use season set reaches only ΔE 5.6 between summer and fall under
  deuteranopia.
- **Ground:** making ground neutral (charcoal) instead of gold lifts the water set to at least
  ΔE 9.6 in both modes. Gold ground collided with emphasis at 5.6.
- **Dark alert:** coral/300 instead of coral/400 lifts it from 4.6 to 12.1 against spring and
  permeable.
- **Known close pair:** fall (gold) versus emphasis (amber) under deuteranopia is ΔE 5.6 in light
  and 12.1 in dark. The emphasis rule below handles it, not color.

### Rules

- **Emphasis is form, not just hue.** `emphasis` is drawn as a band (`emphasis/fill` with an
  `emphasis` edge) or as a threshold or divide line, always with a direct text label. It's never a
  plain solid series next to other series.
- **Opacity:** translucent bands on the site keep their current `rgba` alpha by using
  `color-mix(in srgb, var(--chart-emphasis) 16%, transparent)`. Or they switch to the solid
  `emphasis/fill` where nothing needs to show through. The phase 2 implementer picks per chart and
  records the choice.
- **The deck is light only.** Deck charts bind to each collection's `Light` mode.
- **No reordering of `Chart Categorical`.** Its slot order is the CVD-validated part.
- **Single series without a meaning use `Chart Categorical` slot 1 (cobalt).** This covers the
  wind chart (`--wind-fill`, `--wind-accent`) and the elevation chart's lot highlight
  (`--elev-lot`, `--elev-lot-line`). They're blue by default, not because they're water, so they
  don't take `water/*` tokens.
  - Slot 1's Light and Dark values match `water/body`'s neighbors (cobalt/500 and cobalt/400), so
    nothing visibly changes.
  - Fills use the slot color through `color-mix` at the chart's current alpha.

## Chart type

The four roles reuse existing library styles. Site sizes are about 0.6× the deck sizes, because
site charts render at roughly that scale compared with a 1920px slide. The ratios between roles
are kept.

| Role | Deck (style) | Site (class in `chart-tokens.css`) |
|---|---|---|
| Chart title | `Mono Caps/20/Bold` | `.chart-title`: JetBrains Mono 700, 13px, uppercase |
| Axis and legend labels | `Mono Caps/16/Regular` | `.chart-label`: 400, 11px, uppercase |
| Data values | `Mono/20/Bold` | `.chart-value`: 700, 13px |
| Annotations (averages, band labels) | `Mono Caps/16/Medium` | `.chart-note`: 500, 11px, uppercase |

- **Chart text color:** the `label` and `label/muted` tokens.
- **Not chart text:** intro paragraphs and source lines under a chart. On the site they're page
  body text. In the deck they're Body – SM and Body – XS.
- **Loading the font:** the site loads JetBrains Mono weights 400, 500 and 700 from Google Fonts in
  `chart-tokens.css`, using `@import` with `display=swap`. The fallback is
  `ui-monospace, SFMono-Regular, Menlo, monospace`.

## Rollout

Each phase ends with a check before the next one starts.

1. **Library (PDC Pro Vision).**
   - Create `Chart Semantic` and `Chart Neutral` with the values above, then set scopes and
     descriptions.
   - Add a Charts section to the Styles page: each token in Light and Dark, the four type roles,
     and the emphasis rule.
   - Check that every alias resolves to the tabled Ramps step. Andrew publishes.
2. **Microsite.**
   - Add `docs/assets/chart-tokens.css` and link it from the chart pages with a relative path.
   - Point every chart's prefixed variables at the shared ones.
   - Move chart text to the four classes and audit `species-inventory` and `zones-design`.
   - Check: screenshot each chart in light and dark, and confirm no prefixed variable still holds
     a raw hex value unless it's noted as chart-specific.
   - Re-run `scripts/build_nav.py` only if nav or footer markup changes, which isn't expected.
3. **Deck.**
   - Bind fills and strokes in the native charts on slides 96–101 to the library variables
     (Light mode) and move their text to the four chart styles.
   - Slides 48 and 50: recolor the season colors if they're vector shapes. If they're images,
     replace them with fresh exports from the site.
   - Check: screenshot each chart slide.
4. **Housekeeping.**
   - Close the Chart Categorical → Color Roles item in `2026-10-11-map-tokens-v3-design.md`
     (Out of scope) with a pointer here.
   - Log what shipped in this spec.

## Rulings during implementation

These four rulings came from the plan and were reviewed with it:

- **R1. Hardscape bars use `water/rain` and `water/flow`, not `water/body`.** `water/body` is
  under 3:1 contrast, so it's kept for area fills only.
- **R2. Paired shades derive with `color-mix`.** The partner shade is mixed from the base token:
  `--runoff-perm-2`, `--wbal-perm`, and the deck's permeable partner at 60% opacity.
- **R3. The flow chart's divide is `neutral/reference`.** That keeps `emphasis` for the new swale
  only.
- **R4. Some colors stay chart-specific:**
  - the polar chart's month colors
  - `--spo-hour-grid`
  - the 3D scene's object colors
  - contrast text: `--flow-num-fg`, `--runoff-on-bar`, and `--shed-on-water`
  - Colored text on a classed SVG element passes `style:"fill:…"`. A `fill` attribute loses to
    the class rule, and the check script now flags it.

The execution ledger records the rest, summarized under Shipped.

## Out of scope

- The original reports in `pdc-pro-2026`. They're a separate repo and can adopt
  `chart-tokens.css` later.
- Status pills on `project-plan.html` and `species-inventory.html`. They're page UI, not charts.
- Generating CSS from Figma variables. That was approach C, rejected as custom tooling for about
  25 tokens.
- New chart types or redesigning existing charts. Only colors and type change.

## Shipped

- **2026-10-14, Task 1:** created `Chart Semantic` (12 variables) and `Chart Neutral` (6), and
  verified every alias.
  - Scopes are `ALL_FILLS` and `STROKE_COLOR` on every token. Figma rejects `TEXT_FILL` alongside
    `ALL_FILLS`, and `ALL_FILLS` already includes text fills.
- **2026-10-14, Task 2:** added `Chart Documentation` (`1336:50`) to the Styles page.
  - Sections: Semantic and Neutral, with a Light and a Dark swatch per token (36 swatches, all
    bound, each with an explicit mode), plus Type roles and Categorical.
  - The Styles section widened to 9408.
- **2026-10-14, Tasks 3–5:**
  - `docs/assets/chart-tokens.css` and `scripts/check_chart_tokens.py` are in place.
  - `water.html` (8 charts) and `sun-solar.html` (3 charts) use the tokens and the four type
    roles. Both were checked in light and dark with headless Chrome.
  - Layout adjustments for the wider monospace caps:
    - The runoff-by-surface scale goes to 50k.
    - The flow schematic viewBox is 900 wide, with a 280-wide legend.
    - The polar compass and hour labels sit at explicit radii.
    - The precip mean label reads "mean".
  - Value labels get a halo in the surface color so reference lines don't cross them.
  - **Kept chart-specific (R4):**
    - the polar chart's 12 `monthColors`, four of which already use season tokens
    - `--spo-hour-grid`, which overlays the aerial photo
    - the 3D scene's object colors
    - contrast text: white on markers (`--flow-num-fg`), dark on the water fill
      (`--shed-on-water`)
    - dark text on bars (`--runoff-on-bar`)
  - **Known limitation:** browsers without `color-mix` drop the translucent bands.
- **2026-10-14, Task 6:** `climate.html` now uses the tokens.
  - Besides the wind chart, the temperature and precipitation charts had unprefixed variables
    the spec missed:
    - `--series-high` → Categorical 7 (coral, warm)
    - `--series-low` → Categorical 5 (teal, cool)
    - `--series-precip` → `water/rain`
  - Wind uses Categorical 1, with the fill mixed 55% into the surface color.
  - **Audit:** `zones-design.html` has no charts. `species-inventory.html` draws an observation
    site map with taxon colors (`--group-*`) and status pills.
    - It's a map, not a chart, so it's deferred, consistent with treating maps as graphics.
    - Its status pills were already out of scope.
- **2026-10-14, Task 7:** the deck's native charts on slides 96–101 are bound to the library chart
  tokens.
  - Every SOLID paint in the six frames is bound: 0 unbound, 0 text outside a frame, 0 overlapping
    text pairs.
  - Text uses the four role styles: 6 titles, 100 labels, 38 notes, 28 values.
  - **Gotcha:** `setBoundVariableForPaint` resets the paint's opacity to 1. The translucent paints
    were restored afterward:
    - bands at 12–14%
    - season bars at 92%
    - Sankey links at 30% and nodes at 95%
    - the permeable partner at 60% of those (R2)
  - Unlisted hex `#33332e`, the winter baseline, maps to neutral `reference`.
  - **Runoff slide:** the lawn row's value and area label sit inside the bar end in white (about
    4.4:1 on sage), because they ran off the chart.
  - **Elevation slide:** "Freestone Ave" now sizes to its text, so it doesn't break mid-word.
- **2026-10-14, Task 8:** the deck's sun charts use the season tokens.
  - Bound: 100 paints on slide 48 and 146 on slide 50, plus the four Sun Path Key swatch
    overrides on slide 50. All opacities were preserved.
  - Chart text:
    - Slide 50's labels use `Mono Caps/16/Regular`.
    - **Exception:** slide 48 keeps its Inter 9.5–15px text. At the role sizes its four small
      sun charts had 5 overlapping labels, so the original fonts were restored.

## Pickup (parked 2026-10-14)

**State at park:**
- **Figma:** the `Chart Semantic` and `Chart Neutral` collections are published in PDC Pro
  Vision. The Styles page has a `Chart Documentation` frame (`1336:50`). Deck slides 96–101, 48
  and 50 are bound to the tokens.
- **Microsite:** `water.html`, `sun-solar.html` and `climate.html` link
  `docs/assets/chart-tokens.css`.
- **Checks:** run all four from the repo root; all pass:

  ```bash
  python3 scripts/check_chart_tokens.py tokens
  python3 scripts/check_chart_tokens.py page docs/water.html precip runoff wbal elev flow storm shed wuse
  python3 scripts/check_chart_tokens.py page docs/sun-solar.html spc sp3d spo
  python3 scripts/check_chart_tokens.py page docs/climate.html wind series
  ```

**Restructure impact:** this matters before rebasing `restructure/home-site`.
- That branch deletes `docs/` and `scripts/`, which removes `docs/assets/chart-tokens.css`,
  `scripts/check_chart_tokens.py` and the chart edits in the three pages.
- The shared chart palette and its check belong with the public microsite, so they should move to
  `site-toolkit`, along with this spec and its plan.
- The CLAUDE.md convention ("chart colors and chart text come from `chart-tokens.css`") moves with
  them.
- Expect modify/delete conflicts on all of these during the rebase. Copy them to the toolkit first,
  then `git rm` them on the branch.

**Open follow-ups**, all from the final review's minor findings:
1. **Chart colors on page variables:**
   - Chart elements still on the page's `--accent` (flow markers, legend dots, watershed bracket)
     should move to `emphasis`.
   - Climate's `--band-frost` and `--band-frost-line` need tokens.
   - Gridlines still use the page's `--grid` and `--baseline`; switch them to `neutral/grid`.
   - The sp3d azimuth and compass labels have no class and no type role.
   - CLAUDE.md's shared-identifier list should name `--chart-*`.
2. **Check script:**
   - Catch `hsl()`, `oklch()` and named colors.
   - Make the font-role check work on unprefixed text classes (climate).
3. **`color-mix` wording:** browsers without `color-mix` render the bands black, not hidden.
   Correct the "Known limitation" line or add an `@supports` fallback.
4. **Polish:**
   - Tight spots: runoff row labels at the left edge, wind-rose "N" against "12%", polar
     "W 6PM".
   - Unit casing in value labels ("gal" next to "FT²").
   - Duplicate dark declarations in climate.

