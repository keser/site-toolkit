# Context map set: documented satellite, community and historic views

Status: approved 2026-10-24; R1 built. Southern New England (R6) is the top of the series; no world view.

## Goal

Replace the screenshot-based context views with standalone, full-screen map sheets built from
documented public sources. Every sheet records its source, capture date and a computed scale. The
toolkit and microsite use these sheets. The course slides keep their mixed text-and-map layout;
afterwards the owner swaps each slide screenshot for a crop of the same source image.

## Decisions so far

- **Public data, not Google Earth** (owner, 2026-10-23). Google Earth stays only for views it alone
  can make (the tilted 3D capture on 09.2).
- **One sheet per view**, in the existing map-sheet template (legend with title, scale, north, source,
  date), in Figma's `Regional & overlay` section next to 01 to 06.
- **Scale comes from the data.** Every source below is georeferenced, so the scale bar and north
  arrow are computed, not read off a screenshot.

## The sheets

| # | Sheet | Extent (about) | Source | License | Replaces |
|---|---|---|---|---|---|
| R1 | Site, satellite | Lot plus 100 ft, base map frame (5.79 px/ft, north at −65.46°) | CT ECO 2023 orthoimagery, 3 in | CT State GIS Office, public | Base map's hidden `Aerial_Photo` screen capture; the aerial layer under 24a–30a and 09 |
| R2 | Neighborhood, satellite | 0.5 mi across | CT ECO 2023 ortho | public | 06 Sector compass background; microsite "The Neighborhood" card |
| R3 | Community resources | 8 mi across (Portland, Middletown, Cromwell, East Hampton) | NAIP 2023, 1 m, plus the nine resources from course slide 58 | USDA, public domain | Slide 58 map; 05 Sector compass background; microsite "A Brief History of Portland" card |
| R4 | County | Middlesex County, 82 × 46 mi frame | Sentinel-2 cloudless 2016 (EOX), lines from Census TIGERweb 2020 | CC BY 4.0; TIGER public domain | (new) |
| R5 | State | Connecticut, 205 × 115 mi frame | Sentinel-2 cloudless 2016 (EOX), TIGERweb 2020 lines | CC BY 4.0; TIGER public domain | Slide 10 state view |
| R6 | Region | Southern New England and Long Island Sound | Sentinel-2 Cloudless 2016 (EOX) | CC BY 4.0, credit "Sentinel-2 cloudless – https://s2maps.eu by EOX IT Services GmbH (Contains modified Copernicus Sentinel data 2016)". Later years are CC BY-NC-SA 4.0, so 2016 keeps the license simple | Slide 10 world/region view |
| H1 | 1934 aerial survey | R2's neighborhood frame | UConn MAGIC's 1934 mosaic (CT ECO `Mosaic_1934_MAGIC`): Fairchild Aerial Surveys, spring 1934, originals at the CT State Library | no terms stated; private until confirmed | Slide 13 (frame 09180, the same survey) |
| H2 | 1990 color infrared | R2's neighborhood frame | CT DEP 1990 CIR, frame 0585, Keystone Aerial Surveys, Aug 1990, UConn Library MAGIC (scanned PDF) | state agency record served by MAGIC; credit as MAGIC asks (to confirm on their site) | Slide 14 and 159; microsite "Historic Images (1990)" |
| S1 | Lidar terrain | 820 × 461 ft around the lot | CT 2023 lidar (already fetched) | public | Ties to 28a; microsite option |

Each sheet gets an inset locator (small outline of the next view up) so the series reads as a zoom
from region to lot.

## Community resources (R3)

From course slide 58: hospital (2.5 mi), fire department (0.6 mi), gas station (0.4 mi), grocery
store (0.6 mi), population center (1.6 mi), public space (1.1 mi), town hall and zoning (0.3 mi),
farm supply store (4.1 mi), building supply store (3.5 mi), plus "beyond the map" notes (UConn
Extension in Haddam, CT River Coastal Conservation District). The slide has categories and
distances but not the places' names. Each needs a name and location, plotted as a numbered marker
with the map-marker component, and a table on the sheet: number, resource, name, distance by
road. Distances are recomputed from the plotted points (straight line) and noted as such, unless
the owner wants road distance.

