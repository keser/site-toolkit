# Base map component: one grayscale base map for every property sheet

**Date:** 2026-10-15
**Status:** Draft. Waiting on Andrew's answers to **Decisions needed**. Nothing built yet.
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

A visual comparison sits on the Map Set page: frame **`TEMP plant reconciliation`** (`1522:269`). Base
map plants are gray, labeled with their node number. CSV plants are dashed magenta outlines, labeled
with their ID. It gets deleted once the plant list is settled.

The two drawings were edited separately: the base map for most maps, the Zones drawing for the
species work. So neither is a clean superset of the other.

## Proposed component

### Name and home

`Lot 86 / base map`, in the library, on the Base Map page. Each property's own file gets its own
`<Property> / base map`. Unlike `_site-legend`, it's **published**: open question 3 explains why.

### Contents, bottom to top

1. **Ground:** lot fill, paving (`stone-paver` ×7), garden beds, grass areas. Taken from the grayscale
   map as is.
2. **Underlay image:** the 2136 × 2059 image (Figma hash `12f7a3c6`, listed in
   `site-plan/maps/sources.md`). Its opacity is kept as it is today. The water maps' variant
   (`452daab3`) becomes an override on those sheets if it's still needed. That's open question 4.
3. **Plants, canopy first:** every plant is a `Vegetation` instance named `plant P###`, ordered by
   layer:
   1. canopy
   2. sub-canopy
   3. shrub
   4. herbaceous
   5. groundcover
   6. vine
   7. root

   Tall plants are drawn first, so understory plants stay visible on top of them. The 32 px minimum
   short side carries over.
4. **Structures:** `structure` ×7, utility poles, connections.
5. **Lot 86 boundary:** above the plants. The species apply script currently re-draws it on top as a
   workaround; this replaces that.

Map labels such as road names and neighbor roles go on a separate `labels` layer at the top. That
covers the earlier open item about moving labels into their own layer. Plant labels stay inside each
`Vegetation` instance, because they move with the plant.

### Vegetation changes

- **Label visibility** binds to `Map display` `plant-labels`. Today every label is hidden by a
  per-instance override. Those overrides get cleared, so the variable decides.
- **Label text** becomes the plant's short code from the CSV, not today's letter codes. That's open
  question 2.
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

## Build order

1. Settle the plant list (decisions 1 and 2), then update `mapped-plants.csv`.
2. Build `Lot 86 / base map` from the grayscale map:
   - match and rename the plants
   - add the missing plants
   - delete the dropped ones
   - reorder the layers
   - bind the label variable
3. Check it against the old grayscale map with a screenshot overlay.
4. Update `species_maps_apply.py`, then move the three species maps onto sheets.
5. Move the remaining sheets, in the set order from the sheet spec.

## Decisions needed

1. **Source of truth for positions.**
   - **(a)** Base map positions, adding the 13 CSV-only plants at their Zones positions.
   - **(b)** Zones and CSV positions, adding whichever base-map-only plants are real.
   - **(c)** Plant by plant, using the overlay.

   Recommendation: **(a)**. The base map is on 13 frames and is the drawing Andrew uses. The CSV
   carries the IDs and attributes, and those attach to base map plants by matching. The loose pairs
   and the 21 unmatched base map plants still need Andrew's eye on the overlay: which are real plants,
   which are duplicates, and which have been removed from the site.
2. **Plant labels.** On sheets with labels on, what should show: the species short code (BW for black
   walnut, from the CSV label column's prefix), the plant ID (P001), or the base map's letter codes
   (A–EE, whose key isn't recorded anywhere)?
3. **How slides use library maps.** Do slide decks place these maps as library instances, or as
   pasted copies?
   - If they're instances, the base map and the Lot 86 legend have to be published. That means
     `_site-legend` loses its underscore.
   - If they're pasted and detached, unpublished is fine.
4. **The water underlay (`452daab3`).** Is it a deliberate variant, for example with contours
   or drainage, or an older copy of the same image?
