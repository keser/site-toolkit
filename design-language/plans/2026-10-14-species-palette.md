# Species Palette Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `Species` token collection, three Lesson 07 species maps (status, layer, function) in PDC Pro Vision, and the matching microsite tokens.

**Architecture:** Palette values live as Ramps step names in a JSON file in this repo, validated by a small tested Python checker. Figma gets a `Species` variable collection aliasing those Ramps steps, three `map-key` variants, and a `Species` page with three map frames whose plant-symbol instances are overridden from a per-site CSV kept in the private `lot-86-site-plan` repo. The microsite reads the same values through `chart-tokens.css`.

**Tech Stack:** Python 3 (stdlib only) + pytest; Figma Plugin API via `use_figma` (load the `figma-use` skill first); plain static HTML/CSS; headless Chrome for screenshots.

**Spec:** `design-language/specs/2026-10-14-species-palette-design.md`

## Global Constraints

- Figma file: PDC Pro Vision, key `aF9SVeTLwFN8PCEiU2OSBQ`. Never edit the Base Map page (`0:1`) or any plant-symbol main component (`39:5716` deciduous tree, `39:5719` coniferous tree, `39:5745` shrub, `39:5773` hedgerow, `57:755` perennial).
- `Species` collection: modes `Light` and `Dark`; every variable aliases a `Ramps` variable; scopes exactly `["ALL_FILLS", "STROKE_COLOR"]`; 20 variables.
- Status values and borders: native = sage, Solid; naturalized = gold, Medium dash; cultivated = cobalt, Fine dash; invasive = coral, Solid, `weight/xl`, `coral/Casing`.
- Layer Light fills: canopy sage/700, sub-canopy sage/600, shrub sage/500, herbaceous sage/300, groundcover sage/200, vine violet/500, root amber/500; `layer/stroke` sage/800.
- Function letters: N nitrogen fixer, D dynamic accumulator, P pollinator / insectary, E edible, W wildlife food or habitat, M medicinal, B biomass / chop-and-drop.
- Validation floor: CIELAB ΔE ≥ 10 under normal vision and simulated deuteranopia, protanopia, tritanopia (Machado 2009, severity 1.0) for every pair of status Base colors and every adjacent pair of height-layer fills, in both modes. Contrast ≥ 3:1 for status Shade and `layer/stroke` against `#fcfcfb` and `#f0f0ee` (light) and `#1a1a19` (dark).
- Privacy: plant data (species per plant) goes only in `~/Code/keser/site-plans/lot-86-site-plan`. This public repo gets palette values, code, and the demo microsite only.
- Microsite conventions from `CLAUDE.md`: relative links, prefixed CSS, chart colors from `docs/assets/chart-tokens.css`, never meaning by color alone.
- Commit locally on branch `species-palette`; never push without Andrew's go-ahead.

## Review Focus