## Build steps

1. **Fetch.** Extend `tools/fetch_ct_eco.py` with a custom box size and the `Historic_1934` and
   `NAIP` layers at coarser pixel sizes. Add a small `tools/fetch_s2cloudless.py` (EOX WMS, 2016 layer) for
   R6. Download the MAGIC 1990 PDF and extract the raster. Tests for the new box and layer
   options, as for the existing ones.
2. **Render.** One script in the Lot 86 repo (`site-plan/data/context_maps_build.py`) writes each
   view as a sheet-ready image plus a JSON of lot outline, markers and scale-bar length in pixels.
   R1 renders in the base map frame so it drops under the base map and every derived sheet.
3. **Figma.** Build sheets R1–S1 from the template; scale bars and north arrows from the JSON;
   source and date in the legend; new `map-key` variants where a sheet needs one (resources,
   historic). Swap R1 into the base map component as the aerial layer.
4. **Sources.** One row per image in `site-plan/maps/sources.md`, with URL, date and license.
5. **Microsite.** Use R2, R3, H1 and H2 in the home page history cards, R5/R6 if a region view is
   wanted; credits on each.
6. **Slides (owner).** Swap the course-deck screenshots for crops of the same images.

## Not in scope

- Unique site photos (zone strengths, zone 1 photos) and found images without a known source, such
  as the 1930s main-street flood photo from the town Facebook group (slide 55). Those stay with the
  owner until a source is found; nothing without a known source is published.

## Open questions for the owner

