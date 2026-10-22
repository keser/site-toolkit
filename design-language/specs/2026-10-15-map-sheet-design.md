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

Site fields come from the property's `site-legend` component (see **Site values** below). Sheet fields
are typed on each sheet.

| Field | Set on | Notes |
|---|---|---|
| Title | sheet | Long titles take a manual line break if needed. |
| Scale statement + north text | `site-legend`; regional sheets type their own | "SCALE: 1″ = 20′ / NORTH: −65.43°" |
| Scale bar | `map-scale` variant, exposed on the legend | `Lot`, `Garden detail`, `Regional` |
| North indicator | `North` variant: `Rotated` or `Up` | Replaces the two stacked child layers. |
| Location | `site-legend` | `Show location`, default off. |
| Elevation | `site-legend` | **Two lines** ("Min: 103 ft" / "Max: 107 ft"), matching area. `Show elevation`, off for regional maps. |
| Area | `site-legend` | `Show area`, off for regional maps. |
| Source credit | sheet | New. `Show source`, on for regional and overlay sheets. Text comes from the sources list's Attribution column. |
| Author | `site-legend` | |
| Date | sheet | Lowercase, auto width, never wraps. |

**Overflow fix:** two-line elevation (about −170 px) plus a 48 px gap between fields instead of 64
(6 gaps, −96 px). A 360 px title cap was dropped: the title sits inside the shared `label` component,
whose heading has a fixed height, so wrapping it would mean layout overrides inside a nested component
that's also used on the maps. Measured after the build, every one of the 28 legends ends at or before
1842 px. The build check fails any legend whose last visible child ends past 1880, which leaves room
for the 40 px right padding.

### Site values

Option B (decided 2026-10-15): each property has a local **`site-legend`** component. It's a
`map-legend` instance with that site's values typed once and the inner legend exposed, so North, the
toggles, and the scale are set on each sheet. It's published (renamed from `site-legend` on 2026-10-15), because slides build maps from these
pieces too. Every sheet in a property's file uses its `site-legend`, so site values live in one place
per file and stay with that property.

Why not variables: a file that uses the library can't add modes to a library collection (extended
collections, which can, appear to be Enterprise-only). Putting one mode per property in the library
would leave every property's location in the shared file.

Why not text properties: the legend's text sits inside nested `label` instances. Text properties would
mean adding them to `label` and exposing nested properties, and `label` is also used on the maps.

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
| 09.1 | Sun path 3D scene | drawing | light | `scene` (`174:5469`) | — |
| 10 | Site water flow | property | light | Site Water Flow Map | |
| 11 | Catchment area | property | light | Design Site Catchment Area Map | |
| 12 | Zones | property | light | Current Zone Map | |
| 13 | Microclimates | property | light | Microclimates | |
| 14 | Zone circulation | property | light | Zone Circulation | |
| 15 | Soil sample locations | property | light | Soil Sample Site | — |
| 16 | Species – status | property | light | Species – Status | |
| 17 | Species – layer | property | light | Species – Layer | |
| 18 | Species – function | property | light | Species – Function | |
| 19 | Plant inventory (ID → species table) | table | light | [to make] | — |
| 20 | Succession | property | light | Succession | |
| 21 | Thematic design | property | light | — | Thematic Design |
| 22 | Garden detail (veg garden & chicken run) | property | light | `22 Garden detail` | [to make] |
| 23 | Resilience brainstorm | property | light | Resilience Brainstorm page | — |

Thematic Design is the one existing proposal. The current dark sector duplicates (`155:2782`,
`155:2916`, `169:4139`) fold into their light sheets via the `Sheet` mode.

## Build order

1. **Variables:** the `Sheet` and `Map display`
   collections.
2. **Legend:**
   - `North` variant
   - `site-legend` for Lot 86
   - two-line elevation
   - 48 px field gap
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

A third collection, **`Site`**, was created and then deleted the same day, unbound, when Andrew
chose option B (see **Legend → Site values**).

### Step 2: legend (2026-10-15)

On the Keys page:

