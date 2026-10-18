# Base map component: one grayscale base map for every property sheet

**Date:** 2026-10-15
**Status:** Andrew answered the four open questions on 2026-10-15 (see **Decisions**). The plant list is
settled (see **Plant list**). `Lot 86 / base map` is built (`1543:617`, Base Map page) on 2026-10-16
(see **Build notes**).
**Scope:** personal project, so there's latitude to be opinionated.
**Builds on:** `2026-10-15-map-sheet-design.md` (the sheet's `content` layer holds this component),
`2026-10-15-property-map-set-audit.md` (finding 2: four plant inventories).

## Goal

Every property sheet's `content` layer holds one instance of a single base map component. Plants,
structures, paving, and boundary are drawn once. A sheet changes only:

- **plant labels:** the `Map display` mode on the sheet frame
- **plant fills:** overrides on the instance (species maps)
- **everything drawn on top:** the sheet's `annotations` layer

This replaces 13 copies of the grayscale base map, 7 frames built from the old per-type plant
components, and the color base map's separate plant set.

## What exists

| Source | Plants | Component | Positions |
|---|---|---|---|
| Grayscale base map `168:3180` (+12 copies) | 79 | `Vegetation` (Type × Color) | Base map drawing. Labels are letter codes (A–EE), all hidden. |
| Color base map `155:3976` | 78 | `Vegetation` | Same drawing, Full Color variants |
| Species maps, Zones, Sector `[base map]` (7 frames) | 71 | old per-type components | Zones drawing, named `plant P###` |
| `mapped-plants.csv` (lot-86-site-plan) | 71 | — | IDs, species, status, layer, function for the 71 Zones-drawing plants |

## Reconciliation (measured 2026-10-15)

Plant centers were compared in frame coordinates. Pairs had to be the same type and within 45 px.

- **58 pairs.**
  - Most large trees agree within a few pixels.
  - 18 pairs are loose (16–38 px apart, or the type differs). Examples:
    - P001 black walnut vs `2701`: 48 px apart, and 200 vs 283 px wide.
    - P005 striped maple paired with a perennial.
    - P013 is a shrub that lands on a hedgerow.
- **13 CSV plants with no base map partner:**
  - P029 and P030: two Norway spruces at the bottom edge, mostly behind the legend.
  - P011, P012, P038: Norway maple shrubs and a tree, near the north spruces.
  - P014 (highbush blueberry), P008, P058, P059.
  - P050, P051, P065: hostas.
  - P001 (walnut) has no partner within 45 px.
- **21 base map plants with no CSV ID:**
  - **Trees:** `2681` (west, 120 px), `2689`, `2690`, `2691` (the three 72 px trees in the middle),
    `2701` (the big walnut), `2704` (113 px, south of the walnut).
  - **Shrubs:** `2720`, `2730`, `2732`.
  - **12 perennials:** `2693`, `2696`, `2697`, `2698`, `2699`, `2711`, `2713`, `2733`, `2735`, `2736`,
    `2739`, `2740`.

The two drawings were edited separately: the base map for most maps, the Zones drawing for the
species work. So neither is a clean superset of the other.

### Plant list (decided 2026-10-15)

Marking 92 rows against a side-by-side overlay was slower than naming species on one drawing. Andrew
chose the CSV plants instead, at their Zones drawing positions:

- **The CSV is the plant list.** Most of the 12 base-map-only perennials were approximate placeholders,
  so they're dropped.
- **Trees are the accurate part,** and most trees agree in both drawings. Of the six base-map-only
  trees:
  - The big walnut (`2701`) is dropped. P001, at 200 px, is the right size and position. It stands in
    the neighbor's yard.
  - The other five are real. They join the CSV at their base map positions and sizes:
    - P072, striped maple (`2704`), shading out the vegetable garden
    - P073 and P074, apple trees (`2691`, `2690`)
    - P075, peach tree (`2689`)
    - P076, Japanese maple (`2681`), in the neighbor's front yard
- **Shrubs:**
  - `2731` was a rough drawing of the blueberries, which are P010 and P014.
  - `2730` and `2732` were blackberries, and have been removed.
- **Species named for the 15 blanks.** Three are grapes, and they move to the vine layer:
  - P058 and P059, Catawba grapes (cultivated)
  - P067, a river grape growing wild under the dawn redwood

  P055 and P056 stay "unknown flowering perennial."
- **Removed plants stay in the CSV but off the map.** P016, the boxwood hedge, was removed in October
  2026. The base map draws the site as it is now.

The marking sheet (`base-map-reconcile.csv`) is retired. So is the overlay frame.

## Proposed component

### Name and home

`Lot 86 / base map`, in the library on the Base Map page, **published**. Slides place maps as layered,
full-screen visualizations in the same arrangement as a sheet: base layer, key, legend, and content.
The base layer is either this drawing or a background image, such as satellite, a Google Earth aerial,
or a photo. The Lot 86 legend is published too, renamed from `_site-legend / Lot 86` to
`Lot 86 / site-legend`.

Each other property's file gets its own `<Property> / base map` and `<Property> / site-legend`.

### Layers are the emphasis controls

The grayscale map is already built in named layers, and sheets already tune them. Measured 2026-10-15:

| Layer | Default | Seen on sheets |
|---|---|---|
| `Aerial_Photo` | hidden | hidden everywhere (its image is the underlay listed in `sources.md`) |
| `Contour lines` | 10% | 50% on the water flow map |
| neighboring lots (with their buildings) | 25% | 25% |
| `Lot 86` (boundary, buildings, paving, beds, utilities) | 100% | 100%; `electrical` and `water` sublayers hidden except on utility and water maps |
| `Trees & Plants` | 100% | left out of the water flow map |
| `Municipal Infrastructure` | 100% | moved above the overlay on the water map; `water` and `electrical` hidden by default |

The component keeps these as **top-level layers with stable names**, so a sheet emphasizes or quiets
a layer by overriding its opacity or visibility on the instance. Andrew sets these by eye per map, as
he does now. The spec adds two things only:

- **Standard opacity steps:** 100, 50, 25, and 10. Sheets pick from these, so like maps match.
- **Boolean toggles** for the layers that are switched on and off whole: `Show plants`,
  `Show contours`, `Show utilities` (the electrical and water sublayers), and `Show aerial`.

Turning on `Show aerial` gives an aerial base for overlay sheets without leaving the drawing. A
separate photo or satellite base still goes straight into the sheet's `content` layer instead of the
component.

### Contents, bottom to top

1. `Aerial_Photo` (hidden)
2. `Contour lines`
3. neighboring lots
4. `Lot 86`: ground, paving, beds, buildings, utilities
5. `Trees & Plants`: every plant a `Vegetation` instance named `plant P###`, ordered by layer:
   1. canopy
   2. sub-canopy
   3. shrub
   4. herbaceous
   5. groundcover
   6. vine
   7. root

   Tall plants are drawn first, so understory plants stay visible on top of them. The 32 px minimum
   short side carries over.
6. `Lot 86 boundary`: a copy of the lot line above the plants, so canopy never hides it. This
   replaces the boundary re-clone in the apply script.
7. `Municipal Infrastructure`
8. `labels`: map labels such as the street name and neighbor roles. This closes the earlier open item
   about moving labels into their own layer.

### Vegetation changes

- **Label visibility** binds to `Map display` `plant-labels`. Today every label is hidden by a
  per-instance override. Those overrides get cleared, so the variable decides.
- **Label text** is the plant ID (`P012`). The ID is the primary map label because it doubles as an
  inventory number. Species and function codes stay in the CSV, and the key lists them per ID.
  `P012` in 10 px mono is about 24 px wide, so it fits the 32 px minimum. The old letter codes
  (A–EE) are dropped.
- **Label color** follows the plant's fill. The contrast rule already in `species_maps_apply.py`
  (`textOn`) stays: species sheets override fills, so they also set label colors.
- **The color variant** (`Color=Full Color`) stays for now. The color base map is revisited later.

### How sheets use it

| Sheet | Instance overrides |
|---|---|
| Most lot sheets | none; `Map display: Labels off` |
| Species – Status / Layer / Function | plant fills and label colors (the apply script); `Labels on` |
| Succession, Thematic Design | none; draw in `annotations` |
| Garden detail | the instance is scaled up and cropped to the garden; `Labels on` |
| Water maps | `Contour lines` at 50%; `Show plants` off or plants at 25% |
| Sheets with markers and arrows | `Trees & Plants` at 25–50% so annotations stand out |

Overrides are keyed by layer name inside the instance. That's why every plant is named by ID, and
why renaming a plant later would drop its overrides on every sheet.

### Apply script

`species_maps_apply.py` changes:

- It finds plants inside the sheet's `content` → base map instance, not in a copied `site-map`
  frame.
- It writes fills and label colors as instance overrides.
- It drops the layer reorder and the boundary re-clone, because both are now in the component.
- It keeps the 32 px check, but reports violations instead of resizing. A resize has to happen in the
  component.
- Badges (function map) go into the sheet's `annotations` layer.

## Plant inventory key

Plant IDs on the map need a lookup. The set gets an **inventory sheet**, a table generated from
`mapped-plants.csv`, with these columns:

- ID
- species
- status
- layer
- function codes

There's no species-code column. The CSV's only codes are the old letter labels (`BW`, `DT`), which mix
species and symbol types.

Species sheets keep their color keys, built from `map-key-shell` rows. The inventory sheet is the
ID → species reference for every sheet with labels on. It slots into the set after the species sheets.

## Build order

1. Settle the plant list in `mapped-plants.csv` (done 2026-10-15: 76 rows).
2. Build `Lot 86 / base map` from the grayscale map:
   - replace its plants with the CSV plants, as `Vegetation` instances at their Zones positions
   - keep P072–P076 at their base map positions and sizes
   - leave out plants whose notes say `REMOVED`
   - order the plants canopy first
   - add the boundary copy and the `labels` layer
   - add the toggles
   - bind the label variable and set label text to the IDs
3. Check it against the old grayscale map with a screenshot overlay.
4. Update `species_maps_apply.py`, then move the three species maps onto sheets.
5. Build the inventory sheet.
6. Move the remaining sheets, in the set order from the sheet spec.

## Decisions (2026-10-15)

1. **The plant list and positions come from the CSV** (the Zones drawing), plus five base map trees.
   This reverses the first answer, positions from the base map, which needed a plant-by-plant
   reconciliation. See **Plant list**.
2. **Plant ID is the primary map label** (`P012`), for inventory. Species and function codes stay
   associated in the CSV. A key (the inventory sheet) maps ID to species.
3. **Published.** Slides build maps as layered full-screen visualizations from these pieces, so the
   base map and the Lot 86 legend are published library components.
4. **Layer emphasis is per sheet.** The two underlay images both sit in the hidden aerial layer. The
   real per-map difference is layer opacity (contours, plants, neighboring lots) and visibility
   (utilities, plants), which the component exposes as described in **Layers are the emphasis
   controls**.

## Build notes (2026-10-16)

`Lot 86 / base map` (`1543:617`) was built by script from the grayscale map (`168:3180`) and the CSV:

- **Plants:** 75 `Vegetation` (Grayscale) instances named `plant P###`. P016 is left off (removed).
  - The Zones drawing sits 2 px right of the base map drawing; buildings, pool, and driveway all
    measure +2 px in x. Plant positions were shifted 2 px left to match.
  - P072–P076 take their size and position from the old base map nodes.
  - Grapes use the `Perennial` shape. `Vegetation` has no vine shape yet; the layer column still
    says `vine`, which sets their draw order.
- **Labels:** `Vegetation` labels are now 10 px in all ten variants. Each plant's `Show label` is
  bound to `Map display` `plant-labels`, and its text is the plant ID. Every ID fits its symbol.
- **Layers, bottom to top:** `Aerial_Photo` (hidden), `Contour lines` (10%), `neighboring lots`,
  `Lot 86`, `Trees & Plants`, `Lot 86 boundary`, `Municipal Infrastructure`, `labels` (empty, for
  street names and neighbor roles). Neighboring lots keep their own opacities (two at 25%).
- **Toggles:** `Show plants` and `Show contours` (on), `Show utilities` (off; the `electrical` and
  `water` frames in `Lot 86` and `Municipal Infrastructure`), `Show aerial` (off).
- **Canvas fill** is copied from the old map as a raw color. It isn't bound to a variable yet.

The old grayscale map stays until every sheet uses the component.

### Species sheets (2026-10-16)

Andrew kept the CSV sizes where they differ from the old base map (P002, P004, P006, P017, P022,
P039, P040).

The three species maps are now sheets on the Map Set page, built from `00 Sheet template`:

| Sheet | Node | Key |
|---|---|---|
| `16a Species – status` | `1545:2035` | `map-key` Species – Status |
| `17a Species – layer` | `1545:2857` | `map-key` Species – Layer |
| `18a Species – function` | `1545:3506` | `map-key` Species – Function |

`species_maps_apply.py` now targets these sheets:

- It finds the plants inside the `Lot 86 / base map` instance in `content`.
- It writes fills, strokes, and label colors as overrides on each plant's shape. Every run first resets
  each plant to the `Vegetation` component's look.
- Status and layer plants are drawn at full plant opacity, as on the old maps. Status fills stay at 50%.
- It reports plants under 32 px instead of resizing them, and it reports IDs that are on the base map
  but not in the CSV.
- Badges go into `annotations`.

First run: status 73 applied (P055 and P056 have no status), layer 75, function 41 (34 have no
function codes). No problems, and no plant under 32 px.

Still the same as on the old maps: the key covers the top-left corner, including part of P001 and
P001's function badges. The old Species page frames stay until Andrew retires them.

### Plant inventory sheet (2026-10-16)

`19 Plant inventory` (`1548:2324`, Map Set page) is built by `plant_inventory_apply.py` in the Lot 86
repo, which rebuilds the table in place from the CSV:

- **Content:** one panel with the key's border and fill, holding three column groups of 25 rows. Removed
  plants aren't listed. A line under the title spells out the function codes.
- **Type:** the Mono and Mono Caps 16 px styles, with text bound to `Sheet` `text/primary` and
  `text/secondary`, so the table follows Light and Dark.
- **No key layer:** the table is the key, so the sheet drops the empty key shell.
- **Legend:** title "plant inventory", body "75 plants / not to scale". The scale bar and north arrow are
  hidden. The date is the month of the last rebuild.
- **Fit:** the panel ends at y = 879, above the legend at 940. Three long species names wrap to two
  lines. Each group has room for about two more rows, so past about 80 plants the table needs a fourth group or a second sheet.

### Lot sheets moved (2026-10-16)

Every lot map in the set is now a sheet on the Map Set page, in set order:

| Sheet | Node | From | Base map overrides |
|---|---|---|---|
| `07a Base map` | `1550:2359` | Base map (new) | labels on |
| `08a Sector compass – base map` | `1553:5499` | `169:3793` | contours 30%, plants off |
| `10a Site water flow` | `1553:3290` | `238:3573` | contours 50%, municipal `water` shown |
| `11a Catchment area` | `1553:4394` | `238:4187` | contours 50% |
| `12a Zones` | `1553:13812` | `189:2269` | contours 30% |
| `13a Microclimates` | `1553:14519` | `1382:10661` | none |
| `14a Zone circulation` | `1553:15189` | `1382:10660` | none |
| `15a Soil sample locations` | `1553:6633` | `368:1605` | contours off |
| `20a Succession` | `1553:15889` | `1416:5867` | contours off |
| `21b Thematic design` | `1553:16543` | `1416:6474` | contours off |

How each move was made:

1. Each old map's emphasis was read from its `site-map` layers and set as overrides on the base map
   instance. Contours at 30% fall outside the standard steps; they're kept as drawn.
2. Overlays were copied into `annotations` at the same positions. Keys went into `key` where they
   were. The legend took the old title and date. Sheets other than `07a` have labels off.

Fixes and differences from the old maps:

- **Water flow:** `Trees & Plants` sat inside `Lot 86`, and a second `Municipal Infrastructure` was
  drawn above the overlay with its `water` line on. The sheet shows plants and turns on only the
  municipal `water` frame (a direct visibility override, not `Show utilities`). Municipal now sits under
  the overlay.
- **Zones:** the legend title was "current Microclimate map", carried over from a copy. It now reads
  "current zone map".
- **Zone circulation:** the old frame was 1938 wide. Its drawing moved 18 px left. The circulation key
  ran under the legend, so it moved up to end at y = 920. It sits in `annotations`, because `key`
  holds the zones key.
- **Microclimates and Zone circulation:** their keys are the hand-built frames named
  "Sector Compass Key", now named `key`. They aren't `map-key` instances yet.
- **Succession and Thematic design:** their keys are drawn inside the overlay, so the sheets have no
  `key` layer. Their dates held a line-separator character (U+2028) where the space belongs, which
  made the date wrap. It's now a plain space.
- **Not moved:** the image version of the zone map (`189:2268`, aerial base) and the dark sector map
  (`169:4139`). The set list has one light sheet for each.

Overlays were drawn over the old plant positions, so annotations near plants that moved can sit a few
pixels off. The old frames stay on their pages until Andrew retires them.

## Current and proposed states (2026-10-18)

`Lot 86 / base map` is now a component set (`1597:6795`) with one variant property, `state`.

- **`state=current`** (`1543:617`) is the site as it stands. It's the original component, so its key
  is unchanged and all 15 sheet instances still use it, with their Show toggles intact.
- **`state=proposed`** (`1597:6796`) is the redesign: things moved to their new places, plus new
  structures. It started as an exact copy of current. Edits to it don't touch existing sheets.
- Both variants are stacked in the set, 80 px apart. The set description explains the two states.
- **Tool sheds are visible** in both. The large tool shed, between apple P074 and peach P075, is
  8′ × 10′ (47 × 59 px at 5.85 px/ft), long side running north–south along the tree line. It had been
  drawn 40 × 41; it was resized about its center.
