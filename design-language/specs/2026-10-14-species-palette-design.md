# Species palette: status, layer and function maps

**Date:** 2026-10-14
**Status:** Built 2026-10-14; all three maps filled 2026-10-15 (see **Shipped**). Plan: `design-language/plans/2026-10-14-species-palette.md`.
**Scope:** personal project, so there's latitude to be opinionated.
**Deadline:** Lesson 07.

## Goal

Lesson 07 needs three species maps of the demo site, each answering one question:

1. **Status:** which plants are native, naturalized, cultivated, or invasive?
2. **Layer:** which forest-garden layer does each plant occupy?
3. **Function:** what does each plant do for the system?

Each meaning should keep one color everywhere it appears: the maps, the species charts, and the
microsite's status pills. Site Toolkit Design Language is the source of truth, as it is for the map and chart
tokens.

## Where this sits

This is the first of four sub-projects Andrew sequenced on 2026-10-14:

1. **Species palette (this spec)** — first, because Lesson 07 is due.
2. Regional map style — key, footer, color rules, and `map-scale` variants for the aerial-based
   regional maps (watersheds, bioregion, hardiness zones). Its own spec.
3. Re-point every slide map or drawing that uses the legend to the Site Toolkit Design Language library.
4. Base map cleanup — last; Andrew does it himself after Lesson 07.

**Superseded 2026-10-15:** the property map set reorders this work: sheet template, then base map
component, then species maps. See `2026-10-15-property-map-set-audit.md`.

## What Andrew decided (2026-10-14)

- **Three maps, one per question.** Taxon group (Plantae, Insecta, …) is dropped from the maps:
  63 of 66 inventoried species are plants, so it separates almost nothing.
- **Status has four values:** Native, Naturalized, Cultivated, Invasive.
- **Drawing style:** the gray base map with the existing plant symbols, `map-key`, and
  `map-legend`, like the Zones and Water maps. Not the iNaturalist aerial.
- **Approach A:** a new `Species` variable collection, beside `Chart Semantic`, so a meaning has
  one color on maps, charts, and the microsite.
- **Plant symbols are recolored by instance override only.** The symbols are components on the
  Base Map page, which is part of Andrew's deferred cleanup, so their main components are not
  edited.
- **Plant data lives in a table in the private site repo** (`lot-86-site-plan`), not in Figma and
  not in this public repo.

## Token structure

`Species` is a new collection in Site Toolkit Design Language.

- **Modes:** `Light` and `Dark`, like the chart collections, so the microsite works in dark mode.
  The deck binds to `Light`.
- **Values:** every variable aliases a `Ramps` step.
- **Scopes:** `ALL_FILLS` and `STROKE_COLOR`.
- **Size:** 20 variables per mode.

### `status/*` — 12 variables

Each status has a Tint, Base, and Shade, so it follows the map rule: filled areas use Tint with a
Shade border; lines use Base; markers use Shade. In `Light`, each aliases the same steps as the
hue's `Color Roles` entries.

| Status | Hue | Border on maps | Rationale |
|---|---|---|---|
| `status/native/*` | sage | Solid | Belongs here; matches the existing green. |
| `status/naturalized/*` | gold | Medium dash | Arrived and stayed. |
| `status/cultivated/*` | cobalt | Fine dash | Planted on purpose. |
| `status/invasive/*` | coral | Solid, `weight/xl`, `coral/Casing` | The alert hue, the same as chart `alert`. |

The border treatment is the second cue, so status never depends on color alone.

### `layer/*` — 8 variables

Symbol shape is the primary layer cue, and color reinforces it. The five height layers are one
sage scale, taller is darker. Vine and root sit outside the height scale, so they take their own
hues.