- **`map-legend` is a component set** (`1517:8947`), with `North=Rotated` (the original `168:1310`, so
  every existing instance stayed linked) and `North=Up` (`1517:8887`).
  - Properties: `North`, `Show location` (default off), `Show elevation`, `Show area`, `Show source`
    (default off).
  - The new `source` field sits before the date.
  - Field gap is 48. Elevation is on two lines.
- **Colors use `Sheet` variables:**
  - 23 paints in the legend (panel fill and border, label text as instance overrides)
  - 36 in `map-scale` and `north-indicator` (scale segments and arrow)
  - The arrow's outer Union fill also needed binding, in the mains and in the legend's nested copies.
    Without that, the arrow disappeared on a dark sheet.
  - The shared `label` component wasn't touched.
  - A temporary dark test frame was checked and deleted.
- **`map-scale` is a component set** (`1517:9841`):
  - `Scale=Lot` (the original `1160:2867`)
  - `Garden detail` (0 / 5′ / 10′)
  - `Regional` (`Mid label` and `End label` text properties, default 50 mi / 100 mi)
  - Label frames no longer clip, so long labels stay centered on their ticks.
  - It's exposed in both legend variants.
- **`Lot 86 / site-legend`** (`1517:9914`): wraps a `North=Rotated` legend at 1920 × 140, exposed.
- **All 28 existing instances:**
  - 4 were switched to `North=Up`: the two satellite sector maps and their dark copies. They had shown the
    north-up arrow by hand.
  - Location is still off on all 28.
  - Wrapped dates (fixed-width text) were set back to auto width.

**Still to do in the legend:** the library defaults still hold Lot 86's values. They switch to neutral
placeholders after every Lot 86 sheet uses `site-legend`. Swapping an instance to the wrapper adds a
nesting level, so per-sheet title and date overrides don't carry over and are re-applied during
migration.

### Step 3: key shell (2026-10-15)

- **`map-key-shell`** (`1520:1220`, Keys page, next to the legend):
  - `Title` text property, style `Mono/32/Bold`.
  - One **`Rows` slot** whose preferred contents are `map-key-row`.
  - Each sheet drops its own rows into the slot. There are no per-map variants.
  - The slot wraps horizontally (32 column gap, 16 row gap). At the default 938 width, 421-wide rows
    sit in two columns. Resize the shell to 485 for one column.
  - The panel border is excluded from layout, matching the existing keys. Otherwise two 421 rows didn't fit.
  - Panel fill, border, and title use `Sheet` colors.
- **`map-key-row`** (`480:889`):
  - Heading and body text bound to `Sheet` `text/primary` and `text/secondary`.
  - The white fill on each variant's `text` frame was removed, because it showed as white boxes on a dark
    panel. Nothing changes on light panels.
- The old `map-key` set (16 Lot 86 variants) is untouched. It stays until each sheet migrates.

### Step 4: sheet template (2026-10-15)

- **New page `Map Set – Lot 86`** (`1520:8041`), after Keys. Lot 86's sheets will live here as they
  migrate.
- **`00 Sheet template`** (`1520:8042`): 1920 × 1080, clips, fill bound to `Sheet` `canvas`.
  - Explicit modes: `Sheet: Light` and `Map display: Labels on`.
  - Layers:
    - `content`: empty, 1920 × 1080, clips, stretches
    - `annotations`: empty, same
    - `key`: a `map-key-shell` instance at (40, 40), pinned top left
    - `legend`: a `Lot 86 / site-legend` instance at (0, 940), pinned bottom, stretches
- **Using it:** duplicate the template, rename it `NN Title`, then:
  1. Set the key's Title and drop rows into its slot.
  2. Set the legend title, date, North, scale, and toggles.
  3. Set the frame's `Sheet` mode (Dark over imagery) and `Map display` mode.
  4. Fill `content` with a base map instance or a source image.
  5. Draw in `annotations`.
- Light and Dark were both checked by screenshot with a temporary duplicate, which was deleted.

### Step 5: regional, overlay, and added sheets (2026-10-16)

Andrew asked for every visual in the set, including the resilience brainstorm and the 3D sun scene
(rows 09.1 and 23). All sheets sit on the Map Set page in set order. Lot sheets are recorded in the base
map spec.

