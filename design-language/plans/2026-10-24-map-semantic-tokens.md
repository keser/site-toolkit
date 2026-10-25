# Map Semantic tokens and token QA

Status: built 2026-10-24.

## Why

A token QA after the context map set found map color scales defined as hex copies. The Python
build scripts held one copy and the Figma keys another, with the Ramps step only in a comment. The
sun-hours scale was written out twice (shade and roof solar), and S1's contours had already
drifted: the map lines were `#5b4a32` and the key swatch `#5c4a33`. Neither color was on the Ramps.

## Decisions

| Question | Chosen | Why |
|---|---|---|
| Alias the other map color systems? | **Yes, for scales shared by a raster and a key, or by two sheets.** Not one token per map. | That is where copies drift. Per-map tokens would only rename the Ramps. |
| External palettes (USDA hardiness zones, colors sampled from the 1990 CIR photo) | **Stay raw**, with their source noted | They describe outside data; snapping them to the Ramps would misrepresent it. |
| S1 elevation tint (owner, 2026-10-24) | **Moves onto the Ramps:** sage/100 → gold/50 → gold/200 | Compared with sage/100 → gold/50 → amber/200 (high ground turns peach) and sage/50 → gold/100 → amber/100 (turns pink). gold/200 keeps the low-green, high-gold look closest to the old tan. |
| Contour color | **Slate, as 28a already used:** 1 ft slate/400, index slate/600 | Two terrain sheets, one contour system. S1's brown was the outlier; dark gold/800 was considered and dropped so one token serves both sheets. |
| Boundary lines in keys (R4–R7) | **Ramps primitives**, as other keys do: `neutral/Black`; faint "other areas" charcoal/400 (NA10 ecoregions charcoal/500) | Lines over imagery are `neutral/White` at reduced opacity; the key's grey stands in for that. A new Sheet `mark/secondary` was considered; existing keys bind primitives directly, so it wasn't added. |

## Built

- **Figma `Map Semantic`** collection (`VariableCollectionId:2030:2`, one mode, `Value`), 13 colors
  aliased to the Ramps, scoped to fills and strokes, with WEB code syntax `var(--map-…)`:
  - `sun/full-sun`, `part-sun`, `part-shade`, `shade`: gold/100, gold/300, slate/400, slate/700.
  - `vigor/bare`, `sparse`, `moderate`, `dense`: charcoal/100, sage/100, sage/300, sage/600.
  - `terrain/low`, `mid`, `high`: sage/100, gold/50, gold/200.
  - `terrain/contour`, `contour-index`: slate/400, slate/600.
- **Mirror:** `tokens/map.json`; `tools/tokens.py` resolves it (and `species.json`) through
  `ramps.json` for raster renders; `tools/tests/test_tokens.py`.
- **Lot 86 build scripts** (shade, roof solar, vegetation index, canopy height, S1) read colors by
  token name. Every raster except S1 re-rendered byte-identical; the shade and imagery reports now
  name the token instead of the Ramps step.
- **Figma bindings:**
  - The Sun Hours, Shadow Study, Roof Solar, Vegetation Index, Terrain and Lidar Terrain key
    variants now use Map Semantic. S1's elevation swatch is a gradient with stops bound to
    `terrain/*`.
  - S1's and 28a's contours use `terrain/contour*`.
  - The County, State, Region, Bioregion NA10 and CIR 1990 key lines use the Ramps (raw before).
  - `map-site-marker` digits use `neutral/White`, and so do the label backgrounds on S1 and R7
    (still 85%).
- **S1 re-rendered** in Figma and on the microsite (`docs/assets/context-terrain.jpg`).

## Left open (from the QA)

- No variable outside Map Semantic has code syntax (170 of 183).
- `neutral/White` and `neutral/Black` are scoped to every property; narrowing to fills and strokes
  is safe once checked against effect bindings.
- `check_chart_tokens.py` hard-codes chart hex pairs; `species.json` resolves through the Ramps,
  which is the better pattern.
- `palette_check.py` crashes without arguments instead of printing usage.
- Older sheets still carry raw paints: 03/04 Watershed (45 each), 09.1 Sun path 3D scene (171),
  02 Hardiness zone (USDA colors; stay raw by the rule above).
- The CIR 1990 key swatches stay raw: they are sampled from the photo.
- The sun-path preview image in the Lot 86 repo (`preview-*.jpg`, local check only) uses its own
  season colors, not `Chart Semantic` `season/*`.