| Token | Light | Use |
|---|---|---|
| `layer/canopy` | sage/700 | symbol fill |
| `layer/sub-canopy` | sage/600 | symbol fill |
| `layer/shrub` | sage/500 | symbol fill |
| `layer/herbaceous` | sage/300 | symbol fill |
| `layer/groundcover` | sage/200 | symbol fill |
| `layer/vine` | violet/500 | symbol fill |
| `layer/root` | amber/500 | symbol fill |
| `layer/stroke` | sage/800 | every layer symbol's stroke |

Sage has nine steps (50–800), too few for five layers to each get a Tint, Base, and Shade, so
layers get one fill step and share `layer/stroke`.

### Dark mode

`Dark` values are set during validation, using the chart-token method: start one step lighter
than `Light` for Base and Shade and one step darker for Tint, then adjust until every check
below passes. The deck never uses `Dark`.

### Validation

- **Color-vision deficiency:** simulate deuteranopia, protanopia, and tritanopia (Machado
  matrices) and require a CIELAB ΔE of at least 10 between every pair of status Base colors,
  and between adjacent layer fills, in both modes.
- **Contrast:** status Shade borders and `layer/stroke` reach 3:1 against the map's gray base
  and against the microsite surfaces (`#fcfcfb` light, `#1a1a19` dark).
- **On failure,** change the hue or step. Don't add more dash patterns to compensate.
- Record the results in this spec under **Shipped**.

## Function badges

Function isn't in the collection. A plant can have several functions, which one color can't
show, so function is shown as letters.

- Each function is a letter on a `map-site-marker` Numbered Circle, scaled down to sit beside a
  plant symbol. A plant with several functions gets a short row of badges.
- Badges are neutral: `charcoal/Shade` fill with white text. The letter carries the meaning.
- On the function map the plant symbols stay gray (no override); the badges are the subject.

| Letter | Function |
|---|---|
| N | Nitrogen fixer |
| D | Dynamic accumulator |
| P | Pollinator / insectary |
| E | Edible |
| W | Wildlife food or habitat |
| M | Medicinal |
| B | Biomass / chop-and-drop |

## The three maps

- **Page:** a new `Species` page in Site Toolkit Design Language, matching the topic pages Andrew set up.
  The species charts move there from `Site Data Visualizations`.
- **Frames:** three 1920×1080 frames, `Species – Status`, `Species – Layer`, and
  `Species – Function`, each built like the Zones map: base map, plant symbols, `map-legend`
  footer, and `map-key` in a corner.
- **Keys:** three new `map-key` variants, `Theme=Default` with `Map Type` set to
  `Species – Status`, `Species – Layer`, and `Species – Function`.
  - Status and layer rows use `map-region-sample` swatches bound to the Species tokens; status
    rows also carry their border dash.
  - Function rows use the letter badge as the swatch.
- **Overrides:** only plant-symbol instances inside these three frames are overridden. Status
  uses `status/<value>/tint` fill and `status/<value>/shade` stroke plus the dash; layer uses
  `layer/<value>` fill and `layer/stroke`.
- **Known risk:** Andrew's later base map cleanup may change the plant symbols' layer structure,
  which can reset or orphan these overrides. Re-run the apply script after the cleanup.
- **`nut tree`:** its main component isn't on any page (possibly orphaned). Check it before
  building; if it is orphaned, ask Andrew whether to restore or replace it.

## Data flow

1. **Table.** `lot-86-site-plan` gets a CSV of mapped plants with the columns `symbol_id`,
   `label`, `species`, `status`, `layer`, and `functions` (space-separated letters, for example
   `N P E`).
2. **Seed.** Seed one row per plant symbol on the Zones map: its instance ID, its symbol type, and
   a `layer` guessed from the symbol type (coniferous and deciduous tree → canopy, nut tree →
   sub-canopy, shrub and hedgerow → shrub, perennial → herbaceous). Andrew fills in `species`,
   `status`, and `functions`, and corrects `layer`.
3. **Apply.** A `use_figma` script, written in the plan, reads the table and sets the overrides
   and badges in the three frames. It reports any `symbol_id` it can't find, and any row with an
   unknown status, layer, or letter, rather than skipping silently.
