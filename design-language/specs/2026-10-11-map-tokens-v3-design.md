# Map Tokens v3: Color Roles, Casing Lines, Dash Set, Component Cleanup

Status: built 2026-10-11, extended through 2026-10-14 (map keys, map migration, Slides template colors and text, deck text). Parked 2026-10-14 for the repo restructure; see **Pickup** at the end. Plan: site-plan/plans/2026-10-11-map-tokens-v3.md.
[2026-10-10-map-tokens-v2-design.md](2026-10-10-map-tokens-v2-design.md) (built; plan
[2026-10-10-map-tokens-v2.md](../plans/2026-10-10-map-tokens-v2.md)).

## Goal

Make the token system cover every line and fill treatment Andrew actually uses on the map keys of
the PDC Pro Vision Figma file (`aF9SVeTLwFN8PCEiU2OSBQ`). Andrew's two inventory frames on the
Keys page are the evidence: `line-inventory` (`708:4501`) and `fill-inventory`
(`699:2103`).

## What the inventories showed (2026-10-11)

- **Casing lines:** a weight-5 stroke in a mid-ramp step (cobalt/400, magenta/400, violet/400,
  gold/300) with a drop shadow 4px down, blur 1, in that hue's darkest step. `Line Sample` has no
  shadow option, and 5 isn't a weight tier.
- **Six dash patterns** are in use: `[2,2]`, `[4,4]`, `[8,8]`, `[12,8]`, `[14,8]`, `[16,9]`.
  `Line Sample` defines two.
- **Translucent fills** are exact ramp steps, mostly raw hex, at 10, 30, 40, 50, 80, and 100%.
  Some are not Tint (`cobalt/700 @ 50%` ×3, `gold/400 @ 50%`).
- **Region overlays** pair a translucent fill with a dashed border, usually weight 8.
- `Site Marker` still has an `Icon` instance-swap property though the icon variant was removed.
  `Dot / Hexagon` uses a raw fill and stroke instead of styles.

## Decisions (resolved 2026-10-11)

| Fork | Chosen | Why |
|---|---|---|
| Collection name | **`Color Roles`** (was `Map Overlay`) | Shade/Base/Tint are roles used by maps and potentially charts, not overlay-specific. "Theme" was avoided because it implies light/dark modes. |
| Translucent fills | **Always a ramp's Tint at 25% or 50%** | Matches how overlays are used; the 50-style set already covers it. |
| Dash set | **Fine `[2,2]`, Medium `[8,8]`, Coarse `[16,9]`** | Three distinct steps; others remap. |
| Hexagon marker | **Keep** | Andrew's call. |
| Casing shadow color | **`<hue>/Shade` (step 700)**, not the 800 step in the inventory | Keeps casing inside the role system; visually very close. |
| Casing line weight | **`lg` (4)** with a `Base` stroke, replacing weight 5 | 5 isn't a tier; 4 is closest. |
| Chart Categorical | **Unchanged for now** | Its order is validated for color-blind adjacency; re-pointing it to roles changes chart colors and needs re-validation. Separate step. |
| Migration scan scope | **Keys page + the two inventory frames** | Andrew's maps are restyled by hand; other pages can be scanned later on request. |

## 1. Tokens

- **Rename** the `Map Overlay` collection to `Color Roles`. Variable names and IDs are unchanged,
  so every binding survives. Update every reference in the spec, plan, Styles page, and memory note.
- **Fill styles: unchanged** at 50 (per hue: `Shade/100`, `Base/100`, `Tint/100`, `Tint/50`,
  `Tint/25`). Rule: translucent fills are always Tint at 25 or 50%.
