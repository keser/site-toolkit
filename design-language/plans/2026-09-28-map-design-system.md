# Map Asset Design System — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILLS: `figma-use` (Plugin API syntax rules) and
> `figma-generate-library` (design-system phase discipline — variables before components, scopes
> on every variable, deterministic naming, state ledger) for every `use_figma` call in this plan.
> Use superpowers:subagent-driven-development or superpowers:executing-plans to work
> task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the map asset design system speced out in
`site-plan/specs/2026-09-28-map-design-system-design.md` — an expanded color palette, a
line-style vocabulary, a marker component, and a legend-row component — inside the PDC Pro
Vision Figma file. Retrofitting existing Base Map geometry onto this system is explicitly **not**
part of this plan (Fork 4 in the spec) — a separate, later pass.

**File:** `aF9SVeTLwFN8PCEiU2OSBQ` ("PDC Pro Vision"), pages `Base Map` (`0:1`) and `Keys`
(`222:2275`).

**Spec:** `site-plan/specs/2026-09-28-map-design-system-design.md` — read this first; it has the
full meaning inventory and the reasoning behind every decision below.

**State ledger:** `/tmp/design-system-state-map-assets-2026-09-28.json` — write to this after
every task per `figma-generate-library`'s state-management rules; re-read it at the start of
every session that resumes this plan.

## Pre-staged findings (from the 2026-09-28 audit — don't re-discover these)

- `Ramps` collection (`VariableCollectionId:145:261`): 9 hues × 9 steps each
  (`50,100,200,300,400,500,600,700,800`) = 81 variables. Naming: `<hue>/<step>`.
- `Map Overlay` collection (`VariableCollectionId:145:395`): 9 semantic variables (sage, cobalt,
  coral, gold, magenta, charcoal, slate, teal, violet), each a `VARIABLE_ALIAS` into `Ramps`,
  scoped `ALL_FILLS, STROKE_COLOR`.
- Sampled hex values: `gold/500 = #907600` (dark olive, not a true yellow), `coral/500 =
  #d2383b` (red, not pink-orange) — confirms no real orange/yellow currently exists.
- Zero paint styles, zero effect styles anywhere in the file.
- `Lot 100` boundary stroke, `driveway` fill, `water-connection` stroke, `garden bed` fill on
  the Base Map page are all raw hardcoded RGB, no bound variables — only `electrical-wire`
  strokes are bound (`boundVar: ["color"]`). Confirms the "barely used" finding — no action
  needed here, this is Fork-4 territory (deferred).
- Keys page (`222:2275`) has 7 legend frames: `Sector Compass Key` (×2 dupes + 1 real
  componentized version in the `Components` section at `153:2052`), `circulation element key`
  (×2: `222:2293`, `423:3878`), `Contour Practice Key` (×3: `423:3758`, `424:3929`, `424:4012`),
  `site water flow key` (`423:3709`), generic `Key` (`423:3795`).
- Confirmed bug: in `424:3929` and `424:4012`, every soil-sample legend row's label text reads
  "soil sample 02 location" regardless of the adjacent marker's number (1–5) — the marker number
  badge (`soil-sample-site` → child text) is correct per row; the row's heading text
  (`soil sample 02 location`) was copy-pasted and never retyped. Fixed by Task 4.

---

## Task 1: Palette foundation — add `amber`, contrast-audit all 10 hues — ✅ done 2026-09-28

**Files:** Figma variables only (`Ramps`, `Map Overlay` collections in `aF9SVeTLwFN8PCEiU2OSBQ`).

**Interfaces:**
- Consumes: nothing (first task).
- Produces: `amber/50`…`amber/800` in `Ramps`; `amber` semantic variable in `Map Overlay`;
  written contrast-audit results (below).

- [x] **Step 1: Read the full 9-step progression of two existing hues** (`gold` and `coral`) —
  confirmed all 9 `Map Overlay` semantics alias their hue's `/700` step (not `/500` as
  originally guessed), so `amber`'s semantic aliases `amber/700` too.

