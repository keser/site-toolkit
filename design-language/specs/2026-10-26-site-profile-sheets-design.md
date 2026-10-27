# Site Profile page and profile sheets — design

**Date:** 2026-10-26 · **Status:** built 2026-10-26 · Scope mode: personal project (HLSD),
opinionated.

## Why
The site file's Data Visualizations page had become a thinner copy of the microsite: the same
charts, without the findings or the links to maps. The owner reframed it. The toolkit produces a
**site profile**: the numeric, tabular, and visual findings for each category of a site. Each
profile has two outputs, built separately on purpose:

1. **The microsite**, designed for reading on the web: it scrolls, adapts to the screen, and can be
   interactive.
2. **Figma sheets**, one per map or chart at a fixed 1920×1080, for decks and for viewing one sheet
   at a time.

So the toolkit is two things: a design language for maps, and the assets for producing a site
profile across both outputs.

## Decisions
1. **Rename the site file's Data Visualizations page to Site Profile.** Its sections follow the
   microsite's pages and nav groups (Current state, Synthesis, Proposal), one section per page. My
   call: Wind folds into Climate and Elevation into Water, because that's where the microsite
   shows them.
2. **Every chart, table, or written finding gets its own profile sheet** at the map sheets'
   1920×1080. Each sheet is a component, so decks place it live, as they do map sheets. A category
   that leads to a map links to that sheet in the Map Set instead of copying it. A category with
   no map gets only charts or a written finding.
3. **Content that doesn't fit one sheet is split.** Water's charts (1856×3728 now) become two or
   three sheets. A long table (species inventory) gets a summary sheet that points to the full
   table on the web. Don't shrink type to make content fit.
4. **The library holds the template; the site file holds the sheets.** The library gets a profile
   sheet template next to the map sheet template `00`. It has the same canvas, legend strip, and
   tokens, with a chart area and a findings panel in place of the map and key. Site data stays out
   of the library, the same rule the maps follow.
5. **Sheet IDs use a prefix for each microsite page, then a number:** `SUN1`, `CLIM1`, `WATER1`,
   `FLOOD1`, `SECT1`, `SPEC1`, `SYN1`. Map sheet IDs (`R2`, `H3`, `NNa`) don't change.

## How the two outputs stay aligned
They are built separately, and some drift between them is intended. What must match is the
foundation, the way andrewkeser.com's front-end tokens track its Figma variables:

| Shared foundation | Where it lives | How it's kept |
|---|---|---|
| Color | `design-language/tokens/*.json` (Ramps steps per mode), the Figma collections, and the microsite CSS mirrors | `tools/check_chart_tokens.py tokens` (already exists) |
| Type | Library text styles and the microsite fonts | Same families and roles |
| Data | The site repo's data files and build scripts | Both outputs read the same numbers. A sheet's source note names the file |
| Findings | The microsite's "Findings for design" text | A sheet's findings panel quotes the page's findings, without rewording them |

Intended drift is fine: layout, interaction, chart size, dark mode on the web, splitting into
several sheets. A drift in the foundation is a bug: a different number, an off-token color, or a
finding that exists in only one output.

**Sync is a checklist, run on request** (like the project-plan page), not a generator. A script
that renders both outputs from one source would need a renderer for each, and it would break
whenever a chart's design changed. Revisit that for charts already generated from data (sun paths,
elevation profiles) if keeping them in sync by hand becomes a chore.

## Build order
1. Library: profile sheet template (and any chart key parts it needs). Publish.
2. Site file: rename the page, regroup its sections by microsite page, and rebuild each existing
   chart as a profile sheet component.
3. Deck: add a slide per profile sheet after the map sheets, grouped by section.
4. Docs: the toolkit README, `design-language/README.md` (site file pages), the toolkit and Lot 86
   CLAUDE.md files, and a "sync the site profile" checklist next to the project-plan sync.

## Built in the library (2026-10-26)
- **`00P Profile sheet template`** (`2168:2034`), a copy of `00`: the key shell at one column (485
  wide, title "Sheet title") at top left, a `profile-findings` instance under it, and the chart
  area (`content – chart area`, 1315 × 860 at (565, 40)). The legend hides scale, north,
  elevation, and area, and shows source; it's centered.
- **`profile-findings`** (`2168:2031`): a panel the width of a one-column key, with text
  properties `Title` (default "Findings for design") and `Body`. Body text is `Mono/20/Bold`,
  not caps, so a quoted finding reads as a sentence.
- **`map-legend` gets `Show scale & north`** (boolean, default on), bound to `map-scale` and the
  variant's own north arrow. Each variant's other north arrow stays hidden and unbound. Map
  sheets don't change.

## Site file sheets
Each findings panel quotes the matching page's findings that the chart supports, prefixed with
their quadrant (Strength, Weakness, Opportunity, Threat). Charts move in as they are, scaled to
the chart area; their title line moves into the key title.

| ID | Sheet | From (Data Visualizations) | Microsite page |
|---|---|---|---|
| SUN1 | Sun path charts | Sun path charts | sun-solar |
| SUN2 | Garden horizon and solar section | Garden solar analysis (top two) | sun-solar |
| SUN3 | Garden day length and roof | Garden solar analysis (bottom two) | sun-solar |
| CLIM1 | Climate survey | Climate survey charts | climate |
| CLIM2 | Seasonal wind roses | Seasonal wind roses | climate |
| WATER1 | Seasonal rain and precipitation | Water charts (first two) | water |
| WATER2 | Storms and runoff | Water charts (next two) | water |
| WATER3 | Water balance | Water charts (sankey) | water |
| WATER4 | Elevation cross-sections | Elevation cross-sections | water |
| WATER5 | Elevation profile A–B | Elevation profile A–B | water |
| FLOOD1 | Flood risk | Flood risk | flood-hazard |
| SPEC1 | Species inventory | Species inventory | species-inventory |

The Sun section's overlay and 3D diagram duplicate map sheets 09 and 09.1, so the page links to
those maps instead. Sectors has no chart; its section links to map sheets 05, 06, and 08a.

## Built in the site file (2026-10-26)
- The page is renamed Site Profile. Six sections (Sun & solar, Climate, Water, Flood, Species,
  Sectors) each have a doc header and title, a "Maps:" line whose names link to the map sheets,
  and the sheets three to a row. Contents and the Cover card point at them.
- The 12 sheets are components built from library parts: the key shell (title only; its rows slot
  is hidden), `profile-findings`, and `map-legend` (North=Up, scale and north off, source on,
  author heading "created by"). Charts are clones of the old sections' charts, scaled to the
  chart area.
- Course framing was removed from two chart captions on the way in: CLIM1's caption now quotes
  the climate page's source line instead of the course material it was digitized from, and FLOOD1
  drops a reference to course work.
- The old sections are kept below, named "Superseded – …", until the owner confirms they can go.
  The plugin API can't save a named version, so deleting them would rely on Figma's autosave
  history.

## Deck (2026-10-26)
One "Site profile" row of 12 slides, in section order, before "Property – proposed": the
profile describes the current state, so it comes ahead of the design. Each slide holds a live
instance of its sheet.

## Left to the builder
- The template's exact layout (chart area and findings panel proportions), within the sheet
  spec's canvas and legend rules (`specs/2026-10-15-map-sheet-design.md`).
- Which existing charts need splitting, judged on legibility at 1920×1080.
