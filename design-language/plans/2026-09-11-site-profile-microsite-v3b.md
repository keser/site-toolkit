# Site Profile Microsite V3b Implementation Plan (Zones & Design)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Zones & Design section (hub + 3 pages) to the live microsite, authored from three source markdown files rather than ported from an existing report.

**Architecture:** New content authoring using the established `.viz-root` visual pattern (same CSS system as `index.html`/`sun-solar.html`). No new build tooling. 9 raw images get compressed via `sips` (built into macOS) before embedding.

**Tech Stack:** Plain HTML/CSS, `sips` for image processing (no new dependency — ships with macOS).

**Spec:** `site-plan/specs/2026-09-11-site-profile-microsite-v3b-design.md`

## Global Constraints

- Every internal link relative, never root-absolute — `grep -rn 'href="/' docs/` and `grep -rn 'src="/' docs/` must both return nothing, every task.
- All body text is reproduced verbatim from the source markdown — this is Andrew's own course analysis, not content to paraphrase, summarize, or "improve." Wording, voice, and grammatical person are never altered; typo/agreement corrections are fine without individual flagging. **Superseded:** the matrix tables below are shown in sentence case, not the source's ALL CAPS — a deliberate call made while writing this plan's task content (all-caps is a slide-design artifact, not authorial style, and reads poorly on the web), not an oversight. The tasks' actual HTML is the source of truth for this; this line originally said to keep the caps and was wrong.
- Images: `sips -Z 1200 -s format jpeg -s formatOptions 65 <source.png> --out <dest.jpg>` — this exact command, tested during spec-writing (produces 140–290KB files from 368KB–2.5MB sources).
- `body { margin: 0; }` required in every new page's `<style>` block (V1's white-border lesson, documented in this repo's CLAUDE.md).
- Exact address/coordinates permitted; third-party names never permitted (source content already clean — no name appears anywhere in the three markdown files).

---

### Task 1: Compress and copy the 9 zone/microclimate images

**Files:**
- Create: `docs/assets/zones-design/microclimates-aerial.jpg`
- Create: `docs/assets/zones-design/microclimates-map.jpg`
- Create: `docs/assets/zones-design/current-zones-map.jpg`
- Create: `docs/assets/zones-design/current-zones-strengths-1.jpg`
- Create: `docs/assets/zones-design/current-zones-strengths-2.jpg`
- Create: `docs/assets/zones-design/brainstorm-zone1-nw-1.jpg`
- Create: `docs/assets/zones-design/brainstorm-zone1-nw-2.jpg`
- Create: `docs/assets/zones-design/brainstorm-zone1-se.jpg`
- Create: `docs/assets/zones-design/brainstorm-map.jpg`

**Interfaces:**
- Produces: 9 JPEG files at `docs/assets/zones-design/*.jpg` that Tasks 2-4 embed via `<img src="assets/zones-design/<filename>.jpg">`.

- [ ] **Step 1: Create the subfolder and compress each image**

```bash
mkdir -p docs/assets/zones-design
SRC=/Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-04-design/assets

sips -Z 1200 -s format jpeg -s formatOptions 65 "$SRC/slide-64-microclimates-aerial-drone-photo.png" --out docs/assets/zones-design/microclimates-aerial.jpg
sips -Z 1200 -s format jpeg -s formatOptions 65 "$SRC/slide-65-current-microclimate-map.png" --out docs/assets/zones-design/microclimates-map.jpg
sips -Z 1200 -s format jpeg -s formatOptions 65 "$SRC/slide-69-current-zones-map.png" --out docs/assets/zones-design/current-zones-map.jpg
sips -Z 1200 -s format jpeg -s formatOptions 65 "$SRC/slide-71-current-zone-strengths-1.png" --out docs/assets/zones-design/current-zones-strengths-1.jpg
sips -Z 1200 -s format jpeg -s formatOptions 65 "$SRC/slide-72-current-zone-strengths-2.png" --out docs/assets/zones-design/current-zones-strengths-2.jpg
sips -Z 1200 -s format jpeg -s formatOptions 65 "$SRC/slide-77-zone-01-nw-side-yard-1.png" --out docs/assets/zones-design/brainstorm-zone1-nw-1.jpg
sips -Z 1200 -s format jpeg -s formatOptions 65 "$SRC/slide-78-zone-01-nw-side-yard-2.png" --out docs/assets/zones-design/brainstorm-zone1-nw-2.jpg
sips -Z 1200 -s format jpeg -s formatOptions 65 "$SRC/slide-79-zone-01-se-side-yard.png" --out docs/assets/zones-design/brainstorm-zone1-se.jpg
sips -Z 1200 -s format jpeg -s formatOptions 65 "$SRC/slide-80-zone-brainstorm-map.png" --out docs/assets/zones-design/brainstorm-map.jpg
```

- [ ] **Step 2: Verify**

```bash
ls -la docs/assets/zones-design/*.jpg
du -sh docs/assets/zones-design/
```

Expected: 9 files, each under ~350KB (the spec's tested range was 140–290KB on 3
representative files), total well under 3MB (vs. ~13MB of source PNGs). Confirm each
file is a valid JPEG: `file docs/assets/zones-design/*.jpg` should say "JPEG image data"
for all 9.

- [ ] **Step 3: Commit**

```bash
git add docs/assets/zones-design/
git commit -m "Compress and add the 9 zones/microclimates images"
```

---

### Task 2: Build the Microclimates page

**Files:**
- Create: `docs/microclimates.html`

**Interfaces:**
- Consumes: `docs/assets/zones-design/microclimates-aerial.jpg`, `docs/assets/zones-design/microclimates-map.jpg` (Task 1).
- Produces: the CSS pattern (`.viz-root` vars, `.panel`, `.species-list`, `.two-col`) that Tasks 3-4 copy from this file's `<style>` block.

