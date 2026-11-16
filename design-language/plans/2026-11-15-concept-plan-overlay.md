# Concept Plan Overlay Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move every proposal out of `Lot 86 / base map` into a `Lot 86 / concept plan` overlay
component, restack the sheets on a current-state base map, and convert drawn rectangles and ellipses
to frames.

**Architecture:** Figma Plugin API scripts via the Figma MCP `use_figma`, run against the Lot 86 –
Site Plan file (`iFt6im4itRdGt8UJ44GHyc`). Each task is one or a few calls. Its test is a read-back
of node structure plus a screenshot compared with a "before" screenshot.

**Tech Stack:** Figma Plugin API (design file), Figma MCP.

**Spec:** `design-language/specs/2026-11-15-concept-plan-overlay-design.md`

## Global Constraints
- **File and IDs:**
  - Site file: `iFt6im4itRdGt8UJ44GHyc`.
  - Base map set: `1597:6795`, with `state=current` `1543:617` and `state=proposed` `1597:6796`.
  - Concept frame `4103:2`; groups: Vegetation `4103:3`, Water `4103:4`, Soil & Animals `4103:5`,
    Zones & Access `4103:6`, Structures & Energy `4103:7`, Cell labels `4153:26720`.
  - New shed instance `1597:6927`.
- **Sheets:**
  - Overviews 32b–37b: `4134:16`–`4134:21`.
  - Details 32.1b–37.1b: `4134:3745`–`4134:3750`.
  - Views C/D/E: `4126:18`, `4126:639`, `4126:1080`.
  - 22b `4083:709`, 31b `4083:2341`.
- **Property names** move over unchanged, so deck text and docs still match: `Show water`,
  `Show zones & access`, `Show vegetation`, `Show structures & energy`, `Show soil & animals`,
  `Show layer detail`, `Show cell labels`; plus the new `Show proposed fixtures` (default on).
- **Figma connection** (workspace CLAUDE.md):
  - One heavy call at a time, never in parallel.
  - A dropped response isn't a failure: read the canvas before retrying.
  - Return values under 48 KB.

## Review Focus
1. **Toggle visibility binding is lost when nodes move** to the new component, and a group shows on
   every sheet. Check each group's `componentPropertyReferences.visible` after the move.
2. **The overlay drifts from the base map** inside the crop views (scale 2.0 / 1.333). Compare a
   known point (shed at 1482,535) on view E before and after.
3. **Converted frames lose a variable-bound fill or a dashed stroke.** Compare the paint and
   `dashPattern` count before and after on a sample.
4. **The deck changes look in an unexpected way after accepting.** Screenshot all 13 Lesson 9 map
   sheets before Task 1 and after Task 6.
5. **The proposed variant is deleted while an instance still uses it.** Search for remaining
   instances first; abort if any.

---

### Task 0: Baseline
- [ ] Screenshot the 12 concept sheets, 22b and 31b at 960 px. Save them in the scratchpad as
  `before-<sheet>.png`.
- [ ] Record each sheet's current base-map toggle values; the inventory is already in the session.

### Task 1: Build `Lot 86 / concept plan`
**Produces:** a component, ID recorded, with the properties above.
- [ ] Create the component on the Base Map page next to the set:
  - frame 1920×1080, no fill, `clipsContent=false`
  - name `Lot 86 / concept plan`
- [ ] Add the boolean properties, with defaults per the spec.
- [ ] Move the six groups from `4103:2` into it, in the same order, keeping their x and y. Add a
  `Proposed fixtures` frame holding a clone of the new shed instance at its base-map position.
- [ ] Rebind each group's `visible` to the new component's matching property.
- [ ] **Test:**
  - Read back the children and their `componentPropertyReferences`.
  - Place a temporary instance with all toggles on, screenshot it, and compare it with 32b-before
    minus the base map. Remove the temporary instance.

### Task 2: Shapes → frames
**Produces:** a helper used by Task 2 only. Scope: the new component, then each sheet's
`annotations` on the Map Set page, one sheet per call.
- [ ] Convert per the spec's rules.
- [ ] **Test:**
  - Each call returns converted / skipped counts by reason.
  - Before and after screenshots of 22b, 31b, 21.1b, 20a and 13a match by eye.

### Task 3: Views C/D/E
- [ ] In each view component, insert an overlay instance directly above the base map instance, with
  the same x, y and size, and `isExposedInstance=true`.
- [ ] **Test:** a screenshot of view E shows the shed outline on the base map's shed footprint,
  using the base-map value 1482,535 × scale.

### Task 4: Sheets
- [ ] **Overviews 32b–37b:**
  - Wrap them as `content` (the base map instance, set to `state=current`) and `annotations` (an
    overlay instance, 1920 at 0,0).
  - Copy the concept toggles over.
- [ ] **Details 32.1b–37.1b:** copy the concept toggles from the view's base map instance to the
  view's overlay instance. Set the view's base map to current.
- [ ] **22b and 31b:**
  - Set the base map to current.
  - Add an overlay instance at the top of `annotations`, at the base map's x, y and size.
  - Turn on only `Show cell labels` and `Show proposed fixtures`.
- [ ] **Test:** after screenshots match before screenshots, except:
  - the plastic shed now shows under its removal marker
  - the cell labels now sit on top on 22b and 31b

### Task 5: Retire the proposed variant
- [ ] Search every page for instances of `1597:6796`. Abort if any are found.
- [ ] Delete `1597:6796`, then remove the concept properties and the `state` property from the base
  map set.
- [ ] **Test:** a read-back shows the set holds one component with `Show plants`, `Show contours`,
  `Show utilities` and `Show aerial` only. 07a's screenshot is unchanged.

### Task 6: Publish, deck and docs
- [ ] Andrew publishes the site file and accepts the update in the deck.
- [ ] Screenshot deck slides 223, 225, 228, 230, 233, 235, 238, 246, 250, 258, 260, 263, 264.
- [ ] **Update the docs:**
  - the two amended specs (a pointer to this design)
  - `concept-plan-layers.md`'s map and toggle reference
  - the Lesson 9 build memory
- [ ] Commit in site-toolkit and pdc-pro-2026.
