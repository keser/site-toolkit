# Base map views: one drawing, many crops

Status: approach agreed 2026-11-01; not built. Build after the PDC Lesson 8 submission.

## Problem

Lot sheets all show the whole lot at one scale. Detailed maps (22b, 31b) crowd the drawing, and
their keys cover map detail. Zooming in today means rescaling a whole base-map instance by hand
(22 at 4×, 22b at 5/3 × with a typed offset), which also thickens every stroke.

## Decisions

1. **One drawing per state, many views.** `Lot 86 / base map` keeps one variant axis, `state`
   (current, proposed). Views are not variants: a view axis would multiply full copies of the
   drawing (2 states × 7 views = 14), and every geometry fix would have to be repeated in each.
   Constraint for all future map work: keep the number of variants and instances to maintain low.
2. **A view is a component that crops the drawing.** A fixed-size, clipped frame holding a nested
   base-map instance that the view positions, scales and rotates. The nested `state` property is
   exposed on the view, so a sheet switches current/proposed on the view. Sheets place views, not
   raw base maps, so no sheet carries its own transform.
3. **Views for Lot 86:**

   | View | Shows | Working region |
   |---|---|---|
   | A. Whole lot + context | Lot plus the neighbors' yard behind | — |
   | B. Lot fit | Rear boundary at the map edge, zoomed in | — |
   | C. House & front yard | Detailed plant mapping | Theme 1 · Porch & Songbird |
   | D. Shade garden | Pool to dawn redwood | Theme 2 · Shade Retreat |
   | E. Veg garden & paddock | Today's 22 / 22b area | Theme 3 · Kitchen & Hens |
   | F. Orchard & woodland | — | Themes 4 + 5 |

4. **Region views follow the working regions (the themes on 21b).** These are areas of the yard
   that share a theme, not permaculture zones. Any site gets one region view per working region,
   which scales to properties much larger than 0.43 ac: more regions, same pattern.
5. **Rotation in 90° steps only.** Labels and markers turn with the view, and Figma can't
   counter-rotate text inside an instance. Each view states its north value for the legend.
6. **Detailed plants live in the master drawing** as their own layer, hidden by default, shown by
   region views (Show toggle or a Map display mode). One source; whole-lot views stay clean.
7. **Close views put the key beside the map, not over it** (for example a 1280-wide map area and a
   600-wide key panel). Dense sheets split front and back so keys stay short.
8. **Standard scales** become `map-scale` variants (candidates: 1″ = 20′, 12′, 8′, 5′) instead of
   typed overrides.

## Open

- **Stroke weight when zoomed.** Scaling an instance scales its strokes. Options: bind base-map
  stroke weights to variables with a mode per zoom level, or accept heavier lines. Decide after a
  side-by-side comparison of both at 5/3 × and 4×.
- **Crop bounds, rotations and scales per view**, to be proposed for approval before building.

## Lot boundary (2026-11-01)

The 0.43 ac plan outline is the property's current legal definition (pins in the ground agree).
Andrew will still measure from the pins on the next site visit. Keep the hidden
`Lot 86 boundary – traced 0.571 ac (reference)` layer until then. Overlays that run past the rear
line (Theme 5 on 21b, 31b, C06; Zone 5 on 12a, 14a, C01; succession on 20a; goals on C04; flow
arrows on 10a and 11a) get redrawn, after the views exist.

## Order

1. Finish the Lesson 8 round: review, publish the site file, Map Set slides.
2. Stroke comparison and decision.
3. Views A and B; move the lot sheets onto B. About 40 sheets, so small batches.
4. Views C–F with the detail-plant layer; split dense sheets front/back with side-panel keys.
5. Redraw overlays that overrun the rear line.
