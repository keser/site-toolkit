# Map Asset Design System — Keys & Legends

Status: approved 2026-09-28, extended 2026-09-29 — Phases 1–4 and Phase 6 (the "Layer Styles"
rework below: Tone (Shade/Tint), Area fill/stroke, opacity, the Caption component, and Marker
`Shape`) built and confirmed working. Phase 5's retrofit is deferred indefinitely (Fork 4); its
other step, using the system for new map additions, is ongoing manual work.

## Goal

Systematize the map assets used across the PDC Pro Vision Figma file (design file
`aF9SVeTLwFN8PCEiU2OSBQ`) — area/polygon fills, line styles (with/without arrows), and site
markers (with/without labels) — plus the legend "key" components that document them, so that:

- Colors come from one shared, high-contrast palette instead of raw hex per shape.
- No meaning relies on color alone to be distinguished from another.
- Legend keys are built from one shared component instead of copy-pasted frames.

The Keys page (`222:2275`) is the existing inventory of every legend item created so far, across
the Base Map and all practice/lesson maps built from it.

## Current-state findings (audited 2026-09-28)

- **A "Map Overlay" variable collection already exists** — 9 named semantic colors (sage,
  cobalt, coral, gold, magenta, charcoal, slate, teal, violet), each aliased to a "Ramps"
  primitive collection (81 values — a full hue × shade scale). Properly scoped to
  `ALL_FILLS, STROKE_COLOR`. This is good infrastructure that's barely used.
- Of the map feature types sampled on the Base Map page (site boundary, driveway, water
  connection, electrical wiring, garden bed), only **electrical wiring** binds its stroke to a
  Map Overlay variable — everything else uses raw hardcoded RGB.
- **No paint styles or effect styles exist anywhere in the file** (0 of either).
- **Dash patterns are set freehand per vector, not from any shared set.** Site boundary uses
  `[8,8]`, garden bed uses `[4,8]`, and water-connection and electrical-wire both use the
  identical `[2,2]` — two different meanings sharing one line style, differentiated only by
  color. This is the concrete case for the "color alone" requirement to fix.
- **The Keys page has 7 separate hand-built legend frames** (Sector Compass Key ×2 duplicate
  copies + 1 real componentized version in the `Components` section, Circulation Element Key
  ×2, Contour Practice Key ×3, Site Water Flow Key, a generic "Key"). Only the Sector Compass
  Key's rows are real component instances — every other key is a copy-pasted frame tree.
- **That copy-paste pattern already caused a live bug:** in two different Contour Practice Key
  copies, all five soil-sample legend rows read "soil sample 02 location" regardless of number —
  the marker's number badge was updated correctly each time (it's a separate text layer), but the
  adjacent freeform label text was copy-pasted from row 2 and never retyped for rows 1, 3, 4, 5.
  A bound component would have made this class of error much harder to make.

## Scope inventory — meanings that need representing

Compiled from every legend row currently on the Keys page, plus Lesson 6 content already
committed in `pdc-pro-2026` that will need map representation soon.

**Area / polygon fills** (~9 distinct meanings so far): site/design boundary interior, water
catchment area, erosion risk area, invasive treatment zone, retained lawn corridor, de-lawned &
deep-mulched footprint, vegetable garden, chicken paddock, garden bed. Lesson 6 will add: the
compost/wood-processing cluster, drying/staging area, building-material pile.

**Line styles** (~12+ meanings across 4 families):
- *Water:* water flow, water flow on contour, water drainage, underground water line, effective
  vs. theoretical catchment divide, swale, roof/gutter runoff.
- *Circulation/access:* CAR foot path, monthly foot path, seasonal truck path, paved driveway.
- *Boundaries:* design site boundary, invasive-treatment-zone boundary.
- *Utilities:* electrical wire.
- *Directional/flow arrows:* water "enters / crosses / exits," mulch/material-flow arrows
  (Lesson 6 Goals Map notes).

