# Toolkit usage audit (after Lesson 9)

Date: 2026-11-15. Scope mode: personal project, opinionated. Read-only audit of how the Site
Design Toolkit library is applied in the Lot 86 site file, the PDC deck (last 70 slides) and the
microsite. Outcome: the toolkit floor in `2026-10-15-map-sheet-design.md` ("Toolkit floor") and
the Phase 0 sweep below.

## What holds up
- Every color variable aliases a Ramps step; the JSON mirrors and `check_chart_tokens.py` catch drift.
- Current sheets (`NNa`): 440 paints bind `Sheet`, and nearly every text node has a style.
- All 59 sheet borders bind `Sheet / panel/border` at 6 px.
- The site file has no local styles or variables.

## Findings

### Property – proposed (Lesson 9 concept sheets)
- Raw paints: 32b 28 of 69 fills and 25 of 110 strokes; 34b 14 of 18 fills; 36b 18 of 22 strokes.
  Values are Figma defaults (`#262626`, `#e6e6e6`, `#d9d9d9`) and translucent hues that match no
  Ramps step (`#61c3b7` at 25%, `#e748c1` at 25%).
- 24 distinct stroke weights, about 95% unbound to `Stroke`; scaled values (5.33, 10.67, 13.33)
  on detail sheets. Over 40 dash patterns.
- Template file still in use: `Pill` ×20 (the `zones` groups on 32b, 34b and their details);
  `TEMPLATE: PDC PRO / Black` and `Yellow 100` ×34 (22b's posts, gates and nursery bed, then
  copied with the rotation tunnel into 31b, 32b, 37b and details); `Custom Style / Color 1` on 14a.
- The six detail sheets replace the `content` layer with a view instance.
- All 12 concept sheets use local keys. Allowed for concept maps since 2026-11-15.

### Regional & overlay
- 449 paints bind Ramps directly. Allowed by the floor.
- 69 unstyled text nodes, including 24 in Inter 7.2.

### Site Profile
- About 700 unstyled text nodes in about 50 fractional sizes, mostly Inter. The microsite's
  charts use JetBrains Mono through four `--chart-font-*` tokens; Figma has no matching styles.
- 1,391 of 2,154 solid paints raw (65%).

### Deck (last 70 slides)
- 334 of 1,401 text nodes unstyled (Inter 16, 20, Italic 16).
- 2,129 color bindings to local `TEMPLATE: PDC PRO` collections (three duplicate copies of 18
  variables) against about 300 to the toolkit.
- 22 local text styles, including `Mono/16/Bold` three times and Caption and Label families the
  toolkit lacks.

### Library
- 33 text styles, all slide-sized. 23 are a JetBrains Mono size × weight × case grid, named by
  size. Mono line heights are `auto`.
- Inter body styles track −4% at every size, 16 px included (Inter's guidance is about −1% at
  16 px). Caps labels have 0 tracking. Body LG is 40/40.
- No tier below slide size, so the doc components use raw Inter 13/18/36.
- No spacing, radius or size variables. `Map display / plant-labels` uses `ALL_SCOPES`.

### Microsite
- Page text is `system-ui`. About 220 raw `font-size` declarations. No typography JSON, so the
  check can't see type drift.

## Phase 0 sweep log (2026-11-15)