1. **A CSV row whose `symbol_id` doesn't exist in a frame**, or an unknown status/layer/letter → the apply script lists it in `problems` and leaves that symbol unchanged; it never throws midway or silently skips. (Task 8 Step 3 asserts on the returned `problems`.)
2. **A CSV row with blank `status` or `functions`** (Andrew hasn't filled it in yet) → that symbol keeps its gray look on the status/function maps, and the row is counted under `blank`, not `problems`. (Task 8.)
3. **A label-text color that loses contrast on the new fill** (black "DT" on sage/700) → the apply script picks black or white text by the fill's luminance. (Task 8 Step 1 test of `textOn`.)
4. **A palette JSON entry naming a Ramps step that doesn't exist** (typo `sage/550`) → the checker reports it as a failure instead of crashing with `KeyError`. (Task 1 test `test_unknown_ramp_step_is_reported`.)
5. **`chart-tokens.css` species values drifting from `species.json`** after a palette change → `check_chart_tokens.py tokens` fails with the token name. (Task 9 Step 1 test.)

---

## File map

| File | Responsibility |
|---|---|
| `design-language/tokens/ramps.json` (create) | Ramps primitives exported from Figma: `{"sage/500": "#698436", …}`. Public palette data. |
| `design-language/tokens/species.json` (create) | Species token → Ramps step per mode, plus the validation groups. The single source the checker, CSS, and Figma script use. |
| `tools/palette_check.py` (create) | Pure functions: hex → Lab, Machado simulation, ΔE, contrast, `check(ramps, palette)`. CLI prints failures. |
| `tools/tests/test_palette_check.py` (create) | Tests for the above. |
| `tools/check_chart_tokens.py` (modify) | `check_tokens()` also verifies the `--species-*` values against `species.json`. |
| `tools/tests/test_check_chart_tokens.py` (modify) | Test for the species drift check. |
| `docs/assets/chart-tokens.css` (modify) | Adds `--species-*` in all three blocks. |
| `docs/species-inventory.html` (modify) | Links `chart-tokens.css`; status and taxon colors move to tokens. |
| `lot-86-site-plan/site-plan/data/mapped-plants.csv` (create, private repo) | One row per mapped plant. |
| `design-language/specs/2026-10-14-species-palette-design.md` (modify) | Shipped log, validated Dark values. |

**Why a new tool (`palette_check.py`):** the chart-token validation script lived only in a scratchpad. This is the second palette needing the same check, which meets the "generalize when a second need appears" rule. Maintenance cost: one stdlib-only file with tests; failure mode is a wrong matrix constant, which the white-point and red/green tests catch.

---

### Task 1: Palette checker

**Files:**
- Create: `tools/palette_check.py`
- Test: `tools/tests/test_palette_check.py`

**Interfaces:**
- Produces: `hex_to_rgb(h) -> tuple[float,float,float]` (0–1 sRGB); `simulate(rgb, kind) -> rgb` with `kind in {"normal","deutan","protan","tritan"}`; `delta_e(hex_a, hex_b, kind="normal") -> float`; `contrast(hex_a, hex_b) -> float`; `check(ramps: dict, palette: dict) -> list[str]` (empty = pass). CLI: `python3 tools/palette_check.py design-language/tokens/ramps.json design-language/tokens/species.json`.
- Palette JSON shape (used by Tasks 2, 3, 9):

```json
{
  "tokens": { "status/native/base": {"light": "sage/500", "dark": "sage/400"} },
  "checks": {
    "floor_de": 10,
    "contrast_min": 3.0,
    "distinct": [["status/native/base", "status/naturalized/base"]],
    "adjacent": [["layer/canopy", "layer/sub-canopy"]],
    "edges": ["status/native/shade", "layer/stroke"],
    "surfaces": {"light": ["#fcfcfb", "#f0f0ee"], "dark": ["#1a1a19"]}
  }
}
```

- [ ] **Step 1: Write the failing tests**

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from palette_check import check, contrast, delta_e, hex_to_rgb, simulate

RAMPS = {"a/500": "#476de7", "b/500": "#698436", "c/500": "#ef5c58", "k/900": "#000000", "w/0": "#ffffff"}


def palette(tokens, **checks):
    base = {"floor_de": 10, "contrast_min": 3.0, "distinct": [], "adjacent": [], "edges": [],
            "surfaces": {"light": ["#ffffff"], "dark": ["#000000"]}}
    base.update(checks)
    return {"tokens": tokens, "checks": base}


def test_contrast_black_on_white_is_21():
    assert round(contrast("#000000", "#ffffff"), 1) == 21.0


def test_delta_e_of_a_color_with_itself_is_zero():
    assert delta_e("#698436", "#698436") == 0


def test_simulation_keeps_white_white():
    for kind in ("deutan", "protan", "tritan"):
        assert all(abs(c - 1) < 0.01 for c in simulate(hex_to_rgb("#ffffff"), kind))


def test_deuteranopia_collapses_red_green():
    assert delta_e("#ff0000", "#00b000", "deutan") < delta_e("#ff0000", "#00b000") / 2


def test_distinct_pair_below_floor_is_reported():
    p = palette({"x": {"light": "a/500", "dark": "a/500"}, "y": {"light": "a/500", "dark": "a/500"}},
                distinct=[["x", "y"]])
    assert any("x" in f and "y" in f for f in check(RAMPS, p))


def test_adjacent_checks_only_neighbors():
    t = {n: {"light": s, "dark": s} for n, s in (("p", "a/500"), ("q", "b/500"), ("r", "a/500"))}
    assert check(RAMPS, palette(t, adjacent=[["p", "q", "r"]])) == []


def test_low_contrast_edge_is_reported():
    p = palette({"e": {"light": "w/0", "dark": "k/900"}}, edges=["e"])
    assert len(check(RAMPS, p)) == 2


def test_unknown_ramp_step_is_reported():
    p = palette({"x": {"light": "a/550", "dark": "a/500"}})
    assert any("a/550" in f for f in check(RAMPS, p))
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tools/tests/test_palette_check.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'palette_check'`

- [ ] **Step 3: Write the implementation**

```python
#!/usr/bin/env python3
"""Checks a token palette for color-vision-deficiency separation and edge contrast.

Usage:
  python3 tools/palette_check.py design-language/tokens/ramps.json design-language/tokens/species.json
"""
import itertools, json, sys

# Machado, Oliveira & Fernandes (2009), severity 1.0, applied to linear RGB
MACHADO = {
    "protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}
KINDS = ("normal", "deutan", "protan", "tritan")

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def _lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _gam(c):
    c = min(max(c, 0.0), 1.0)
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def simulate(rgb, kind):
    if kind == "normal": return rgb
    lin = [_lin(c) for c in rgb]
    return tuple(_gam(sum(m * v for m, v in zip(row, lin))) for row in MACHADO[kind])

def _lab(rgb):
    r, g, b = (_lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)

def delta_e(a, b, kind="normal"):
    la, lb = _lab(simulate(hex_to_rgb(a), kind)), _lab(simulate(hex_to_rgb(b), kind))
    return sum((p - q) ** 2 for p, q in zip(la, lb)) ** 0.5

def contrast(a, b):
    lum = lambda h: sum(w * _lin(c) for w, c in zip((0.2126, 0.7152, 0.0722), hex_to_rgb(h)))
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

def check(ramps, palette):
    fails, c = [], palette["checks"]
    for mode in ("light", "dark"):
        hexes = {}
        for name, steps in palette["tokens"].items():
            step = steps[mode]
            if step not in ramps: fails.append(f"{mode} {name}: unknown Ramps step {step}")
            else: hexes[name] = ramps[step]
        pairs = [p for g in c["distinct"] for p in itertools.combinations(g, 2)]
        pairs += [p for g in c["adjacent"] for p in zip(g, g[1:])]
        for a, b in pairs:
            if a not in hexes or b not in hexes: continue
            for kind in KINDS:
                d = delta_e(hexes[a], hexes[b], kind)
                if d < c["floor_de"]: fails.append(f"{mode} {a} vs {b}: ΔE {d:.1f} under {kind}")
        for e in c["edges"]:
            if e not in hexes: continue
            for s in c["surfaces"][mode]:
                r = contrast(hexes[e], s)
                if r < c["contrast_min"]: fails.append(f"{mode} {e} on {s}: contrast {r:.2f}")
    return fails

if __name__ == "__main__":
    ramps, palette = (json.load(open(p)) for p in sys.argv[1:3])
    fails = check(ramps, palette)
    for f in fails: print("FAIL", f)
    print("OK" if not fails else f"{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tools -q`
Expected: all pass (28 existing + 8 new).

- [ ] **Step 5: Commit**

```bash
git add tools/palette_check.py tools/tests/test_palette_check.py
git commit -m "Add palette_check: CVD separation and edge contrast for token palettes"
```

---

### Task 2: Export Ramps and validate the Species values

**Files:**
- Create: `design-language/tokens/ramps.json`, `design-language/tokens/species.json`

**Interfaces:**
- Consumes: `palette_check.check` and CLI (Task 1).
- Produces: `species.json` with all 20 tokens and both modes passing the checker. Token names exactly: `status/{native,naturalized,cultivated,invasive}/{tint,base,shade}`, `layer/{canopy,sub-canopy,shrub,herbaceous,groundcover,vine,root,stroke}`.

- [ ] **Step 1: Export Ramps and the Color Roles aliases from Figma** (read-only `use_figma`)

```js
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const hex = c => "#" + [c.r, c.g, c.b].map(x => Math.round(x * 255).toString(16).padStart(2, "0")).join("");
const ramps = cols.find(c => c.name === "Ramps"), roles = cols.find(c => c.name === "Color Roles");
const out = { ramps: {}, roles: {} };
for (const id of ramps.variableIds) { const v = await figma.variables.getVariableByIdAsync(id); out.ramps[v.name] = hex(v.valuesByMode[ramps.modes[0].modeId]); }
for (const id of roles.variableIds) {
  const v = await figma.variables.getVariableByIdAsync(id); const val = v.valuesByMode[roles.modes[0].modeId];
  out.roles[v.name] = val.type === "VARIABLE_ALIAS" ? (await figma.variables.getVariableByIdAsync(val.id)).name : hex(val);
}
return out;
```

Write `out.ramps` to `design-language/tokens/ramps.json` (sorted keys, 2-space indent). Keep `out.roles` for Step 2; it tells you which Ramps step each `<hue>/Tint|Base|Shade` uses.

- [ ] **Step 2: Write `species.json` with Light values from the spec and Dark candidates**

Light: each `status/<value>/{tint,base,shade}` takes the step that `<hue>/Tint|Base|Shade` aliases in `out.roles` (hue per the Global Constraints). Layer Light values as in Global Constraints.
Dark candidates (spec rule): Base and Shade one step lighter than Light, Tint one step darker; layer fills one step lighter; `layer/stroke` → sage/200.
`checks`:

```json
{
  "floor_de": 10,
  "contrast_min": 3.0,
  "distinct": [["status/native/base", "status/naturalized/base", "status/cultivated/base", "status/invasive/base"]],
  "adjacent": [["layer/canopy", "layer/sub-canopy", "layer/shrub", "layer/herbaceous", "layer/groundcover"]],
  "edges": ["status/native/shade", "status/naturalized/shade", "status/cultivated/shade", "status/invasive/shade", "layer/stroke"],
  "surfaces": {"light": ["#fcfcfb", "#f0f0ee"], "dark": ["#1a1a19"]}
}
```

- [ ] **Step 3: Run the checker**

Run: `python3 tools/palette_check.py design-language/tokens/ramps.json design-language/tokens/species.json`
Expected on first run: possibly FAIL lines. For each, move the failing token one Ramps step (or, for a status pair, change hue only with Andrew's OK) and re-run until `OK`. The adjacent sage layers are the likeliest failure; if 300 vs 200 fails, try 300 vs 100 for groundcover before anything else. Record every change and the final ΔE minimums.

- [ ] **Step 4: Checkpoint with Andrew if any Light value changed from the spec.** Light values are what the deck shows; show the before/after and get a yes before continuing. Dark-only changes need no checkpoint.

- [ ] **Step 5: Commit**

```bash
git add design-language/tokens/ramps.json design-language/tokens/species.json
git commit -m "Add Species palette values, validated for CVD separation and contrast"
```

---

### Task 3: Create the `Species` collection in Figma

**Files:** none in the repo (Figma only).

**Interfaces:**
- Consumes: `species.json` (Task 2) — paste its `tokens` object into the script as `TOKENS`.
- Produces: collection `Species` with modes `Light`, `Dark`; 20 variables named exactly as the token names; return their IDs.

- [ ] **Step 1: Run the create script** (`use_figma`, load `figma-use` first)

```js
const TOKENS = /* paste species.json "tokens" here */ {};
const cols = await figma.variables.getLocalVariableCollectionsAsync();
if (cols.some(c => c.name === "Species")) throw new Error("Species already exists; inspect before re-running");
const ramps = cols.find(c => c.name === "Ramps");
const byName = {};
for (const id of ramps.variableIds) { const v = await figma.variables.getVariableByIdAsync(id); byName[v.name] = v; }
const col = figma.variables.createVariableCollection("Species");
col.renameMode(col.modes[0].modeId, "Light");
const dark = col.addMode("Dark"), light = col.modes[0].modeId;
const created = [], missing = [];
for (const [name, steps] of Object.entries(TOKENS)) {
  const l = byName[steps.light], d = byName[steps.dark];
  if (!l || !d) { missing.push(name); continue; }
  const v = figma.variables.createVariable(name, col, "COLOR");
  v.scopes = ["ALL_FILLS", "STROKE_COLOR"];
  v.setValueForMode(light, figma.variables.createVariableAlias(l));
  v.setValueForMode(dark, figma.variables.createVariableAlias(d));
  created.push({ name, id: v.id });
}
return { collectionId: col.id, created: created.length, missing, ids: created };
```

Expected: `created: 20`, `missing: []`.

- [ ] **Step 2: Verify aliases** (read-only)

```js
const col = (await figma.variables.getLocalVariableCollectionsAsync()).find(c => c.name === "Species");
const rows = [];
for (const id of col.variableIds) {
  const v = await figma.variables.getVariableByIdAsync(id);
  const names = await Promise.all(col.modes.map(async m => (await figma.variables.getVariableByIdAsync(v.valuesByMode[m.modeId].id)).name));
  rows.push(`${v.name}: ${names.join(" / ")} scopes=${v.scopes.join(",")}`);
}
return rows;
```

Expected: 20 rows, each matching `species.json` light/dark, scopes `ALL_FILLS,STROKE_COLOR`.

- [ ] **Step 3:** Record the collection ID in the spec's Shipped section (Task 10 commits it).

---

### Task 4: Styles page `Species Documentation` frame

**Files:** none in the repo.

**Interfaces:**
- Consumes: the `Species` collection (Task 3); `map-region-sample` (`1121:4095`) and `map-site-marker` (`473:862`).
- Produces: frame `Species Documentation` in the Styles section (`701:2`), placed to the right of `Chart Documentation` (`1336:50`).

- [ ] **Step 1: Inspect** `Chart Documentation` (`1336:50`) with a read-only script returning its child tree (names, layout, sizes, text styles) and the section's bounds. Match its structure: title, one sub-section per group, swatch cards with a Light and a Dark swatch per token (explicit variable mode on each), static caption text with token name and Ramps step.

- [ ] **Step 2: Build** the frame with three sub-sections, hues in Andrew's doc order (magenta, coral, amber, gold, sage, teal, cobalt, violet, slate, charcoal, neutral):
  - **Status:** per value, Tint/Base/Shade swatches in both modes, plus a `map-region-sample` instance showing its border (`Border=Solid|Medium|Fine|Solid`, fill and stroke bound to the value's tint/shade; invasive stroke `weight/xl` with the `coral/Casing` effect style).
  - **Layer:** the 8 layer tokens in both modes, in height order then vine, root, stroke.
  - **Function:** 7 rows: a `map-site-marker` (`Style=Numbered, Shape=Circle`, `Number` = letter) and its meaning.

  Widen section `701:2` if the frame doesn't fit (Chart Documentation widened it to 9408). Return all created IDs.

- [ ] **Step 3: Screenshot** the frame and check: no clipped text, every swatch bound (run a query for SOLID paints without `boundVariables.color` inside the frame; expect 0 outside text).

---

### Task 5: `map-key` variants and function badges

**Files:** none in the repo.

**Interfaces:**
- Consumes: `Species` variables; `map-key` set `153:2052` (variant `Theme=Default, Map Type=Zones – Current` is the model: VERTICAL frame → `title` TEXT → `key-container` → `key-grid` GRID of `map-key-row` instances); `map-key-row` (`480:889`; props `Heading#480:0`, `Body#480:4`, `Show Body#480:8`, `Swatch Type=Area|Line|Marker`, `Size`).
- Produces: three variants `Theme=Default, Map Type=Species – Status|Species – Layer|Species – Function`; return their IDs.

- [ ] **Step 1: Clone the Zones – Current variant three times** into the set, rename each (`Theme=Default, Map Type=Species – Status`, etc.), set `title` text (load its fonts first) to `Species – Status`, `Species – Layer`, `Species – Function`, and set the grid rows:
  - **Status (4 rows, Area):** headings `native`, `naturalized`, `cultivated`, `invasive`; bodies `belongs here`, `arrived and stayed`, `planted on purpose`, `remove or contain`. In each row's nested `map-region-sample`, set `Border` (Solid, Medium, Fine, Solid) and bind fill → `status/<v>/tint`, stroke → `status/<v>/shade`; invasive stroke weight bound to `Stroke` `weight/xl` and effect style `coral/Casing`.
  - **Layer (7 rows, Area):** canopy, sub-canopy, shrub, herbaceous, groundcover, vine, root, with bodies `tallest trees`, `small trees`, `shrubs`, `non-woody perennials`, `low spreading plants`, `climbers`, `roots and tubers`. Fill → `layer/<v>`, stroke → `layer/stroke`, `Border=Solid`.
  - **Function (7 rows, Marker):** the seven letters; swap each row's nested marker to a `map-site-marker` `Style=Numbered, Shape=Circle` with `Number` = letter; heading = the meaning in lower case, `Show Body` off.

  Remove extra rows (Zones has 5) or clone `map-key-row` to add rows. Lay out the set's variants so none overlap (place new variants below the current lowest). Return variant IDs and per-row heading text.

- [ ] **Step 2: Screenshot** each new variant; check headings, swatch borders (dash visible), and the letter badges.

---

### Task 6: `Species` page and three map frames

**Files:** none in the repo.

**Interfaces:**
- Consumes: Zones map frame `189:2268` (on page `189:1729`); the three key variants (Task 5).
- Produces: page `Species`; frames `Species – Status`, `Species – Layer`, `Species – Function`; inside each, every plant-symbol instance renamed `plant P001`…`plant Pnnn` in identical order across the three frames. Return frame IDs and the plant count.

- [ ] **Step 1: Check `nut tree`.** Its main component (`39:5767`) has no parent. Read-only: count `nut tree` instances in `189:2268` and return them. **Checkpoint:** ask Andrew whether to keep the instance as is (it still renders), swap it to `deciduous tree`, or restore the component. Don't continue until he answers.

- [ ] **Step 2: Create the page and clone** in one `use_figma` call: switch to the Zones page (`189:1729`) once, create the page with `figma.createPage()` and name it `Species`, clone `189:2268` three times, and move each clone with `newPage.appendChild(clone)`. On each clone:
  - Rename the frame. Position the frames left to right, 104 px apart, away from (0,0).
  - Delete the `Zones` overlay child and any `Pill` instances.
  - Swap the `map-key` instance's variant to the matching `Species – …` Map Type.
  - Set the `map-legend` title text to the frame name.
  - Rename plant instances: collect instances whose main component's name is in `["deciduous tree","coniferous tree","nut tree","shrub","hedgerow","perennial"]` via `frame.findAllWithCriteria({types:["INSTANCE"]})` (document order), and name the nth one `plant P` + zero-padded n (3 digits).

  Return `{frames: [...ids], plantCount, perTypeCounts}`; `plantCount` must be equal in all three frames.

- [ ] **Step 3: Move the species charts.** Move section `Species Inventory — 58 Freestone Avenue` (`161:142`) from `Site Data Visualizations` to the `Species` page, below the three frames (spec: "The species charts move there"). Return its new position.

- [ ] **Step 4: Screenshot** one frame (they're identical at this point) and confirm the key and legend read correctly.

---

### Task 7: Seed the plant table (private repo)

**Files:**
- Create: `~/Code/keser/site-plans/lot-86-site-plan/site-plan/data/mapped-plants.csv`

**Interfaces:**
- Consumes: plant names and types from Task 6.
- Produces: CSV with header `symbol_id,label,symbol_type,species,status,layer,functions`. `symbol_id` = `P001`…; `status` ∈ {native, naturalized, cultivated, invasive, blank}; `layer` ∈ the 7 layer names; `functions` = space-separated letters from N D P E W M B, or blank.

- [ ] **Step 1: Read** (read-only, on the `Species` page) every `plant P…` instance in `Species – Status`: name, main component name, and `x`,`y` rounded. Return as a list.

- [ ] **Step 2: Write the CSV** from that list. `label` = `<symbol_type> @ <x>,<y>` so Andrew can find each plant. `layer` guess: coniferous tree, deciduous tree → canopy; nut tree → sub-canopy; shrub, hedgerow → shrub; perennial → herbaceous. Leave `species`, `status`, `functions` blank.

- [ ] **Step 3: Commit in the private repo**

```bash
cd ~/Code/keser/site-plans/lot-86-site-plan
git add site-plan/data/mapped-plants.csv
git commit -m "Seed mapped-plants table for the species maps"
```

- [ ] **Step 4: Checkpoint.** Ask Andrew to fill in `species`, `status`, and `functions` (and correct `layer`). Tasks 8's layer map can run on the seed alone; the status and function maps need his data. Do Task 9 while waiting.

---

### Task 8: Apply the table to the three maps

**Files:** none in the repo (the script embeds the CSV as JSON).

**Interfaces:**
- Consumes: the CSV (Task 7), the three frame IDs (Task 6), `Species` variables (Task 3), `map-site-marker` (`473:862`), `map-region-sample` (`1121:4095`) for dash patterns.
- Produces: overridden symbols and badges; returns `{applied, blank, problems}` per frame.

- [ ] **Step 1: Convert the CSV to a JSON literal**

```bash
python3 -c "import csv,json,sys; print(json.dumps(list(csv.DictReader(open(sys.argv[1])))))" ~/Code/keser/site-plans/lot-86-site-plan/site-plan/data/mapped-plants.csv
```

Before using it in Figma, sanity-check the luminance helper the script uses, in Python:

```bash
python3 -c "
import json
r=json.load(open('design-language/tokens/ramps.json'))
lin=lambda c:c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
L=lambda h:sum(w*lin(int(h[i:i+2],16)/255) for w,i in zip((0.2126,0.7152,0.0722),(1,3,5)))
textOn=lambda h:'black' if (L(h)+0.05)/0.05 >= 1.05/(L(h)+0.05) else 'white'
assert textOn('#ffffff')=='black' and textOn('#000000')=='white'
for s in ('sage/700','sage/200'): print(s, textOn(r[s]))"
```

Expected: no assertion error; `sage/700 white`, `sage/200 black`.

- [ ] **Step 2: Run the apply script** (`use_figma`, switch to the `Species` page once). Paste `ROWS` and the three frame IDs.

```js
const ROWS = /* JSON from Step 1 */ [];
const FRAMES = { status: "<Species – Status id>", layer: "<Species – Layer id>", function: "<Species – Function id>" };
const STATUS = ["native", "naturalized", "cultivated", "invasive"];
const LAYERS = ["canopy", "sub-canopy", "shrub", "herbaceous", "groundcover", "vine", "root"];
const LETTERS = ["N", "D", "P", "E", "W", "M", "B"];
const BORDER = { native: "Solid", naturalized: "Medium", cultivated: "Fine", invasive: "Solid" };
const col = (await figma.variables.getLocalVariableCollectionsAsync()).find(c => c.name === "Species");
const V = {}; for (const id of col.variableIds) { const v = await figma.variables.getVariableByIdAsync(id); V[v.name] = v; }
const ramps = (await figma.variables.getLocalVariableCollectionsAsync()).find(c => c.name === "Ramps");
const R = {}; for (const id of ramps.variableIds) { const v = await figma.variables.getVariableByIdAsync(id); R[v.name] = v; }
const strokeCol = (await figma.variables.getLocalVariableCollectionsAsync()).find(c => c.name === "Stroke");
let weightXl = null; for (const id of strokeCol.variableIds) { const v = await figma.variables.getVariableByIdAsync(id); if (v.name === "weight/xl") weightXl = v; }
const casing = (await figma.getLocalEffectStylesAsync()).find(s => s.name === "coral/Casing");
const regionSet = await figma.getNodeByIdAsync("1121:4095");
const dash = {}; for (const v of regionSet.children) { const m = v.name.match(/Border=(\w+)/); if (m) { const b = v.findOne(n => "dashPattern" in n && n.strokes && n.strokes.length) ; dash[m[1]] = b ? [...b.dashPattern] : []; } }
const markerSet = await figma.getNodeByIdAsync("473:862");
const badgeComp = markerSet.children.find(c => c.name.includes("Style=Numbered") && c.name.includes("Shape=Circle"));
const resolveHex = async (variable) => { // Light value through the alias chain
  let val = variable.valuesByMode[Object.keys(variable.valuesByMode)[0]];
  while (val && val.type === "VARIABLE_ALIAS") { const t = await figma.variables.getVariableByIdAsync(val.id); val = t.valuesByMode[Object.keys(t.valuesByMode)[0]]; }
  return val;
};
const lin = c => c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
const textOn = rgb => { const L = 0.2126 * lin(rgb.r) + 0.7152 * lin(rgb.g) + 0.0722 * lin(rgb.b); return (L + 0.05) / 0.05 >= 1.05 / (L + 0.05) ? R["neutral/Black"] : R["neutral/White"]; };
const bound = (v) => figma.variables.setBoundVariableForPaint({ type: "SOLID", color: { r: 0, g: 0, b: 0 } }, "color", v);
const report = {};
for (const [kind, frameId] of Object.entries(FRAMES)) {
  const frame = await figma.getNodeByIdAsync(frameId);
  const plants = {}; for (const n of frame.findAllWithCriteria({ types: ["INSTANCE"] })) if (n.name.startsWith("plant P")) plants[n.name.slice(6)] = n;
  for (const old of frame.findAll(n => n.name.startsWith("badge P"))) old.remove(); // safe re-run
  const r = { applied: 0, blank: 0, problems: [] };
  for (const row of ROWS) {
    const node = plants[row.symbol_id];
    if (!node) { r.problems.push(`${row.symbol_id}: not in frame`); continue; }
    const label = node.findOne(n => n.type === "TEXT");
    if (kind === "status") {
      if (!row.status) { r.blank++; continue; }
      if (!STATUS.includes(row.status)) { r.problems.push(`${row.symbol_id}: unknown status ${row.status}`); continue; }
      const tint = V[`status/${row.status}/tint`], shade = V[`status/${row.status}/shade`];
      node.fills = [bound(tint)]; node.strokes = [bound(shade)];
      node.dashPattern = dash[BORDER[row.status]] || [];
      if (row.status === "invasive") { node.setBoundVariable("strokeWeight", weightXl); await node.setEffectStyleIdAsync(casing.id); }
      if (label) { await Promise.all(label.getStyledTextSegments(["fontName"]).map(s => figma.loadFontAsync(s.fontName))); label.fills = [bound(textOn(await resolveHex(tint)))]; }
      r.applied++;
    } else if (kind === "layer") {
      if (!LAYERS.includes(row.layer)) { r.problems.push(`${row.symbol_id}: unknown layer ${row.layer}`); continue; }
      const fill = V[`layer/${row.layer}`];
      node.fills = [bound(fill)]; node.strokes = [bound(V["layer/stroke"])];
      if (label) { await Promise.all(label.getStyledTextSegments(["fontName"]).map(s => figma.loadFontAsync(s.fontName))); label.fills = [bound(textOn(await resolveHex(fill)))]; }
      r.applied++;
    } else {
      const letters = (row.functions || "").trim().split(/\s+/).filter(Boolean);
      if (!letters.length) { r.blank++; continue; }
      const bad = letters.filter(l => !LETTERS.includes(l));
      if (bad.length) { r.problems.push(`${row.symbol_id}: unknown function ${bad.join(" ")}`); continue; }
      letters.forEach((l, i) => {
        const b = badgeComp.createInstance();
        node.parent.appendChild(b);
        b.rescale(0.5);
        b.setProperties({ "Number#473:0": l });
        b.name = `badge ${row.symbol_id} ${l}`;
        b.x = node.x + node.width + 2 + i * (b.width + 2); b.y = node.y;
      });
      r.applied++;
    }
  }
  report[kind] = r;
}
return report;
```

Notes for the implementer: the badge's default fill is `<hue>/Shade` from the component; confirm it's `charcoal/Shade` after the first run, and if not, bind each badge's circle fill to `Color Roles` `charcoal/Shade`. Fonts for the badge text are loaded by `createInstance` only if the component's font is available; if `setProperties` throws a font error, load the component text's font first.

- [ ] **Step 3: Verify the report and bindings.** Expected: `problems: []` for every row Andrew filled; `blank` equals the number of rows he left empty. Then run a read-only query per frame for plant instances with a SOLID fill lacking `boundVariables.color`; expect 0 among `applied` plants.

- [ ] **Step 4: Screenshot** each frame at 1920 wide. Check: dashes visible on naturalized and cultivated, invasive cased, label letters readable, badges not overlapping neighbors. If badges collide, move the row below the symbol instead (`b.y = node.y + node.height + 2`) and re-run (the script removes old badges first).

---

### Task 9: Microsite tokens and species page

**Files:**
- Modify: `docs/assets/chart-tokens.css`, `docs/species-inventory.html`, `tools/check_chart_tokens.py`, `tools/tests/test_check_chart_tokens.py`

**Interfaces:**
- Consumes: `design-language/tokens/species.json`, `design-language/tokens/ramps.json` (Task 2).
- Produces: CSS custom properties `--species-status-<value>-<tint|base|shade>` and `--species-layer-<value>` in all three `chart-tokens.css` blocks; `check_species_tokens(css_text) -> list[str]` in `check_chart_tokens.py`, called from `check_tokens()`.

- [ ] **Step 1: Write the failing test** (append to `tools/tests/test_check_chart_tokens.py`)

```python
from check_chart_tokens import check_species_tokens


def test_species_token_drift_is_reported():
    css = (".viz-root { --species-status-native-base: #000000; }\n"
           "@media (prefers-color-scheme: dark) {\n"
           "  :root:where(:not([data-theme=\"light\"])) .viz-root { --species-status-native-base: #000000; }\n}\n"
           ":root[data-theme=\"dark\"] .viz-root { --species-status-native-base: #000000; }")
    fails = check_species_tokens(css)
    assert any("--species-status-native-base" in f for f in fails)
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 -m pytest tools/tests/test_check_chart_tokens.py -q`
Expected: FAIL with `ImportError: cannot import name 'check_species_tokens'`.

- [ ] **Step 3: Implement** in `tools/check_chart_tokens.py`:

```python
import json
SPECIES = ROOT / "design-language/tokens/species.json"
RAMPS_JSON = ROOT / "design-language/tokens/ramps.json"

def species_css_name(token):
    return "--species-" + token.replace("/", "-")

def check_species_tokens(css):
    ramps, tokens = json.loads(RAMPS_JSON.read_text()), json.loads(SPECIES.read_text())["tokens"]
    light, media, forced = (decls(b) for b in blocks(css))
    fails = []
    for token, steps in tokens.items():
        prop = species_css_name(token)
        want_l, want_d = ramps[steps["light"]], ramps[steps["dark"]]
        if light.get(prop, "").lower() != want_l: fails.append(f"{prop} light {light.get(prop)} ≠ {want_l}")
        if media.get(prop, "").lower() != want_d: fails.append(f"{prop} dark {media.get(prop)} ≠ {want_d}")
        if forced.get(prop, "").lower() != want_d: fails.append(f"{prop} forced dark {forced.get(prop)} ≠ {want_d}")
    return fails
```

and in `check_tokens()`, before `return fails`: `fails += check_species_tokens(css)`.

- [ ] **Step 4: Run the test (passes) and the tokens check (fails until CSS exists)**

Run: `python3 -m pytest tools -q && python3 tools/check_chart_tokens.py tokens`
Expected: tests pass; tokens check prints 60 `--species-*` failures (20 tokens × 3 blocks).

- [ ] **Step 5: Generate the CSS lines** and paste them into the three blocks of `docs/assets/chart-tokens.css` (after the categorical line in each):

```bash
python3 - <<'EOF'
import json
r = json.load(open("design-language/tokens/ramps.json"))
t = json.load(open("design-language/tokens/species.json"))["tokens"]
for mode in ("light", "dark"):
    print(mode + ":")
    print("  " + " ".join(f"--species-{k.replace('/', '-')}: {r[v[mode]]};" for k, v in t.items()))
EOF
```

Also update the header comment to name the `Species` collection. Run `python3 tools/check_chart_tokens.py tokens` → `OK`.

- [ ] **Step 6: Move the species page onto tokens** (`docs/species-inventory.html`):
  - Add `<link rel="stylesheet" href="assets/chart-tokens.css">` beside the page's other head links.
  - In all three variable blocks, replace the raw values:
    - `--status-native` → `var(--species-status-native-shade)` (pills and bar carry white text; Shade keeps contrast).
    - `--status-introduced` → `var(--chart-neutral-label-muted)` (iNaturalist can't split introduced; spec).
    - `--group-plantae` → `var(--chart-categorical-1)`, `--group-insecta` → `var(--chart-categorical-3)`, `--group-mammalia` → `var(--chart-categorical-4)`, `--group-fungi` → `var(--chart-categorical-5)`, `--group-other` → `var(--chart-neutral-label-muted)`. **Ruling:** slot 2 (sage) is skipped because sage means native on this page; slots stay in their validated order otherwise.
  - Because these now reference tokens, declare them once in the light block and delete them from both dark blocks (the climate pattern).
  - Rename `--status-*` and `--group-*` to the page prefix `--spi-status-*`, `--spi-group-*` everywhere in the file, so the checker can target them, then run:

Run: `python3 tools/check_chart_tokens.py page docs/species-inventory.html spi`
Expected: `OK`. Fix any `line N:` failures it reports (page variables as chart paint, unclassed SVG text) the same way the water/sun/climate pages were fixed.

- [ ] **Step 7: Screenshot** the page in light and dark (headless Chrome, `data-theme` set on `<html>` in a scratch copy, as in the chart follow-ups). Check pill text contrast, the bar, and the taxon legend.

- [ ] **Step 8: Update `CLAUDE.md`** chart-colors bullet: add "Species colors come from the `--species-*` tokens; values live in `design-language/tokens/species.json`."

- [ ] **Step 9: Commit**

```bash
git add tools/check_chart_tokens.py tools/tests/test_check_chart_tokens.py docs/assets/chart-tokens.css docs/species-inventory.html CLAUDE.md
git commit -m "Species tokens on the microsite: chart-tokens.css, species page, drift check"
```

---

### Task 10: Record what shipped

**Files:**
- Modify: `design-language/specs/2026-10-14-species-palette-design.md`
- Modify: `~/.claude/projects/-Users-andrewkeser-Code-keser-site-toolkit/memory/figma_styles_page_sync.md`

- [ ] **Step 1: Spec.** Set **Status** to shipped with the date. Under **Shipped**, record: the validated Light/Dark table and minimum ΔE per check; any Light value changed in Task 2 and Andrew's approval; the collection ID; the Styles frame ID; the three key-variant IDs; the page and frame IDs; plant count; the `nut tree` decision; the badge placement used; the microsite changes including the slot-2 ruling.

- [ ] **Step 2: Memory.** Append a short "Species (date)" paragraph to `figma_styles_page_sync.md`: the `Species Documentation` frame ID, and that re-syncing it means re-running Task 4 after any `species.json` change.

- [ ] **Step 3: Commit**

```bash
git add design-language/specs/2026-10-14-species-palette-design.md
git commit -m "Log species palette shipped state"
```

- [ ] **Step 4: Checkpoint.** Show Andrew the branch log and ask before merging to `main` or pushing.