This is new content, hand-authored directly with markers in place (no port_report.py —
there's no source fragment to wrap).

- [ ] **Step 1: Create the page**

Create `docs/microclimates.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Microclimates — Lot #86</title>
<style>
  .viz-root {
    color-scheme: light;
    --surface-1: #fcfcfb; --page: #f9f9f7; --text-primary: #0b0b0b;
    --text-secondary: #52514e; --text-muted: #898781; --border: rgba(11,11,11,0.10);
    --grid: #e1e0d9;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) .viz-root {
      color-scheme: dark;
      --surface-1: #1a1a19; --page: #0d0d0d; --text-primary: #ffffff;
      --text-secondary: #c3c2b7; --text-muted: #898781; --border: rgba(255,255,255,0.10);
      --grid: #2c2c2a;
    }
  }
  :root[data-theme="dark"] .viz-root {
    color-scheme: dark;
    --surface-1: #1a1a19; --page: #0d0d0d; --text-primary: #ffffff;
    --text-secondary: #c3c2b7; --text-muted: #898781; --border: rgba(255,255,255,0.10);
    --grid: #2c2c2a;
  }
  * { box-sizing: border-box; }
  body { margin: 0; }
  .viz-root {
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--page); color: var(--text-primary);
    padding: 32px 20px 60px;
  }
  .wrap { max-width: 900px; margin: 0 auto; }
  h1 { font-size: 24px; font-weight: 600; margin: 0 0 6px; }
  .subhead { color: var(--text-secondary); font-size: 14px; line-height: 1.5; margin: 0 0 24px; }
  h2.section-head { font-size: 13px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text-muted); margin: 28px 0 12px; }
  .panel {
    background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px;
    padding: 18px 20px; margin-bottom: 16px;
  }
  .photo-block { margin-bottom: 16px; }
  .photo-block img { width: 100%; height: auto; border-radius: 12px; border: 1px solid var(--border); display: block; }
  .photo-caption { font-size: 12.5px; color: var(--text-secondary); margin: 8px 0 0; line-height: 1.5; }
  .photo-credit { font-size: 11px; color: var(--text-muted); margin: 2px 0 0; }
  table.matrix-table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
  table.matrix-table th, table.matrix-table td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--grid); vertical-align: top; }
  table.matrix-table th { color: var(--text-muted); font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.03em; }
  table.matrix-table td { color: var(--text-secondary); }
  .table-scroll { overflow-x: auto; margin-bottom: 16px; }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  @media (max-width: 640px) { .two-col { grid-template-columns: 1fr; } }
  .species-list { font-size: 13px; color: var(--text-secondary); line-height: 1.9; margin: 0; padding-left: 20px; }
  .species-list em { color: var(--text-muted); font-style: italic; }
  .qa-block { margin-bottom: 18px; }
  .qa-block .q { font-size: 13.5px; font-weight: 600; color: var(--text-primary); margin: 0 0 6px; }
  .qa-block .a { font-size: 13px; color: var(--text-secondary); line-height: 1.6; margin: 0; }
</style>
</head>
<body>
<!-- NAV:START -->
<!-- NAV:END -->
<div class="viz-root">
  <div class="wrap">
    <header>
      <h1>Microclimates</h1>
      <p class="subhead">Four distinct microclimate zones identified on the property, the known plant species already growing in them, and observations from studying how they shift with the planned Reset-phase clearing.</p>
    </header>

    <div class="photo-block">
      <img src="assets/zones-design/microclimates-aerial.jpg" alt="Aerial drone photo showing microclimate with afternoon shade and dense wind block">
      <p class="photo-caption">Aerial drone photo showing microclimate with afternoon shade and dense wind block.</p>
      <p class="photo-credit">Photo by Andrew Keser, July 2026.</p>
    </div>

    <h2 class="section-head">Microclimate Types</h2>
    <div class="table-scroll">
      <table class="matrix-table">
        <tr><th>Type</th><th>Name</th><th>Description</th></tr>
        <tr><td>Type 01</td><td>Wet, Humid &amp; Shaded</td><td>Heavily shaded areas with dense foliage, high moisture retention.</td></tr>
        <tr><td>Type 02</td><td>Hot, Dry, Direct Sun</td><td>Direct sun, wind exposure with dry dead soil with low water retention.</td></tr>
        <tr><td>Type 03</td><td>Cool, Shaded &amp; Breezy</td><td>Morning sun from the east, with afternoon shade &amp; southern winds spring through fall.</td></tr>
        <tr><td>Type 04</td><td>Hot, Direct Sun, Thermal Mass</td><td>Similar sun exposure as Type 02, but with much higher water retention from roof drip line. The boxwood hedge shades the ground through most of the day, but the home's walls provide thermal mass which could provide heat in early spring/late fall to extend growing potential.</td></tr>
      </table>
    </div>

    <div class="photo-block">
      <img src="assets/zones-design/microclimates-map.jpg" alt="Current Microclimate Map showing the four microclimate zones drawn on the site plan">
      <p class="photo-caption">Current Microclimate Map — scale 1" = 20', north -65.43°, location 41°34'22.04"N 72°38'03.90"W, elevation min 106 ft / max 114 ft.</p>
      <p class="photo-credit">Map created by Andrew Keser, August 2026.</p>
    </div>

    <h2 class="section-head">Known Plant Species</h2>
    <p class="subhead" style="margin-bottom:16px;">Species observed before the formal Lesson 8 iNaturalist survey (see the <a href="species-inventory.html">Species Inventory</a> page for the surveyed set — the two lists overlap heavily but were compiled differently).</p>
    <div class="two-col">
      <div>
        <p class="photo-caption" style="font-weight:600; text-transform:uppercase; letter-spacing:0.03em; color:var(--text-muted);">Native (27)</p>
        <ol class="species-list">
          <li>Allegheny Blackberry — <em>Rubus Allegheniensis</em></li>
          <li>American Burnweed — <em>Erechtites Hieraciifolius</em></li>
          <li>American Elm — <em>Ulmus Americana</em></li>
          <li>American Jumpseed — <em>Persicaria Virginiana</em></li>
          <li>American Plantain — <em>Plantago Rugelii</em></li>
          <li>American Pokeweed — <em>Phytolacca Americana</em></li>
          <li>Bitternut Hickory — <em>Carya Cordiformis</em></li>
          <li>Canada Yew — <em>Taxus Canadensis</em></li>
          <li>Common Blue Wood Aster — <em>Symphyotrichum Cordifolium</em></li>
          <li>Eastern American Blue Violets — <em>Boreali Americanae</em></li>
          <li>Eastern Black Walnut — <em>Juglans Nigra</em></li>
          <li>Eastern Poison Ivy — <em>Toxicodendron Radicans</em></li>
          <li>Horseweed — <em>Erigeron Canadensis</em></li>
          <li>Juniper Haircap Moss — <em>Polytrichum Juniperinum</em></li>
          <li>Mexican Stonecrop — <em>Sedum Mexicanum</em></li>
          <li>Northern Highbush Blueberry — <em>Vaccinium Corymbosum</em></li>
          <li>Northern Lady Fern — <em>Athyrium Angustum</em></li>
          <li>Northern Whitecedar — <em>Thuja Occidentalis</em></li>
          <li>Ohio Haircap Moss — <em>Polytrichum Ohioense</em></li>
          <li>Queen of the Prairie — <em>Filipendula Rubra</em></li>
          <li>Riverbank Grape — <em>Vitis Riparia</em></li>
          <li>Seductive Entodon Moss — <em>Entodon Seductrix</em></li>
          <li>Sensitive Fern — <em>Onoclea Sensibilis</em></li>
          <li>Thicket Creeper — <em>Parthenocissus Inserta</em></li>
          <li>Upright Yellow Woodsorrel — <em>Oxalis stricta</em></li>
          <li>Virginia Creeper — <em>Parthenocissus Quinquefolia</em></li>
          <li>Wild Bergamot — <em>Monarda Fistulosa</em></li>
        </ol>
      </div>
      <div>
        <p class="photo-caption" style="font-weight:600; text-transform:uppercase; letter-spacing:0.03em; color:var(--text-muted);">Introduced (34)</p>
        <ol class="species-list">
          <li>Asian Bittersweet — <em>Celastrus Orbiculatus</em></li>
          <li>Asiatic Dayflower — <em>Commelina Communis</em></li>
          <li>Black-Eyed Susan — <em>Rudbeckia Hirta</em></li>
          <li>Bloody Crane's-Bill — <em>Geranium Sanguineum</em></li>
          <li>Carpet Bugle — <em>Ajuga Reptans</em></li>
          <li>Common Chickweed — <em>Stellaria Media</em></li>
          <li>Common Dandelion — <em>Taraxacum Officinale</em></li>
          <li>Common Grape Hyacinth — <em>Muscari Botryoides</em></li>
          <li>Common Lantana — <em>Lantana Camara</em></li>
          <li>Garden Privet — <em>Ligustrum ovalifolium</em></li>
          <li>Goatsbeard — <em>Aruncus dioicus</em></li>
          <li>Gooseneck Loosestrife — <em>Lysimachia clethroides</em></li>
          <li>Goutweed — <em>Aegopodium podagraria</em></li>
          <li>Ground-Ivy — <em>Glechoma Hederacea</em></li>
          <li>Hairy Bittercress — <em>Cardamine Hirsuta</em></li>
          <li>Japanese Maple — <em>Acer Palmatum</em></li>
          <li>Japanese Stiltgrass — <em>Microstegium Vimineum</em></li>
          <li>Japanese White Pine — <em>Pinus Parviflora</em></li>
          <li>Jerusalem Artichoke — <em>Helianthus Tuberosus</em></li>
          <li>Koyamaki — <em>Sciadopitys Verticillata</em></li>
          <li>Lesser Periwinkle — <em>Vinca Minor</em></li>
          <li>Low Smartweed — <em>Persicaria Longiseta</em></li>
          <li>Mock Strawberry — <em>Potentilla Indica</em></li>
          <li>Norway Maple — <em>Acer Platanoides</em></li>
          <li>Norway Spruce — <em>Picea Abies</em></li>
          <li>Orange Day-lily — <em>Hemerocallis Fulva</em></li>
          <li>Purple Coneflower — <em>Echinacea purpurea</em></li>
          <li>Purple Loosestrife — <em>Lythrum salicaria</em></li>
          <li>Scented Hosta — <em>Hosta plantaginea</em></li>
          <li>Small-leaved Plantain Lily — <em>Hosta sieboldii</em></li>
          <li>Sycamore Maple — <em>Acer pseudoplatanus</em></li>
          <li>Tree-of-heaven — <em>Ailanthus altissima</em></li>
          <li>White Clover — <em>Trifolium repens</em></li>
          <li>Whorled Coreopsis — <em>Coreopsis verticillata</em></li>
        </ol>
      </div>
    </div>

    <h2 class="section-head">Observations &amp; Ideas</h2>
    <div class="two-col">
      <div>
        <p class="photo-caption" style="font-weight:600; text-transform:uppercase; letter-spacing:0.03em; color:var(--text-muted);">Observations</p>
        <div class="qa-block">
          <p class="a">Most of the clean up and maintenance projects I have planned for the site may drastically change the microclimates. For example, Zone 4 will get much more afternoon summer sun without the dense shade trees and vines along the north western property line.</p>
        </div>
        <div class="qa-block">
          <p class="a">Zone 5 has lots of potential fuel and mulch. The compost pile is covered with dry brush that can be shredded and used as mulch. The Norway maples can be cut back to season and use as firewood.</p>
        </div>
        <div class="qa-block">
          <p class="a">Zone 2 is currently a pass through zone. Most circulation paths go from Zone 1 to Zone 3 while walking through Zone 2. Aside from the mature decorative trees there isn't really keeping anyone in Zone 2.</p>
        </div>
      </div>
      <div>
        <p class="photo-caption" style="font-weight:600; text-transform:uppercase; letter-spacing:0.03em; color:var(--text-muted);">Ideas</p>
        <div class="qa-block">
          <p class="a">I've always wanted a reason to grow espalier fruit trees closer to the house and the pathway between the house and the pool deck could be a great fit for this.</p>
        </div>
        <div class="qa-block">
          <p class="a">Instead of building a pergola or some kind of man made structure to provide shade over the pool, I could replace the hostas with vining plants like grapes, or cold hardy kiwi and passion flower. Then this space can provide some kind of fruit yield while shading the areas where people spend the most time.</p>
        </div>
        <div class="qa-block">
          <p class="a">Bring more clover closer to the house instead of having it in far out zones.</p>
        </div>
        <div class="qa-block">
          <p class="a">Incorporate cooking area and fire pit into zone 2 so its close enough to where people gather but far enough from any flammable structure.</p>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- FOOTER:START -->
<!-- FOOTER:END -->
</body>
</html>
```

- [ ] **Step 2: Stamp and verify**

```bash
python3 scripts/build_nav.py
```

Expected: `stamped docs/microclimates.html`.

```bash
grep -c 'class="site-nav"' docs/microclimates.html   # expect: 1
grep -c 'class="site-footer"' docs/microclimates.html   # expect: 1
grep -c '<img' docs/microclimates.html   # expect: 2
grep -rn 'href="/' docs/microclimates.html   # expect: nothing
grep -rn 'src="/' docs/microclimates.html   # expect: nothing
```

Confirm the two image files referenced actually exist (`docs/assets/zones-design/microclimates-aerial.jpg`, `docs/assets/zones-design/microclimates-map.jpg`, both from Task 1). Read through the finished page for well-formedness. You likely don't have a browser tool — substitute structural inspection as in prior phases.

- [ ] **Step 3: Commit**

```bash
git add docs/microclimates.html
git commit -m "Add the Microclimates page"
```

---

### Task 3: Build the Current Zones page

**Files:**
- Create: `docs/current-zones.html`

**Interfaces:**
- Consumes: `docs/assets/zones-design/current-zones-map.jpg`, `current-zones-strengths-1.jpg`, `current-zones-strengths-2.jpg` (Task 1). Consumes the CSS pattern from `docs/microclimates.html` (Task 2) — read that file's `<style>` block and reuse it verbatim (same class names: `.panel`, `.photo-block`, `.matrix-table`, `.table-scroll`, `.two-col`, `.species-list`, `.qa-block` — this page won't use `.species-list`/`.two-col` for species, but will reuse `.two-col` for the SWOT grid and `.matrix-table`/`.table-scroll` for the zone matrix).