**Markers** (~10+ meanings): water meter / connection point, grey water access, water spigot,
planned downspout, soil-sample sites (numbered 1–5), interim waste pit, long-term compost
system, ChipDrop drop-off site, understory plantings, pawpaw/mushroom site.

That's roughly 9 area meanings, 12+ line meanings, and 10+ marker meanings already documented,
before whatever Lessons 7–10 add. One color per individual meaning would blow well past the
existing 9-hue palette — see Fork 1 below.

## Decision forks — resolved 2026-09-28

**Fork 1 — hue-to-meaning binding: global (e.g. "blue always means water"), or local to each
map's own legend?** **Resolved: local, not global.** Andrew's call: color doesn't need a fixed
site-wide meaning — the same hue can mean "water" on one map and something unrelated on another,
as long as its use is consistent *within that map's own legend* and the legend documents what it
means there. This drops the rigid family→hue table from the earlier draft of this fork. What it
means for the system:
- The palette (below) is a shared, accessible, pre-vetted set of options — not a fixed
  meaning-to-color dictionary.
- Every map's Legend Row instances are the source of truth for what a color means *on that map*.
- The non-color-alone requirement still applies per map: within a single map/key, two different
  meanings must not share both the same color AND the same line style/marker shape — that's
  still checked at build time (see Accessibility checkpoints below), just scoped per-map instead
  of globally.
- **Base map context:** the base map itself (aerial/hand-drawn) stays greyscale — color is used
  only for the overlay lines/shapes/markers drawn on top of it, never for recoloring terrain or
  structures. Contrast checks only need to account for overlay-color-on-greyscale, not arbitrary
  photo colors.

**Palette expansion — resolved: add one new hue.** Andrew wants a true orange/yellow option,
which the existing 9 hues don't actually cover — `gold/500` (`#907600`) reads as dark olive/
mustard, not a bright yellow or orange, and `coral/500` (`#d2383b`) reads as red, not
pink-orange. Add one new hue, **amber**, as a full matching 9-step ramp (`amber/50` through
`amber/800`, same step scale as the existing 9 hues) in the `Ramps` collection, plus a
corresponding `Map Overlay` semantic variable scoped the same way (`ALL_FILLS, STROKE_COLOR`).
This brings the shared palette to 10 options. (If a distinct second hue — true yellow separate
from orange — turns out to be wanted once maps are actually built, that's a cheap follow-up, not
bundled into v1.)

**Fork 2 — line-style vocabulary — resolved at the recommended default.** Figma has no native
"stroke style" variable type, so this is a small documented enum plus reusable Line components,
not bindable tokens the way color is: Weight (thin / standard / heavy) × Dash (solid / fine-dash
/ coarse-dash) × Arrow (none / single / double) — a bounded set, not a combination invented ad
hoc per line as today.

**Fork 3 — marker shape vocabulary — resolved, then expanded 2026-09-29.** Original default
(numbered circle / icon-in-circle) held, then grew a second axis once Andrew confirmed markers
also need non-circle shapes. See "Layer Styles" below for the final `Style × Shape` design.

**Fork 4 — retrofit scope — resolved, then deferred indefinitely 2026-09-29.** Build the full
system now (palette, line styles, markers, legend row component). Applying/retrofitting it onto
existing Base Map geometry (driveway, garden beds, site boundary, etc. — currently almost all raw
hex) is an explicit, separate, opt-in follow-up pass, not part of this build. **Update
2026-09-29:** not just deferred — off the table for now. The color Base Map was built once to meet
a specific requirement and has seen little use since; all of Andrew's actual work has been in the
greyscale version, so there's no live need to retrofit or keep the color hex values current. Revisit
only if the color version is needed again (e.g. for a slide deck).

## Layer Styles — Tone, Opacity, Stroke Rules, Captions, and Marker Shape (added 2026-09-29)

The Task 1–4 build (below) shipped Area/Line/Marker/Legend-Row using only each hue's single
existing `/700` semantic step, no stroke on Area, and no caption system. Feedback after using it:
that's a narrower, more muted palette than intended, and misses real patterns already established
elsewhere in the file. This section documents what changes, grounded in specific existing
examples rather than invented from scratch — every rule below was found live in the file, not
proposed cold.

