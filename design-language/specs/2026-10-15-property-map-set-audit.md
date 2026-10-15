# Property map set: audit

**Date:** 2026-10-15
**Status:** Audit done. Andrew answered the open questions the same day, and the legend fixes in
**Changes made** are applied. The design spec comes next.
**Scope:** personal project, so there's latitude to be opinionated.

## Goal

Andrew wants a standalone **property map set** (decided 2026-10-15). It is a set of maps that presents a
property's analysis to its owner, separate from the slide decks. Every map uses the same canvas
and the same key and legend format. The set includes:

- lot maps drawn over the base map
- regional maps: watershed, bioregion, hardiness zone
- overlays on aerial imagery, such as solar paths

Slides keep their own layouts. Screenshots inside multi-column slides can stay.

## Decisions so far (2026-10-15)

1. **The map sheet is the shared unit.** Every sheet has four layers:
   1. map content
   2. annotations frame: lines, regions, captions, badges
   3. key
   4. legend
2. **Map content comes in three kinds:**
   - **Property:** an instance of the grayscale base map component.
   - **Regional:** a source image or redrawn map.
   - **Overlay:** aerial imagery with drawn layers on top.
3. **One base map component**, built from the grayscale map:
   - All plants are `Vegetation` instances named by plant ID.
   - Plants are drawn canopy first. The Lot 86 boundary sits above the plants.
   - Plant labels turn on or off per sheet through a boolean variable mode.
4. **Species maps override plant fills** inside the base map instance. They don't hide the base map's
   plants and draw their own.
5. **Where things live:**
   - The library holds the building blocks.
   - Lot 86's set stays in the library as the demo.
   - Each real property gets its own Figma file that uses the library.
   - A checklist of the maps in a set goes into `template/` once the set has worked for Lot 86.
6. **Order:**
   1. sheet template
   2. base map component
   3. species maps
   4. other lot maps
   5. regional and overlay sheets

   This replaces the 2026-10-14 order, which put the regional style first and the base map cleanup last.
7. **The color base map is kept as is** for now. It may come back later as a variable mode instead of a copy.

## Inventory

File: Site Toolkit Design Language. "Veg" counts `Vegetation` instances (the current plant
component). "Old" counts the older per-type plant components: deciduous tree, coniferous tree,
shrub, hedgerow, perennial.

### Lot maps (property kind)

| Page | Frame | Node | Plants | Key | Legend title | Date | Location shown |
|---|---|---|---|---|---|---|---|
| Base Map | Full Color + Detail Base Map | `155:3976` | 78 veg | — | sector compass map | July 2026 | no |
| Base Map | Base Map North @ -65.43˚ | `168:3180` | 79 veg | — | sector compass map | July 2026 | no |
| Resilience Brainstorm | Base Map North @ -65.43˚ (loose parts) | `1382:8378` | 79 veg | loose frame | loose `map-legend` instance | — | — |
| Zones & Microclimates | Current Zone Map Image | `189:2268` | 71 old | Zones – Current | current Microclimate map | August 2026 | no |
| Zones & Microclimates | Current Zone Map Base Map – August 2027 | `189:2269` | 71 old | Zones – Current | current Microclimate map | August 2026 | no |
| Zones & Microclimates | Microclimates | `1382:10661` | 79 veg | — | current Microclimate map, over a stale "sector compass map" legend | August 2026 | **yes** |
| Zones & Microclimates | Zone Circulation (1938 wide) | `1382:10660` | 79 veg | — | current zone map, over a stale legend | August 2026 | **yes** |
| Zones & Microclimates | Zones Brainstorm Map | `1382:11309` | 79 veg | — | Zones brainstorm map, over a stale legend | August 2026 | **yes** |
| Sector Analysis | Sector Compass Diagram – Base Map | `169:3793` | 71 old | Sector Compass (Tints) | sector compass map | July 2026 | no |
| Sector Analysis | … [Dark] | `169:4139` | 71 old | Sector Compass (Shades) | sector compass map | July 2026 | no |
| Water & Watershed | Site Water Flow Map | `238:3573` | 79 veg | Site Waterflow Map | Site Water Flow Map | August 2026 | no |
| Water & Watershed | Design Site Catchment Area Map | `238:4187` | 79 veg | Catchment Area | Design Site Catchment Area Map | August 2026 | no |
| Water & Watershed | Contour Practice Map | `238:4171` | 79 veg | Contour Practice | Contour & Water-Flow Practice | August 2026 | no |
| Water & Watershed | Midterm Water Brainstorm | `244:2129` | 79 veg | Water Brainstorm | WATER BRAINSTORM | August 2026 | no |
| Soil | Soil Brainstorm | `364:823` | 79 veg | Soil Brainstorm | Soil Building Goals Brainstorm | "SEPTEMBER2026" | **yes** |
| Soil | Soil Sample Site | `368:1605` | 79 veg | Soil Sample | Soil Sample Locations | "SEPTEMBER2026" | **yes** |
| Species | Species – Status | `1397:1531` | 71 old | Species – Status | species status map | October 2026 | no |
| Species | Species – Layer | `1397:2075` | 71 old | Species – Layer | species layer map | October 2026 | no |
| Species | Species – Function | `1397:2664` | 71 old | Species – Function | species function map | October 2026 | no |
| Species | Succession | `1416:5867` | 79 veg | Succession | identifying succession | October 2026 | no |
| Species | Thematic Design | `1416:6474` | 79 veg | Thematic Design | thematic design | October 2026 | no |