- [ ] **Step 1: Create the page**

Create `docs/current-zones.html` using the identical `<head>`/`<style>` block from `docs/microclimates.html` (copy it verbatim — same CSS classes, same variables, same `body { margin: 0; }`), changing only the `<title>` to `Current Zones — Lot #86`. Add one new CSS class not in Task 2's page, for the SWOT grid's 4 labeled sections:

```css
  .swot-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: var(--text-muted); margin: 0 0 8px; }
  .swot-list { font-size: 13px; color: var(--text-secondary); line-height: 1.7; margin: 0; padding-left: 18px; }
```

Body content:

```html
<!-- NAV:START -->
<!-- NAV:END -->
<div class="viz-root">
  <div class="wrap">
    <header>
      <h1>Current Zones</h1>
      <p class="subhead">The five permaculture zones as they exist today — Zone 01 (most intensively used, closest to the house) through Zone 05 (least visited, wild) — with the existing-conditions matrix, photos, and a SWOT analysis of the current layout.</p>
    </header>

    <div class="photo-block">
      <img src="assets/zones-design/current-zones-map.jpg" alt="Current Zones map showing the five zone boundaries and circulation paths">
      <p class="photo-caption">Current Zone Map — scale 1" = 20', north -65.43°, location 41°34'22.04"N 72°38'03.90"W, elevation min 106 ft / max 114 ft. Circulation: car foot path; daily foot path house-to-driveway; daily foot path walk dog/get eggs; monthly foot path coop-to-compost; seasonal truck path camper &amp; firewood.</p>
      <p class="photo-credit">Map created by Andrew Keser, August 2026.</p>
    </div>

    <h2 class="section-head">Zone Legend</h2>
    <div class="table-scroll">
      <table class="matrix-table">
        <tr><th>Zone</th><th>Definition</th></tr>
        <tr><td>Zone 01</td><td>House, front &amp; side yard</td></tr>
        <tr><td>Zone 02</td><td>Flower &amp; shade gardens</td></tr>
        <tr><td>Zone 03</td><td>Veg garden &amp; chickens</td></tr>
        <tr><td>Zone 04</td><td>Back yard with work areas</td></tr>
        <tr><td>Zone 05</td><td>Least maintained or visited area, primarily invasive vines</td></tr>
      </table>
    </div>

    <h2 class="section-head">Existing Conditions</h2>
    <div class="table-scroll">
      <table class="matrix-table">
        <tr><th></th><th>Zone 01</th><th>Zone 02</th><th>Zone 03</th><th>Zone 04</th><th>Zone 05</th></tr>
        <tr><td><b>Description</b></td><td>House, front and side yards</td><td>Shade and flower gardens</td><td>Veg garden and chicken coop</td><td>Back yard and work areas</td><td>Unmaintained wild area</td></tr>
        <tr><td><b>Frequency of visits</b></td><td>Daily</td><td>Daily</td><td>Daily</td><td>Weekly</td><td>Rarely visit prior to this course</td></tr>
        <tr><td><b>Theme / active primary</b></td><td>Living area, home access, song bird feeding area</td><td>Ornamental flowering plants and trees</td><td>Growing vegetables &amp; herbs, chickens</td><td>Wood piles, fire pit, brick oven</td><td>Mature trees, overgrown invasive vines &amp; shrubs</td></tr>
        <tr><td><b>Water</b></td><td>Water connection, spigot with 150ft hose</td><td>Within range of watering system</td><td>No current water connection</td><td>No water system in reach</td><td>Never watered</td></tr>
        <tr><td><b>Structures</b></td><td>Single family home</td><td>Stone walkway, above ground pool &amp; pool deck</td><td>Chicken coop, tool shed, feed storage, fencing</td><td>Fire pit, brick oven, camper</td><td>Not applicable</td></tr>
        <tr><td><b>Plants / plant systems</b></td><td>Ornamental flowers and shrubs, shade tree</td><td>Shade trees, perennial flowers &amp; shrubs</td><td>Herbs &amp; vegetables</td><td>Grapes, blueberries, apple trees, peach tree, lawn grass</td><td>Mature oaks, Norway spruce, eastern pine, invasive ground cover</td></tr>
        <tr><td><b>Animals</b></td><td>Domesticated dogs &amp; cats, squirrels, birds, skunks, raccoons</td><td>Same as Zone 01</td><td>+ domesticated chickens, groundhogs, red fox</td><td>+ coyote, deer, raptor birds</td><td>Same as Zone 04</td></tr>
        <tr><td><b>Additional considerations</b></td><td>Annual plantings in place can be replaced with perennials</td><td>Mature trees starting to compete, need to decide what stays</td><td>Overgrown property lines provide too much shade for grow beds</td><td>Willing to reduce total lawn coverage in favor of lower maintenance option</td><td>Covered in poison ivy, Virginia creeper &amp; Asiatic bittersweet</td></tr>
      </table>
    </div>

    <h2 class="section-head">Zone Strengths</h2>
    <div class="photo-block">
      <img src="assets/zones-design/current-zones-strengths-1.jpg" alt="Zone 1 pool deck and Zone 5 back area photos">
      <p class="photo-caption"><b>Zone 1 pool deck</b> creates the perfect dark, moist, shaded habitat to store hardwood logs inoculated with mushrooms.</p>
      <p class="photo-caption"><b>Zone 5 area</b> largely unused or maintained for years. After pruning this back we will be able to produce a yield of firewood, woody material to shred and mulch for groundcover. The mulberry tree is dying back, so most of its dead or dying branches will be buried or composted to improve soil health in other zones. I plan to coppice the maples to harvest the logs and use future sprouts as source of mulch.</p>
      <p class="photo-credit">Photos by Andrew Keser, June &amp; August 2026.</p>
    </div>
    <div class="photo-block">
      <img src="assets/zones-design/current-zones-strengths-2.jpg" alt="Zone 1 front porch and NW side yard path photos">
      <p class="photo-caption"><b>Zone 1 front porch</b> is most used outdoor space with daily use. Shaded porch provides great place to relax and drink a cup of coffee while bird or people watching. Everything has grown well here over the years.</p>
      <p class="photo-caption"><b>Zone 1 north western side</b> of the property facing south. The path between the hedgerow and the hostas along the deck is the most walked pathway on the property with daily use. To get from the back door of the house to the chicken coop, you walk from Zone 1 to Zone 3 while passing through Zone 2.</p>
      <p class="photo-credit">Photos by Andrew Keser, June &amp; August 2026.</p>
    </div>

    <h2 class="section-head">SWOT Analysis</h2>
    <div class="two-col">
      <div>
        <p class="swot-label">Strengths</p>
        <ul class="swot-list">
          <li>Even within .43 acres, there's still a wide range of microclimates within zones which can provide a variety of habitats or spaces to produce a yield.</li>
          <li>For the most part, each zone is a blank slate with flexibility around what is done moving forward.</li>
          <li>Current plantings in less than ideal zone can be transplanted to somewhere more appropriate.</li>
        </ul>
        <p class="swot-label" style="margin-top:18px;">Opportunities</p>
        <ul class="swot-list">
          <li>Utilize Zones 1 &amp; 2 more for producing yields of flowers, herbs and fruits.</li>
          <li>Utilize microclimates in Zones 1 &amp; 2 to add diversity to plant life and habitats they provide.</li>
          <li>Bring more intention to what's planted so everything is serving a purpose, producing a yield or habitat.</li>
          <li>Remove non-native varieties so plants and trees that are there are providing habitat for native animals and insects.</li>
          <li>Add features to Zone 2 so people can spend time there and enjoy the heavily shaded areas full of ornamental trees and perennial plants.</li>
        </ul>
      </div>
      <div>
        <p class="swot-label">Weaknesses</p>
        <ul class="swot-list">
          <li>Current plantings are more circumstantial than they are intentionally planted to utilize a zone or benefit from proximity to home.</li>
          <li>Zones are underutilized.</li>
          <li>Lots of invasive species (invasive to Connecticut, USA) that have grown out of control.</li>
          <li>Poor use of Zones 1 &amp; 2, given how frequently they are visited and used.</li>
        </ul>
        <p class="swot-label" style="margin-top:18px;">Threats</p>
        <ul class="swot-list">
          <li>Invasive shrubs, vines and tree species in Zone 5 render the space unusable and dangerous to use — dead limbs could fall with strong winds, and poison ivy covers the ground where the adjacent neighbors pass through.</li>
          <li>The weight of the Asiatic bittersweet and Virginia creeper growing on the fence in Zone 5 is already leading to structural damage.</li>
          <li>Overgrown property lines reduce sun exposure for prime growing areas like vegetable garden and fruit trees/bushes in Zone 4.</li>
        </ul>
      </div>
    </div>
  </div>
</div>
<!-- FOOTER:START -->
<!-- FOOTER:END -->
```