- [x] **Step 2: Generate the `amber` ramp.** First pass used H=30° — the contrast audit (Step 4)
  found this sat only 18.4° from `gold`'s H=49° at full saturation, a real confusability risk.
  Revised to **H=22°**, the exact midpoint between `gold` (49°) and `coral` (355°/−5°), giving a
  26.7° gap to both. Final ramp: `amber/50 #fdefe7` → `amber/500 #d75509` → `amber/800 #4e1f03`.
  Created in `Ramps`, scopes `[]` (hidden, matching the existing 81).

- [x] **Step 3: Create the `amber` semantic variable in `Map Overlay`** — aliased to
  `amber/700` (`#7a3005`), scopes `ALL_FILLS, STROKE_COLOR`, matching the existing 9.

- [x] **Step 4: Contrast-audit all 10 `Map Overlay` hues.**
  - **Vs. light bg (`#f9f9f7`):** all 10 pass comfortably, 7.8–9.8 contrast ratio (well above the
    3.0 AA-large threshold).
  - **Vs. dark bg (`#0d0d0d`):** **all 10 fail** AA-large (1.88–2.37, need ≥3.0). Flagged, not
    fixed — see Open flag below.
  - **Pairwise hue check:** `cobalt` vs `slate` sit only 1.7° apart in hue, but `slate` is
    desaturated (13% vs `cobalt`'s 62%), so they read as vivid-blue vs. blue-grey-neutral, not a
    real collision. `gold` vs `amber` was the one real finding — fixed by the Step 2 hue
    revision.
  - **Open flag for Andrew:** every `Map Overlay` color is tuned for light backgrounds only. Not
    an issue for the Figma canvas itself, but relevant if any of these colors get reused in this
    repo's dark-mode-aware HTML pages later — would need a parallel dark-mode variant set, out of
    scope for this task.

- [x] **Step 5: Validate** — all 10 variable IDs returned and recorded in the state ledger
  (`/tmp/design-system-state-map-assets-2026-09-28.json`). Built a temporary 10-swatch strip
  bound live to the `Map Overlay` variables, screenshotted it for visual confirmation (amber
  reads clearly distinct from both gold and coral), then removed the temporary strip from the
  page.

---

## Task 2: Line-style vocabulary — ✅ done 2026-09-28

**Interfaces:**
- Consumes: nothing new (line color comes from the Task 1 palette, applied per-map at use time,
  not fixed here).
- Produces: a small set of `Line Sample` components (for legend swatches only) plus a written
  stroke-property table.

**Finding to build from:** Figma's native `strokeCap` property supports `'ARROW_LINES'` and
`'ARROW_EQUILATERAL'` directly on a vector's stroke — arrows do **not** need a separate
component or overlay glyph. This simplifies the vocabulary to plain stroke properties
(`strokeWeight`, `dashPattern`, `strokeCap`), which is also why actual map lines don't get
"line components" instanced onto them the way markers do — a map line follows custom path
geometry per line, so the reusable unit is the *style* (the property combination), applied
directly to each line's own vector, not a drag-and-drop component.

- [x] **Step 1: Lock the stroke-property table.** Built as 3 proper variant axes (Weight:
  Thin/Standard/Heavy = 1/2/3px; Dash: Solid/Fine/Coarse = `[]`/`[2,2]`/`[8,8]`; Cap:
  None/Single/Double) rather than a flat name list — only 8 of the 27 possible combinations were
  built (the ones mapping to an actual inventory meaning), not a full cross product. Arrow caps
  use Figma's per-vertex `strokeCap` on a `VECTOR` node's `vectorNetwork` (via
  `setVectorNetworkAsync`), not the simpler uniform `LineNode.strokeCap` — that's what makes
  "single arrow" (one end only) possible; `LineNode.strokeCap` would arrow both ends.

- [x] **Step 2: Built the `Line Sample` component set** (`472:867`, on the Keys page, positioned
  past the existing `Components` section) — 8 variants: `Weight=Standard,Dash=Solid,Cap=None` ·
  `Weight=Standard,Dash=Coarse,Cap=None` · `Weight=Standard,Dash=Solid,Cap=Single` ·
  `Weight=Standard,Dash=Solid,Cap=Double` · `Weight=Heavy,Dash=Solid,Cap=None` ·
  `Weight=Thin,Dash=Solid,Cap=None` · `Weight=Thin,Dash=Fine,Cap=None` ·
  `Weight=Thin,Dash=Fine,Cap=Single`. Rendered in a fixed neutral grey (not bound to any palette
  color), since these swatches represent shape, not color — color gets set per-instance when a
  map actually uses one.

- [x] **Step 3: Validate** — screenshotted all 8 variants in a 4×2 grid: solid, coarse-dash,
  single-arrow, and double-arrow read clearly distinct in row 1; heavy-solid, thin-solid,
  thin-fine-dash, and thin-fine-dash-with-arrow read clearly distinct in row 2. All 8
  distinguishable by shape alone.

---

## Task 3: Marker component — ✅ done 2026-09-28

**Interfaces:**
- Consumes: Task 1 palette (colors applied per-map, not fixed on the component); the existing
  `water meter` marker instance (`423:3753` or similar) as the icon-marker pattern to extend.
- Produces: one `Site Marker` component set; soil-sample markers on the Keys page migrated to it.

- [x] **Step 1: Built the `Site Marker` component set** (`473:862`) — variant `Style` =
  `Numbered | Icon | Dot`. Audited the existing `water meter` marker first (`423:3753` →
  main component `40:5870`, "water connection") — turned out to be a plain filled circle with a
  2-letter text code inside ("WM"), not a true pictogram. No real icon glyph assets exist
  anywhere in the file yet, so `Icon` ships with one placeholder default (`Icon/Generic`, a
  small white diamond, `473:851`) via an `INSTANCE_SWAP` property — ready for real icons (water
  drop, compost bin, etc.) to be swapped in per-instance later, none invented now. `Numbered`:
  circle + `TEXT` property `Number` (default `"1"`). `Dot`: plain filled circle, smaller
  diameter, no text/icon. Component properties: `Number#473:0` (TEXT), `Icon#473:4`
  (INSTANCE_SWAP) — both added on the component **set**, not on an individual variant, per the
  component-property owner-narrowing rule.

- [x] **Step 2: Migrated all 6 `soil-sample-site` markers** on the Keys page (1 in `424:3929`,
  5 in `424:4012`) to `Site Marker, Style=Numbered` instances, `Number` set to the correct digit
  read live off each original marker before replacing it (1, and 1–5). Old copy-pasted frames
  removed. This only touches the marker badge — the adjacent row heading text ("soil sample 02
  location," repeated on every row) is untouched, as planned; that's Task 4's fix.

- [x] **Step 3: Validate** — screenshotted both rebuilt keys. All digits read correctly (1 / and
  1,2,3,4,5); each screenshot also incidentally shows the file's existing marker-shape variety
  already in real use (circle for most markers, a diamond for "interim waste pit") — good
  precedent for Task 4, not something this task needed to change.

---

## Task 4: Legend Row component (built last) — ✅ done 2026-09-28

**Interfaces:**
- Consumes: Task 1 (palette), Task 2 (Line Sample components), Task 3 (Site Marker component) —
  this task is deliberately last because it needs all three swatch types finalized to build a
  single row component that can render any of them.
- Produces: one `Legend Row` component; all 7 existing Keys-page legend frames rebuilt from
  instances of it.

- [x] **Step 1: Built the `Legend Row` component** (`480:889`) — variant `Swatch Type` =
  `Area | Line | Marker`. Simplified from the original plan: rather than an `INSTANCE_SWAP`
  property for Line/Marker, each variant just nests a real instance of a Task 2/3 component
  directly (Line nests a `Line Sample` instance, Marker nests a `Site Marker` instance) — the
  nested instance's own variant controls (Weight/Dash/Cap, or Style/Number) are already editable
  per-instance through normal Figma nested-override behavior, so a wrapper `INSTANCE_SWAP`
  property would have added complexity without adding capability. `Area`: plain rect, fill bound
  to a `Map Overlay` variable (rebindable per instance). Component properties on the set:
  `Heading` (TEXT), `Body` (TEXT) + `Show Body` (BOOLEAN, default off).

- [x] **Step 2: Rebuild each of the 7 existing key frames** from `Legend Row` instances, one
  key per `use_figma` call. **Finding while rebuilding:** the `paths` container inside each key
  uses Figma's `GRID` layout mode, which auto-places children into a 2-column grid by insertion
  order and ignores manually-set child `x`/`y` — don't fight this, just append rows in the
  desired reading order and let the grid place them (this explains why the original hand-built
  rows all had suspiciously round `x` offsets like `442.5` — that was the grid's own math, not a
  hand-placed value).
  1. `Sector Compass Key` — already uses instances via a different pattern (`Mode=Dark/Light`
     symbols in the `Components` section); left as-is, not forced into `Legend Row`.
  2. ✅ `circulation element key` (`222:2293`) — 5 rows (Line-type: CAR Foot Path, Monthly Foot
     Path, Seasonal Truck Path). 2 of the 5 rows had literal unfilled `"Title"` placeholder text
     already in the source file — pre-existing incomplete content, preserved as-is (still reads
     "Title") rather than inventing content; flagged for Andrew.
  3. ✅ `circulation element key` (`423:3878`) — 6 rows (2 Area, 4 Line), all with body text
     shown. Hit and fixed a real Figma gotcha here: the master `Legend Row`'s `body` text had
     `layoutSizingHorizontal: FILL` set while `visible: false` at construction time, which never
     actually took effect — revealing it later collapsed the node to 0 width, wrapping text one
     character per line and blowing out the row height (see Gotcha note below). Fixed on the
     master component and all 6 already-created rows by toggling visible → resize → re-apply
     FILL.
  4. ✅ `site water flow key` (`423:3709`) — 7 rows (4 Area, 2 Line, 1 coded Marker). The "WM"
     water-meter row couldn't reuse the existing `water connection` component directly as a
     nested swap-in — Figma doesn't allow deleting a required child from inside a component
     instance (`Error: Removing this node is not allowed`) — worked around it by using the
     `Site Marker, Style=Numbered` variant with `Number="WM"` instead (that property accepts any
     short text, not just digits).
  5. ✅ `Contour Practice Key` (`423:3758`) — 5 rows (2 Area, 2 Line, 1 Dot). One row ("High
     Points") had **no swatch content at all** in the source file — genuinely blank, not just a
     placeholder label. Gave it a neutral charcoal Dot as a placeholder and flagged it; the real
     visual treatment is Andrew's call.
  6. ✅ **`Contour Practice Key` (`424:3929`) — the "soil sample 02" bug is fixed here.** All 12
     rows rebuilt (6 Area, 6 Marker — 1 Numbered, 4 Dot, 1 Icon using the default diamond for
     "Interim Waste Pit"). Every area color rebound to a real `Map Overlay` variable (verified by
     reading bindings back). Soil sample row now reads "Soil Sample 01 Location."
  7. ✅ **`Contour Practice Key` (`424:4012`) — same bug, same fix.** All 7 rows rebuilt; the 5
     soil-sample rows now read "Soil Sample 01" through "05," each genuinely distinct.
  8. ✅ Generic `Key` (`423:3795`) — 12 rows. Found a second, worse instance of the duplicate-
     content pattern here: 5 different point meanings (municipal water meter, grey water access,
     water spigot, pool, planned downspout) were **all literally the same `water connection`
     instance** — indistinguishable from each other, not just mislabeled. Fixed the same way as
     the soil-sample markers: `Site Marker, Style=Numbered` with each row's own short code
     (W/G/S/P/D) as the `Number` text. Also found ~9 of the 12 rows shared the identical body
     text "water concentrates here" (clearly wrong for rows like "Idea: create soil sponge") —
     left body hidden (matching the source file's own choice to hide it) rather than surface or
     invent corrected copy.

  **Mechanical finding used throughout:** the `paths` container inside every key uses Figma's
  `GRID` layout mode, which auto-places children into a 2-column grid by insertion order and
  ignores manually-set child `x`/`y` — rows are appended in reading order and the grid handles
  placement (this also explains the original hand-built rows' oddly-precise offsets like
  `442.5` — that was the grid's own math, not a hand-placed value).

- [x] **Step 3: Validate** — read-only sweep across all 7 rebuilt keys: 54 total `Legend Row`
  instances, zero leftover plain `"label"` frames anywhere, zero duplicate headings except the
  one pre-existing `"Title"` placeholder pair (flagged, not fixed). Both soil-sample keys confirm
  unique, correct numbering.

---

## Task 5: Layer Styles rework (Phase 6 — Tone, Area stroke, Caption, Marker Shape) — ✅ done 2026-09-29

**Spec:** see "Layer Styles" section in `site-plan/specs/2026-09-28-map-design-system-design.md`
(added 2026-09-29) for the full reasoning and the specific live examples each rule is grounded
in — this task implements that section.

**Interfaces:**
- Consumes: Tasks 1–4's output (`Map Overlay` variables, `Legend Row`, `Site Marker`,
  `Line Sample`), plus the `caption` component from the Template file
  (`KDVfc0v5jT8jKB3OK11axN`, node `31:2535`).
- Produces: a `Tint` semantic variant per hue (20 total colors) + curated Paint Styles; a stroke
  slot on `Legend Row`'s `Area` variant; a ported `caption` component in `aF9SVeTLwFN8PCEiU2OSBQ`;
  a 12-variant `Site Marker` (`Style × Shape`).

- [x] **Step 1: Added the `Tint` tier.** Renamed all 10 `Map Overlay` semantics to `<hue>/Shade`
  (safe — same variable ID, existing bindings unaffected) and added 10 `<hue>/Tint` variables
  aliased to each hue's `/500` step. Contrast audit: all 10 Tints pass ≥3.0 against light bg
  (3.84–4.75). Against black text specifically, 3 came in borderline under the stricter 4.5
  AA-normal-text bar — `coral` (4.37), `magenta` (4.19), `violet` (4.47) — all still pass AA-large
  (≥3.0); flagged, not revised, matching Task 1's precedent of surfacing rather than silently
  adjusting. Pairwise hue check: `coral` vs `amber` sit 23.3° apart at the Tint tier (close to,
  but under, the 25° comfort line from Task 1) — visually distinguishable in the validation
  screenshot (pink-red vs. orange), not treated as a collision. Built 20 curated Paint Styles
  (`<hue>/Shade`, `<hue>/Tint`), each bound to its variable. Screenshotted a temporary 20-swatch
  Shade/Tint strip for visual confirmation — Tint reads clearly brighter and more distinct
  hue-to-hue than Shade, matching the goal — then removed the temporary strip.

- [x] **Step 2: Added a stroke to `Legend Row`'s `Area` variant.** Split the single `area-fill`
  rect into two independent layers: `fill` (existing rect, renamed, `visible` wired to a new
  `Show Fill` BOOLEAN component property, default `true`) and a new `stroke` rect (no fill,
  `strokeWeight: 2`, `strokeAlign: INSIDE`, stroke bound to a variable, default `sage/Shade`).
  Validated both documented cases directly: fill=`coral/Tint` + stroke=`coral/Shade` renders a
  bright fill with a visibly darker border (the fill/stroke pairing rule); `Show Fill: false` +
  stroke=`amber/Shade` renders a clean stroke-only outline with no fill, matching the
  `goal-zone: invasive treatment` precedent. Both test instances removed after validation.

- [x] **Step 3: Ported the `caption` component.** Pulled full structural detail from the
  template (`KDVfc0v5jT8jKB3OK11axN`, node `31:2535`, `COMPONENT_SET` `37:317`): `Style`
  (`Dark`/`Light`) × `Size` (`SM`/`LG`), font `JetBrains Mono Bold` (confirmed available in
  `aF9SVeTLwFN8PCEiU2OSBQ`), `SM` padding 4px/16px text, `LG` padding 8px/20px text. Rebuilt
  natively in the `Keys` page (new `caption` `COMPONENT_SET`, `640:4373`) — `Dark` variants are a
  faithful port (`cornerRadius: 0`, `#262626` fill/stroke, white text, matching source exactly).
  `Light` variants ship with the live-customization pattern baked in as the new default rather
  than the template's literal near-invisible border: `cornerRadius: 3`, white fill @ 85% opacity,
  black text, stroke bound to a variable (default `charcoal/Shade`) at 100% opacity/weight 1.5 —
  ready to rebind per instance to match whatever it's captioning. Validated by rebinding a test
  instance's stroke to `coral/Shade` and setting its text to "Invasive Treatment Zone" — visually
  matches the real Goals Map example almost exactly. Test instance removed after validation.

- [x] **Step 4: Added the `Shape` axis to `Site Marker`.** Renamed the 3 existing variants to
  `Style=<X>, Shape=Circle` (same IDs, no instance impact), then built 9 new variants
  (`Numbered/Icon/Dot` × `Square/Triangle/Hexagon`) by cloning each Circle variant and swapping
  its `ELLIPSE` for a `RECTANGLE` (Square) or `POLYGON` (`pointCount: 3` Triangle, `pointCount: 6`
  Hexagon) at the same footprint, then `appendChild`-ing each into the existing `Site Marker` set
  — 12 variants total. **Hit and fixed a real bug:** first pass rotated the hexagon polygon 90° to
  get a flat-top orientation, which threw off its rendered bounding box badly enough to hide
  sibling content entirely (the `Icon` variant's hexagon swallowed its own icon). Fixed by
  dropping the rotation — Figma's default pointy-top hexagon reads fine at this size, no rotation
  needed. **Triangle centering, corrected from the spec's phrasing:** a triangle's centroid sits
  at 2/3 of its height from the apex — *below* true bounding-box center, not above — so content
  needs to shift **down** (not up, as the spec draft said) to read as optically centered; applied
  a 4px downward nudge, confirmed visually. Verified all 18 `Site Marker` instances already
  placed inside the 54 Task 4 `Legend Row` rows resolved `Shape=Circle` automatically with zero
  manual fixup needed and zero regressions (still 54 rows, all headings unchanged).

- [x] **Step 5: Audited Task 4 rows for opacity.** Checked all 22 `Area`-type rows across the 6
  rebuilt keys — zero fills using an opacity outside `{25%, 50%, 100%}` (all were unset/100%, as
  expected — Task 4 never touched fill opacity). Confirmed rather than assumed; no-op.

- [x] **Step 6: Validated.** All sub-validations done inline per step above (20-swatch Tint/Shade
  strip, Area fill+stroke and stroke-only cases, caption stroke-recolor test, full 12-variant
  Marker grid at 4× zoom). No regressions to the 54 existing `Legend Row` instances at any point.

**Post-Task-5 follow-up:** the "Interim Waste Pit" row (`424:3929`) was built in Task 4 as
`Style=Icon` with the generic placeholder diamond, called out at the time as an approximation of
the original standalone `waste-pit` `POLYGON` marker. With `Shape` now available, swapped it to
`Style=Dot, Shape=Triangle`, `amber/Tint` fill — a direct, faithful match to the original design
instead of a diamond-in-a-circle stand-in. Verified the full key still renders correctly — all
other 11 rows unchanged.

---

## Final Verification (after all 4 tasks) — ✅ all confirmed 2026-09-28

- [x] All 10 `Map Overlay` variables exist, scoped `ALL_FILLS, STROKE_COLOR`, none left at
  `ALL_SCOPES`.
- [x] Line Sample and Site Marker component sets both documented with deterministic names,
  returned IDs recorded in the state ledger.
- [x] Every one of the 7 rebuilt Keys-page frames uses `Legend Row` instances — 54 total
  instances, zero remaining plain `"label"` frames anywhere on the page (confirmed via
  `findAllWithCriteria`).
- [x] The "soil sample 02 location" bug is gone — every soil-sample row (both keys, 6 rows
  total) reads its own correct number, "01" through "05."
- [x] No changes made to Base Map page geometry (driveway, garden beds, site boundary fills,
  etc.) — only the Keys page was touched throughout Tasks 1–4; Fork 4 retrofit remains untouched
  and deferred.
- [x] Reviewed every rebuilt key via screenshot — content matches the original meaning in every
  row; three pre-existing content issues were found along the way and deliberately **not**
  invented around: 2 unfilled `"Title"` placeholder rows (`circulation element key`, `222:2293`),
  1 row with no swatch content at all ("High Points," `423:3758`), and 5 markers that were all
  literally the same instance before this pass (now fixed with distinct W/G/S/P/D codes,
  `423:3795`). All flagged to Andrew rather than guessed at.

## Known follow-ups (not done, intentionally out of scope for this plan)

- **Fork 4 retrofit — deferred indefinitely (2026-09-29).** Base Map page geometry (driveway,
  garden beds, site boundary, electrical, etc.) still uses raw hex almost everywhere. Not just
  postponed — the color Base Map has seen little use since it was built to meet a one-off
  requirement; Andrew's actual work is all in the greyscale version, so there's no live need to
  retrofit or keep the color hex values current. Revisit only if the color version is needed
  again.
- **Dark-mode contrast** — all 10 `Map Overlay` colors fail WCAG AA-large against a dark
  background; only matters if these colors are ever reused in this repo's dark-mode HTML pages.
- **Content gaps found, not fixed — confirmed placeholder/non-issues (2026-09-29), no action
  needed:** the 2 `"Title"` placeholder rows, the blank "High Points" swatch, and the
  "water concentrates here" body-text copy-paste spanning ~9 rows of the generic `Key`.
- **Further component cleanup and real content is Andrew's, manually** — applying the system to
  existing/new map assets, and further refining the components built here (including replacing
  `Site Marker`'s placeholder icon).
- **Icon variant has only one placeholder glyph** (a generic diamond) — real per-meaning icons
  (water drop, compost bin, etc.) can be swapped in later; none were invented.
- **3 of the 10 new `Tint` colors** (`coral`, `magenta`, `violet`) are borderline under WCAG
  AA-normal-text (4.5) against black text — all still pass AA-large (≥3.0). Flagged, not revised.
- **`coral/Tint` vs. `amber/Tint`** sit 23.3° apart in hue — under the 25° comfort line used in
  Task 1's audit, though clearly distinct in the validation screenshot. Worth a second look if a
  map ever uses both together.
- **Area's stroke-matches-fill-hue rule is a manual convention, not enforced by the component** —
  Figma variables can't derive "darker than whatever the fill is currently bound to," so pairing
  `sage/Tint` fill with `sage/Shade` stroke has to be applied and spot-checked by hand per
  instance.
- **`Legend Row`'s `Area` variant's fill-opacity limit (25/50/100)** is a documented convention,
  not a hard constraint — nothing stops setting an arbitrary opacity value on an instance.

## Addendum (2026-10-10): Styles documentation page

Built a style-library reference on the `Styles` page (`699:2080`), section `Styles` (`701:2`),
mirroring the layout of the andrewkeser.com file's `Color` section (`KHXmdS7ZK7MouTlefKIZ43`,
`37:4`): three 1440px frames, each a status bar + title, then rows of description column +
swatches/cards.

- `Color Documentation — Ramps` (`701:3`): all 92 `Ramps` variables (10 hues × 9 steps + neutral).
- `Color Documentation — Semantic Tokens` (`701:251`): 20 `Map Overlay` cards (Tint, Shade) and
  the 7 `Chart Categorical` slots shown in Light and Dark via explicit variable modes, plus a
  contrast-audit note summarizing the follow-ups above.
- `Typography Documentation` (`701:447`): all 17 local text styles, specimens using the live style.

Every swatch is variable-bound and every specimen uses its text style, so the page stays current
as values change. No Dimension frame — this file has no number variables. Page text uses Inter and
JetBrains Mono (this file's families), not the website file's Barlow. Each frame's script deletes
and rebuilds its own frame by name, so re-running it after adding a hue or style is safe; the card
text (alias names, hex values) is static and does need that re-run to refresh.
