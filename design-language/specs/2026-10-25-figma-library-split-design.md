# Figma library split: toolkit library and per-site files — design

Status: approved, 2026-10-25. Prerequisite met: one team on Professional (Andrew, 2026-10-25). Scope mode: personal project (HLSD), opinionated.

## Intent

The Site Toolkit Design Language file holds two kinds of work: the site-agnostic system (tokens,
styles, components, sheet template) and one site's content (Lot 86 maps, charts, imagery, course
maps). Splitting them lets:

- any site file and any deck use the system from one maintained place;
- a site's maps become components that its decks use live, instead of static PNGs that go stale;
- course material stay with the site until the course ends, out of the toolkit.

This finishes the plan the design-language README already states: generalize the map system into
library files that any site file can consume.

## Goals, non-goals, anti-goals

- **Goals:** a published toolkit library with no site content except a labeled Lot 86 demo; a Lot 86
  site file that uses the library's variables, styles, and components; Lot 86 sheets as components
  the Lot 86 deck can use.
- **Non-goals:** generalizing the Lot 86 charts into reusable chart components; a starter file for
  new sites (follow-up, below); changing any token, style, or component design.
- **Anti-goals:** a sheet that silently loses its library link (local copies of styles or variables
  look right and drift later); breaking existing bindings in the library file; Lot 86 working
  differently from future sites.

## Decisions (Andrew, 2026-10-25)

1. **Split into a toolkit library and one file per site.**
2. **The library shows Lot 86 as a snapshot demo**, like the microsite: image exports of finished
   sheets and charts, credited and dated, linking to the Lot 86 file. Lot 86's file is the source of
   truth. (Option B, keeping Lot 86's finished sheets in the library, was declined: Lot 86 would then
   work differently from every future site, and the library can't use components from a file that
   uses the library.)