Note: the source SWOT threat about poison ivy names visiting "neighborhood kids" by role only in the original ("neighborhood kids love to come look at our chickens") — this plan's version above generalizes it to "the adjacent neighbors," matching this repo's established privacy convention for third parties. This is a deliberate wording adjustment from the literal source text, the one intentional deviation from "verbatim" in this task — every other line is unchanged.

- [ ] **Step 2: Stamp and verify**

```bash
python3 scripts/build_nav.py
```

Expected: `stamped docs/current-zones.html`.

```bash
grep -c '<img' docs/current-zones.html   # expect: 3
grep -rn 'href="/' docs/current-zones.html   # expect: nothing
grep -rn 'src="/' docs/current-zones.html   # expect: nothing
grep -c 'neighborhood kids' docs/current-zones.html   # expect: 0 (deliberately generalized per the note above)
```

Confirm the three image files exist. Confirm NAV/FOOTER stamped once each.

- [ ] **Step 3: Commit**

```bash
git add docs/current-zones.html
git commit -m "Add the Current Zones page"
```

---

### Task 4: Build the Zones Brainstorm page

**Files:**
- Create: `docs/zones-brainstorm.html`

**Interfaces:**
- Consumes: `docs/assets/zones-design/brainstorm-zone1-nw-1.jpg`, `brainstorm-zone1-nw-2.jpg`, `brainstorm-zone1-se.jpg`, `brainstorm-map.jpg` (Task 1). Reuses the CSS pattern from `docs/microclimates.html` (Task 2) — same as Task 3.

