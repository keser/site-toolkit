# Concept plan overlay: proposals above the base map, not inside it

Status: built 2026-11-15 (overlay `4175:1896`); site file publish and deck accept pending. Amends `2026-10-15-base-map-component-design.md` and
`2026-10-15-map-sheet-design.md`.

## Why

The Lesson 9 build put the whole concept plan inside `Lot 86 / base map`'s `state=proposed` variant:
- five layer groups
- the Cell A/B labels
- the new 10×10 shed

Sheets showed groups with `Show …` toggles on the base map. That broke the sheet model, where drawn
work sits in `annotations` above the map. On 22b and 31b, which draw their own overlays, the base
map's cell labels render under those overlays and get covered (Andrew, 2026-11-15).

**Rule (Andrew):** the base map holds current fixtures only. The clothesline and barrel pond belong
there. Proposed ideas are overlays.

## Goals
- The base map shows the site as it is. No proposed variant.
- Every proposal lives in one overlay component, edited once, so each sheet stays in sync. A change
  like the shed move stays a single edit.
- The cell labels sit above every overlay, so nothing covers them.
- Drawn shapes are frames, not rectangles or ellipses (Andrew's preference; he did the same on
  21b's thematic circles).

**Non-goals:**
- No new map content.
- No change to keys, legends, or what each sheet shows.

**Anti-goals:**
- Any Lesson 9 deck map looking different after publish, apart from the old shed showing under its
  removal marker.
- Breaking the 13 deck instances. They have no overrides, so a structural change inside the sheets
  flows through on publish.

## Approaches
1. **One overlay component (chosen).** A new `Lot 86 / concept plan` component holds the proposals,
   with the same toggles. Sheets stack it over a current-state base map. One edit point; costs one
   more component and an overlay inside each crop view.
2. **Copy the layers into each sheet's `annotations`.** Simple to read, but every change repeats on
   up to 12 sheets. Rejected.
3. **Patch only the labels** on 22b and 31b. Fixes the symptom, keeps the structure. Rejected.

## Design

### `Lot 86 / concept plan` (new component, Base Map page, next to the base map)

**Frame:** 1920×1080, no fill, no clip, the base map's coordinates.

**Contents**, moved from the proposed variant's `Concept plan` frame (same names, same order):
- `Vegetation`
- `Water`
- `Soil & Animals`
- `Zones & Access`
- `Structures & Energy`
- `Cell labels`, on top

**New group `Proposed fixtures`:** the new 10×10 shed outline, moved from the proposed variant's
`Lot 86` group.

**Properties** (moved from the base map, same defaults):
- `Show water`, `Show zones & access`, `Show vegetation`, `Show structures & energy` and
  `Show soil & animals`: all default off.
- `Show layer detail`: default on.
- `Show cell labels`: default on.
- `Show proposed fixtures`: new, default on.

### `Lot 86 / base map`
- **Delete `state=proposed`** once no instance uses it, along with the `state` property. The set
  becomes the current drawing only.
- **Remove the concept toggles** from the base map. It keeps `Show plants`, `Show contours`,
  `Show utilities` and `Show aerial`.
- **Old shed:** the plastic 10×8 shed stays in the drawing, since it's current. On proposed sheets
  it now shows under the `remove: plastic shed` marker, which is more accurate than before.

### Sheets

**Overviews `32b`–`37b`:** restructured to the spec's layers, `content` (base map) +
`annotations` (overlay instance) + key + legend. Each overlay instance takes the toggles its base
map instance has today.

**Crop views C, D and E:**
- Each view component gets an overlay instance directly above its base map instance, at the same
  offset and scale.
- Expose it as a nested instance, so sheets set the toggles on it, as they do on the base map today.

**Detail sheets `32.1b`–`37.1b`:** move their toggle settings from the view's base map to the
view's overlay.

**`22b` and `31b`:**
- Swap their base map to current.
- Add an overlay instance at the top of `annotations`, at the base map's offset and scale.
- Turn on only `Show cell labels` and `Show proposed fixtures`, so the labels sit above the sheet's
  own drawing.
- The sheet's own new-shed marker stays.

**`21.1b` and the `a` sheets:** already current. They get no overlay, except where they showed cell
labels.
- Those labels only ever rendered on the proposed variant, so the current sheets never showed them.
- Leave them off unless Andrew wants labels on 12a or 14a.

### Shapes → frames

**In scope:** the overlay component, plus the `annotations` of every sheet on the Map Set page.

**Converted:**
- Each `RECTANGLE` becomes a `FRAME` with the same corner radius.
- Each full `ELLIPSE` becomes a `FRAME` with radius = min(w, h) / 2. A circle stays a circle; an
  out-of-round ellipse becomes a stadium (Andrew: convert all).

**Carried over:** name, position, size, rotation, parent order, fills and strokes (bound variables
and styles included), stroke weight, alignment and dashes, effects, opacity, blend mode,
constraints, and component property references (visibility toggles).

**Not converted:**
- arcs, donuts and partial ellipses (`arcData`), as on 08a's sector compass
- masks
- shapes inside boolean operations or inside instances
- vectors, lines and polygons

### Publishing
1. Publish the site file.
2. Accept in the deck.
3. Check every Lesson 9 map slide (223, 225, 228, 230, 233, 235, 238, 246, 250, 258, 260, 263,
   264) against before-screenshots.
4. Check 22b and 31b's sheets, which aren't in the Lesson 9 deck except 22b on 250.

## Left to the builder
- Batch size per call, with a before and after screenshot of each sheet.
- The order: build the overlay first; delete the proposed variant last.
- Record the change in both amended specs and the Lesson 9 follow-ups.