4. **No new toolkit tool yet.** Per "sections first, tools later", the script becomes a reusable
   tool in `tools/` only when a second site needs it. Once the table has worked on this site, add
   its columns to `template/`.

## Microsite

`docs/species-inventory.html` is the demo site's page, so it adopts the tokens directly.

- `docs/assets/chart-tokens.css` gains `--species-status-<value>-tint|base|shade` and
  `--species-layer-*` in its light and dark blocks.
- The status pills and the native/introduced bar use those tokens.
- The page's data comes from iNaturalist, which only says native or introduced. Until the table
  supplies the finer split, "introduced" uses `--chart-neutral-label-muted` rather than guessing
  among naturalized, cultivated, and invasive.
- The taxon bars (`--group-*`) have no fixed meaning, so they move to `Chart Categorical`, the
  existing rule for series without a meaning.
- `tools/check_chart_tokens.py` checks the new tokens' hex values, and the page check covers
  `species-inventory.html`.

## Checks

- **Palette:** the validation above passes in both modes, with results recorded.
- **Figma:** in the three frames, every override is bound to a Species variable (zero raw
  paints), and each map gets a screenshot.
- **Styles page:** add a `Species Documentation` frame with each token in Light and Dark, the
  status border treatments, and the badge letters. See the memory note on re-syncing the Styles
  page.
- **Microsite:** `python3 -m pytest tools`, the token and page checks, and light and dark
  screenshots of `species-inventory.html`.

## Out of scope

- The regional map style, `map-scale` variants, and slide re-pointing (sub-projects 2 and 3).
- Editing the plant-symbol main components or anything else on the Base Map page.
- New plant symbols, for example separate vine or root symbols. Vine and root plants use the
  nearest existing symbol until the base map cleanup.
- A taxon-group map.

## Shipped

### 2026-10-14

**Palette.** Values live in `design-language/tokens/species.json` (Ramps steps per mode) and are
checked by `tools/palette_check.py` against `design-language/tokens/ramps.json`.

| Token | Light | Dark |
|---|---|---|
| `status/native/tint · base · shade` | sage/400 · **sage/600** · sage/700 | sage/500 · sage/500 · sage/400 |
| `status/naturalized/…` | gold/100 · gold/500 · gold/700 | gold/200 · gold/400 · gold/400 |
| `status/cultivated/…` | cobalt/200 · cobalt/500 · cobalt/700 | cobalt/300 · cobalt/400 · cobalt/400 |
| `status/invasive/…` | coral/200 · coral/500 · coral/700 | coral/300 · coral/400 · coral/400 |
| `layer/canopy · sub-canopy · shrub · herbaceous · groundcover` | sage/700 · 600 · 500 · 300 · **100** | sage/600 · 500 · 400 · 200 · 50 |
| `layer/vine · root · stroke` | violet/500 · amber/500 · sage/800 | violet/400 · amber/400 · sage/200 |

- **Changed from the tables above, with Andrew's approval:**
  - `status/native/base` sage/500 → sage/600. At sage/500, native and invasive had the same
    lightness and were ΔE 4.7 apart under deuteranopia. It no longer equals the `sage/Base` role.
  - `layer/groundcover` sage/200 → sage/100. Herbaceous and groundcover were ΔE 9.7 apart.
- **Dark:** Shade is step 400 for every status. The rule's first guess (one step lighter, 600)
  measured 2.5–2.8:1 on `#1a1a19`.
- **Minimums:** Light — status pairs ΔE 13.3, adjacent layers 10.4, edge contrast 8.05:1. Dark —
  11.9, 10.4, 5.26:1.

**Figma (Site Toolkit Design Language).**
- `Species` collection `VariableCollectionId:1393:12`, 20 variables, Light and Dark, all aliased
  and scoped `ALL_FILLS`, `STROKE_COLOR`.