- [ ] **Step 1: Create the page**

Create `docs/zones-brainstorm.html` using the identical `<head>`/`<style>` block from `docs/microclimates.html` (copy verbatim), title `Zones Brainstorm — Lot #86`. No new CSS classes needed beyond what Tasks 2-3 already defined (`.qa-block` for the Q&A pairs, `.photo-block` for photos, `.matrix-table`/`.table-scroll` for the proposed matrix).

Body content:

```html
<!-- NAV:START -->
<!-- NAV:END -->
<div class="viz-root">
  <div class="wrap">
    <header>
      <h1>Zones Brainstorm</h1>
      <p class="subhead">Proposed changes to the current zone layout — an exploratory brainstorm, not committed design decisions. Feeds the Mid-Term Site Water Design Brainstorm.</p>
    </header>

    <h2 class="section-head">Questions</h2>
    <div class="qa-block">
      <p class="q">Review your client must/nice/avoid list. How might you consider changing the zone layout to meet these needs?</p>
      <p class="a">The overall layout can remain the same, but the ways we use them can be done more effectively so they align to current use patterns. For example, adding a seating area in the already shaded gardens of Zone 02 could offer another gathering space with good views similar to the front porch in Zone 01.</p>
    </div>
    <div class="qa-block">
      <p class="q">How can you place elements in proximity to other elements to improve efficiency based on location?</p>
      <p class="a">Reducing the distance between the house and the wood pile is a clear opportunity after this analysis. The wood pile can be moved to be next to the south eastern side of the house in Zone 01 instead of being all the way out in Zone 04. Now wood can be dropped off in our driveway, instead of down the adjacent neighbors' driveway where it has to be hauled back up to the house for burning.</p>
    </div>
    <div class="qa-block">
      <p class="q">How does the site's slope and aspect influence the zoning?</p>
      <p class="a">The lot is a gentle slope with a max elevation of 114 ft and min of 106 ft. This impacts the direction of water run off but other than that, it doesn't dictate views or paths people take. The lot is much longer than it is wide and the slope is not really noticeable unless you are actively measuring it.</p>
    </div>
    <div class="qa-block">
      <p class="q">What client elements might be best placed on the edge between two zones?</p>
      <p class="a">The edges between Zone 02 and Zones 01 and 03 have the most opportunities to expand upon what's already there or where people are already walking through or visiting. My goal is to draw people through the yard from Zone 01 through Zone 04 which can be done by placing pathways, seating areas and clearings to draw the eye towards the back of the property.</p>
    </div>
    <div class="qa-block">
      <p class="q">Are there areas of the site that are far from the house that are visited frequently?</p>
      <p class="a">Far from the house is a relatively short distance given the lot is .43 acres total, but in a practical sense, Zones 4 &amp; 5 don't require daily visits for chores or active use, but it's fairly easy to notice something out of place in those zones while standing in Zone 3. We also recently installed game cameras to track the movement of animals on the property which gives us instant access to Zones 4 &amp; 5 from anywhere.</p>
    </div>
    <div class="qa-block">
      <p class="q">Do you have ideas for ways to save energy, time, and resources by adjusting the current zones?</p>
      <p class="a">The zones will likely remain as is, but what we do within each will be adapted to amplify what's already happening. For example, Zone 02 is already used daily, but since it lacks proper seating or gathering space, there's no real reason to stay there since you're likely passing through to Zone 03. Moving the wood pile and work station closer to the house will help reduce how much transporting needs to be done. Zones 4 and 5 already have mature trees growing and producing material to mulch or chip so I want to encourage that more to keep a steady supply of wood chips and mulch.</p>
    </div>

    <h2 class="section-head">Zone 01 — North Western Side Yard</h2>
    <div class="photo-block">
      <img src="assets/zones-design/brainstorm-zone1-nw-1.jpg" alt="Zone 1 NW side yard, hostas along pool deck and annual/perennial garden bed">
      <p class="photo-caption">Remove hostas and replace with something that can provide shade for pool deck and walking path to back yard. Retain view towards backyard with clear site line to draw people back in the yard.</p>
      <p class="photo-caption">Annual and perennial garden gets hot summer sun but this bed could be used for vining fruits that can provide shade and fruit. Generally speaking I would like to diversify from hostas to sun loving plants.</p>
    </div>
    <div class="photo-block">
      <img src="assets/zones-design/brainstorm-zone1-nw-2.jpg" alt="Zone 1 NW side yard, boxwood hedge and house-side microclimate">
      <p class="photo-caption">Relocate hostas to Zone 4-5 in shadier microclimate and replace with grapes or other cold hardy fruits that can double as shade canopy over deck. Consider replacing boxwood hedge with some shade trees and pollinator plants.</p>
      <p class="photo-caption">Utilize microclimate along house to grow espalier trees that can help block late afternoon sun and cool the house. Or consider replacing boxwood hedge with something that adds height and provides shade.</p>
    </div>

    <h2 class="section-head">Zone 01 — Southeastern Side Yard</h2>
    <div class="photo-block">
      <img src="assets/zones-design/brainstorm-zone1-se.jpg" alt="Zone 1 SE side yard, boxwood hedge and former elevated deck">
      <p class="photo-caption">Boxwood hedge to be removed and replaced with line of willow trees to be pollarded to produce fence and mulch material. This is the lowest elevation point on the property, so I am considering a mini-swale to help collect and store storm water runoff.</p>
      <p class="photo-caption">Former elevated deck w/entrance to home in Zone 1 now sits empty. This section of Zone 1 will be used as a drop off point for raw materials, firewood storage and work station. The long term plan is to not depend on the adjacent neighbors' driveway for wood delivery and camper load in/load out, so a truck must be able to drive through this pathway moving forward.</p>
      <p class="photo-credit">Photos by Andrew Keser, June 2026.</p>
    </div>

    <h2 class="section-head">Brainstorm Map</h2>
    <div class="photo-block">
      <img src="assets/zones-design/brainstorm-map.jpg" alt="Zones Brainstorm map with proposed changes annotated per zone">
      <p class="photo-caption">Zones Brainstorm Map — scale 1" = 20', north -65.43°, location 41°34'22.04"N 72°38'03.90"W, elevation min 106 ft / max 114 ft.</p>
      <p class="photo-credit">Map created by Andrew Keser, August 2026.</p>
    </div>
    <div class="table-scroll">
      <table class="matrix-table">
        <tr><th>Zone</th><th>Proposed change</th></tr>
        <tr><td>Zone 1</td><td>Add more shade plants to Zone 1 in areas where people spend time (deck, porch, walkway to deck). Move wood pile to behind driveway instead of Zone 4.</td></tr>
        <tr><td>Zone 2</td><td>Add seating area, add more native plantings in ornamental shade garden. Collect and redirect water to trees.</td></tr>
        <tr><td>Zone 3</td><td>Move shed to shaded area by coop, remove fencing and use raised beds.</td></tr>
        <tr><td>Zone 4</td><td>Rebuild 3-bin compost system, move wood pile and work area to Zone 1.</td></tr>
        <tr><td>Zone 5</td><td>Get invasive plants under control, pollard maples to regrow material to chip.</td></tr>
      </table>
    </div>

    <h2 class="section-head">Proposed Future State</h2>
    <p class="subhead">Same row structure as the <a href="current-zones.html">Current Zones</a> existing-conditions matrix — read them side by side.</p>
    <div class="table-scroll">
      <table class="matrix-table">
        <tr><th></th><th>Zone 01</th><th>Zone 02</th><th>Zone 03</th><th>Zone 04</th><th>Zone 05</th></tr>
        <tr><td><b>Frequency of visits</b></td><td>Daily</td><td>Daily</td><td>Daily</td><td>Monthly</td><td>Monthly</td></tr>
        <tr><td><b>Theme / active primary</b></td><td>Plantings provide shade, fruits, herbs and flowers to attract birds</td><td>Stop and sit or pass through</td><td>Veg garden</td><td>Fruit, berry, hops yield</td><td>Mimic nature, build habitat</td></tr>
        <tr><td><b>Water</b></td><td>Water spigot on southeast side of house by driveway</td><td>Hose in Zone 01 reaches Zone 02</td><td>Buried hose from Zone 01 runs to Zone 03 but needs repair to avoid leak</td><td>Need to capture and direct water around trees for heavy rain events</td><td>No water access</td></tr>
        <tr><td><b>Structures</b></td><td>No new structures</td><td>Small water feature, shaded seating</td><td>Build new shed &amp; relocate within zone</td><td>Build new compost system</td><td>No structures</td></tr>
        <tr><td><b>Plants / plant systems</b></td><td>Guilds of native mixed perennials</td><td>Decorative shade trees and flowering shrubs</td><td>Primary veg garden in raised beds</td><td>Dwarf fruit tree orchard, shrubs and hop vines</td><td>Mature oaks, maples &amp; spruce trees</td></tr>
        <tr><td><b>Animals</b></td><td>Attract wild song birds &amp; small mammals</td><td>Wild song birds &amp; small mammals</td><td>Keep chickens in Zone 03, protect against predators</td><td>Provide habitat for animals &amp; insects</td><td>Provide habitat for animals &amp; insects</td></tr>
        <tr><td><b>Additional considerations</b></td><td>Least flexibility in terms of what can change aside from plantings</td><td>Add shade cover so gathering areas aren't so hot in summer afternoons</td><td>This zone will likely change the most with clean up projects this fall</td><td>Mulch the lawn in this area and fully commit to orchard production</td><td>This area is undergoing treatment to remove poison ivy &amp; bittersweet</td></tr>
      </table>
    </div>
  </div>
</div>
<!-- FOOTER:START -->
<!-- FOOTER:END -->
```