- **New: 10 effect styles `<hue>/Casing`.** Each is one drop shadow, offset (0, 4), blur 1,
  spread 0, color bound to `Color Roles` `<hue>/Shade`. Check during the build whether a bound
  effect color keeps alpha 1 (the opacity overwrite seen on paints shouldn't matter here, since
  Shade's alpha is already 1).

## 2. Components

- **`Line Sample`** (`472:867`):
  - Rename the `Dash` value `Coarse` → `Medium` (it is `[8,8]`); instances keep their look.
  - Add `Dash = Coarse` `[16,9]` variants where a Medium variant exists.
  - Add a `Weight` value `Bold`, bound to `weight/lg` (4). The existing Thin/Standard/Heavy stay
    bound to `xs`/`sm`/`md`. *Revised 2026-10-13:* Bold is bound to `weight/xl` (6), to match the
    line weight on the maps. `weight/lg` stays available as an instance override.
  - Add a `Casing: None | Shadow` axis. Existing variants become `Casing=None`. Add one Shadow
    variant, `Weight=Bold, Dash=Solid, Cap=None, Casing=Shadow`, with stroke `charcoal/Base/100`
    and the `charcoal/Casing` effect style. Every casing line in the inventory is solid, so other
    dash/cap combinations aren't added.
  - No variant axis is removed.
- **`Site Marker`** (`473:862`): delete the `Icon` instance-swap property; keep Hexagon; bind
  `Dot / Hexagon` fill to `charcoal/Base/100` and its stroke to a charcoal style with a weight tier,
  matching the other variants.
- **`caption`** (`640:4373`): rename `Style` values `Light` → `Tint`, `Dark` → `Shade`. Black and
  White are unchanged.
- Same safeguard as v2: snapshot instance paints and effects before editing a main component, and
  restore only what changed, so no existing map changes appearance.

## 3. Styles page

- Semantic Tokens frame: retitle to Color Roles.
- Stroke frame:
  - Line Treatments grid becomes Fine / Medium / Coarse × caps × weight tiers.
  - Add a Casing row (one sample per hue, weight `lg`).
  - Add a **Region recipe** card: Tint 25% or 50% fill + Base border at weight `xl` (6) or `2xl`
    (8) + a named dash. This documents strokes as shape borders.
- Add a Casing effect-styles row to the Fill Styles or Stroke frame.

## 4. Migration checklist (Andrew's, manual)

Generated by a read-only scan of the Keys page and the two inventory frames, with node IDs:

- Translucent fills that aren't Tint 25/50 (wrong role, or 10/30/40/80%).
- Raw-hex fills and strokes that match a role exactly, which can be rebound.
- Dashes outside the set, with the proposed mapping: `[4,4]` → Fine; `[12,8]`, `[14,8]` → Coarse.
- Weight-5 casing lines, to swap for `Line Sample` with `Casing = Shadow`.

## Styles page revisions (2026-10-12)

Andrew reviewed the built Styles page before restyling the keys.

- **Hue display order:** magenta, coral, amber, gold, sage, teal, cobalt, violet, slate,
  charcoal, then neutral. This loosely follows the visible spectrum, then the greys. Every doc
  frame uses it (Ramps, Color Roles, Fill Styles, Casing). Exception: the Chart Categorical
  section keeps its own order, which is validated for color-blind adjacency. The `HUES`
  constant in both plans' Prelude A follows this order. Variable and style order in Figma's
  panels is unchanged.
- **No aerial backgrounds:** the #AFABA4 fill behind the Fill Styles swatches and region cards
  is removed. Swatches never sit on that tone in practice, so it distorted how they read. This
  replaces v2 §6's "mid-grey background".
- **Sample sizing:** line-treatment samples are 96×72 with a 64px line. Before, xl and 2xl
  arrowheads were clipped and touched their labels. Casing samples use fixed 160px columns
  with labels on two lines, so the two rows line up.

## Legend Row nesting (2026-10-12)

Goal: restyle a key from the selected Legend Row, without double-clicking down to its layers.

- **`Line Sample` becomes a full grid:** Weight (Thin `xs`, Standard `sm`, Heavy `md`, Bold `xl`)
  × Dash (Solid, Fine, Medium, Coarse) × Cap (None, Single, Double) = 48 `Casing=None` variants.
  Add 12 `Casing=Shadow` variants (Solid × each cap × each weight), for 60 in all. Shadow
  started with no cap only (52); Andrew needed cased arrows in legends, so Single and Double
  were added on 2026-10-12. Dashed casing isn't used anywhere, so it isn't added. Chosen over
  two legend weights (26) and weight-as-override (13). Figma component properties can't hold
  numbers, so with an override, weight would not appear in the exposed dropdowns. The 10
  existing variants keep their nodes, and the default stays charcoal.
- **New `Region Sample`** (60×24, matching the old Area rectangles):
  - Variants: `Border` = None / Solid / Fine / Medium / Coarse.
  - Boolean: `Show Fill`.
  - Defaults: fill `charcoal/Tint/50`, border `charcoal/Base/100`, inside, `weight/md`.
  - The border weight is fixed. A legend swatch is a symbol, and `xl`/`2xl` would fill a 60×24
    swatch.
  - Colors are style overrides, the same as for lines.
- **`Legend Row`** (`480:889`):
  - Area nests `Region Sample` in place of its loose `fill` and `stroke` rectangles.
  - Legend Row's own `Show Fill` property moves to `Region Sample`.
  - Line resets its nested default to `Standard / Solid / None`.
  - Line, Marker, and Area expose their nested instance's properties.
- **Accepted appearance change:** Andrew waived the "no instance changes appearance" rule for
  this step, since every key is being restyled. The 22 Area rows reset to the default region.
  Their colors before the change, for reference (fill · stroke, stroke `weight/sm` solid):

  | Row | Heading | Fill | Stroke |
  |---|---|---|---|
  | `494:969` | CAR Foot Path | sage/Shade | sage/Shade |
  | `496:1156` | Design Site Boundary | teal/Shade | sage/Shade |
  | `496:1162` | Water Catchment Area | coral/Shade | sage/Shade |
  | `496:1071` | Design Site Boundary | slate/Shade | sage/Shade |
  | `496:1093` | Erosion Risk Area | coral/Shade | sage/Shade |
  | `496:1107` | Idea: Trench Rain Garden | cobalt/Shade | sage/Shade |
  | `496:1128` | Idea: Gutter → Barrel | magenta/Shade | sage/Shade |
  | `496:1150` | Idea: Create Soil Sponge | gold/Shade | sage/Shade |
  | `494:1004` | Effective Catchment | charcoal/Shade | sage/Shade |
  | `494:1010` | Theoretical Catchment | coral/Shade | sage/Shade |
  | `487:867` | Design Site Boundary | teal/Shade | sage/Shade |
  | `487:873` | Retained Lawn Corridor | sage/Shade | sage/Shade |
  | `487:879` | Vegetable Garden | slate/Shade | sage/Shade |
  | `487:913` | Invasive Treatment Zone | coral/Shade | sage/Shade |
  | `487:919` | Proposed Chicken Paddock | amber/Shade | sage/Shade |
  | `487:925` | De-Lawned & Deep Mulched | magenta/Shade | sage/Shade |
  | `489:934` | Design Site Boundary | teal/Shade | sage/Shade |
  | `489:940` | Vegetable Garden | slate/Shade | sage/Shade |
  | `495:4209` | Roof: Metal, No Gutters | cobalt/Shade | sage/Shade |
  | `495:4215` | Driveway: Paved Asphalt | coral/Shade | sage/Shade |
  | `495:4221` | Proposed: SE-Corner Swale, Rain Garden | magenta/Shade | sage/Shade |
  | `495:4227` | Outfall / Low Point | teal/Shade | sage/Shade |

## Mono text styles (2026-10-12)

`Caption` and `Label` (12 JetBrains Mono styles) are replaced by one set,
`Mono/<size>/<weight>`, for captions and labels on maps and slides.

**What the scan found.** Neither family matched the maps:

| | Caption / Label | Map text |
|---|---|---|
| Sizes | 32, 24, 20, 16 | 24, 20, 18, 16 |
| Weights | Regular, Bold | SemiBold, Bold, ExtraBold |
| Tracking | −4% | 0% |
| Line height | Fixed, inconsistent on Bold | Auto |
| Uses | 48 runs (only `Caption – LG/MD – Bold`) | ~1,190 unstyled runs |

Label was used only by its own Styles page specimens.

**Decision:** codify actual use (chosen over merging the two families as-is, or a new scale
applied by hand). The set lists every size and weight the maps use, at 0% tracking and auto
line height:

| Size | Weights |
|---|---|
| 32 | Bold |
| 24 | SemiBold, Bold, ExtraBold |
| 20 | SemiBold, Bold, ExtraBold |
| 18 | Bold |
| 16 | SemiBold, Bold, ExtraBold |

- `Caption – LG – Bold` and `Caption – MD – Bold` were renamed to `Mono/32/Bold` and
  `Mono/20/Bold`, keeping their IDs. Their 48 runs changed tracking from −4% to 0%, the only
  visible change. The other 10 Caption/Label styles were deleted.
- Unstyled runs were bound only where size, weight, line height, and tracking matched
  exactly, so nothing moved. Main components were bound first, so instances inherited.
- **SemiBold becomes Bold.** `use_figma` scripts can't load JetBrains Mono SemiBold: Figma's
  hosted fonts lack it, and Andrew's local copy is the Google Fonts variable font, whose
  named weights skip 600. The 324 SemiBold runs (Keys 121, Water 66, Sector Analysis 54,
  Soil 37, Zones 28, Base Map 18) reported a missing font to scripts. Figma desktop
  rendered them and never flagged them, so its Replace Fonts prompt never appeared.
  Bold was chosen over JetBrains Mono NL SemiBold, which renders identically but is a
  second, local-only family without ligatures. One family loads everywhere, the set has no
  SemiBold, and those runs are one step heavier. Andrew restyled Legend Row's text himself;
  a script swapped the rest with `setRangeFontName`, which works on text whose current font
  is missing, and bound them. Done 2026-10-12: no SemiBold remains.
- **All caps lives in a sibling set, `Mono Caps/<size>/<weight>`.** Andrew prefers caps for
  mono text in keys, but `Mono` must also work in sentence case on slides. Figma's editor
  can't override text case on a styled layer (changing it detaches the style), so caps
  can't be a per-layer or per-component override. `Mono Caps` matches `Mono`'s values plus
  `textCase = UPPER`, and sizes are added only when a key needs one. It started with
  `Mono Caps/24/ExtraBold` (Legend Row heading) and `Mono Caps/20/Bold` (Legend Row body),
  which all 54 Legend Rows inherit. Former SemiBold runs in caps added `Mono Caps/24/Bold`
  and `Mono Caps/16/Bold`, for 4 Caps styles.
- **Left unstyled, off the scale:** Zones' 8 and 10 Bold, Soil's 13/15/16 Medium, Base Map's
  8 Bold and five 24 ExtraBold runs with a fixed line height. Five runs on Keys use a text
  style from an external library. These are restyled by hand with the keys.
- **Not done:** trimming weights. Three heavy weights at 16, 20, and 24 is a lot, but merging
  them is a visible restyle. It's a one-style edit later.

## Map key component (2026-10-13)

Components on Keys are now prefixed `map-` (`map-key`, `map-key-row`, `map-line-sample`,
`map-region-sample`, `map-site-marker`, `map-scale`, `map-legend`). Renames kept node IDs.

- **`map-key`** (`153:2052`) has a `Theme` axis (Default, Tints, Shades) and a `Map Type` axis.
  `Theme` exists for maps that need more than one color treatment of the same key, such as
  Sector Compass. Maps with one treatment use `Default`. Andrew built Template, Zones – Current,
  Site Waterflow Map, and both Sector Compass themes.
- **The 7 remaining examples became `Theme=Default` variants** (built by script from Andrew's
  Site Waterflow variant): Catchment Area `1194:485`, Water Brainstorm `1194:4416`, Contour
  Practice `1194:4315`, Microclimates `1194:4701`, Resilience Brainstorm `1194:4791`, Soil Sample
  `1194:4573`, and Soil Brainstorm `1194:4909`. Each one is as wide as its old example.
- **Text was kept as written** so Andrew can spot where Mono Caps changes the look. Older keys
  used Inter, and every key is moving to JetBrains Mono. Two exceptions:
  - "soil sample 02 location" was a copy-paste slip and is numbered 01–05.
  - Water Brainstorm's hard line breaks were removed.
- **Color mapping, from Andrew's built variants:**
  - Filled areas use a `<hue>/Tint/25|50|100` fill style and a `<hue>/Shade` border.
  - Unfilled borders and lines use the role closest to the old color, usually `<hue>/Base`.
  - Lines are `Bold`, `Solid`, `Single` cap, with `<hue>/Casing`.
  - Numbered markers use `<hue>/Shade` with white text. Where the old marker was light, they
    use `<hue>/Tint` with black text instead.
  - Dot markers keep the component default role, `Shade`.
- **`map-shape-marker`** (`1193:489`, Triangle and Diamond) is a new component. These shapes
  never carry a number or letter, and a triangle or diamond can't center a label the way a
  circle can. The fill binds to `charcoal/Shade` by default, and the stroke is `neutral/Black`
  at `weight/sm`, the same as the Dot marker. A key row's Marker swatch swaps its nested
  `map-site-marker` for it.
- **`map-key-row` centers its text when the body is hidden.** Each variant's `text` frame has a
  minimum height equal to the swatch (44) and centers its contents vertically. When the body
  is shown, the text is already at least 44 tall, so nothing moves. When it's hidden, the
  heading lines up with the swatch. It's set once in the component, with no per-variant
  overrides.
- **`Line Sample` Bold is `weight/xl` (6)**, changed by Andrew to match the maps. The Styles
  page casing row was rebound to `xl`.
- **Known gaps:**
  - `map-line-sample` has no dot cap. Water Brainstorm's "underground water line" has lost its
    filled-circle ends.
  - The Numbered `Square` and `Hexagon` variants of `map-site-marker` don't bind their text to
    the `Number` property, so Soil Sample's digits are set as text overrides.

## Map migration (2026-10-13)

The maps on Zones & Microclimates, Water, and Soil now use the components and tokens.

**Excluded:** Andrew is restyling the base map himself. That covers the Base Map page and the base-map layer inside every map: `Base Map North @ …` frames, the Zones page's loose `site-map`, and `Municipal Infrastructure`. Sector Analysis already used `map-key` and the `Sector Diagram` component, so it needed nothing.

- **Keys:** 8 one-off key frames were replaced by `map-key` instances at the same top-left
  position, and the old frames were deleted:
  - both Zones maps → Zones – Current;
  - the 4 Water maps → Site Waterflow Map, Contour Practice, Water Brainstorm, Catchment Area;
  - the 2 Soil maps → Soil Brainstorm, Soil Sample.

  Several instances are bigger than the frames they replaced.
- **The key is the source of truth for its map.** A map's regions, lines, and markers use the
  same role, fill style, and casing as the matching key row. Elements without a key row got
  the role closest to their old color:
  1. Find the hue: from the bound `Ramps` variable, or the nearest ramp primitive for a raw
     color. Near-black becomes `neutral/Black`.
  2. Pick the role (Tint step, 500, or 700) closest to that step.
  3. Translucent fills become `<hue>/Tint/25|50|100`, by nearest opacity.
  4. Stroke weights bind to the nearest tier. 5 becomes `xl` and 1.5 becomes `sm`.
  5. Drop shadows become `<hue>/Casing`, and every cased line uses `<hue>/Base`.

  Dash patterns were kept as drawn, since they aren't tokens.
- **Markers became instances.**
  - Water's `water connection` instances became `map-site-marker` Numbered Circle, keeping their letters.
  - Soil sample sites became Numbered Square.
  - Soil goal markers and waypoints became Dot Circle.
  - Contour high points became `map-shape-marker` Triangle, scaled to 50.
  - The waste pit became a Diamond.
- **Left as is:**
  - the white 85% fills on Soil's `label-bg` callouts (no token; their borders were bound);
  - `caption` and `Pill` instances;
  - all text styles.
- **Catchment Area key:** the "effective catchment" border is now `neutral/Black`, to match
  the near-black boundary on its map.

## Slides template colors (2026-10-13)

PDC Pro Vision is the library for all permaculture assets, including Slides decks. The Slides
template (`KDVfc0v5jT8jKB3OK11axN`) had its own palette, its first one. Its colors now come
from the Ramps.

- **Linked to the library.** Each `TEMPLATE: PDC PRO` variable is an alias to a PDC Pro Vision
  Ramps variable imported from the library. A Slides file can do this: a single-variable test
  passed before the full conversion. Variable IDs are unchanged, so every existing binding keeps
  working.
- **Mapping**, chosen by nearest color and checked for contrast:

  | Template | Ramps |
  |---|---|
  | Green 100 / 500 | sage/100 / sage/700 |
  | Neutral 500 / 400 / 300 / 200 / 100 / 50 | charcoal/800 / 700 / 600 / 200 / 100 / 50 |
  | Red 100 / 500 | coral/400 / coral/700 |
  | Blue 100 / 500 | cobalt/600 / cobalt/800 |
  | Yellow 100 / 500 | gold/100 / gold/600 |
  | Magenta 100 / 500 | magenta/400 / magenta/700 |

  White and Black stay as raw values.
- **Trade-offs Andrew accepted:**
  - The light green (`#cbec95`) becomes sage/100. Its lightness is the same, so black text stays
    at 16:1, but the green is softer.
  - The neon highlight (`#ff00c3`) and the electric link blue (`#0738ff`) become the calmer
    magenta/400 and cobalt/600.
  - The warm off-white page color (`#faf6f2`) becomes charcoal/50.
  - Yellow 500 is gold/600 rather than gold/500, which lifts its contrast on gold/100 to 4.8:1.
- **Theme collections.** `PDC-PRO Slide Templates` and `Keser Garden Theme` (Color 1–8, Link,
  Highlight) are aliases to the `TEMPLATE: PDC PRO` variables. That makes two hops to the Ramps.
- **Update path:**
  1. Change a Ramps value in PDC Pro Vision and publish it.
  2. Accept the update in the template, then publish the template.
  3. Accept the update in each deck.
- **Still open, from the Slides review:**
  - The template's text styles still duplicate the old Caption/Label set. They should map to
    `Mono Caps`, and Fraunces and Inter should move into the library.
  - `caption`, `Pill`, `label`, the table cells, and the icons exist in both files.
  - The course deck holds pasted copies of the maps. Each finished map should become a library
    component.

## Slides template text styles (2026-10-13)

- **Library styles added.** PDC Pro Vision gained `Mono Caps/32/Bold`, `32/Regular`, `24/Regular`,
  `20/Regular`, and `16/Regular`. Each is JetBrains Mono in all caps, with auto line height and 0%
  tracking. They join the existing 24/Bold, 20/Bold, and 16/Bold.
- **Publishing gotcha.** The first two publishes didn't include the new styles, and the Publish
  dialog showed nothing to publish. Adding a description to each style made them register as
  changes, and the next publish went through.
- **Template mapping.** Every Caption/Label run in the template now uses the library style:

  | Template style | Mono Caps |
  | --- | --- |
  | Caption – LG, Label – LG | 32/Regular |
  | Caption – LG – Bold, Label – LG – Bold | 32/Bold |
  | Label – MD | 24/Regular |
  | Label – MD – Bold | 24/Bold |
  | Caption – MD, Label – SM | 20/Regular |
  | Caption – MD – Bold, Label – SM – Bold | 20/Bold |
  | Caption – SM | 16/Regular |
  | Caption – SM – Bold | 16/Bold |

  That covers 179 runs. Only 41 needed direct edits. The rest sit inside instances and follow
  their main component.
- **Name gotcha.** Several template style names used non-breaking spaces around their dashes,
  so an exact-name match missed them. The script compares names after normalizing whitespace.
- **Deleted.** Six styles with no uses: `Caption`, `Label`, and `Caption Alt`, each defined twice.
- **Kept for now.** The 12 old Caption/Label styles are unused in the template but stay until the
  course deck migrates off them.
- **Left alone.**
  - One `Caption Alt` run and two `Subheader` runs come from another library.
  - The `Caption Alt` run is inside a remote instance (`I53:1653;33:352`), so it can't be fixed from
    the template.
- **Display and body styles.**
  - The library already had the Inter styles (Title – Regular, Subheader, Body LG/MD/SM) with the
    same values, so their 73 template runs now use the library copies. That includes two runs that
    pointed to a third library.
  - Title – Bold (Fraunces Bold 160), Header (Fraunces SemiBold 120), and Quote (Fraunces Regular
    100, LH 95%, LS −4%) were added to the library under the template's names. Their 11 template
    runs were relinked after the library was published. No template text uses a local style now.
  - The Styles page's Display section now documents all five display styles. The Medium rows in the
    Mono section were mislabeled "Bold" and are now named correctly.
- **Legacy styles deleted.** Thirteen template styles had no uses in the template or the course
  deck: the New York Title/Header/Quote set, the duplicate Title 2/Subheader/Body set (two copies
  each), and Body Small. All 13 were deleted. The template keeps 20 local styles that nothing
  uses. They mirror the library and stay until the deck is relinked.
- **Course deck relinked.** All 2,272 styled runs in the course deck now use PDC Pro Vision styles.
  - **Local copies.** 264 runs used the deck's own copies of the template styles. They map the same
    way as the template. The three `Caption – LG – Bold` copies without forced caps went to
    `Mono/32/Bold` rather than Mono Caps.
  - **Instance text.** About 1,670 runs sit inside template components (`slide-header`,
    `table-body-cell`, `caption`, `item-label`, `Pill`). They are overridden in the deck.
    - The template's components already use these styles, but the template offered nothing to
      publish.
    - The overrides match the template, so a later template update won't conflict.
  - **Header.** 16 Header runs were New York Medium and are now the library Header (Fraunces
    SemiBold). The plugin can't load New York, an Apple system font, so the switch used a
    node-level `setTextStyleIdAsync`. That call doesn't need the old font loaded. Every Header
    still fits on one line.
  - **Inter 20px body.** Seven runs moved to Body – SM (24). The library has no 20px body style.
  - **Not covered.** About 2,300 unstyled text nodes, mostly labels in the pasted maps, are left
    for a separate pass.
  - **Local styles deleted.** After the relink, the deck's 46 local styles and the template's 20 were unused. All were deleted. Neither file has local text styles now; all text styles come from PDC Pro Vision.
- **Publishing.** Neither file offered anything to publish after the relink. Pointing text at a
  different style isn't a library change, so the deck picks up library styles only when its own
  text is relinked.

## Out of scope

- ~~Re-pointing `Chart Categorical` to Color Roles.~~ Closed 2026-10-14: kept on Ramps for its Dark mode; see `2026-10-14-chart-tokens-design.md`.
- Scanning map pages other than Keys.
- Per-tier dash scaling (still open from v2).
- **Base map cleanup (deferred 2026-10-14).** Andrew is holding off on base map edits; it's cleanup
  work, not a blocker.
- **`map-scale` variants (deferred 2026-10-14).** There's one scale for now. A variant gets added
  when a future map zooms in on a single zone at a larger scale.

## Compact key rows (2026-10-14)

`map-key-row` (`480:889`) gained a `Size` axis (`SM`, `Default`) across all three Swatch Types.
Andrew built the SM variant, which has a smaller title and body, for content-dense keys such as
Sector Compass and Soil Brainstorm. He switched the keys that need it himself.

## Open-items pass (2026-10-14)

- **Marker numbers.** The Square (`641:1200`) and Hexagon (`641:1208`) text layers in
  `map-site-marker` now bind to `Number#473:0`, as Circle already did.
  - Before binding, the script recorded the text on all 16 Square instances (6 on Keys, 10 on Soil).
    It wrote that text back through the property afterward.
- **Dot cap.** `map-line-sample` gained `Cap=Dot` (`1317:4939`), Standard/Fine with
  `CIRCLE_FILLED` ends. It covers the only filled-circle line on the maps: the 2px dashed
  electrical-wire and water-connection lines.
  - The set uses an auto-flow grid, so the variant was appended as a new fifth row rather than
    placed in a column.
  - Water Brainstorm's "underground water line" key row uses it.
  - The Styles page's Line Treatments grid has a new "Fine [2,2] · Dot" row (`1323:12`). The
    dots scale with stroke weight and overwhelm the line from lg up, which is why the component
    has Dot only at Standard.
- **Site Water Flow key** (`1188:3545`).
  - The width went from 1478 to 978. It stays two columns like the other keys, with rows switched
    to `Size=SM`, so the key ends above the house's WM marker.
  - The "water meter/connection point" row is now two rows: WM "Water meter" with the original
    body, and WC "Connection point" with the body hidden. That matches the two markers on the map.
  - The map instance carried size and per-row `Size` overrides. Both were reset to match.
- **Visual check of 8 migrated maps.** Zones (both), Contour Practice and Water Brainstorm were
  clean. Fixes:
  - Water Brainstorm now clips its content. Its `water-access` overlay ran 38px past the left edge.
    Site Water Flow and Catchment already clipped.
  - In the Catchment key, the "theoretical catchment" row was the only SM row. It's back to Default.
  - The "cross east-southeast" caption moved 158px left so it clears the Catchment key.
  - **Open (Andrew).** On the Soil maps, the legend's extra LOCATION column pushes "SEPTEMBER 2026"
    past the frame: about 170px on Brainstorm and 40px on Sample.
- **Caption consolidated into the library.**
  - The template's `caption` instances now use the library's `caption` (`640:4373`). Dark became
    Shade, the closest match (charcoal, square corners). Light became White.
  - The deck's 203 caption instances were swapped the same way.
  - The template's two caption sets (`37:317`, and the unused `51:586`) were deleted.
  - The library's text layer is named `caption text` and the template's was `text`, so text was
    saved and restored around each swap. Wrapping didn't carry over: 14 fixed-width deck captions
    had their text set back to fill and wrap.
  - Four empty caption instances on template slide `29:2452` had no text layer before the swap.
  - Four deck captions that hug their text overflow the image frame they sit in by 8–21px. This
    was unchanged by the swap (same padding and style).
  - Pill, label, table cells, item-label, slide header/footer and icons stay template-only
    (Andrew, 2026-10-14).
- **Deck maps stay snapshots** (Andrew, 2026-10-14). The course deck is a dated record of submitted
  work. Live map components are for new and client decks.
  - The deck's `map-legend`, map key, `north-indicator` and Sector Diagram instances already link
    to the current library components. Their names are stale only because the deck hasn't accepted
    library updates, which happens in the Libraries panel, per component.
  - `north-alt` (3 instances) points to a component no longer in the library.
- **Deck unstyled text.** 390 runs that exactly matched a library style (family, weight, size,
  line height, tracking, case) were bound. About 1,900 runs don't match and stay unstyled. The
  largest group is 527 JetBrains Mono Thin 20 caps runs inside template components; the library
  has no Thin.

## Deck slide text (2026-10-14)

Andrew's rule: the course deck, not the template, is the source of truth for slide layouts in use.
Text on course slides gets a style, with a new one created where needed. Content inside template
components can wait.

- **JetBrains Mono Thin.** All 527 runs are the `div` layer of the template's `slide-header`, the
  "|" separators in each slide header. They're template content, so they're deferred.
- **New library styles:**
  - `Body/Body – XS`: Inter Regular 16/20, −4%.
  - `Body/Body – XS Bold`: Inter Bold 16/20, −4%. The plant list was at 0% tracking, so it tightens
    slightly to match the Body family.
  - `Mono/16/Bold Italic`: JetBrains Mono Bold Italic 16/20. It uses a fixed 20px line height,
    not the Mono family's auto, so it sits on the same lines as Body – XS Bold in species lists.
  - All three are documented on the Styles page.
- **Assigned now, existing styles:**
  - Soil-assessment questions (slides 131–149): JetBrains Mono Bold 22 → `Mono/20/Bold`, 44 runs.
  - Slides 13–15 headings: JetBrains Mono SemiBold 32 caps → `Mono Caps/32/Bold`. Figma has no
    JetBrains Mono SemiBold, so the change was applied at the node level.
  - Body copy on slides 13–15 and 94, and the chart intros on slides 96–101: Inter 24 and Inter 23
    → `Body – SM`.
- **Assigned after publish, new styles:**
  - Plant list (slide 66): Inter Bold 16 → `Body – XS Bold`. JetBrains Mono Bold Italic 16 and
    Bold 16 → `Mono/16/Bold Italic`.
    - The Bold 16 runs are the blank separator lines plus each column's first Latin name, which
      was non-italic by mistake.
  - Q&A answers (Inter 16) and chart source lines (Inter 17) → `Body – XS`.
- **Assigned after publish (done 2026-10-14):** 61 runs to `Body – XS Bold` and 143 to
  `Mono/16/Bold Italic` on slide 66, and 46 to `Body – XS`.
  - On slide 66, the blank separator lines between species are set back to an unstyled 16px line
    height. At 20px the 14-item column overflowed into the slide footer. They are empty
    paragraphs, not text.
- **Still unstyled on course slides (8 runs):**
  - Stat callouts in JetBrains Mono Bold 56: "1 / 10" (slides 54, 84) and "247 properties"
    (slide 54).
  - A JetBrains Mono Bold 15 caption bar on slide 145.
  - "Summer 2026" in Inter SemiBold 36 on the title slide.
- **Last 8 runs (Andrew approved the suggestions, 2026-10-14):**
  - The slide 145 caption bars, Mono Bold 15, now use `Mono/16/Bold`.
  - "Summer 2026" on the title slide, Inter SemiBold 36, now uses `Subheader` and becomes regular
    weight.
  - New library style `Mono/56/Bold` (JetBrains Mono Bold 56, auto, 0%) for stat callouts, with a
    row on the Styles page.
    - Applied after the publish to "1 / 10" and "247 PROPERTIES" on slide 54, and to
      "508,000 gal" and "~129,000 gal" on slide 84.
    - Both stat values on slide 54 now hug their height (74px), so the two cards line up.
    - "247 properties" renders in caps through a case setting, so its text is retyped in capitals
      to keep a single non-caps style.
- **Header dividers.** The `slide-header` "|" separators moved from JetBrains Mono Thin to
  `Mono Caps/20/Regular`, the next weight up among the existing styles. That's 4 `div` layers in
  the template's components and 527 runs in the deck.
- **North indicator.** `north-alt` is deprecated: it was drawn already tilted to −65.43°, so it
  broke when a map's orientation changed.
  - Maps carry two `north-indicator` layers, north up and −65.43°, and Andrew turns on the one that
    matches. Regional maps and satellite images are usually north up. Lot maps use −65.43°.
  - The deck's three hidden `north-alt` instances (slides 52, 86, 87) were swapped to
    `north-indicator` −65.43° and kept hidden.
- **Andrew, 2026-10-14:** he removed the account number from slide 97. He hid the Soil maps' location
  layer, which makes the legend fit, and accepted the library updates in the deck.
- **Charts are treated as graphics.** Labels inside the native charts (slides 48, 50, 96–101, 14
  sizes from 9 to 21px) stay unstyled, like the maps.
- **Layout fixes.** On slides 13–15, the right column's `row-2` was fixed at 116 while the left
  was 142, which clipped the last line of the right paragraph. It's now 142.
- **Template.** Four empty caption instances on slide `29:2452` were deleted.
- **Privacy flag.** Slide 97's source line quotes the water-utility account number, the same one
  this repo redacts. It's left as is in the course deck for Andrew to decide.

## Pickup (parked 2026-10-14)

**State at park:** everything is committed and pushed to `main` (`4488966`).
- **PDC Pro Vision (`aF9SVeTLwFN8PCEiU2OSBQ`):** published.
- **Slides template (`KDVfc0v5jT8jKB3OK11axN`):** has no local text styles left, but shows nothing
  to publish.
- **Course deck (`4HO6wuq75jFhX7OuMpqPNs`):** has accepted the library updates.

**Done in the library and files:**
- **Map components:** `map-key` (12 variants), `map-key-row` (Size SM/Default),
  `map-line-sample` (adds `Cap=Dot`, `1317:4939`), `map-site-marker` (Number bound on all shapes),
  `map-shape-marker`, `map-region-sample`, `caption`.
- **Text styles:** Mono and Mono Caps; Body including XS and XS Bold; Fraunces Title/Header/Quote;
  `Mono/16/Bold Italic`; `Mono/56/Bold`.
- **Slides:** the template and course deck use library text styles and the library caption.
- **Map frames:** use the key instances and tokens; the base map is untouched.

**Still open (nothing blocking):**
- **Base map cleanup:** Andrew is doing this himself; deferred.
- **`map-scale` variants:** add when a zoomed zone map needs a second scale.
- **Live map components:** turn finished maps into library components for new and client decks.
  The course deck stays snapshots.
- **Species map and status pills:** the species-inventory map palette and the status pills on the
  project-plan and species pages are unaddressed.

**Restructure notes:**
- This spec belongs to the design system, so it moves to
  `site-toolkit/design-language/specs/`. Re-sync before rebasing `restructure/home-site`.
- Memory note `figma_styles_page_sync` ("re-sync the Styles page after Keys-page edits") still
  applies wherever this work continues.