| Sheet | Node | Content | Mode |
|---|---|---|---|
| `01 Bioregion` | `1558:7737` | `bioregion.png`, filled to 1920 × 940 | dark |
| `02 Hardiness zone` | `1558:8059` | the regional crop (NY to Cape Cod), filled to 1920 × 940 | dark |
| `03 Macro watershed` | `1558:8264` | image; marker, caption, and the hidden watershed graphic in `annotations` | dark |
| `04 State watershed` | `1558:8516` | same | dark |
| `05 Sector compass – community` | `1558:8769` | satellite image from the `[Dark]` frame; sector diagram in `annotations` | dark |
| `06 Sector compass – neighborhood` | `1558:9417` | same | dark |
| `09 Sun paths` | `1558:9974` | Frame 38's aerial, scaled 1.034× to 1920 × 868 and centered above the legend | dark |
| `09.1 Sun path 3D scene` | `1558:10279` | the vector scene, scaled to 900 px tall | light |
| `23a Resilience brainstorm` | `1558:10655` | base map; `Sector Regions` in `annotations` | light |

**Regional legends** use the library `map-legend` (North = Up), widened to 1920:

- Elevation, area, and location are hidden. Source shows its placeholder until `sources.md` has
  attribution.
- **The scale is hidden until it's measured from the source.** The watersheds had hand-drawn bars
  labeled "100M" and "10M", and the north-up sector maps carried the lot's 1″ = 20′. None of them
  can be trusted. The label body reads "north up / scale to come".
- The 3D scene also hides north; its body reads "3d view / not to scale".
- The hand-built scale bars and north arrows were dropped.

**`map-key` follows the sheet's Light and Dark modes now.** The dark sector sheets showed white key
panels whose row text had turned light. All 17 variants changed:

- panel fill bound to `panel/fill`, border to `panel/border`, title to `text/primary`
- 61 row descriptions carried a raw gray override (`#3A3936`). They're now bound to `text/secondary`.

In Light mode, the panel, border, and title resolve to the same white and black as before. The
descriptions get slightly darker (`charcoal/800`). Frames outside the Map Set page don't set a
`Sheet` mode, so they show Light.

**Keys are all `map-key` instances now** (2026-10-16). The hand-built "Sector Compass Key" frames are
gone from the Map Set page:

- **New variants (Theme = Default):** `Macro Watershed`, `State Watershed`, `Sun Paths`,
  `Hardiness Zone`, `Bioregion`. The watershed and sun path rows, text, and swatch paints were copied
  from the hand-built keys.
  - `Hardiness Zone` lists zones 5a to 7b, the zones on the regional crop. Swatch colors are sampled
    from the map image, and ranges come from the 2023 USDA legend image.
  - `Bioregion` has one row, the red boundary. The bioregion's name waits on the source.
- **Existing variants used:** `Microclimates`, `Zones – Current` (zone circulation), and
  `Resilience Brainstorm`.
  - The `Microclimates` swatches were pale stand-ins that didn't match the map. They now use the map's
    colors.
  - Zone circulation keeps its own zone 05 wording ("least maintained or visited…") as an instance
    override.
  - Microclimates and Resilience are narrowed to 999 on their sheets, the old keys' width.
- **Project-site markers** on 01 and 02 are placed by estimate from Portland's latitude and longitude.
  Andrew checks them.

### Step 6: legend values pinned, Styles page (2026-10-16)

**Lot 86's legend values are now explicit overrides**, so the library defaults can change without
touching the set:

- In `Lot 86 / site-legend` (`1517:9914`): the scale and north statement, location, elevation, area,
  and author.
- On all 24 Map Set legends: title, label body, author, and date.

Nothing changed visually. **The library defaults are still Lot 86's.** Switching them to neutral
placeholders waits on Andrew. Slides build maps from the published `map-legend`, so any slide legend
that leans on a default would change when its file accepts the update.

**The Styles page documents `Sheet` and `Map display`** in a new frame, `Sheet Documentation`
(`1588:18372`, x = 11040; section `701:2` is now 12544 wide). It's cloned from Species Documentation:

- **Sheet:** one row per variable with live Light and Dark swatches, each pinned to its mode. The
  alias captions (`neutral/white / neutral/black`) are static, so update them after any change to the
  collection.