- Styles page: `Species Documentation` (`1394:12`), right of Chart Documentation; the Styles
  section widened to 10976. Rows are in meaning order (native → invasive, canopy → root), like
  Chart Documentation, not hue order.
- `map-key` variants: `Species – Status` (`1395:899`), `Species – Layer` (`1395:973`),
  `Species – Function` (`1395:1067`). Function badges bind `charcoal/Shade`.
- `Species` page (`1396:1531`) with `Species – Status` (`1397:1531`), `Species – Layer`
  (`1397:2075`), and `Species – Function` (`1397:2664`). The species charts section (`161:142`)
  moved there from Site Data Visualizations.
- **Source map:** the gray-base Zones map, `Current Zone Map Base Map – August 2027` (`189:2269`).
  The plan named `189:2268`, which is the aerial version.
- 71 plants per frame, `plant P001`–`P071`: 15 deciduous, 18 coniferous, 1 nut tree, 12 shrub,
  2 hedgerow, 23 perennial. Their labels are species codes (BW, NS, SM, …).
- **`nut tree`:** its main component (`39:5767`) has no parent page but still renders. Andrew
  chose to keep it as is until the base map cleanup.
- **Legend:** titled per map, dated October 2026. The source Zones legend reads "current
  Microclimate map", which looks like a copy slip on that map; it was not changed.

**Plant data and apply script (private, `lot-86-site-plan`).**
- `site-plan/data/mapped-plants.csv`, seeded with 71 rows: `label` is the species code and
  position, `layer` is guessed from the symbol.
- `site-plan/data/species_maps_apply.py` prints the `use_figma` script. Re-run it after editing
  the CSV and after the base map cleanup. Two fixes beyond the plan:
  - Binding a variable resets fill opacity to 1. The plants are 50% fills, so the script restores
    each plant's opacity from the source map after binding.
  - Label text is black or white by contrast with the fill composited over white at its opacity,
    not the solid fill.
- Seed run: layer 71 applied; status and function 71 blank; no problems. Bad rows (missing ID,
  unknown status, layer, or letter) are reported and not applied.

**Microsite.**
- `chart-tokens.css` carries `--species-*` in all three blocks; `check_chart_tokens.py tokens`
  checks them against `species.json`.
- `species-inventory.html` links `chart-tokens.css` and uses the page prefix `spi`:
  - native → `--species-status-native-shade`; introduced → `--chart-neutral-label-muted`.
  - Taxon colors use Chart Categorical slots 1, 3, 4, 5. Slot 2 (sage) is skipped because sage
    means native on this page.
  - Pill and bar-label text uses `--surface-1`, so it reads in both modes (≥5.7:1).
  - The taxon bars never rendered (`.bar-fill` was an inline span); fixed with `display: block`.
  - Its gridlines, baseline, crosshair, and axis labels moved to chart tokens and the label role.

### 2026-10-15: plant data

- **Source:** the Lesson 07 plant-layers sheet in `pdc-pro-2026` (status in CT, layer, functions,
  yield, wildlife value), not iNaturalist. iNaturalist only says native or introduced and has no
  layer or function; the sheet's status vocabulary is the same four values as the map.
- **Matching:** symbol codes were decoded from the base map's plant legend and Andrew's
  corrections. Generic codes (conifer → Norway spruce unless noted) follow his rules. Plants the
  sheet lacks were set by hand. Layer is the species' mature layer, not the symbol's size.
- **Functions:** keyword rules over the sheet's Functions, Yield / uses, and Wildlife columns map
  to E, W, P, and B. No on-site plant matches N, D, or M.
- **Result:** status 55 applied, 16 blank (generic perennials and unknown shrubs); layer 71;
  function 41 plants, 64 badges. The removed hedge (P016) is hidden on the three species frames
  only. Fungi (7 plants in the sheet) are left off the layer map by Andrew's choice.
- **Badge placement:** symbols 60 px or wider get the badge row centered under their label;
  smaller ones get it alongside.
- The CSV now has a `notes` column for management history.