1. **Resource names.** The nine places behind slide 58's markers (name or address for each).
2. **Hurricane date (answered 2026-10-24).** The 1938 New England Hurricane. The slide 13 photo is
   not from it: its caption reads "Aerial survey of Connecticut 1934 photograph 09180, Fairchild
   Aerial Survey Co Apr 1934", a 1934 statewide grid frame, and it already shows the quarries
   flooded. The owner used it by mistake (confirmed 2026-10-24). The course needs real 1938 damage
   photos: the CT State Library's 1938 Hurricane Aerial Photographs
   (https://libguides.ctstatelibrary.org/hg/aerialphotos/1938), 132 oblique views flown Sept 23–24,
   1938, including the Connecticut River to Cromwell. Open: which items show Portland, and each
   item's rights statement. The library's catalog sites (CT Digital Archive, CONTENTdm) refused
   connections on 2026-10-24, so the search waits. Frame 09180 can still serve as a 1934 "before".
3. **Flood photo.** The source of the slide 55 photo, if it can be traced.

## Progress

- **R1 Site – satellite (2026-10-24).** `context_maps_build.py` in the Lot 86 repo writes
  `context/r1-site.jpg` and `context.json` (5.79 px/ft, north −65.46°, 40 ft bar = 231.7 px). The
  sheet sits in `Regional & overlay`. The base map's aerial layer now holds the same image, and the
  unsourced 2026-07-03 screen capture is hidden in both variants.
- **Scale bar fixed (2026-10-24).** New `map-scale` variant `Scale=Base map` draws 40 ft at the
  computed 231.7 px. All 24 sheets that used `Scale=Lot` (every base-map-frame sheet, the template and
  the course sheets) now use it. `Lot` is unused; `Garden detail` (22, 30a) is not yet checked.
- **R2 Neighborhood – satellite (2026-10-24).** CT ECO 2023 ortho, north up, fetched with the new
  `fetch_ct_eco.py --width-ft --height-ft --pixel-ft` options. Each regional sheet picks its extent so
  a round distance spans the fixed 234 px bar (here 300 ft, 0.78 px/ft), instead of resizing the bar.
- **R3 Community resources (2026-10-24).** NAIP 2023 true color, 1 mi = 234 px, framed so the points
  sit left of a new `map-key` variant (Default / Community Resources). Places come from slide 58: the
  slide map was fitted to NAIP by matching water (93% overlap) and each marker matched to
  OpenStreetMap; the owner confirmed them and named marker 8 as Tractor Supply. Road distances are
  re-routed from the lot with OSRM; changed from the slide: hospital 2.5 → 2.4 mi, gas 0.4 → 0.3, population
  center 1.6 → 1.7, public space 1.1 → 0.8 (to the park entrance), farm supply 4.1 → 3.9, building supply
  3.5 → 3.6. The two off-map resources are a note in the key, as the owner asked.
- **R4 Middlesex County and R5 Connecticut (2026-10-24).** NAIP was fetched first and dropped: it
  stops at the state line in blocky tiles and stripes Long Island Sound. Both sheets use Sentinel-2
  cloudless 2016 (`tools/fetch_s2cloudless.py`, EPSG:4326, reprojected into State Plane), with Census
  TIGERweb 2020 lines. Scales: 10 mi and 25 mi on the 234 px bar. R4 outlines R3's frame; R5 outlines
  Middlesex County. New `map-key` variants County and State carry the full CC BY credit. The TIGER
  lines are legal boundaries, so they run into the Sound.
- **R6, S1, H2 (2026-10-24).** R6 Southern New England: Sentinel-2 cloudless 2016, 50 mi = 234 px,
  CT/RI/MA lines strong and neighbors faint. S1 Lidar terrain: bare earth tinted 88–122 ft under a 3×
  hillshade, 1 ft contours with 5 ft index labels, 100 ft = 234 px. H2: the MAGIC 1990 frame 0585,
  registered to NAIP by matching water (`cir_1990_fit.py` in the Lot 86 repo) and resampled into R2's
  frame so the two compare directly; phase correlation against R2 puts it within about 5 ft near the
  lot. MAGIC states no reuse terms, so H2 stays out of the public microsite until they confirm.
- **Left:** H1 (waits on a working 1938 source), the microsite step, and the owner's slide swaps.
- **H1 reset to the 1934 survey (owner, 2026-10-24).** No overhead grid survey of the 1938 hurricane
  was found, only low oblique shots of buildings and waterways, so the hurricane map is dropped. H1
  is now the oldest overhead view of the site: MAGIC's 1934 mosaic in R2's frame, so 1934, 1990 (H2)
  and 2023 (R2) line up. CT ECO's `Historic_1934` service has no frames over Portland. The mosaic
  is built from separate tiles and sat about 75 ft off here: corrected by matching the quarry and
  river shorelines, then the lot's street (`mosaic_1934_fit.json`). Flood history stays on the course
  storm slides; the owner is tracing that photo's source.
- **Publishing:** H1 and H2 have no stated reuse terms (MAGIC; CT State Library), so both stay out of
  the microsite until confirmed. R1–R6 and S1 are clear to publish with their credits.
- **Published (2026-10-24).** Home: R3 and R2 in the history cards. Base map page: R1. Climate page:
  R4–R6 as a regional series, and R7 in the bioregion panel. Water page: S1. H1 and H2 wait on reuse
  terms.
- **R7 Bioregion (owner chose option A, 2026-10-24).** One Earth's NA10 is RESOLVE Ecoregions 2017
  #335, #338, #339 (CC BY 4.0), so R7 traces their union on Sentinel-2 cloudless 2016, 250 mi = 234 px.
  One Earth gets credit for the grouping and name; its own map image (sheet 01) stays unpublished.
- **S1 on the Ramps (owner, 2026-10-24).** The elevation tint is now Map Semantic `terrain/low`, `mid`,
  `high` (sage/100 → gold/50 → gold/200), and the contours are slate like 28a's. See
  `2026-10-24-map-semantic-tokens.md`.
