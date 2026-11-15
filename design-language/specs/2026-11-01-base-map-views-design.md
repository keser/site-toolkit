# Base map views: one drawing, many crops

Status: approach agreed 2026-11-01. Revised 2026-11-14 (see "Frame and keys" below): the
whole-lot frame stays, and the rear-line overlay redraws are dropped. Views C, D and E built
2026-11-14 (see "Built"); the open questions closed the same day.

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
8. **Standard scales** become `map-scale` variants instead of typed overrides. The built views set
   two of them, added 2026-11-14: `Base map 2×` (1″ = 10′, views C and D) and `Base map 4⁄3×`
   (1″ = 15′, view E). The detail sheets still carry typed labels until they switch over. Add others
   (12′, 8′, 5′) when a view needs them.

## Closed (2026-11-14)

- **Stroke weight when zoomed.** Accept the heavier lines. Views C–E were built at 2× and 4⁄3× and
  read well on the Lesson 9 detail sheets. Variable stroke modes per zoom level stay an option if a
  4× view looks too heavy.
- **Crop bounds, rotations and scales per view.** Set by the built views C–E (see "Built").
  Views A, B and F get proposed the same way if they're ever built.

## Lot boundary (2026-11-01)

The 0.43 ac plan outline is the property's current legal definition (pins in the ground agree).
Andrew will still measure from the pins on the next site visit. Keep the hidden
`Lot 86 boundary – traced 0.571 ac (reference)` layer until then. Overlays that run past the rear
line (Theme 5 on 21b, 31b, C06; Zone 5 on 12a, 14a, C01; succession on 20a; goals on C04; flow
arrows on 10a and 11a) get redrawn, after the views exist.

## Frame and keys (2026-11-14)

1. **Keep the whole-lot frame.** Sheets keep today's 1920×1080 frame instead of tightening it to
   the 0.43 ac line. The spare space outside the lot holds the keys, so keys stop covering
   on-lot elements. Place keys over off-lot ground with no design content (on 21b: top left over
   Lot 85, and the bottom band over Lot 87 and the street). Those spots cover most maps. When a
   map's focus is the ground those keys would cover, the rear woodland area can hold the key
   instead (a sector map, for example).
2. **Overlays may cross the rear line.** All adjacent owners have approved the work (site plan
   R18), and rear woodland work extends onto the rear neighbor's lot. The overlay redraws listed under "Lot
   boundary" are dropped. Keep the lot boundary visible and above every overlay so on-lot and
   shared work stay readable.
3. **Views A and B are likely unnecessary.** The whole-lot frame already serves as both. Region
   views (C–F) remain, built when a detail map needs one.
4. **Concept plan groups in `state=proposed` (PDC Lesson 9).** Five layer groups (Water, Zones &
   Access, Vegetation, Structures & Energy, Soil & Animals) live in a `Concept plan` frame in the
   proposed variant, each hidden by default. Each group is bound to a boolean property: `Show water`,
   `Show zones & access`, `Show vegetation`, `Show structures & energy`, `Show soil & animals`. A
   sixth, `Show layer detail` (default on), shows the analysis detail. A sheet turns on one group.
   The integrated plan shows all five and turns layer detail off. Existing sheets on `state=proposed` don't change.

## Order

1. Finish the Lesson 8 round: review, publish the site file, Map Set slides.
2. ~~Stroke comparison and decision.~~ Closed 2026-11-14: accept heavier lines (see "Closed").
3. ~~Views A and B; move the lot sheets onto B.~~ Likely unnecessary (2026-11-14, "Frame and
   keys" item 3).
4. Views C–F with the detail-plant layer; split dense sheets front/back with side-panel keys.
   C, D and E are built; see "Built".
5. ~~Redraw overlays that overrun the rear line.~~ Dropped 2026-11-14.

## Built (2026-11-14)

Three view components in the site file's Components page, Lot 86 section, "views". Each exposes
its base-map instance, so a sheet sets the concept plan toggles on the view. The Lesson 9 detail
sheets (`32.1b`–`37.1b`) place them.

| View | Component | Scale |
|---|---|---|
| C | `view C – house & front` | 2× (1″ = 10′) |
| D | `view D – shade garden` | 2× (1″ = 10′) |
| E | `view E – garden end` | 4⁄3× (1″ = 15′) |

Views A, B and F aren't built.