- **Map display:** two live plants in frames set to Labels on and Labels off. A plant's `Show label`
  is bound to `plant-labels` on the instance, not in the Vegetation main, so these demo instances
  carry the binding themselves.

**The library legend defaults are placeholders now** (2026-10-16, Andrew's go-ahead): title
"map title", "SCALE: 1″ = 00′ / NORTH: 0.00°", zeroed location, elevation, and area, "Author name",
"month year". Both `map-legend` variants changed. Every Map Set legend kept Lot 86's values; the
regional sheets show zeros only in their hidden location, elevation, and area fields. Slide legends
that leaned on the old defaults pick up placeholders when their file accepts the update; swap them to
`Lot 86 / site-legend`.

### Step 7: garden detail (2026-10-16)

`22 Garden detail` (`1589:17426`) sits between 21b and 23a (23a moved to x = 50880).

- **Scale.** The lot drawing is 234 px = 40′ (5.85 px/ft). The `Garden detail` scale bar is
  234 px = 10′, so the base map instance is rescaled 4×. The legend reads 1″ = 5′.
- **Crop.** The garden is the hidden `Vegetable Garden` marker in the base map (`1543:747`, 198 × 236
  at 1020, 246), the same area Succession and Zones call "veg garden & chicken run". At 4× it is
  792 × 944, centered in the 1920 × 940 map area. The striped maple P072 shading it is in frame.
- **Annotations:** the Succession area outline and a Thematic caption, "veg garden & chicken run".
- **Legend:** `map-scale` = `Garden detail`; area hidden (it's the lot's area).
- **Rescale scales strokes too**, so the lot boundary and plant outlines are 4× heavier. Thinning
  waits until the sheet has content.
- **Parked (2026-10-18).** The garden's contents aren't course work. The current beds will be
  replaced once Andrew decides where the coop's water collection goes and how much sun the area gets
  after the striped maples are cut back. The rectangle inside the outline is the coop and run, which
  share one roof. The property's in-ground beds are already on the base map.
- **The garden fence is back on the base map** (2026-10-18). The `Vegetable Garden` instance
  (`1543:747`) is the fence. It had been hidden when removing the fence was on the table, which is on
  hold. It's visible again on every lot sheet with its "VG" label hidden and its fill cleared (the
  tan fill came from the color base map). The amber stand-in outline on this sheet was removed; the
  caption stays.
- **The tool sheds are on the base map too** (2026-10-18), so it records the current state.
  `small tool shed` (`1543:749`) sits inside the fence on its west edge; `large tool shed`
  (`1543:748`) sits just east of the fence. Both are `structure` instances restyled to match the
  coop: roof panels gray (0.8) instead of the color map's brown, and the "TS" label hidden. A
  proposed-state map will move things and add a tentative 10′ × 10′ shed (about 58 × 58 px).

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

### Regions rebuilt from components (2026-10-18)

The Resilience brainstorm (23a) and Microclimates (13a) maps had their keys migrated but still drew
their regions as plain frames with raw hex fills. All 20 regions are now `map-region-sample`
instances, each copying its key swatch's fill and border, so the map and key can't drift.

- **`map-region-sample` stretches now.** Its `fill` and `border` layers were pinned top-left, so a
  resized instance didn't scale. All five variants use Stretch constraints; key swatches (60 × 40)
  are unchanged.
- **Resilience (`Sector Regions`, 10):** key Tint fills, no border. Sage → Wildlife Corridor (seven
  regions, including the top band), teal → Winter Sun Path, gold → Winter Wind, slate → Pollutants,
  coral → Spring → Fall Wind. Fire is key-only; nothing on the map uses it.
- **Microclimates (`Microclimates`, 10):** fills at 50% from the key; borders are each type's 3 px
  Shade (cobalt, coral, gold, magenta) instead of the old 4 px `slate/800`.
- Instances are named after their key row. Old frames were deleted after a screenshot check.

### Regional sheets tidied (2026-10-18)

- **Scale:** 01–04 legends read "north up / not to scale" instead of "scale to come". No regional
  scale bar was verified against the image crops before turn-in.