**Still open.**
- ~~Map key swatches are opaque, but the map's plant fills are 50%, so a symbol reads lighter on the
  map than in the key.~~ Closed for the layer map on 2026-10-15 (below). The status map stays at 50%.

### 2026-10-15: solid layer fills, layer stacking, minimum plant size

- **Problem:** at 50% fill over white, adjacent layer steps measured ΔE 4.9 (canopy–sub-canopy)
  and 4.9 (sub-canopy–shrub), under the floor of 10. Canopy and sub-canopy symbols are both
  circles, so color is the only cue between them, and on the map they read as one green.
- **Explored** (minimum ΔE over normal and CVD views, adjacent pairs canopy → herbaceous):
  - Current steps at 50%: 4.9 · 4.9 · 10.0. Fails.
  - Current steps at 75%: 7.4 · 7.7 · 15.4. Fails.
  - Wider steps (sage 800/600/400/200) at 75%: 15.0 · 15.3 · 15.0. Passes, but canopy becomes
    sage/800, the `layer/stroke` value, so the stroke would need another hue, and the key would
    still not match the map.
  - Current steps solid: 10.7 · 10.4 · 21.0. Passes with no palette change.
- **Chosen (Andrew, 2026-10-15):** solid layer fills, with no token changes. The 50% fills
  existed so overlapping crowns stayed readable; drawing order replaces that. Plants are stacked
  canopy → sub-canopy → shrub → herbaceous → groundcover → vine → root, bottom to top, so the
  understory draws over crowns. A copy of the Lot 86 boundary (`Lot 86 boundary (above plants)`)
  sits above the plants.
- **Accepted costs:** where two canopy crowns overlap, only the sage/800 stroke on sage/700 separates
  them. A tree covered by a higher layer loses its label, because labels live inside the plant
  symbols; moving labels to their own layer belongs to the base map cleanup.
- **Status map unchanged:** its tints are different hues and pass at 50%.
- **Minimum plant size:** small plants were hard to read. On all three species frames, every plant
  symbol's short side is at least 32 px; the long side keeps its length (or grows to 32), and
  center and rotation are kept. 29 plants changed (shrub dots 20 → 32, perennial pills 40×16 →
  40×32, GR strips 19×91 → 32×91). The Zones source map (`189:2269`) keeps its original sizes
  until the base map cleanup.
- **Apply script:** `species_maps_apply.py` now sets layer fills to opacity 1, picks label color
  against the solid fill, sorts plants by layer, and redraws the boundary copy on each run. Run on
  2026-10-15: status 55, layer 71, function 41 applied; no problems. Function badges were re-placed
  against the new sizes.
- **Labels on every frame:** the plant components hard-code a label color for their default fill
  (shrub and conifer labels are white), so on the gray Function map those labels were white on light
  gray. Components can't pick a label color by contrast, so the component was left alone; instead
  the script re-picks every plant's label (black or white) against its final fill on all three
  frames, including plants with no data.
- **Badge placement:** trees (short side 60 px or more) keep the badge row centered under the label.
  Smaller symbols try below, above, right, and left of the symbol and take the spot that covers the
  least of other labels and badge rows (weight 6), other symbols (1), and never the legend or key
  (20). The old rule placed every small symbol's badges to its right, crowding the north bed.
- **The 32 px minimum is enforced by the script** on every run, so the base map cleanup can't
  silently undo it.
- **Base maps:** the same 32 px minimum (short side, center and rotation kept) was applied to the
  `Vegetation` instances on both base maps, `Full Color + Detail Base Map` (`155:3976`) and the
  grayscale `Base Map North @ -65.43˚` (`168:3180`): 37 plants each, mostly 32×30 perennials and
  shrubs, plus a 23×22 shrub, three hedgerows (16–28 px thick), and three elongated perennials.
  Colors are unchanged. Andrew uses the grayscale base map far more than the color one, which was
  used once in a presentation; the color base map's palette will be revisited later.

