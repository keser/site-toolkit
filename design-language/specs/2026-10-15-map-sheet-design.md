# Map sheet: standard canvas for the property map set

**Date:** 2026-10-15
**Status:** Andrew answered the open questions on 2026-10-15 (see **Decisions**). Nothing built yet.
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

The set is what a property owner receives: **polished sheets only**.

- **Course work stays separate.** Brainstorm and practice maps are made to meet the course rubric and
  live in the Figma file's **Course Specific** sections. They use the same components but aren't part
  of the set and don't follow this checklist:
  - Water page: Contour Practice, Midterm Water Brainstorm
  - Zones page: Zones Brainstorm
  - Not yet in a section: Soil Brainstorm, the Resilience Brainstorm page
- **Current and proposed.** Each lot sheet type can have a **current** version (the site as it is) and
  a **proposed** version (the design). Rough iterations in between aren't part of the set.
  - Numbering: `NNa` is current, `NNb` is proposed. For example, `13a Zones – current` and
    `13b Zones – proposed`.
  - The legend title carries the state.
  - Regional and overlay sheets describe what exists, so they have only one version.

Order follows the analysis, from regional to lot scale. Square brackets mark sheets that don't exist
yet. The **Proposed** column is filled in as designs are made.

| # | Sheet | Kind | Mode | Current | Proposed |
|---|---|---|---|---|---|
| 01 | Bioregion | regional | dark | [to make] | — |
| 02 | Hardiness zone | regional | dark | [to make] | — |
| 03 | Macro watershed | regional | dark | Macrowatershed | — |
| 04 | State watershed | regional | dark | State Watershed | — |
| 05 | Sector compass – community | overlay | dark | `129:1020` | — |
| 06 | Sector compass – neighborhood | overlay | dark | `129:1019` | — |
| 07 | Base map | property | light | Base Map North | — |
| 08 | Sector compass – base map | property | light | `169:3793` | |
| 09 | Sun paths | overlay | dark | Frame 38 | — |
| 10 | Site water flow | property | light | Site Water Flow Map | |
| 11 | Catchment area | property | light | Design Site Catchment Area Map | |
| 12 | Zones | property | light | Current Zone Map | |
| 13 | Microclimates | property | light | Microclimates | |
| 14 | Zone circulation | property | light | Zone Circulation | |
| 15 | Soil sample locations | property | light | Soil Sample Site | — |
| 16 | Species – status | property | light | Species – Status | |
| 17 | Species – layer | property | light | Species – Layer | |
| 18 | Species – function | property | light | Species – Function | |
| 19 | Succession | property | light | Succession | |
| 20 | Thematic design | property | light | — | Thematic Design |
| 21 | Garden detail | property | light | [to make] | [to make] |

Thematic Design is the one existing proposal. The current dark sector duplicates (`155:2782`,
`155:2916`, `169:4139`) fold into their light sheets via the `Sheet` mode.

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
4. **Sheet template:** a frame to duplicate, with the four layers. The components inside it do the
   sharing.
5. Then the base map component spec, then migration in the order the audit set.

Each step is checked by screenshot and by the legend overflow check before the next.

## Built

### Step 1: variables (2026-10-15)

Three new collections in Site Toolkit Design Language. Nothing is bound to them yet; step 2 does that.

**`Sheet`** (`VariableCollectionId:1516:34`), modes `Light` and `Dark`. Every value aliases a `Ramps`
step.

| Variable | Light | Dark | Scopes | Use |
|---|---|---|---|---|
| `canvas` | neutral/White | neutral/Black | frame fill | sheet background |
| `panel/fill` | neutral/White | neutral/Black | frame, shape fill | legend, key, and caption panels |
| `panel/border` | neutral/Black | neutral/White | stroke | panel outlines |
| `text/primary` | neutral/Black | neutral/White | text fill | titles, headings, values |
| `text/secondary` | charcoal/800 | charcoal/200 | text fill | key row body text |
| `mark/primary` | neutral/Black | neutral/White | fill, stroke | scale bar dark segments, north indicator |
| `mark/inverse` | neutral/White | neutral/Black | fill, stroke | scale bar light segments |

The dark panel is pure black, matching the existing `caption` Black style. It can switch to
charcoal/800 if a softer panel reads better over imagery. The decision gets made at the first dark
sheet.

**`Map display`** (`VariableCollectionId:1516:42`), modes `Labels on` and `Labels off`. It has one
boolean, `plant-labels`, which binds to the `Vegetation` label visibility in the base map step.

**`Site`** (`VariableCollectionId:1516:44`), mode `Lot 86`. Each string variable holds one legend text
node's full content. That's because Figma binds a variable to a whole text node, not part of one.

| Variable | Lot 86 |
|---|---|
| `legend/scale-north` | SCALE: 1” = 20’ / NORTH: -65.43° (two lines) |
| `legend/location` | coordinates (shown only with `Show location`) |
| `legend/elevation` | Min: 103 ft / Max: 107 ft (two lines) |
| `legend/area` | 0.43 ac / 18,730 ft² (two lines) |
| `legend/author` | Andrew Keser |

This replaces the per-fact list in **Legend → Site variables** above (`elevation-min`, `area-ac`, and
so on). The legend needs whole-node strings.

### Site values in other properties' files

A file that uses the library can't add modes to a library collection. Figma's extended collections
can, but they appear to be an Enterprise feature. So the `Site` collection can't give each property's
own file its values. There are two options:

- **A. One mode per property in the library's `Site` collection.** This works on any plan. The cost:
  every property's location and details sit in the shared library, visible to every file that uses it.
- **B. A local `site-legend` component in each property file.** It's a library legend instance with
  that site's values typed once. Every sheet in the file uses `site-legend`, so the values still live
  in one place per file and stay with that property.
  - Under B, the library legend's fields are better as component text properties than as `Site`
    variables.
  - `Site` then becomes unnecessary, even for Lot 86, which would use its own `site-legend` the same way.

Recommendation: **B**. It keeps each property's data in its own file, which matches how the repos
split public and private. It also works on any Figma plan. If Andrew's plan includes extended
collections, `Site` with a per-file extension is cleaner still. Pending Andrew's answer, `Site` stays
as built but unbound.

## Decisions (2026-10-15)

1. **Brainstorm maps are course-specific.** They stay in Course Specific sections, not the set.
   Customers get polished current and proposed sheets.
2. **Light and dark use a `Sheet` variable mode**, not `[Dark]` duplicate frames.
3. **The sheet template is a frame to duplicate**, not a component. The legend, key, base map, and
   variables already carry the shared parts. A sheet component would need its `content` and
   `annotations` as slots, and Figma supports those only partly.
4. **Source images** stay in the git-ignored `site-plan/maps/sources/` folder in each site repo, with
   iCloud as the backup. They aren't tracked in git:
   - A private repo has no per-GB charge, but every image version stays in history permanently.
   - GitHub blocks files over 100 MB and recommends keeping repos small.
   - Git LFS avoids the history growth, but it has a storage and bandwidth quota that's billed beyond
     the free tier.