### Tone axis — `Shade` / `Tint`

The Keys page's `Sector Compass Key` (`153:2052`) has two full copies — `Mode=Dark` (`153:2053`)
and `Mode=Light` (`153:2051`) — because Andrew couldn't decide which read better in a given deck.
Inspecting them: this is **not** a background-theme toggle, it's two saturation tiers of the same
hues (dark/saturated vs. pastel/light), and it's built as two entirely separate hand-duplicated
frames (`key – dark` / `key – light`, each with its own full set of row instances) — not a Figma
variable *mode* switch.

**Decision:** formalize this as a per-instance pick, not a page-wide mode switch — Andrew:
"some overlays need darker or lighter treatment depending on context," i.e. it varies within a
single map, not per-map. Every `Map Overlay` hue gets a second semantic variant:
- **`Shade`** — the existing darker `/700` step. Pairs with **white** text/content.
- **`Tint`** — a new, lighter/brighter step (need to pick the exact ramp step per hue during
  Phase 1 rework — the existing `Mode=Light` pastel felt *less* distinct hue-to-hue than the dark
  version on inspection, so "Tint" should land brighter/more saturated than that pastel precedent,
  not just lighter). Pairs with **black** text/content.

This doubles the usable palette from 10 semantic colors to 20 (`amber/Shade`, `amber/Tint`,
`sage/Shade`, `sage/Tint`, etc.), still all sourced from the same `Ramps` primitives.

**Naming note:** deliberately not "Dark/Light" — that name is already used for the *caption*
component's own axis (see below), which is a different concept (neutral background + max-contrast
text, not a hue/saturation choice). `Shade`/`Tint` is also the technically correct color-theory
term for exactly this operation (mixing a hue toward black vs. toward white).

### Palette access — curated styles, full override available

Andrew: "a curated subset works, as long as I can override from a set of predefined styles that
don't necessarily get built into the subset." Two-layer approach:
- **Curated layer:** a defined set of Figma Paint Styles built from the most commonly-needed
  `Map Overlay` Shade/Tint values — these are what show up as quick picks.
- **Override layer:** every swatch's fill/stroke stays a bound *variable*, not just a style
  reference, so any instance can be rebound to any `Ramps`/`Map Overlay` value outside the
  curated set without breaking the pattern — this is the same variable-rebind mechanism already
  used throughout Task 4, just not restricted to the curated list.

### Area fill/stroke rule

Checked two real precedents:
- **Microclimates** (`222:2359`, e.g. `222:2365` "MC-02"): every zone uses fill at exactly **50%
  paint opacity** + stroke at **100% opacity, weight 4**, but the stroke color is a **fixed
  neutral dark** (`~#2a2d39`) across every category — the fill varies, the stroke never does. This
  is the "reduced-opacity fill, solid stroke" pattern Andrew described, but with a stroke rule
  that turned out not to match the intended design.
- **Live Goals Map** (`0:1`, `Soil Building Goals Overlay` frame `364:1131`): `goal-zone: invasive
  treatment` (`364:1138`) has **no fill at all**, stroke-only, dashed — confirms fill can be
  legitimately empty for a pure boundary/region marker. `goal-zone: chicken paddock`, second draft
  (`365:1559`), has both: fill magenta at low opacity, stroke a **visibly darker/more saturated
  version of the same magenta** — not a fixed neutral. This is the actual intended rule, per
  Andrew directly: "in all cases where there is a fill, the stroke should be a darker value from
  the same color ramp."

**Rule:** `Area` variant always supports both fill and stroke as independent, optional-fill
channels:
- Fill: optional — omit entirely for a stroke-only boundary/region outline.
- Stroke: whenever fill is present, bind it to a **darker step of the same hue** as the fill (not
  a fixed neutral, correcting the Microclimates precedent). Stroke-only shapes (no fill) can use
  any hue/step needed for the boundary itself.