**Property – proposed** (16 sheets) swept to the floor:
- Raw paints were bound to the nearest Ramps step when ΔE < 5. Most were exact Ramps hex pasted
  in. `#262626` → charcoal/800, `#e6e6e6` and `#d9d9d9` → charcoal/100, `#cccccc` → charcoal/200.
  Compost `#d9bf8c` → gold/100 (ΔE 12, Andrew's call).
- Template variables were rebound to toolkit targets: `Black` → neutral/Black, `Neutral 500`
  (an alias of charcoal/800) → charcoal/800.
- `Pill` ×8 → toolkit `caption` (Black, LG). Their template main component no longer resolved,
  so they rendered empty.
- Stroke weights were bound to `Stroke`. Detail sheets use Option A (Andrew): each stroke takes
  its overview counterpart's token, matched by layer path, so a token means the same width on
  every sheet. Dot rows are exempt.
- Raw JetBrains Mono Bold 16 labels → `Mono/16/Bold`.

**Library:**
- New `alpha/violet-500-25` and `alpha/white-85`.
- `caption` fills and text bound (the White style uses `alpha/white-85`). `roof-panel` strokes
  bound.

**Base-map symbols** default to grayscale (see the base-map component spec, amended 2026-11-15).

**Deck** (Option A, Andrew): 5,454 template-neutral bindings on all 269 slides were rebound to
Ramps: `Neutral 500` → charcoal/800, `Neutral 400` → charcoal/700, `Neutral 50` (cream) →
charcoal/50 (nearest, ΔE 2.9; pure white is the alternative), White and Black → neutral, `Accent 2`
→ sage/50. The template values were not aliases, so submitted slides shift by up to ΔE 5.1.
**Left for Phase 2:** the template accents, about 740 bindings (`Green 100` ×402, `Blue 100` ×300,
Yellow, Red, Green 500, Magenta). Retire them, or graduate them as slide accents. The three
duplicate `TEMPLATE: PDC PRO` collections stay until then.

**Finding:** a fill bound to a variable doesn't keep a manual paint opacity; it reads back at
100%. Any translucent color needs an `alpha/*` copy. This settles the Phase 1 alpha question.

**Gotcha:** instances inside a hidden frame don't load their children through the Plugin API.
Edit a clone in a visible frame, then move it in.

## Phase 1 log (2026-11-18)

### Inventory
Read-only pass over the site file's Map Set and the library's `map-key` (36 variants).
- Every reusable view but `24a Shadow study` and `26a Color infrared` already places a library
  key. The work was making those keys reusable, not creating them.
- **Lot 86 text in library rows:** "Lot boundary · 1993 plan, 0.43 ac" in nine variants; sector
  compass bodies (Route 17 & 66); catchment, microclimate, zone and succession descriptions; R-series
  source notes.
- **Raw swatches** in seven variants: Microclimates (four Ramps steps at 50%), Zones (violet/300 at
  25%), Macro and State watershed, the old Bioregion, Hardiness, CIR 1990, Aerial 1934. Plus 37 raw
  white overrides on marker numbers inside key rows. A scan has to walk into instances to see those.
- `H3 Aerial survey 1957` used the `Aerial 1934` variant. The sector compass's winter and summer
  sun rows carried the wind rows' text.
- **Watershed:** 03 and 04 share identical rows, but each map is a Google Earth raster with its
  own HUC colors (HUC 8 is mauve on 03, pink on 04), so no single key matches both. A hidden vector
  "nested scale" graphic on both uses cobalt/700, coral/300, gold/400, magenta/400.
- On imagery, charcoal markers (R3) and white-outline-only ecoregions (R7) lose contrast.

### Decisions (Andrew)
1. Reusable list: the spec's fifteen plus sun paths, succession, soil sample, zones, the regional
   placeholder set, lidar, and the historic aerials.
2. Industry palettes go in a new **Reference** collection, not Ramps.
3. Merge the watershed keys. Retire the old Bioregion for NA10, and give NA10 color fills. Add a
   high-contrast marker for imagery.

### Done
**Library**
- `Reference` collection: `usda-hardiness/5a`–`7b`, `cir-1990/vegetation|built|water`. Hardiness
  and CIR swatches bound.
- Ramps: `alpha/cobalt-700-50`, `alpha/coral-300-50`, `alpha/gold-400-50`. Microclimates swatches
  bound to them (and the existing `magenta-400-50`); Zones' zone 2 to `alpha/violet-300-25`; Aerial
  and Soil brainstorm black to `neutral/Black`; the 37 marker-number overrides to `neutral/White`.
  No pixel changed.
- Map Semantic `ecoregion/site|2|3` (gold-100, teal-300, violet-300, all at 50%).
- `map-site-marker` gains `Theme=Dark|Light`. Light: white fill, black stroke and number.
  Existing instances map to Dark. The cloned Light variants first lost the number text's link to `Number`; relinked 2026-11-18. Keys for Community Resources, County, State, Region and
  Bioregion use Light.
- Placeholder text in the eighteen reusable variants that named Lot 86. `Bioregion NA10` →
  `Bioregion` with three area rows (site's ecoregion, two neighbors); `Aerial 1934` →
  `Historic Aerial`; the old `Bioregion` variant deleted.
- Styles page: three alpha swatches, an Ecoregion block under Map semantic, a new Reference
  section, and its Contents entry.

**Site file**
- **Pinning before the text change** (superseded the same day by local keys, below). Setting a row property to the value it already has records
  no override, so an update would replace it. Setting it to a temporary value and back records one
  that survives. Done for every row, title and note in the 24 sheets whose key text changed.
- Sector compass (05, 06, 08a): winter sun path → "Low 25° winter arc through the southern sky;
  keep it open to the ground"; summer → "Near-overhead 72° summer sun; shade hot beds in the
  afternoon" (from the Lesson 3 sector analysis).
- R7: per-ecoregion fills under the outlines, from new per-ecoregion rings in the Lot 86 repo's
  `context_maps_build.py` (`ecoregion_<id>` in `context.json`; the JPG rebuilt byte-identical).
  Bound to the Ramps alphas until the library publishes, then to `ecoregion/*`.
- 01 Bioregion's key detached, so the old variant could be deleted. Its map has no stated license;
  R7 is the publishable sheet.

**Repo:** `tokens/ramps.json`, `map.json`, new `reference.json`; `--map-ecoregion-*` in
`chart-tokens.css`; `check_chart_tokens.py tokens` passes.

### Keys go local (Andrew, 2026-11-18)
In practice, keys driven from the library were slow to edit, and a map and its key have to change
together. All 36 `map-key` instances on the Map Set (17 regional, 18 current, 1 proposed) were
detached into local `key` frames. Rows stay `map-key-row` instances. The library variants stay as
placeholder examples. This is what the map-sheet spec's Key section planned on 2026-10-15.
- The first publish reached the site file before the detach. Pinning held on every row but R7,
  where the library inserted two rows and the pinned text shifted onto the wrong ones. R7's six
  rows were rebuilt locally, and its map fills rebound to `ecoregion/*`.
- A scan of all 214 rows for placeholder text found only hidden rows (zones 3–5 on 12a and 14a,
  09.1's lot boundary). Those were removed.
- Six titles on 25a–30a → `Mono/24/Bold`. The library gains `Mono/14/Regular` for key notes (no
  14 px style existed), with a Styles page row.
- `map-site-marker`: `Contrast` renamed to `Theme=Dark|Light`; Dark is now `neutral/Black`. The
  cloned Light variants had lost the number text's link to `Number`; relinked.
- 24a already has an inline key strip under its 3×3 grid. The inventory missed it because it isn't
  a `map-key` instance. A key panel added there covered the map and was removed.

### Floor sweep: reusable sheets (2026-11-18)
Swept to the floor, visible layers only: 09, 09.2, 12a, 14a, 20a, 24a. A final scan finds no raw
paint, unbound stroke or unstyled text on them.
- **Strokes:** 1→xs, 1.5→sm, 2→sm, 3→md, 3.5→lg, 4→lg, 5→lg, 6→xl, 8→2xl. Frames and instances
  store the binding per side (`strokeTopWeight`…), so a check that reads only `strokeWeight`
  over-reports.
- **12a and 14a paints:** exact Ramps hues and their 25% alphas; `#d9d9d9` → charcoal/100 (ΔE
  2.4). 14a's zone fills were teal-100 and violet-500 at 20% while its own key and 12a use
  `alpha/teal-300-25` and `alpha/violet-300-25`; the map now matches the key. Children inside the
  zone boolean shapes (old Zone 3–5 geometry) take their parent's token; their fills never render.
- **Template:** the visible zone 1 and 2 `Pill` labels on 12a and 14a → toolkit `caption` (Black,
  LG), text kept. 14a's five circulation labels → `Mono Caps/24/Medium`.
- **Left alone:** the hidden "zones 1–5 (superseded 2026-11-14)" groups on 12a and 14a, kept as a
  record. They still hold template Pills and raw fills.
- **Held:** 09.1 Sun path 3D scene. Its lines (0.4–1.21 px), 7.2 px Inter labels and three
  ground colors (ΔE 16–20 from any ramp) belong to a scaled 3D render; binding them to tokens would
  thicken every line. Needs a call: exempt it like dot rows, or rebuild the scene at 1:1.
- **Gotcha:** `fills` returns fresh objects on each read, so `fills.map(p => p === f ? … : p)`
  with `f` from an earlier read changes nothing and reports success. Replace by index, then read
  back.

### Andrew's calls, carried out (2026-11-18)
- **09.1 rebuilt at real sizes.** The scene keeps its 1200 × 760 footprint; its lines and labels
  no longer shrink with it. Hour marks, arcs and time-label frames take 09's tokens by layer name;
  grid lines and altitude rings → `xs`; degree labels → `Mono/14/Regular`; time labels →
  `Mono Caps/16/Bold`; three house-wall faces → charcoal 300/400/500.
- **Watershed sheets 03 and 04 redrawn from USGS.** WBD HU4 0108 → HU8 01080205 → HU10
  0108020507 → HU12 010802050702 and NHDPlus V2 rivers (order 5+ on 03, 4+ on 04) on Sentinel-2
  cloudless 2016, built like R4–R7 (Lot 86 `fetch_wbd.py`, `context_maps_build.py` `w03`/`w04`).
  Same details as the Google Earth versions; the areas match the old key (11,264 / 1,084.6 / 71.3 /
  51.5 sq mi). Lines reach Figma through `upload_assets` as SVG, then bind to tokens. Frames sit at
  a round scale across the 234 px bar (03: 100 mi, 04: 20 mi), because the legend's nested
  `map-scale` won't resize; legends swapped to the scaled site legend. New Map Semantic
  `watershed/basin|huc8|huc10|huc12` (25% alphas); outlines in the same hue. The library's two
  watershed keys merged into one `Watershed` example.
- **Inline key rows (24a, 26a).** A single horizontal row of `map-key-row` instances, taken from
  the library example and detached, replaces 24a's loose swatch-and-text strip and gives 26a a key
  under its reading notes. Rows need fixed widths: HUG collapses them, because their text fills.
- **26a colors** are the 2023 flights', not 1990's, so the Reference collection gains
  `cir-2023/vegetation|built|water`: median class colors sampled from the two panels.

### After the publish (done 2026-11-18)
Andrew published the library and site file. Markers on R3–R7 are `Theme=Light` (map and key); 26a's
swatches bind `cir-2023/*`; 03 and 04 fills and key swatches bind `watershed/*`.

### Open
- Floor sweeps still to do: the sheets not yet scanned (the rest of Property – current, regional, Site Profile).
- Remaining graduation: sector compass, water flow, catchment, succession, soil sample, and species
  function still bind Color Roles directly.

## Plan (Andrew, 2026-11-15)
Maps and slides first; the microsite and charts align later.

- **Phase 0 (now):** write the floor; sweep Property – proposed to it (one sheet first, with a
  mapping table approved before any change); rebind the deck's template colors to toolkit
  variables with the same values.
- **Phase 1:** inventory reusable map views and their keys; run the graduation routine; test
  whether a variable-bound fill keeps a manual opacity before adding `alpha/*` copies; a
  form-only drawing kit (weights, dashes, markers).
- **Phase 2 (after the course):** role-based type restructure. Renames are safe now; value
  changes wait, because Canvas submissions link to live deck sections and would re-render.
- **Phase 3:** align Site Profile chart text and microsite type tokens with four shared chart roles.