### Aerial and regional maps

| Page | Frame | Node | Content | Key | Legend |
|---|---|---|---|---|---|
| Sector Analysis | Sector Compass – Neighborhood, North Up | `129:1019` | sector diagram | Sector Compass (Tints) | `map-legend`, but with the lot's scale and rotation |
| Sector Analysis | … [Dark] | `155:2782` | same | Sector Compass (Shades) | same |
| Sector Analysis | Sector Compass – Community, North Up | `129:1020` | sector diagram | Sector Compass (Tints) | same |
| Sector Analysis | … [Dark] | `155:2916` | same | Sector Compass (Shades) | same |
| Water & Watershed | Macrowatershed | `1382:11448` | aerial image + drawn watersheds | hand-built frame named "Sector Compass Key" | hand-built bar: title, "100M" scale, author, date |
| Water & Watershed | State Watershed | `1382:11450` | same | same | same |
| Solar Paths | Frame 38 | `1382:9032` | aerial image + sun paths (1856×839) | hand-built "Sun Path Key" | none |

### Missing from the file

- **Bioregion and hardiness zone maps.** The Regional Maps page (`1382:11587`) is empty.

### Not maps (out of scope for the set)

- Charts:
  - `Sun Data Visualized` (`1382:11592`)
  - Water Related Data Visualizations (`1386:5954`, `1386:5955`)
  - sun-path and wind-rose frames on Site Data Visualizations
- Loose keys:
  - `Sector Compass Key` (`1382:8981`, `1382:8672`)
  - `Sector Regions` (`1382:8661`)
- Profiles:
  - Elevation Profile A–B (`1442:1695`)
- `Frame 1` on Elevation (`1416:6574`): elevation cross-sections (two profiles, USGS 3DEP).
  It's a visualization, not a map sheet. It sits with the elevation profile.
- `scene` (`174:5469`) on Sector Analysis: 3D sun-path scene. It's a visualization, and a candidate
  overlay sheet.
- `Frame 9` (`125:338`): reference images of other designers' sector analyses. It's slide material only.
  Not part of any property's set.

## Findings

1. **The base map carries its own legend.** Both base map frames include a `map-legend` titled
   "sector compass map", dated July 2026. Every copy brings that legend along. On the three newer Zones
   maps it sits directly under the real legend, in the same position. This is where most of the name
   and date drift comes from. The base map component must not contain a legend.
2. **Four plant inventories exist:**
   - 78 `Vegetation` instances on the color base map
   - 79 `Vegetation` instances on the grayscale map and its 13 copies
   - 71 old-component plants on 7 maps (Zones ×2, Sector ×2, Species ×3)
   - the 71 named plants in `mapped-plants.csv`, which the species maps use

   The base map component needs one list, reconciled against the CSV.