Note: two source lines mentioned "our neighbors driveway" — both rewritten above to "the
adjacent neighbors' driveway," matching this repo's established third-party-reference
convention (same deliberate deviation as Task 3, applied consistently).

- [ ] **Step 2: Stamp and verify**

```bash
python3 scripts/build_nav.py
```

Expected: `stamped docs/zones-brainstorm.html`.

```bash
grep -c '<img' docs/zones-brainstorm.html   # expect: 4
grep -rn 'href="/' docs/zones-brainstorm.html   # expect: nothing
grep -rn 'src="/' docs/zones-brainstorm.html   # expect: nothing
grep -c 'our neighbors driveway' docs/zones-brainstorm.html   # expect: 0 (original unqualified source phrase)
grep -c 'adjacent neighbors' docs/zones-brainstorm.html   # expect: 2 (both instances reworded)
```

Confirm the four image files exist. Confirm NAV/FOOTER stamped once each. Confirm the link to `current-zones.html` resolves (file exists from Task 3).

- [ ] **Step 3: Commit**

```bash
git add docs/zones-brainstorm.html
git commit -m "Add the Zones Brainstorm page"
```

---

### Task 5: Build the Zones & Design hub page

**Files:**
- Create: `docs/zones-design.html`

**Interfaces:**
- Consumes: `docs/microclimates.html`, `docs/current-zones.html`, `docs/zones-brainstorm.html` (Tasks 2-4) — links to all three.

