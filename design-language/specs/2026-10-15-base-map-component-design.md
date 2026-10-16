# Base map component: one grayscale base map for every property sheet

**Date:** 2026-10-15
**Status:** Andrew answered the four open questions on 2026-10-15 (see **Decisions**). The plant list is
settled (see **Plant list**). Two perennials, P053 and P054, still need a species. Ready to build.
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
  - Four are real and join the CSV at their base map positions and sizes:
    - P072, striped maple (`2704`), shading out the vegetable garden
    - P073 and P074, apple trees (`2691`, `2690`)
    - P075, peach tree (`2689`)
  - `2681` (west edge, 120 px) is unconfirmed.
- **Shrubs:**
  - `2731` was a rough drawing of the blueberries, which are P010 and P014.
  - `2730` and `2732` were blackberries, and have been removed.
- **Species named for the 15 blanks**, including three grapes (P058, P059, and the wild grape P067, under
  the dawn redwood), which move to the vine layer. P055 and P056 stay "unknown flowering perennial."
  P053 and P054 are still blank.

The marking sheet (`base-map-reconcile.csv`) is retired. The overlay frame (`1522:269`, Map Set page) stays until the last three plants are settled.

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
- species code
- status
- layer
- function codes

Species sheets keep their color keys, built from `map-key-shell` rows. The inventory sheet is the
ID → species reference for every sheet with labels on. It slots into the set after the species sheets.

## Build order

1. Settle the plant list in `mapped-plants.csv` (done 2026-10-15, apart from P053, P054, and `2681`).
2. Build `Lot 86 / base map` from the grayscale map:
   - replace its plants with the CSV plants, as `Vegetation` instances at their Zones positions
   - keep P072–P075 at their base map positions and sizes
   - order the plants canopy first
   - add the boundary copy and the `labels` layer
   - add the toggles
   - bind the label variable and set label text to the IDs
3. Check it against the old grayscale map with a screenshot overlay.
4. Update `species_maps_apply.py`, then move the three species maps onto sheets.
5. Build the inventory sheet.
6. Move the remaining sheets, in the set order from the sheet spec.

## Decisions (2026-10-15)

1. **The plant list and positions come from the CSV** (the Zones drawing), plus four base map trees.
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
