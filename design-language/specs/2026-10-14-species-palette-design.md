# Species palette: status, layer and function maps

**Date:** 2026-10-14
**Status:** Design approved in chat 2026-10-14; spec awaiting review.
**Scope:** personal project, so there's latitude to be opinionated.
**Deadline:** Lesson 07.

## Goal

Lesson 07 needs three species maps of the demo site, each answering one question:

1. **Status:** which plants are native, naturalized, cultivated, or invasive?
2. **Layer:** which forest-garden layer does each plant occupy?
3. **Function:** what does each plant do for the system?

Each meaning should keep one color everywhere it appears: the maps, the species charts, and the
microsite's status pills. PDC Pro Vision is the source of truth, as it is for the map and chart
tokens.

## Where this sits

This is the first of four sub-projects Andrew sequenced on 2026-10-14:

1. **Species palette (this spec)** — first, because Lesson 07 is due.
2. Regional map style — key, footer, color rules, and `map-scale` variants for the aerial-based
   regional maps (watersheds, bioregion, hardiness zones). Its own spec.
3. Re-point every slide map or drawing that uses the legend to the PDC Pro Vision library.
4. Base map cleanup — last; Andrew does it himself after Lesson 07.

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

`Species` is a new collection in PDC Pro Vision.

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

- **Page:** a new `Species` page in PDC Pro Vision, matching the topic pages Andrew set up.
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

Nothing yet.