- [ ] **Step 1: Create the hub page**

Create `docs/zones-design.html` (same shape as `docs/sun-solar.html`'s hub, adapted):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Zones &amp; Design — Lot #86</title>
<style>
  .viz-root {
    color-scheme: light;
    --surface-1: #fcfcfb; --page: #f9f9f7; --text-primary: #0b0b0b;
    --text-secondary: #52514e; --text-muted: #898781; --border: rgba(11,11,11,0.10);
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) .viz-root {
      color-scheme: dark;
      --surface-1: #1a1a19; --page: #0d0d0d; --text-primary: #ffffff;
      --text-secondary: #c3c2b7; --text-muted: #898781; --border: rgba(255,255,255,0.10);
    }
  }
  :root[data-theme="dark"] .viz-root {
    color-scheme: dark;
    --surface-1: #1a1a19; --page: #0d0d0d; --text-primary: #ffffff;
    --text-secondary: #c3c2b7; --text-muted: #898781; --border: rgba(255,255,255,0.10);
  }
  * { box-sizing: border-box; }
  body { margin: 0; }
  .viz-root {
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    background: var(--page); color: var(--text-primary); min-height: 60vh;
    padding: 32px 20px 60px;
  }
  .wrap { max-width: 900px; margin: 0 auto; }
  h1 { font-size: 22px; font-weight: 600; margin: 0 0 6px; }
  .subhead { color: var(--text-secondary); font-size: 14px; line-height: 1.5; margin: 0 0 24px; }
  .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
  .nav-card {
    display: block; background: var(--surface-1); border: 1px solid var(--border);
    border-radius: 12px; padding: 18px 20px; text-decoration: none; color: inherit;
  }
  .nav-card h3 { font-size: 15px; font-weight: 600; margin: 0 0 6px; color: var(--text-primary); }
  .nav-card p { font-size: 13px; color: var(--text-secondary); margin: 0; line-height: 1.5; }
</style>
</head>
<body>
<!-- NAV:START -->
<!-- NAV:END -->
<div class="viz-root">
  <div class="wrap">
    <header>
      <h1>Zones &amp; Design</h1>
      <p class="subhead">The property's permaculture zones — current conditions, the microclimates within them, and a brainstorm of proposed changes for the future.</p>
    </header>
    <div class="card-grid">
      <a class="nav-card" href="microclimates.html">
        <h3>Microclimates</h3>
        <p>Four microclimate types, known plant species, and observations on how clearing will shift them.</p>
      </a>
      <a class="nav-card" href="current-zones.html">
        <h3>Current Zones</h3>
        <p>The five zones as they exist today — existing-conditions matrix, photos, and a SWOT analysis.</p>
      </a>
      <a class="nav-card" href="zones-brainstorm.html">
        <h3>Zones Brainstorm</h3>
        <p>Proposed changes to the zone layout — exploratory, not committed design decisions.</p>
      </a>
    </div>
  </div>