- How many overlapping elements a given map needs to distinguish determines stroke *weight* and
  whether one is needed at all — Andrew: this is a per-map judgment call, not a fixed rule, so
  weight stays a free property per instance (informed by, but not locked to, the Line weight
  vocabulary from Task 2).

### Opacity — fixed set

**Rule:** fill opacity is chosen from a **fixed set of 25 / 50 / 100%** — covers the majority of
cases per Andrew, replacing freeform per-instance values (Microclimates used 50%, one early Goals
Map draft used 10% — that 10% predates this decision and isn't being kept as a fourth tier).
Stroke opacity is always 100% (matches every example checked — Microclimates, both Goals Map
zones, and every caption instance below).

### Caption system

Andrew pointed to the actual source: the slide-deck template file (`KDVfc0v5jT8jKB3OK11axN`,
"Template – PDC PRO," node `31:2535`) defines a real `caption` `COMPONENT_SET` with two variant
axes — **`Style`**: `Dark` (`#262626` fill + stroke, white text) / `Light` (white fill, near-
invisible stroke, black text) — crossed with **`Size`**: `SM` (16px) / `LG` (20px). A sibling
`Pill` component set (rounder, 32px, badge-style) and a plain `item-label` component follow
similar but distinct patterns — not part of this system.

Checked 7 live instances of this component on the actual Goals Map (`364:1133` ChipDrop,
`364:1139` Invasive Treatment Zone, `364:1142` Chicken Paddock, `364:1152` Camper/Fire
Pit/Brick Oven, `364:1155` Garden Entrance, `364:1136` and `365:1603` Interim Waste Pit/Compost)
— every one is `Style=Light`, detached from the template, and follows one identical customization:
**white fill @ 85% opacity, black text, `cornerRadius: 3`, and the stroke recolored per instance
to match whatever it's captioning, at 100% opacity, weight 1.5.**

**Decision:** this answers "how does a caption relate to the palette" directly — it doesn't need
its own Shade/Tint color variants. It stays neutral (`Style=Dark`/`Light`, unchanged from the
template) for maximum text legibility, and connects to its subject purely through the **stroke**
color, exactly like the Area rule above. Import the template's `caption` component (not rebuild
it from scratch) and standardize the "white 85% / black text / radius 3 / colored stroke @ 100%,
weight 1.5" customization as the documented default for `Style=Light` on a map, rather than a
one-off detach-and-tweak per instance.

### Marker — `Style × Shape`

Confirmed on the live Goals Map: every marker there (`364:1132` ChipDrop, and others) is a plain
colored glyph with no text baked in — the caption box next to it carries the text, matching
Andrew's "transparent markers never have text over them" point. This is a **different**, equally
valid convention from the in-marker-text badges built in Task 3 (soil samples, "WM," "W/G/S/P/D"
codes) — Andrew confirmed explicitly: both stay. Marker text content is free-form (letter, number,
or other glyph), which the existing `Number` TEXT property already supports without change.

New requirement: markers need non-circle shapes too — the existing "interim waste pit" marker is
already a stand-alone diamond-ish `POLYGON`, informally, not part of any component.

**Decision:** add a second variant axis, `Shape`, crossed with the existing `Style` axis:
- `Style`: `Numbered` / `Icon` / `Dot` (unchanged from Task 3)
- `Shape`: `Circle` / `Square` / `Triangle` / `Hexagon`

12 variants total — comfortably under the point where a matrix gets unwieldy, and every
combination is legitimate (e.g. `Dot × Triangle` is exactly the existing waste-pit marker,
formalized). `Square` uses sharp corners by default; corner-radius override stays a per-instance
property, not its own variant, unless that need recurs enough to justify promoting it later.
Triangle needs its text/icon nudged off true bounding-box center — a triangle's visual center
sits below the box center — everything else centers normally.

## Proposed build order

Legend rows are built **last**, deliberately — the component needs to know what swatch types
(area / line / marker) it's rendering, so it depends on Phases 1–3 being locked first rather than
being redesigned per key as those pieces land.