3. **Permaculture Resources moves to the library's Cover page**, to frame what the tools are for.
4. **Inspiration (today's Mood Board) is per site.**
5. **Course material lives in the site file** until the course ends (~2026-11-30). The library and
   `template/` never mention the course.
6. **Contents sections and the Pages index stay** (list-only), rebuilt in both files after the move.

## Which file gets what

Current pages and sections, from the file as of 2026-10-25.

| Current location | Goes to | Notes |
|---|---|---|
| Cover | Library Cover | Gains Permaculture resources and the Pages index |
| Styles (all 10 sections) | Library | Unchanged |
| Components › Documentation, Map keys & legends, Map samples, Base map symbols | Library | Some Map keys & legends components default to Lot 86 text (site name, address, nearby landmarks). They get generic placeholder defaults; see Method step 7 |
| Components › Lot 86 (base map, site-legend, Sector Diagram – North Up) | Site file | Used only by Map Set sheets (19, 40, 3 instances) |
| Map Set › Template (sheet `00`) | Library | A plain frame (sheets were duplicated from it, never instanced). Must not contain Lot 86 instances; check, and swap any for a placeholder |
| Map Set › Regional & overlay, Property – current, Property – proposed | Site file | Sheets become components |
| Map Set › Course maps – remove after PDC | Site file | Deleted after the course |
| Data Visualizations (Sun … Species) | Site file | Lot 86 data |
| Data Visualizations › Perspective – Lesson 8 | Site file, course section | Course work |
| Mood Board | Site file, renamed Inspiration | |
| Permaculture Resources | Library Cover | |
| Assets › Patterns | Library | Generic |
| Assets › Contour textures, aerial-photo, Sector analysis screenshots | Site file | Lot 86 data |
| (new) Demo – Lot 86 | Library | Snapshot, see below |

### Site file pages

Cover, Map Set (Regional & overlay, current, proposed), Data Visualizations, Inspiration, Course
(maps and the Lesson 8 perspective; delete after the course), Assets, and a Lot 86 components
section. Name: **Lot 86 — Site Plan**, in the Keser Holdings HLSD folder next to the library.

## Method

The library keeps the current file, so every variable, style, and component keeps its key and
nothing already bound breaks. Site content moves out.

The API cannot move nodes between files, and pasting sheets into a new file would leave their
Lot 86 component instances pointing back at the source. So the site file starts as a **duplicate**
of the whole file, which keeps every internal link, and is then trimmed. The duplicate's sheets are
bound to its own local copies of the variables and styles, so a script rebinds them to the
library's published ones by name before the local copies are deleted.

1. **Prerequisite (Andrew):** confirm the Keser Holdings team plan can publish libraries, and that
   the library, the new site file, and the Lot 86 deck sit in the same team (on Professional, a
   library reaches only its own team). If either fails, stop here: nothing has changed yet.
2. **Publish the library** as is (Andrew, from the Figma app).
3. **Duplicate the file** (Andrew) and rename the copy Lot 86 — Site Plan.
4. **Spike on one sheet** in the copy (Claude), choosing one with an image fill and a Lot 86 legend:
   - swap instances of library-bound components (Documentation, Map keys & legends, Map samples,
     Base map symbols) to the published library components by name, and check that text and
     visibility overrides survive the swap;
   - rebind its variables, paint styles, text styles, and effect styles from local to library by
     name;
   - convert it to a component;
   - check that nothing reads as local or missing, and whether node IDs match the original file
     (this decides step 12).
   If any check fails, stop and revise the method before step 5.
5. **Swap and rebind the whole copy** (Claude), one section per call (heavy sheets drop the
   connection), including the Lot 86 components' own insides. The check before anything is
   deleted: no node in the copy binds a local variable or style, and no instance outside the Lot 86
   components section points at a local main component. Then delete the copy's local collections
   and styles.
6. **Trim the copy** (Claude): delete what belongs to the library (Styles, Components except Lot 86,
   Template, Permaculture Resources, Patterns). Rename Mood Board to Inspiration; gather course
   work into a Course page. Convert sheets to components.
7. **Trim the library** (Claude): delete what moved to the site file. Move Permaculture resources
   onto the Cover. Build the Demo – Lot 86 page. Give the Map keys & legends components generic
   placeholder defaults ("Project site", "Street", "Landmark"); the site file's instances already
   carry their Lot 86 text as overrides from step 5, so they don't change. Check the Template sheet
   for Lot 86 content.
8. **Publish both** (Andrew). The site file publishes too, so its decks can use the sheets.
9. **Rebuild Contents and Pages** in both files (Claude).
10. **Switch the Lot 86 deck** (`frBhbRkRlEEGSJ3ilSXHEx`) from PNGs to sheet instances (Claude),
    one slide per call. The deck holds whole sheets only (no crops), and leaves out course maps and
    the template, so every slide maps to one sheet component. Charts stay out of the deck.
11. **Paste-properties test** (Andrew), now against the library's styles.
12. **Repoint live links** (Claude). Live references to moved content: `lot-86-site-plan`'s
    `site-plan/data/species_maps_apply.py` and `plant_inventory_apply.py` (they target the file key),
    `site-plan/maps/sources.md` (node IDs), and `pdc-pro-2026/CLAUDE.md`. Course lesson files and
    dated specs and plans are records and keep their old links. The microsite has no Figma links.

In step 5, an instance that shows a library component's default text (no override) gets that
text written as an explicit override first, so the step 7 placeholder defaults can't change a
sheet.

Steps 6 and 7 delete content. Each runs only after the step before it is verified, and Figma's
version history holds the pre-split state (name a version "Before library split" at step 2).

## Spike results (2026-10-25)

Site file: Lot 86 – Site Plan (`iFt6im4itRdGt8UJ44GHyc`). Spike sheet: `25a Sun hours – growing season`
(image fill, Lot 86 legend, Map Semantic colors), plus the `Lot 86 / site-legend` main.

- **Passed.** Swapping the legend main's nested `map-legend` to the library kept every sheet's text
  overrides (checked on 25a and 07a). The map key swap kept all six row overrides. No local
  variable, style, or mode reference was left. The sheet renders identically to the original.
- **Node IDs carry over** in a duplicate, so links into the site file need only the new file key.
  **Except:** converting a frame to a component gives it a new ID (`1868:12634` → `4008:986`), so
  links to a sheet itself must use the component's ID.
- **Run scripts without `setCurrentPageAsync`.** On the image-heavy Map Set page it drops the MCP
  connection; `page.loadAsync()` loads in milliseconds.
- The team-library API lists nothing for this file, but import by key works. The library's
  name-to-key map is stored on a temporary `_migration (delete)` page in the site file for the
  batch scripts, and deleted in step 6.

## Progress

- **Steps 4–6 done (2026-10-25)** in Lot 86 – Site Plan (`iFt6im4itRdGt8UJ44GHyc`).
  - Swapped every library-bound instance, nested ones included, and rebound every variable, style,
    and explicit mode. The gate found 0 local references across 16,672 nodes.
  - Deleted the copy's 11 local collections and 93 local styles.
  - Pages now: Cover, Components (Lot 86 only), Map Set, Data Visualizations, Inspiration,
    Assets, Course.
  - All 43 Map Set sheets are components. Old frame IDs → component IDs are recorded for step 12.
  - Spot renders (07a, 18a, 25a, R4) match the original.
- **Steps 7 and 9 done (2026-10-25).** Andrew saved a version and a local copy of the library first.
  - Library pages now: Cover (with Permaculture resources), Styles, Components, Demo – Lot 86,
    Assets (patterns only).
  - The Template sheet moved to Components as "Sheet template". It held a Lot 86 legend, which was
    detached and reset to the generic `map-legend`.
  - Six Map keys & legends variants got placeholder text. Before that, the site file's 92 instance
    texts that showed the defaults (R3–R7, 10a) were pinned as overrides.
  - Demo – Lot 86 holds five exports: R2, 07a, 21b, Elevation profile A–B, Water charts.
  - Contents and Pages rebuilt in both files.
  - Left as is: the 1990 infrared and 1934 aerial keys credit Connecticut statewide surveys. They
    name a state, not a site.
- **Step 12 done in the repos (2026-10-25):** the Lot 86 scripts and docs point at the site file.
- **Remaining:** step 8 (publish both), step 10 (deck), step 11 (paste-properties test).
- **Lessons:**
  - Setting a text to its current value records no override. Change it and set it back.
  - Text bound to a component property records as an override on the instance that owns it.
  - Text snapshots taken by walking nodes are unreliable inside instances, because Figma loads
    instance children lazily. Verify by render.
  - A sheet that overrides a nested variant (North=Up legends) keeps pointing at the local variant
    after the main component is swapped. Swap nested instances too, outermost first.
  - Text-on-path nodes keep a node-level fill binding that range edits don't clear.

## Demo – Lot 86 page

- Image exports of finished work: one context sheet, the current base map, one proposed sheet, and
  two charts. That set is Claude's default; Andrew can swap any of them.
- Each image is credited with its sheet name and export date, and the page links to the site file.
- Refreshed on request, like the microsite's project plan page.

## Repo and docs changes

- `site-toolkit/CLAUDE.md` Figma section: two files, what each holds, the snapshot demo, and the
  rebuild rule for Contents.
- `design-language/README.md` file layout: library pages; per-site files.
- `lot-86-site-plan/CLAUDE.md` Figma section: the site file, its pages, and the course section's
  end date.
- `~/.claude/CLAUDE.md` workspace map: add the Lot 86 file key (Andrew's private file; Claude asks
  before editing it).
- `template/`: a line on creating the site's Figma file from the library. No course references.

## Risks

- **Rebinding by name misses a node.** The step 5 check (no local bindings left) catches it before
  local copies are deleted.
- **Heavy pages drop the MCP connection.** One section per call; every script is safe to re-run.
- **A pasted or duplicated image loses its fill.** Duplication keeps image hashes; the spike checks
  one image-filled sheet.

## Follow-ups

- A starter site file (Cover, Map Set with `00` instances, Data Visualizations, Inspiration, Assets),
  so a second site starts from structure, not from Lot 86.
- Site-agnostic chart patterns in the library, once a second site needs them.
- Delete the site file's Course page after 2026-11-30.