</div>
<!-- FOOTER:START -->
<!-- FOOTER:END -->
</body>
</html>
```

- [ ] **Step 2: Stamp and verify**

```bash
python3 scripts/build_nav.py
```

Expected: `stamped docs/zones-design.html`.

```bash
grep -c 'class="site-nav"' docs/zones-design.html   # expect: 1
grep -c 'class="site-footer"' docs/zones-design.html   # expect: 1
grep -c 'href="microclimates.html"\|href="current-zones.html"\|href="zones-brainstorm.html"' docs/zones-design.html   # expect: 3
```

Confirm all three linked files exist (Tasks 2-4). Confirm each link resolves.

- [ ] **Step 3: Commit**

```bash
git add docs/zones-design.html
git commit -m "Add the Zones & Design hub page"
```

---

### Task 6: Wire Zones & Design into the nav and Home page

**Files:**
- Modify: `docs/_partials/nav.html`
- Modify: `docs/index.html`

**Interfaces:**
- Consumes: `docs/zones-design.html` (Task 5).

- [ ] **Step 1: Read the current nav and Home page**

Both files may have shifted since this plan was written (V3a's merge already added
Species Inventory). Read them fresh before editing — don't assume the exact text below
still matches; adapt the edit to whatever the actual current content is, following the
same pattern as every prior nav/Home edit in this project (add a link/card in the last
position, matching the established structure).

- [ ] **Step 2: Add to the nav partial**

In `docs/_partials/nav.html`'s `.site-nav__links` div, add
`<a href="zones-design.html">Zones &amp; Design</a>` as the last link (after Species
Inventory).

- [ ] **Step 3: Update the Home page**

In `docs/index.html`:
- Remove the Zones & Design `<div class="nav-card soon">` card from "Coming later".
- Add a real `<a class="nav-card" href="zones-design.html">` card to the end of
  "Available now", matching the exact markup pattern of the other real cards (an `<h3>`
  title and a `<p>` description — write a description in the same voice as the others,
  e.g. "Current permaculture zones, microclimates, and the design brainstorm for their
  future.").
- Since this empties "Coming later" (no cards left), **remove the entire "Coming later"
  section** — its `<h2 class="section-head">Coming later</h2>` heading and the now-empty
  `<div class="card-grid">...</div>` that followed it. Don't leave an empty section
  header with nothing under it.
- Update the subhead sentence (the one already edited twice in this project's history —
  V2 and V3a both touched it) so it no longer promises anything "to follow": every
  section is now live. Read the current sentence and rewrite it to reflect that, e.g.
  "A working reference for designing this 0.43-acre property's permaculture future —
  climate, solar, wind, hazard, watershed, species, and zone data, all in one place."
  (adjust wording to fit the actual current sentence structure you find).

- [ ] **Step 4: Re-stamp and verify**

```bash
python3 scripts/build_nav.py
```

Expected: every `docs/*.html` page reports stamped (nav partial changed).

```bash
grep -c 'zones-design.html' docs/_partials/nav.html   # expect: 1
grep -c 'nav-card soon' docs/index.html   # expect: 0 (Coming later section fully removed)
grep -c 'Coming later' docs/index.html   # expect: 0
grep -rn 'href="/' docs/   # expect: nothing
```

- [ ] **Step 5: Commit**

```bash
git add docs/_partials/nav.html docs/index.html
git commit -m "Wire Zones & Design into the nav and Home page; retire the empty Coming later section"
```

Stage all re-stamped pages too (expected diff, not a mistake).

---

### Task 7: Final verification

**Files:** none created — verification only.

- [ ] **Step 1: Test suite**

```bash
python3 -m pytest scripts/tests/ -v
```

Expected: 16/16 pass (no script code changed in this plan).

- [ ] **Step 2: build_nav.py no-op**

```bash
python3 scripts/build_nav.py
```

Expected: `0 file(s) updated`.

- [ ] **Step 3: Site-wide link crawl**

```bash
ls docs/*.html | wc -l
```

Expected: 22 (18 pre-existing + 4 new: hub + 3 sub-pages).

For every file, extract every internal `href`/`src` and confirm targets exist, including
the 9 image references across the 3 content pages (2 on Microclimates, 3 on Current
Zones, 4 on Zones Brainstorm — matching the 9 unique files from Task 1 one-to-one, no
reuse, no hub images). Confirm zero root-absolute links anywhere. Confirm all 4 new pages are
reachable: the hub from nav (22 pages) and from Home's "Available now" grid; the 3
sub-pages from the hub's card grid; `current-zones.html` ↔ `zones-brainstorm.html`'s
cross-link. Confirm no third-party names — specifically re-check that "neighbor" only
appears in the generalized "adjacent neighbors" form, never with any other qualifier.
Confirm image file sizes: `du -sh docs/assets/zones-design/` should be well under 3MB
total (compressed, not the original ~13MB).

You cannot verify the CSS light/dark toggle or actual visual layout without a browser —
say so explicitly.

- [ ] **Step 4: Commit if anything needed fixing**

If Step 3 found and fixed something, commit with a clear message. Otherwise report the
clean result, no commit.

## Self-Review Notes

- **Spec coverage:** image compression (Task 1), all 3 content pages (Tasks 2-4), hub
  (Task 5), nav/Home wiring including the empty-section cleanup (Task 6), verification
  (Task 7) — matches the spec's full scope including the "Coming later" removal the spec
  calls out explicitly.
- **Placeholder scan:** no TBD/TODO. All body content is real, complete text — either
  verbatim from source or (for the two neighbor-reference lines) an explicit, justified,
  narrowly-scoped deviation with its own verification check.
- **Consistency:** Tasks 3-4 explicitly point at Task 2's file to copy CSS from, rather
  than re-deriving it — same class names used identically across all 4 new pages, so a
  future site-wide style change only needs updating (potentially) 4 places, consistent
  with this project's existing per-page-style-block convention (not a regression from
  how V1/V2 already work).
- **Third-party names:** two source lines named a family/neighbor context generically
  enough already ("neighborhood kids", "our neighbors driveway") that they needed
  rewording to match this repo's established convention (role-based, not even informal
  references) — flagged inline in Tasks 3-4 rather than silently changed, with grep
  checks to verify the rewording actually landed.
