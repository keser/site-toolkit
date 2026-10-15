# Map sheet: standard canvas for the property map set

**Date:** 2026-10-15
**Status:** Draft for Andrew's review. Nothing built yet.
**Scope:** personal project, so there's latitude to be opinionated.
**Builds on:** `2026-10-15-property-map-set-audit.md` (inventory, findings, Andrew's answers).

## Goal

Every map in a property's map set uses one sheet: same canvas, same layer order, same key and legend.
That includes lot drawings, the garden detail, regional maps, and aerial overlays. A property owner
should be able to flip through the set and read every map the same way. Slide decks keep their own
layouts and can still crop from these sheets.

## What exists today (Keys page)

| Component | Node | Today | Gap |
|---|---|---|---|
| `map-legend` | `168:1310` | One component. North is two child layers, one hidden. `Show location` boolean added 2026-10-15. | No scale options. Every field is hand-typed. Long titles overflow 1920. |
| `map-scale` | `1160:2867` | One component: 0 / 20′ / 40′ | Fixed to the lot scale. |
| `north-indicator` | `174:4869` | Variants `-65.43˚`, `Up` (property named `Property 1`) | Fine. Rename the property. |
| `map-key` | `153:2052` | 16 `Map Type` variants × `Theme` (Tints, Shades, Default) | Each variant holds Lot 86's rows. That doesn't work for other properties. |
| `map-key-row` | `480:889` | Heading, body, swatch type, size | Fine. This is the building block. |
| `caption` | `640:4373` | `Style` White, Black, Shade, Tint × `Size` | Fine. |

## The sheet

### Canvas

- **1920 × 1080**, frame name `<NN> <Title>`, for example `07 Species – Layer`.
- Clips content and has a solid background bound to a token.
- The lot maps already use this size. These need re-laying-out:
  - Zone Circulation (1938 wide)
  - Frame 38, sun paths (1856 × 839)
  - the elevation frames (1856 wide)

### Layers, bottom to top

| Layer | Type | Holds |
|---|---|---|
| `content` | frame, 1920 × 1080, clips | One of the three content kinds below. Nothing else. |
| `annotations` | frame, 1920 × 1080, no fill | Lines, regions, captions, markers, badges, region labels. |
| `key` | `map-key` instance | Top left at (40, 40). It moves only when it would cover the subject, and then to top right. |
| `legend` | `map-legend` instance | Pinned to the bottom: (0, 940), 1920 × 140. |

`content` and `annotations` share the canvas's coordinates, so drawn work lines up with the map under it.

### Content kinds

1. **Property:** an instance of the grayscale base map component (its own spec, next).
   - Lot drawings use it at 1:1.
   - The **garden detail** uses the same instance, scaled up and cropped to the garden. Plants and
     structures scale with it.
   - A garden-only base map would be a second copy to keep in sync, so there isn't one.
2. **Regional:** a source image, as an image fill, from `site-plan/maps/sources.md`. It's optionally
   redrawn as vectors in `annotations`, the way the watershed maps already work.
3. **Overlay:** an aerial image in `content`, with the drawn layers in `annotations`. Examples: sun paths
   (Frame 38), North Up sector maps, and later the 3D sun scene.

### Light and dark

Dark is part of the standard set. Rule: **dark over full-color imagery, light over the grayscale base
map**.

- **Mechanism:** a `Sheet` variable collection with `Light` and `Dark` modes. It drives the legend,
  the key panel, the caption text, and the sheet background. Each sheet sets one mode on its frame.
- **Why not variants:** today a dark map is a duplicate frame (`[Dark]`). With a mode, light and dark
  become one frame with one switch. That removes 6 duplicate sector frames and keeps future edits in
  one place.
- Caption `Style` variants stay for one-off emphasis.
- The key's `Theme` (Tints, Shades) is about region fill colors, not light and dark, and stays as is.

### Plant labels

The `Map display` variable collection (`Labels on` / `Labels off`) from the base map plan is set on the
sheet frame too. Both switches sit on the sheet:

- `Sheet`: Light or Dark
- `Map display`: Labels on or off

## Legend

### Fields

| Field | Source | Notes |
|---|---|---|
| Title | per sheet (text property) | Max width 360. Wraps to a second line instead of pushing the row. |
| Scale statement + north text | `Site` variable, or per sheet for regional maps | "SCALE: 1″ = 20′ / NORTH: −65.43°" |
| Scale bar | `map-scale` variant (below) | |
| North indicator | `North` variant: `Rotated` or `Up` | Replaces the two stacked child layers. |
| Location | `Site` variable | `Show location`, default off. |
| Elevation | `Site` variable | **Two lines** ("Min: 103 ft" / "Max: 107 ft"), matching area. `Show elevation` boolean, off for regional maps. |
| Area | `Site` variable | `Show area`, off for regional maps. |
| Source credit | per sheet (text property) | New. `Show source`, on for regional and overlay sheets. Text comes from the sources list's Attribution column. |
| Author | `Site` variable | |
| Date | per sheet (text property) | Lowercase, auto width, never wraps. |

**Overflow fix:** two-line elevation saves about 170 px, and the 360 title width caps the worst case.
Estimated against today's nine overflowing legends, the widest (Soil Building Goals Brainstorm,
2110 px) drops to about 1868 px: 2110 − 170 for elevation − 72 for the title. It gets re-measured
after the build. A build check fails if any legend's last visible child ends past 1880,
which leaves room for the 40 px right padding.