3. **Legend fields that are the same on every map are typed by hand on every map.** Scale, north
   rotation, elevation, area, and author are retyped each time:
   - Succession and Thematic Design show elevation 103–107 ft.
   - Every other map shows 106–114 ft.
   - The North Up sector maps show the lot's 1" = 20' scale and −65.43° rotation, which can't be right for
     north-up neighborhood and community imagery.

   These values should come from one source per site, such as a site-info variable collection.
4. **The location field shows on 5 maps:** Microclimates, Zone Circulation, Zones Brainstorm, Soil
   Brainstorm, and Soil Sample Site. The default is hidden, so each one needs a reason.
5. **Canvas sizes differ.** Lot maps are 1920×1080, except Zone Circulation at 1938. Frame 38 and the
   elevation frames are 1856 wide, which is the slide template's content width.
6. **Regional and overlay maps don't use the library legend or key.** Their legend bars and keys are
   built by hand. One key is still named "Sector Compass Key" from a copy, and the "100M" scale label
   doesn't name its unit clearly.
7. **Dark variants exist only for sector maps.** The set needs a decision on whether dark is part of
   the standard.

## Andrew's answers (2026-10-15)

1. **Location:** hidden on every legend. Andrew re-enables it in a later review where a map needs it.
2. **Elevation:** 103–107 ft, the more accurate figure, on every lot legend.
3. **Scale and north:** the legend keeps north variants (tilted and north up) and gains **scale
   variants**:
   - All lot drawings share one scale (1" = 20').
   - Regional maps will each need their own scale.
   - A planned **zoomed-in garden drawing** (a new map type, for garden detail) will need a
     larger scale too.
4. **No drafts in Figma.** Everything there comes from a real slide or visualization, so every frame
   counts. The three frames I couldn't classify are listed under **Not maps**.
5. **Source images:**
   - Bioregion and hardiness zone appear only as screenshots in slides.
   - Andrew has the source images in iCloud.
   - A source-image folder for map backgrounds and overlays is proposed below.
6. **Dark variants are part of the standard set.** Some maps read better with dark or light captions.
   Sector maps use dark variants to keep contrast over full-color satellite imagery. Over the grayscale
   base map, light variants work better.

## Changes made (2026-10-15)

- `map-legend` (`168:1310`, Keys page) has a new **`Show location`** boolean, default off, bound to
  the location field. The field is hidden in the component.
- The `map-legend` elevation text is now `Min: 103 ft Max: 107 ft`.
- All 28 legend instances across 7 pages are verified: location hidden and elevation 103–107 ft. No
  instance had overridden either value, so the component change reached all of them.
- Soil legends (`364:1108`, `368:1892`):
  - date corrected to "september 2026"
  - date text set back to auto width

Andrew publishes the library for these to reach slides.

## Still open

1. **Nine legends overflow the 1920 frame.** Long titles push the row past the frame edge:

   | Legend | Right edge |
   |---|---|
   | Soil Building Goals Brainstorm | 2110 |
   | Design Site Catchment Area Map | 2038 |
   | Contour & Water-Flow Practice | 2024 |
   | current Microclimate map ×2 | 1981 |
   | Soil Sample Locations | 1981 |
   | current Microclimate map (Microclimates) | 1952 |
   | species function map | 1937 |
   | identifying succession | 1923 |

   Several of these set the date to wrap, which looks like a workaround. The fix belongs in the
   component (for example, two-line elevation like area, or a tighter gap), and the sheet spec
   will settle it.
2. **Source-image folder.** Proposal, following the site repo's media rule (raw media in iCloud,
   never git-tracked):
   - The images live in a per-site iCloud folder, such as `map-sources/`.
   - The site repo tracks a manifest at `site-plan/maps/sources.md`. Each entry lists:
     - the file path
     - the source and provider
     - URL and capture date
     - attribution or license
     - the Figma frame that uses it
   - The attribution column feeds the legend's source-credit field on regional sheets.
   - `template/` gets the same manifest once Lot 86's version works.