- **Source:** 03 and 04 credit "USGS Watershed Boundary Dataset; imagery Google Earth". 01 and 02
  still read "Source credit".
- **"Project Site" labels** on 01–04 are `caption` Black, not Shade.
- **The watershed regions are part of the source image**, so they can't be swapped for
  `map-region-sample` instances without tracing. The key swatches were sampled from the image. The
  hidden `Macro Watershed Graphic` frames on 03 and 04 are an older diagram that isn't used.

### Superseded originals marked (2026-10-18)

Every original frame on a topic page that has a Map Set sheet is renamed
`OLD – see Map Set NN – <original name>` (24 frames, including the three `[Dark]` sector
duplicates and the Resilience page's base map and `Sector Regions` overlay). Content is unchanged;
the frames stay until Andrew retires them. Not marked, because no sheet replaces them: the full-color
base map (`155:3976`), the aerial zone map (`189:2268`), the sun-path scene (`174:5469`), Course
Specific brainstorms and practice maps, inspiration boards, and the Elevation page.

### Course maps added to the Map Set (2026-10-18)

**Decision change:** while the course runs, the Map Set holds the course maps too, so every map is
in one place (reverses Decision 1 for now). They sit in their own section, **Course maps – remove
after PDC** (`1613:11299`), below the second row, numbered `C01`–`C04` so the set numbering is
untouched. Delete the section after the course. 23a Resilience brainstorm stays in the set.

| # | Sheet | Built from | Notes |
|---|---|---|---|
| C01 | Zones brainstorm (`1613:11300`) | 12a Zones + the original's five note callouts | Key retitled "Zones Key". The key covers the original top-left notes, so Zone 3's note joins the bottom band and Zone 4's sits at the top of the Zone 04 region. |
| C02 | Contour practice (`1613:14124`) | 07a + original overlays and `Contour Practice` key | The 18 flow and drainage arrows lived inside the old base-map frame; they're in a `flow arrows` frame in `annotations`. |
| C03 | Water brainstorm (`1613:14247`) | 07a + original overlays and `Water Brainstorm` key | |
| C04 | Soil brainstorm (`1613:14461`) | 07a + original overlays and `Soil Brainstorm` key | Sample 1's marker sits half under the key, as in the original. |

All four use the `Lot 86 / base map` instance, the Lot 86 site legend (title and date from the
original), and `Sheet=Light`, `Map display=Labels off` like 12a. Overlays keep their original
positions, so they can sit a few pixels off plants that moved. The originals are marked
`OLD – see Map Set C0N`.

### File reorganized (2026-10-20)

With every map on the Map Set, the per-topic pages no longer held anything unique. The file now
has eight pages; `design-language/README.md` lists them.

1. **Snapshot first.** Andrew saved the Figma version "Before reorganization: style inventory and
   per-map pages". It keeps the Keys page's Inventory section (the style inventory that led to
   the Styles page) and the OLD frames for case-study screenshots.
2. **Documentation components** on Components > Documentation: `doc-header` (`1736:41`, Label and
   Date), `doc-title` (`1736:282`, Title, Body, Show body), `doc-section-label` (`1736:1524`, same
   properties, 320 wide). Sizes and colors copy the Styles docs' raw Inter 13/18/36; the file's
   text styles are slide-sized, so none fit.
3. **Styles:** the `_Status`/`Divider`/`Content` frames and 41 `Description` labels are now
   instances. The single `Styles` section split into one section per doc.
4. **Components** gathers every main component from Keys and Base Map. The Base Map `Legend` frame
   is renamed `base-map-symbols`.
5. **Data Visualizations** keeps one copy of each chart. Dropped as duplicates: the Water page's
   chart frame, Solar Paths' larger sun charts, Sector Analysis' loose 3D scene.
6. **Map Set** sheets are grouped into sections by kind; sheet names and numbers are unchanged.
7. **Deleted pages:** Keys, Base Map, Solar Paths, Elevation, Sector Analysis, Water & Watershed,
   Soil, Species, Site Data Visualizations. None held a main component when deleted.
8. **Section fills are white** (`neutral/White`) on every page, 2026-10-21. Some were #454545 and a
   few nested chart sections were #FCFCFA.