**Phase 1 — Foundations (tokens)**
1. Add the `amber` hue: a full 9-step ramp in `Ramps` matching the existing step scale, plus its
   `Map Overlay` semantic variable (scoped `ALL_FILLS, STROKE_COLOR`).
2. Contrast-check all 10 `Map Overlay` hues against light/dark backgrounds and against each
   other at small-swatch size (legend chips read differently than full fills).
3. Define the line-style vocabulary (Fork 2) as a small set of reusable Line components — dash
   pattern and arrowheads aren't bindable variables, so this is componentized, not tokenized.

**Phase 2 — Marker components**
1. Build a "Site Marker" component: variants for Numbered / Icon / Dot, with a text/number
   override property.
2. Migrate soil-sample markers to it.
3. Build icon variants for recurring infrastructure marker types, using the existing water-meter
   marker as the pattern to extend.

**Phase 3 — Line components**
1. Build the Line component set per the Fork 2 vocabulary.
2. Document which semantic meaning maps to which line style + family hue — this table becomes
   the map's own internal style guide, and is what a legend row will reference.

**Phase 4 — Legend row component**
1. Build one "Legend Row" component: swatch slot (variant: Area / Line / Marker) + heading +
   optional body text.
2. Rebuild each of the 7 existing key frames from instances of it. This is also where the
   "soil sample 02 location" bug actually gets fixed — each row becomes a bound instance instead
   of independently-typed text.

**Phase 5 — Apply / optional retrofit**
1. Use the finished system for all new Lesson 6+ map additions.
2. (Separate go-ahead required) retrofit existing Base Map geometry to the new variables/styles.

**Phase 6 — Layer Styles rework (2026-09-29 addendum; Phases 1–4 already built without this)**
1. Add a `Shade`/`Tint` second semantic step to all 10 `Map Overlay` hues (20 total); build the
   curated Paint Style layer on top.
2. Add a `stroke` slot to the `Legend Row` `Area` variant (currently fill-only), with the
   same-hue-darker-step binding rule; make fill optional.
3. Import the `caption` component from the Template file and standardize the live
   white-85%/black-text/radius-3/colored-stroke customization as its documented default.
4. Add the `Shape` variant axis (`Circle/Square/Triangle/Hexagon`) to `Site Marker`, crossed with
   the existing `Style` axis (12 variants); fix triangle's optical text-centering.
5. Re-apply the fixed 25/50/100 opacity set to any Task 4 rows that used a different value.

## Accessibility checkpoints (threaded through every phase, not a separate pass)

- Contrast-check every palette hue (all 10, after the amber addition) against both light and
  dark backgrounds, and against every other hue, at the size it's actually used (small legend
  swatches on a greyscale base, not full fills) — this is a one-time check against the shared
  palette, done once in Phase 1, not repeated per map.
- Every meaning gets a non-color differentiator by default: dash pattern for lines, shape/icon
  for markers, and consider a subtle fill pattern for areas whose adjacent zones might render
  close in hue.
- Within any single map, never reuse an identical line style for two different meanings even if
  their colors differ — the water/electrical `[2,2]` collision found in this audit is the
  concrete case to fix first. Since color meaning is now local to each map (Fork 1), this check
  has to be re-run per map, not just once globally.

## Out of scope (this spec)

- Retrofitting all existing Base Map geometry to the new system (Fork 4 — deferred, separate
  go-ahead).
- The Sector Compass / wind-direction / water-flow diagram component family already in the
  Keys page's `Components` section — already properly componentized, not part of this pass.
- The "Chart Categorical" variable collection — serves the HTML dataviz reports (Lesson 1/3
  charts in `pdc-pro-2026`), unrelated to map keys.

## Next step

None — this spec is fully built. Phases 1–4 are Tasks 1–4 and Phase 6 is Task 5 in
`site-plan/plans/2026-09-28-map-design-system.md`, all done 2026-09-28/29. Remaining work is
the plan's "Known follow-ups" list, none of it scheduled.