### Site variables

A `Site` collection with string variables:

- `scale`
- `north`
- `location`
- `elevation-min`
- `elevation-max`
- `area-ac`
- `area-ft2`
- `author`

It has one mode per property; the library has a `Lot 86` mode. Legend text binds to these variables.
This fixes the drift the audit found, where 28 legends each carried hand-typed copies. A property's
own Figma file sets its mode once, at the page level.

### Scale

`map-scale` becomes a component set:

| Variant | Use | Labels |
|---|---|---|
| `Lot` | every lot drawing | 0 / 20′ / 40′ |
| `Garden detail` | zoomed garden drawing | 0 / 5′ / 10′ (set when the garden detail is drawn) |
| `Regional` | regional maps | text properties for the mid and end labels and the unit, such as 0 / 50 mi / 100 mi |

Regional scales differ on every map, so `Regional` takes text properties rather than one variant per
value. The watershed maps' "100M" becomes "100 mi" (or km), with the unit always written out.

## Key

The `map-key` component's 16 `Map Type` variants hold Lot 86's rows, which won't carry over to
another property. Instead:

- **The library keeps a `map-key` shell:** title, panel, light and dark, and a slot for
  `map-key-row` instances.
- **Each sheet builds its key from `map-key-row` instances** in its own file.
- **Lot 86's 16 variants stay** as the demo set's keys until each sheet migrates. After that they're
  removed.

## The set

The checklist of sheets in a property map set. Order follows the analysis, from regional to lot
scale. Square brackets mark sheets that don't exist yet.

| # | Sheet | Kind | Mode |
|---|---|---|---|
| 01 | [Bioregion] | regional | dark |
| 02 | [Hardiness zone] | regional | dark |
| 03 | Macro watershed | regional | dark |
| 04 | State watershed | regional | dark |
| 05 | Sector compass – community | overlay | dark |
| 06 | Sector compass – neighborhood | overlay | dark |
| 07 | Base map | property | light |
| 08 | Sector compass – base map | property | light |
| 09 | Sun paths | overlay | dark |
| 10 | Site water flow | property | light |
| 11 | Catchment area | property | light |
| 12 | Contour & water flow | property | light |
| 13 | Current zones | property | light |
| 14 | Microclimates | property | light |
| 15 | Zone circulation | property | light |
| 16 | Soil sample locations | property | light |
| 17 | Species – status | property | light |
| 18 | Species – layer | property | light |
| 19 | Species – function | property | light |
| 20 | Succession | property | light |
| 21 | Thematic design | property | light |
| 22 | [Garden detail] | property | light |

The four brainstorm maps (water, soil, zones, resilience) are open question 1.

## Build order

1. **Variables:** the `Site` collection with a Lot 86 mode, plus the `Sheet` and `Map display`
   collections.
2. **Legend:**
   - `North` variant
   - bound `Site` fields
   - two-line elevation
   - 360 title width
   - `Show elevation`, `Show area`, `Show source`
   - `map-scale` set
3. **Key shell.**
4. **Sheet template:** a component or a duplicate-me frame (open question 3) with the four layers.
5. Then the base map component spec, then migration in the order the audit set.

Each step is checked by screenshot and by the legend overflow check before the next.

## Open questions for Andrew

1. **Brainstorm maps:** are the water, soil, zones, and resilience brainstorms part of the owner's
   set, or class-only?
2. **Light and dark:** do you agree with a variable mode instead of `[Dark]` duplicate frames?
3. **Sheet template:** a component, so all sheets update together, or a frame you duplicate? A
   component locks the four layers, but `content` and `annotations` then have to be slots, which
   Figma supports only partly. I'd use a frame you duplicate, with the components inside it doing
   the sharing.
4. **Source files:** keep the git-ignored repo folder as the long-term home? If so, the originals
   need a backup outside git. The other choice is to track them in the private repo, which would
   change the site repo's "raw media isn't tracked" rule for this one folder.
