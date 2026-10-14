# Chart Tokens Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** One chart palette and one set of chart type roles, defined in the PDC Pro Vision Figma
library, used by both the course deck's native charts and the microsite's SVG charts.

**Architecture:**
- **Library:** the PDC Pro Vision Figma library gains two variable collections, `Chart Semantic`
  and `Chart Neutral`. Both have Light and Dark modes and alias the Ramps.
- **Microsite:** a plain stylesheet, `docs/assets/chart-tokens.css`, mirrors the tokens as CSS
  custom properties. Each chart's prefixed variables point at those properties.
- **Deck:** chart shapes bind to the library variables, and chart text uses four existing text
  styles.
- **Check script:** a dependency-free Python script guards the hand-copied values and the page
  wiring.

**Tech stack:**
- Figma Plugin API through the `use_figma` MCP tool. Pass `skillNames` `figma-use`, plus
  `figma-use-slides` for the deck.
- Plain HTML, CSS and JS in `docs/`. There's no build step.
- Python 3 standard library for the check script.

**Spec:** `site-plan/specs/2026-10-14-chart-tokens-design.md`

## Global Constraints

### Files and IDs

| What | Value |
|---|---|
| Library file key | `aF9SVeTLwFN8PCEiU2OSBQ`. Collections are created there. |
| Deck file key | `4HO6wuq75jFhX7OuMpqPNs` (a Slides file) |
| Slides template | `KDVfc0v5jT8jKB3OK11axN`. Not touched. |
| Styles page | Page `Styles`. The top-level section is `701:2`. |

### Token rules

- **Collection names** are exactly `Chart Semantic` and `Chart Neutral`. Mode names are exactly
  `Light` and `Dark`, in that order.
- **Every token value aliases a Ramps variable.** No raw colors.
- **Scopes:** `["ALL_FILLS","STROKE_COLOR"]`. The `label` and `label/muted` tokens also get
  `"TEXT_FILL"`.
- **Do not reorder or modify `Chart Categorical`.**
- **CSS custom property names** are `--chart-<group>-<name>`, with `/` replaced by `-`.
  - Examples: `--chart-season-winter`, `--chart-emphasis-fill`, `--chart-neutral-label-muted`.
  - Categorical slots are `--chart-categorical-1` through `--chart-categorical-7`.
- **Dark selectors** in CSS must be exactly the site's existing pair:
  - `@media (prefers-color-scheme: dark) { :root:where(:not([data-theme="light"])) .viz-root { … } }`
  - `:root[data-theme="dark"] .viz-root { … }`
- **Translucent site bands** use `color-mix(in srgb, var(--chart-…) N%, transparent)`, where N is
  the chart's current alpha × 100. Spec rule: the implementer picks per chart; this plan picks
  `color-mix` everywhere on the site.
- **Emphasis is form, not just hue.** `emphasis` is drawn only as a band, a threshold line or a
  divide line, with a direct label. It's never a plain solid series.

### Type rules

- **Font family:** the site's chart text is
  `"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace`.
- **Font loading:** load weights 400, 500 and 700 with
  `@import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap");`
  at the top of `chart-tokens.css`.
- **Type roles:**

  | Role | Deck style | Site |
  |---|---|---|
  | title | `Mono Caps/20/Bold` | 700, 13px, uppercase |
  | label | `Mono Caps/16/Regular` | 400, 11px, uppercase |
  | value | `Mono/20/Bold` | 700, 13px, no transform |
  | note | `Mono Caps/16/Medium` | 500, 11px, uppercase |

- **Page text is unchanged.** Intro paragraphs, notes boxes, `*-src` source lines and page headers
  stay on `system-ui`.

### Project rules

- **Merge safety (CLAUDE.md):** don't rename prefixed variables or classes. Only change their
  values and declarations.
- **Links stay relative:** `assets/chart-tokens.css`, never `/assets/…`.
- **Git safety:** stage by explicit path. No `git reset`, `git restore`, `git stash`,
  `git checkout -- <path>` or `git clean`. Fix forward.
- **Pushing:** commit per task. Never push without Andrew saying "push".
- **Base map:** never edit base map layers in any Figma file.

## Ramp hex values

Copy these verbatim; they come from the Ramps collection.

| Ramp | Hex | Ramp | Hex | Ramp | Hex |
|---|---|---|---|---|---|
| cobalt/200 | `#b4caff` | sage/400 | `#849f55` | charcoal/50 | `#f0f0ee` |
| cobalt/300 | `#8cacff` | sage/500 | `#698436` | charcoal/100 | `#e0dfdd` |
| cobalt/400 | `#638bff` | sage/600 | `#516920` | charcoal/300 | `#b1afac` |
| cobalt/500 | `#476de7` | magenta/400 | `#e748c1` | charcoal/400 | `#959490` |
| cobalt/600 | `#3353c1` | magenta/500 | `#ca18a6` | charcoal/500 | `#7a7975` |
| cobalt/700 | `#233c94` | gold/300 | `#cbad42` | charcoal/600 | `#605f5b` |
| amber/100 | `#fdd9c4` | gold/400 | `#b09100` | charcoal/700 | `#474644` |
| amber/400 | `#f66d1e` | gold/500 | `#907600` | charcoal/800 | `#2e2e2c` |
| amber/500 | `#d75509` | teal/400 | `#2ea89c` | violet/400 | `#a877e5` |
| amber/800 | `#4e1f03` | teal/500 | `#008c81` | violet/500 | `#8e5aca` |
| coral/300 | `#ff8780` | coral/400 | `#ef5c58` | coral/500 | `#d2383b` |
| coral/600 | `#ad1e26` | | | | |

## Rulings

These rulings settle defects found while turning the spec into mappings. Andrew reviews them with
this plan.

- **R1. Hardscape bars use `water/rain`, not `water/body`.** The spec maps `--runoff-hard` and
  `--wbal-hard` to `water/body` (cobalt/200). That's about 1.6:1 against `#fcfcfb`, which breaks
  the spec's own 3:1 rule for marks. `water/body` stays for area fills only.
  - `--runoff-hard` becomes `water/rain` and `--runoff-hard-2` becomes `water/flow`, keeping the
    pair's light/dark shade relationship.
  - `--wbal-hard` becomes `water/flow`, since `--wbal-rain` already takes `water/rain` in the same
    Sankey.
- **R2. Paired shades derive with `color-mix`.** Some charts pair two shades of one meaning:
  `--runoff-perm`/`--runoff-perm-2` and `--wbal-infil`/`--wbal-perm`. The base gets the token, and
  the partner is derived:
  - `--runoff-perm-2: color-mix(in srgb, var(--chart-land-permeable) 75%, var(--chart-neutral-label))`
    is darker in light mode and lighter in dark mode.
  - `--wbal-perm: color-mix(in srgb, var(--chart-land-permeable) 60%, var(--chart-neutral-surface))`
    is the lighter partner.
- **R3. The flow chart's divide is `neutral/reference`.** In `flow-`, `--flow-divide` and
  `--flow-swale-new` would both be `emphasis` in one chart. The divide is a reference line;
  `--flow-swale-new` keeps `emphasis`. `--elev-divide` stays `emphasis` as the spec says, because
  nothing else in that chart is `emphasis`.
- **R4. Chart-specific colors stay as they are, logged in the spec:**
  - the 12 `monthColors` in `sun-solar.html`'s polar chart. Four already reference season tokens
    through `--spo-series-*`.
  - `--spo-hour-grid`, an overlay on an aerial photo
  - the 3D scene object colors in `sun-solar.html` (`house`, `camper`, `coop`, `POOL`, tree
    fills)

---

### Task 1: Library collections `Chart Semantic` and `Chart Neutral`

**Files:**
- Figma library `aF9SVeTLwFN8PCEiU2OSBQ`. Variables only; no canvas changes.

**Interfaces:**
- Consumes: the Ramps variables named `<hue>/<step>`.
- Produces: collections `Chart Semantic` (12 variables) and `Chart Neutral` (6 variables) with the
  names below. Later tasks look up their keys by name.

- [ ] **Step 1: Write the verification script, then run it to see it fail.**

  Save this as the verify script. It returns `ok: false` until the collections exist.

  ```js
  const EXPECT = {
    'Chart Semantic': {
      'season/winter': ['cobalt/500','cobalt/400'], 'season/spring': ['sage/500','sage/400'],
      'season/summer': ['magenta/400','magenta/400'], 'season/fall': ['gold/400','gold/300'],
      'water/rain': ['cobalt/400','cobalt/300'], 'water/flow': ['cobalt/600','cobalt/400'],
      'water/body': ['cobalt/200','cobalt/700'], 'land/permeable': ['sage/500','sage/400'],
      'land/ground': ['charcoal/500','charcoal/400'], 'emphasis': ['amber/500','amber/400'],
      'emphasis/fill': ['amber/100','amber/800'], 'alert': ['coral/600','coral/300'],
    },
    'Chart Neutral': {
      'grid': ['charcoal/100','charcoal/700'], 'axis': ['charcoal/300','charcoal/600'],
      'reference': ['charcoal/600','charcoal/300'], 'label': ['charcoal/800','charcoal/100'],
      'label/muted': ['charcoal/600','charcoal/400'], 'surface': ['charcoal/50','charcoal/800'],
    },
  };
  const cols = await figma.variables.getLocalVariableCollectionsAsync();
  const problems = [];
  for (const [cname, vars] of Object.entries(EXPECT)) {
    const c = cols.find(x => x.name === cname);
    if (!c) { problems.push('missing collection ' + cname); continue; }
    if (c.modes.map(m => m.name).join('/') !== 'Light/Dark') problems.push(cname + ' modes ' + c.modes.map(m => m.name).join('/'));
    for (const [vname, [l, d]] of Object.entries(vars)) {
      const v = (await Promise.all(c.variableIds.map(id => figma.variables.getVariableByIdAsync(id)))).find(x => x.name === vname);
      if (!v) { problems.push('missing ' + cname + ' ' + vname); continue; }
      for (const [i, want] of [[0, l], [1, d]]) {
        const val = v.valuesByMode[c.modes[i].modeId];
        const got = val?.type === 'VARIABLE_ALIAS' ? (await figma.variables.getVariableByIdAsync(val.id)).name : JSON.stringify(val);
        if (got !== want) problems.push(`${vname} ${c.modes[i].name}: ${got} ≠ ${want}`);
      }
      const wantScopes = vname.startsWith('label') ? ['ALL_FILLS','STROKE_COLOR','TEXT_FILL'] : ['ALL_FILLS','STROKE_COLOR'];
      if (wantScopes.some(s => !v.scopes.includes(s))) problems.push(vname + ' scopes ' + v.scopes.join(','));
    }
  }
  return { ok: problems.length === 0, problems };
  ```

  Expected result: `ok: false`, with problems that include `missing collection Chart Semantic`.

- [ ] **Step 2: Create the collections.** Run this `use_figma` script on the library file.

  ```js
  const DEF = {
    'Chart Semantic': [
      ['season/winter','cobalt/500','cobalt/400','Winter series in any chart.'],
      ['season/spring','sage/500','sage/400','Spring series in any chart.'],
      ['season/summer','magenta/400','magenta/400','Summer series in any chart.'],
      ['season/fall','gold/400','gold/300','Fall series in any chart.'],
      ['water/rain','cobalt/400','cobalt/300','Precipitation, pools, rain inputs.'],
      ['water/flow','cobalt/600','cobalt/400','Flow, rivers, storm curves, hardscape (Sankey).'],
      ['water/body','cobalt/200','cobalt/700','Water and lot area fills only, not marks (<3:1).'],
      ['land/permeable','sage/500','sage/400','Permeable or planted ground, infiltration.'],
      ['land/ground','charcoal/500','charcoal/400','Ground or soil lines and edges.'],
      ['emphasis','amber/500','amber/400','The thing to notice. Draw as band or threshold line with a label, never a plain series.'],
      ['emphasis/fill','amber/100','amber/800','Solid band fill under emphasis.'],
      ['alert','coral/600','coral/300','Records, exits, warnings.'],
    ],
    'Chart Neutral': [
      ['grid','charcoal/100','charcoal/700','Gridlines.'],
      ['axis','charcoal/300','charcoal/600','Axis lines, ticks, contours.'],
      ['reference','charcoal/600','charcoal/300','Mean and baseline lines, nodes.'],
      ['label','charcoal/800','charcoal/100','Chart text.'],
      ['label/muted','charcoal/600','charcoal/400','Secondary chart text.'],
      ['surface','charcoal/50','charcoal/800','Ground planes and structure fills.'],
    ],
  };
  const all = await figma.variables.getLocalVariablesAsync('COLOR');
  const ramp = n => { const v = all.find(x => x.name === n); if (!v) throw new Error('no ramp ' + n); return v; };
  const cols = await figma.variables.getLocalVariableCollectionsAsync();
  const created = {};
  for (const [cname, rows] of Object.entries(DEF)) {
    let c = cols.find(x => x.name === cname);
    if (!c) { c = figma.variables.createVariableCollection(cname); c.renameMode(c.modes[0].modeId, 'Light'); c.addMode('Dark'); }
    const [L, D] = c.modes;
    const existing = await Promise.all(c.variableIds.map(id => figma.variables.getVariableByIdAsync(id)));
    for (const [name, l, d, desc] of rows) {
      let v = existing.find(x => x.name === name) || figma.variables.createVariable(name, c, 'COLOR');
      v.setValueForMode(L.modeId, figma.variables.createVariableAlias(ramp(l)));
      v.setValueForMode(D.modeId, figma.variables.createVariableAlias(ramp(d)));
      v.scopes = name.startsWith('label') ? ['ALL_FILLS','STROKE_COLOR','TEXT_FILL'] : ['ALL_FILLS','STROKE_COLOR'];
      v.description = desc;
      (created[cname] ||= []).push(v.id);
    }
  }
  return created;
  ```

- [ ] **Step 3: Run the Step 1 script again.** Expected: `{ ok: true, problems: [] }`.

- [ ] **Step 4: Log it.** Append a line to the spec's new `## Shipped` section:
  `- 2026-10-14 Task 1: Chart Semantic (12) and Chart Neutral (6) created, verified.` Then commit:

  ```bash
  git add site-plan/specs/2026-10-14-chart-tokens-design.md
  git commit -m "Chart tokens: library collections created"
  ```

### Task 2: Styles page Charts section

**Files:**
- Figma library, page `Styles`, a new frame `Chart Documentation` inside section `701:2`.

**Interfaces:**
- Consumes: Task 1 collections, plus the existing text styles `Mono Caps/20/Bold`,
  `Mono Caps/16/Regular`, `Mono/20/Bold`, `Mono Caps/16/Medium`, `Body/Body – SM` and
  `Body/Body – XS`.
- Produces: frame `Chart Documentation`. Nothing downstream depends on it.

- [ ] **Step 1: Read the layout.** Run a read-only script that returns the children of `701:2`
  with x, y, width and height. Also return `701:447`'s child structure (`_Status`, `Divider`,
  `Content`, `Section — *`) to copy its pattern. The new frame goes to the right of the rightmost
  child, at 128px spacing and the same y (64).

- [ ] **Step 2: Build the frame.** Clone `701:447` (Typography Documentation) as the shell. Rename
  it `Chart Documentation`, keep `_Status` and `Divider`, and replace the content:
  - **Header:** title "Charts". The intro reads "Chart Semantic and Chart Neutral, Light and Dark,
    aliasing the Ramps. The microsite mirrors these in docs/assets/chart-tokens.css. Emphasis is
    form, not just hue: draw it as a band or threshold line with a direct label."
  - **Section — Semantic:** one row per token. Each row has two 48×24 swatches; set each swatch
    frame's explicit variable mode for `Chart Semantic` to Light, then Dark, using
    `setExplicitVariableModeForCollection`. Add the token name in `Mono/16/Bold` and the
    "light-ramp / dark-ramp" alias names in `Mono Caps/16/Regular`.
  - **Section — Neutral:** same pattern for the 6 neutral tokens.
  - **Section — Type roles:** four rows with sample text "ANNUAL AVG ≈ 125", "SEP–DEC '24",
    "141" and "Water use by season". Each uses its deck style. The values text names the site
    equivalent, e.g. "site: 700 13px uppercase".
  - **Section — Categorical:** a single note: "Chart Categorical: 7 slots, unchanged; use slot 1
    for single series without a meaning."

- [ ] **Step 3: Verify.** Read back the frame. Check that every swatch fill is bound to its token,
  that the frame doesn't overlap any sibling in `701:2`, and screenshot the frame with
  `get_screenshot` at `maxDimension` 1400.

- [ ] **Step 4: Gate.** Log the work in the spec's `## Shipped` section and commit:

  ```bash
  git add site-plan/specs/2026-10-14-chart-tokens-design.md
  git commit -m "Chart tokens: Styles page Charts section"
  ```

  Then **stop and ask Andrew to publish PDC Pro Vision.** Tasks 7 and 8 can't import the variables
  until he does. Tasks 3–6 don't depend on the publish.

### Task 3: `docs/assets/chart-tokens.css` and the check script

**Files:**
- Create: `docs/assets/chart-tokens.css`
- Create: `scripts/check_chart_tokens.py`

The check script is custom tooling. Its trade-off: it's about 80 lines, it can only drift if the
spec's palette changes, and the payoff is catching a mistyped hex value or a page that missed the
link.

**Interfaces:**
- Produces:
  - CSS properties `--chart-season-{winter,spring,summer,fall}`,
    `--chart-water-{rain,flow,body}`, `--chart-land-{permeable,ground}`, `--chart-emphasis`,
    `--chart-emphasis-fill` and `--chart-alert`.
  - `--chart-neutral-{grid,axis,reference,label,label-muted,surface}` and
    `--chart-categorical-{1..7}`.
  - Font properties `--chart-font-family`, `--chart-font-title`, `--chart-font-label`,
    `--chart-font-value` and `--chart-font-note`.
  - Classes `.chart-title`, `.chart-label`, `.chart-value` and `.chart-note`.
  - Command `python3 scripts/check_chart_tokens.py tokens` checks the stylesheet.
  - Command `python3 scripts/check_chart_tokens.py page docs/<file>.html <prefix> [<prefix> …]`
    checks a page.

- [ ] **Step 1: Write the check script.**

  ```python
  #!/usr/bin/env python3
  """Checks docs/assets/chart-tokens.css against the chart-token spec, and chart pages' wiring.

  Usage:
    python3 scripts/check_chart_tokens.py tokens
    python3 scripts/check_chart_tokens.py page docs/water.html precip runoff wbal elev flow storm shed wuse
  """
  import re, sys
  from pathlib import Path

  ROOT = Path(__file__).resolve().parent.parent
  CSS = ROOT / "docs/assets/chart-tokens.css"

  # (light, dark), copied from site-plan/specs/2026-10-14-chart-tokens-design.md via the Ramps table
  TOKENS = {
      "season-winter": ("#476de7", "#638bff"), "season-spring": ("#698436", "#849f55"),
      "season-summer": ("#e748c1", "#e748c1"), "season-fall": ("#b09100", "#cbad42"),
      "water-rain": ("#638bff", "#8cacff"), "water-flow": ("#3353c1", "#638bff"),
      "water-body": ("#b4caff", "#233c94"), "land-permeable": ("#698436", "#849f55"),
      "land-ground": ("#7a7975", "#959490"), "emphasis": ("#d75509", "#f66d1e"),
      "emphasis-fill": ("#fdd9c4", "#4e1f03"), "alert": ("#ad1e26", "#ff8780"),
      "neutral-grid": ("#e0dfdd", "#474644"), "neutral-axis": ("#b1afac", "#605f5b"),
      "neutral-reference": ("#605f5b", "#b1afac"), "neutral-label": ("#2e2e2c", "#e0dfdd"),
      "neutral-label-muted": ("#605f5b", "#959490"), "neutral-surface": ("#f0f0ee", "#2e2e2c"),
      "categorical-1": ("#476de7", "#638bff"), "categorical-2": ("#516920", "#849f55"),
      "categorical-3": ("#e748c1", "#ca18a6"), "categorical-4": ("#907600", "#b09100"),
      "categorical-5": ("#008c81", "#2ea89c"), "categorical-6": ("#a877e5", "#8e5aca"),
      "categorical-7": ("#ef5c58", "#d2383b"),
  }
  # Chart-specific values allowed to stay raw (plan ruling R4)
  ALLOW_RAW = {"--spo-hour-grid"}
  RAW = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\(")

  def blocks(css):
      light = re.search(r"^\.viz-root \{([^}]*)\}", css, re.M)
      media = re.search(r'@media \(prefers-color-scheme: dark\) \{\s*:root:where\(:not\(\[data-theme="light"\]\)\) \.viz-root \{([^}]*)\}', css)
      forced = re.search(r':root\[data-theme="dark"\] \.viz-root \{([^}]*)\}', css)
      return [m.group(1) if m else None for m in (light, media, forced)]

  def decls(block):
      return dict(re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", block or ""))

  def check_tokens():
      fails = []
      if not CSS.exists():
          return [f"missing {CSS.relative_to(ROOT)}"]
      css = CSS.read_text()
      if "fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700" not in css:
          fails.append("JetBrains Mono import missing")
      light, media, forced = (decls(b) for b in blocks(css))
      if media != forced:
          fails.append("the two dark blocks differ")
      for name, (l, d) in TOKENS.items():
          prop = f"--chart-{name}"
          if light.get(prop, "").lower() != l: fails.append(f"{prop} light {light.get(prop)} ≠ {l}")
          if media.get(prop, "").lower() != d: fails.append(f"{prop} dark {media.get(prop)} ≠ {d}")
      for cls in ("chart-title", "chart-label", "chart-value", "chart-note"):
          if f".{cls}" not in css: fails.append(f"class .{cls} missing")
      return fails

  def check_page(path, prefixes):
      fails = []
      html = (ROOT / path).read_text()
      if '<link rel="stylesheet" href="assets/chart-tokens.css">' not in html:
          fails.append("chart-tokens.css link missing")
      for prefix in prefixes:
          found = re.findall(rf"(--{prefix}-[a-z0-9-]+):\s*([^;]+);", html)
          if not found: fails.append(f"no --{prefix}-* declarations found")
          for prop, val in found:
              if prop in ALLOW_RAW: continue
              if RAW.search(val): fails.append(f"{prop} still raw: {val.strip()}")
      for cls in re.findall(r"\.([a-z0-9]+-[a-z0-9-]+) \{[^}]*font-size", html):
          if any(cls.startswith(p + "-") for p in prefixes) and re.search(rf"\.{cls} \{{[^}}]*fill:", html) \
             and not re.search(rf"\.{cls} \{{[^}}]*font: var\(--chart-font-", html):
              fails.append(f".{cls} is SVG text without a chart font role")
      return fails

  if __name__ == "__main__":
      mode = sys.argv[1] if len(sys.argv) > 1 else "tokens"
      fails = check_tokens() if mode == "tokens" else check_page(sys.argv[2], sys.argv[3:])
      for f in fails: print("FAIL", f)
      print("OK" if not fails else f"{len(fails)} failure(s)")
      sys.exit(1 if fails else 0)
  ```

- [ ] **Step 2: Run it and confirm it fails.**
  Run `python3 scripts/check_chart_tokens.py tokens`. Expected output:
  `FAIL missing docs/assets/chart-tokens.css`, then `1 failure(s)`, with exit code 1.

- [ ] **Step 3: Write `docs/assets/chart-tokens.css`.**

  ```css
  /* Chart tokens — mirrors PDC Pro Vision "Chart Semantic", "Chart Neutral", "Chart Categorical".
     Source of truth: Figma library. Values copied by hand; scripts/check_chart_tokens.py guards them.
     Spec: site-plan/specs/2026-10-14-chart-tokens-design.md */
  @import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap");

  .viz-root {
    --chart-season-winter: #476de7; --chart-season-spring: #698436; --chart-season-summer: #e748c1; --chart-season-fall: #b09100;
    --chart-water-rain: #638bff; --chart-water-flow: #3353c1; --chart-water-body: #b4caff;
    --chart-land-permeable: #698436; --chart-land-ground: #7a7975;
    --chart-emphasis: #d75509; --chart-emphasis-fill: #fdd9c4; --chart-alert: #ad1e26;
    --chart-neutral-grid: #e0dfdd; --chart-neutral-axis: #b1afac; --chart-neutral-reference: #605f5b; --chart-neutral-label: #2e2e2c; --chart-neutral-label-muted: #605f5b; --chart-neutral-surface: #f0f0ee;
    --chart-categorical-1: #476de7; --chart-categorical-2: #516920; --chart-categorical-3: #e748c1; --chart-categorical-4: #907600; --chart-categorical-5: #008c81; --chart-categorical-6: #a877e5; --chart-categorical-7: #ef5c58;
    --chart-font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
    --chart-font-title: 700 13px/1.2 var(--chart-font-family);
    --chart-font-label: 400 11px/1.2 var(--chart-font-family);
    --chart-font-value: 700 13px/1.2 var(--chart-font-family);
    --chart-font-note: 500 11px/1.2 var(--chart-font-family);
  }
  @media (prefers-color-scheme: dark) {
    :root:where(:not([data-theme="light"])) .viz-root {
    --chart-season-winter: #638bff; --chart-season-spring: #849f55; --chart-season-summer: #e748c1; --chart-season-fall: #cbad42;
    --chart-water-rain: #8cacff; --chart-water-flow: #638bff; --chart-water-body: #233c94;
    --chart-land-permeable: #849f55; --chart-land-ground: #959490;
    --chart-emphasis: #f66d1e; --chart-emphasis-fill: #4e1f03; --chart-alert: #ff8780;
    --chart-neutral-grid: #474644; --chart-neutral-axis: #605f5b; --chart-neutral-reference: #b1afac; --chart-neutral-label: #e0dfdd; --chart-neutral-label-muted: #959490; --chart-neutral-surface: #2e2e2c;
    --chart-categorical-1: #638bff; --chart-categorical-2: #849f55; --chart-categorical-3: #ca18a6; --chart-categorical-4: #b09100; --chart-categorical-5: #2ea89c; --chart-categorical-6: #8e5aca; --chart-categorical-7: #d2383b;
    }
  }
  :root[data-theme="dark"] .viz-root {
    --chart-season-winter: #638bff; --chart-season-spring: #849f55; --chart-season-summer: #e748c1; --chart-season-fall: #cbad42;
    --chart-water-rain: #8cacff; --chart-water-flow: #638bff; --chart-water-body: #233c94;
    --chart-land-permeable: #849f55; --chart-land-ground: #959490;
    --chart-emphasis: #f66d1e; --chart-emphasis-fill: #4e1f03; --chart-alert: #ff8780;
    --chart-neutral-grid: #474644; --chart-neutral-axis: #605f5b; --chart-neutral-reference: #b1afac; --chart-neutral-label: #e0dfdd; --chart-neutral-label-muted: #959490; --chart-neutral-surface: #2e2e2c;
    --chart-categorical-1: #638bff; --chart-categorical-2: #849f55; --chart-categorical-3: #ca18a6; --chart-categorical-4: #b09100; --chart-categorical-5: #2ea89c; --chart-categorical-6: #8e5aca; --chart-categorical-7: #d2383b;
  }

  .viz-root svg text { font-family: var(--chart-font-family); }
  .chart-title { font: var(--chart-font-title); text-transform: uppercase; }
  .chart-label { font: var(--chart-font-label); text-transform: uppercase; }
  .chart-value { font: var(--chart-font-value); }
  .chart-note  { font: var(--chart-font-note); text-transform: uppercase; }
  ```

- [ ] **Step 4: Run the check again.**
  Run `python3 scripts/check_chart_tokens.py tokens`. Expected: `OK`, exit code 0.

- [ ] **Step 5: Mutation check.** This proves the test can catch a wrong value.
  1. Temporarily change `--chart-season-fall: #b09100` to `#b09101` in the light block.
  2. Run the check. Expected: `FAIL --chart-season-fall light #b09101 ≠ #b09100`.
  3. Revert the edit with the Edit tool, not git, and run the check again. Expected: `OK`.

- [ ] **Step 6: Commit.**

  ```bash
  git add docs/assets/chart-tokens.css scripts/check_chart_tokens.py
  git commit -m "Chart tokens: shared stylesheet and check script"
  ```

### Task 4: `docs/water.html`, all eight water charts

**Files:**
- Modify: `docs/water.html`. Edit the per-chart blocks in `<style>` (roughly lines 59–180) and add a
  `<link>` in `<head>`.

**Interfaces:**
- Consumes: the Task 3 properties and font variables.

- [ ] **Step 1: Run the page check and confirm it fails.**
  Run `python3 scripts/check_chart_tokens.py page docs/water.html precip runoff wbal elev flow storm shed wuse`.
  Expected: `FAIL chart-tokens.css link missing`, plus many `still raw` lines.

- [ ] **Step 2: Add the link.** Insert it directly after `<title>Water — Lot #86</title>`:

  ```html
  <link rel="stylesheet" href="assets/chart-tokens.css">
  ```

- [ ] **Step 3: Replace each chart's variable blocks.** For each prefix, replace the light line,
  the `@media (prefers-color-scheme: dark) { … }` block and the `:root[data-theme="dark"]` line
  with a single light line. The `--chart-*` tokens switch modes on their own, and custom
  properties resolve on the same `.viz-root`, so the per-chart dark blocks are no longer needed.

  ```css
  .viz-root { --precip-band-et: color-mix(in srgb, var(--chart-emphasis) 14%, transparent); --precip-band-et-line: var(--chart-emphasis); --precip-mean-line: var(--chart-neutral-reference); --precip-series-precip: var(--chart-water-rain); }
  .viz-root { --runoff-hard: var(--chart-water-rain); --runoff-hard-2: var(--chart-water-flow); --runoff-perm: var(--chart-land-permeable); --runoff-perm-2: color-mix(in srgb, var(--chart-land-permeable) 75%, var(--chart-neutral-label)); }
  .viz-root { --wbal-hard: var(--chart-water-flow); --wbal-infil: var(--chart-land-permeable); --wbal-node: var(--chart-neutral-reference); --wbal-perm: color-mix(in srgb, var(--chart-land-permeable) 60%, var(--chart-neutral-surface)); --wbal-rain: var(--chart-water-rain); --wbal-runoff: var(--chart-emphasis); }
  .viz-root { --elev-divide: var(--chart-emphasis); --elev-ground: var(--chart-land-ground); --elev-ground-fill: var(--chart-neutral-surface); --elev-lot: color-mix(in srgb, var(--chart-categorical-1) 16%, transparent); --elev-lot-line: var(--chart-categorical-1); }
  .viz-root { --flow-contour: var(--chart-neutral-axis); --flow-divide: var(--chart-neutral-reference); --flow-exit: var(--chart-alert); --flow-flow: var(--chart-water-flow); --flow-lot: color-mix(in srgb, var(--chart-land-permeable) 10%, transparent); --flow-lot-line: var(--chart-land-permeable); --flow-pool: var(--chart-water-rain); --flow-struct: var(--chart-neutral-surface); --flow-struct-line: var(--chart-land-ground); --flow-swale-new: var(--chart-emphasis); --flow-swale-old: var(--chart-land-permeable); }
  .viz-root { --storm-curve: var(--chart-water-flow); --storm-curve-dot: var(--chart-water-rain); --storm-evt: color-mix(in srgb, var(--chart-emphasis) 18%, transparent); --storm-evt-line: var(--chart-emphasis); --storm-rec: var(--chart-alert); }
  .viz-root { --shed-land: var(--chart-neutral-surface); --shed-land-line: var(--chart-land-ground); --shed-river: var(--chart-water-flow); --shed-site: var(--chart-emphasis); --shed-water: var(--chart-water-rain); }
  .viz-root { --wuse-base: var(--chart-neutral-reference); --wuse-excess: color-mix(in srgb, var(--chart-emphasis) 16%, transparent); --wuse-excess-line: var(--chart-emphasis); --wuse-fall: var(--chart-season-fall); --wuse-spring: var(--chart-season-spring); --wuse-summer: var(--chart-season-summer); --wuse-winter: var(--chart-season-winter); }
  ```

  Also check these for hard-coded hex inside each prefixed chart's script and replace them with the
  matching `var(--chart-…)`:
  - `.flow-num { fill: #fff; … }` is white text on colored markers. Keep `#fff`: it's a contrast
    color, not a meaning. Add `--flow-num-fg: #fff;` to the flow block and add `--flow-num-fg` to
    `ALLOW_RAW` in the check script, with a comment pointing at this step.
  - Grep the script section: `grep -n '"#[0-9a-fA-F]\{6\}"' docs/water.html`. Map each hit to a
    token, or log it as chart-specific in the spec under R4.

- [ ] **Step 4: Assign text roles.** Edit each SVG text class in place. Keep its `fill` color
  unless it's `var(--text-*)`, and map those: `--text-primary` → `var(--chart-neutral-label)`;
  `--text-secondary` and `--text-muted` → `var(--chart-neutral-label-muted)`. Replace
  `font-size`, `font-weight` and `letter-spacing` with the role's `font:` line, and add
  `text-transform: uppercase;` for label, note and title.

  | Role | `font:` value | Classes |
  |---|---|---|
  | label | `var(--chart-font-label)` | `precip-ax`, `runoff-axt`, `runoff-lbl`, `runoff-seclbl`, `runoff-val-m2`, `elev-axt`, `flow-cl`, `flow-lbl`, `flow-lbl-m`, `storm-axl`, `storm-axt`, `shed-axt`, `shed-maplbl`, `shed-rd`, `wbal-nsub`, `wuse-axl`, `wuse-axt`, `wuse-seclbl` |
  | value | `var(--chart-font-value)` | `precip-val`, `runoff-val`, `storm-dot-lbl`, `shed-rn`, `wuse-val`, `wuse-dot-lbl`, `flow-num` |
  | note | `var(--chart-font-note)` | `precip-mean-lbl`, `precip-et-lbl`, `elev-note`, `elev-note-b`, `flow-lbl-b`, `runoff-lbl-b`, `shed-maplbl-b`, `wbal-nlbl` |

  HTML legends (`.runoff-legend`, `.wuse-legend`) also get
  `font: var(--chart-font-label); text-transform: uppercase;`. Page text classes (`*-note`
  callout boxes, `*-src`, `*-headline`, `*-foot`) stay unchanged.

  Example, before and after:

  ```css
  .wuse-axt { fill: var(--text-muted); font-size: 10px; }
  .wuse-axt { fill: var(--chart-neutral-label-muted); font: var(--chart-font-label); text-transform: uppercase; }
  ```

- [ ] **Step 5: Run the page check again.**
  Run `python3 scripts/check_chart_tokens.py page docs/water.html precip runoff wbal elev flow storm shed wuse`.
  Expected: `OK`.

- [ ] **Step 6: Visual check in light and dark.**
  1. Serve the site with `python3 -m http.server 8765 --directory docs`, in the background.
  2. Open `http://localhost:8765/water.html` in Chrome through the claude-in-chrome tools. Load
     them with one ToolSearch call, in a new tab.
  3. Screenshot every chart section in light mode. Set
     `document.documentElement.dataset.theme = "dark"` with `javascript_tool`, then screenshot
     them again.
  4. Look for each Review Focus failure: label overlap, clipping, unreadable text, and bands that
     hide data.
  5. Fix any overlap by shortening the label's position offset or the chart's left margin in that
     chart's script. Never shrink below the role sizes.
  6. Stop the server.

- [ ] **Step 7: Commit.**

  ```bash
  git add docs/water.html scripts/check_chart_tokens.py
  git commit -m "Chart tokens: water charts use shared palette and chart type"
  ```

### Task 5: `docs/sun-solar.html`, the three sun charts

**Files:**
- Modify: `docs/sun-solar.html`. Edit the `spc`, `sp3d` and `spo` blocks (roughly lines 66–160)
  and add a `<link>` in `<head>`.

**Interfaces:**
- Consumes: the Task 3 properties.

- [ ] **Step 1: Run the page check and confirm it fails.**
  Run `python3 scripts/check_chart_tokens.py page docs/sun-solar.html spc sp3d spo`. Expected:
  FAIL lines.

- [ ] **Step 2: Add the link** right after the `<title>` element:
  `<link rel="stylesheet" href="assets/chart-tokens.css">`.

- [ ] **Step 3: Replace the variable blocks.** Delete each prefix's two dark blocks, then:

  ```css
  .viz-root { --spc-series-winter: var(--chart-season-winter); --spc-series-spring: var(--chart-season-spring); --spc-series-summer: var(--chart-season-summer); --spc-series-fall: var(--chart-season-fall); }
  .viz-root { --sp3d-series-winter: var(--chart-season-winter); --sp3d-series-spring: var(--chart-season-spring); --sp3d-series-summer: var(--chart-season-summer); --sp3d-series-fall: var(--chart-season-fall); --sp3d-ground: var(--chart-neutral-surface); --sp3d-ground-ring: var(--chart-neutral-axis); }
  ```

  `spo` keeps its light and dark `--spo-hour-grid` values, which are allowed raw under R4. Its
  season series become token references:

  ```css
  .viz-root { --spo-series-winter: var(--chart-season-winter); --spo-series-spring: var(--chart-season-spring); --spo-series-summer: var(--chart-season-summer); --spo-series-fall: var(--chart-season-fall); --spo-hour-grid: rgba(11,11,11,0.28); }
  @media (prefers-color-scheme: dark) {
    :root:where(:not([data-theme="light"])) .viz-root { --spo-hour-grid: rgba(255,255,255,0.3); }
  }
  :root[data-theme="dark"] .viz-root { --spo-hour-grid: rgba(255,255,255,0.3); }
  ```

- [ ] **Step 4: Assign text roles,** using the Task 4 Step 4 method.

  | Role | Classes |
  |---|---|
  | label | `spc-axis-label`, `spc-direct-label`, `spo-hour-line-label`, `spo-polar-axis-label` |
  | note | `spc-axis-label-strong`, `spc-direct-label-strong`, `spo-polar-compass-label`, `spo-direct-label`, `spo-compass-label` |

  The legends `.sp3d-legend-row`, `.spo-legend-row` and `.spo-month-legend` get the label font and
  uppercase.

  `.spo-direct-label` and `.spo-compass-label` sit over an aerial photo. Keep their existing
  fill, stroke and paint-order halo properties, and change only the font.

- [ ] **Step 5: Run the page check again.**
  Run `python3 scripts/check_chart_tokens.py page docs/sun-solar.html spc sp3d spo`. Expected:
  `OK`.

- [ ] **Step 6: Visual check.** Repeat the Task 4 Step 6 procedure for
  `http://localhost:8765/sun-solar.html`: light and dark, all three charts plus the hover
  crosshair on `spc`.

- [ ] **Step 7: Log and commit.** Log ruling R4 (month colors, 3D object colors and the hour grid
  stay chart-specific) under the spec's `## Shipped` section, then:

  ```bash
  git add docs/sun-solar.html site-plan/specs/2026-10-14-chart-tokens-design.md
  git commit -m "Chart tokens: sun charts use shared palette and chart type"
  ```

### Task 6: `docs/climate.html` wind chart, plus the audit of `species-inventory` and `zones-design`

**Files:**
- Modify: `docs/climate.html`. Edit the `--wind-*` declarations at roughly lines 21–62, the chart
  text classes at lines 137–140, and the `<head>` link.
- Possibly modify: `docs/species-inventory.html` and `docs/zones-design.html`.

**Interfaces:**
- Consumes: the Task 3 properties.

- [ ] **Step 1: Run the page check and confirm it fails.**
  Run `python3 scripts/check_chart_tokens.py page docs/climate.html wind`. Expected: FAIL.

- [ ] **Step 2: Add the link and repoint the wind variables.** Add the `<link>` after `<title>`.
  In all three places that declare `--wind-fill` and `--wind-accent` (light, media-dark,
  forced-dark), set:

  ```css
  --wind-fill:      color-mix(in srgb, var(--chart-categorical-1) 55%, var(--surface-1));
  --wind-accent:    var(--chart-categorical-1);
  ```

  The three copies are now identical, and the dark ones resolve through the tokens. Keep the
  copies, since those blocks also carry the page's universal identifiers.

- [ ] **Step 3: Assign text roles.** These are unprefixed classes on a single-chart page.
  - Label role: `.axis-label`, `.dir-label`, `.value-label`.
  - Value role: `.value-label-strong`.
  - Keep `text-anchor: middle` where it's present.

  The check's class rule only looks at prefixed classes. Verify these four by eye in Step 5.

- [ ] **Step 4: Audit the other two pages.** Run
  `grep -n 'createElementNS\|svg.chart\|#[0-9a-fA-F]\{6\}' docs/species-inventory.html docs/zones-design.html`.
  - If either page draws a chart, give it the same treatment as above, with its prefix added to
    the check command, and record that in the spec.
  - If neither draws one, log "audited, no charts" in the spec's `## Shipped` section.

- [ ] **Step 5: Run the check and the visual check.**
  1. Run `python3 scripts/check_chart_tokens.py page docs/climate.html wind`. Expected: `OK`.
  2. Repeat the Task 4 Step 6 procedure for `climate.html#wind`.

- [ ] **Step 6: Commit.**

  ```bash
  git add docs/climate.html site-plan/specs/2026-10-14-chart-tokens-design.md
  git commit -m "Chart tokens: wind chart; audit of remaining pages"
  ```

  Add `docs/species-inventory.html` and/or `docs/zones-design.html` to the `git add` only if
  Step 4 changed them.

### Task 7: Deck native charts, slides 96–101

**Precondition:** Andrew has published PDC Pro Vision after Task 2.

**Files:**
- Figma deck `4HO6wuq75jFhX7OuMpqPNs`, frames named `viz (native …)` on slides 96–101. Find
  them by name, never by stored ID.

**Interfaces:**
- Consumes: the variable keys of `Chart Semantic` and `Chart Neutral`, read from the library in
  Step 1. Text style keys:
  | Role | Style | Key |
  |---|---|---|
  | title | `Mono Caps/20/Bold` | `d235ec436ce15a297555b6503a1f05ab3a6b9dd7` |
  | label | `Mono Caps/16/Regular` | `0151bafbaa937367be1eda13644cbd874d127176` |
  | value | `Mono/20/Bold` | `b8ac1fd3f391906908a8e7e0241cf56107600869` |
  | note | `Mono Caps/16/Medium` | `25b822c2a4081bb2283e6223da7ade3928f36f7b` |

- [ ] **Step 1: Read the token keys.** Run a read-only script on the library that returns
  `{ "<collection>:<name>": key }` for all 18 variables, plus `Chart Categorical`
  `slot-1-cobalt`.

- [ ] **Step 2: Bind the colors.** Run one script per slide, so each write is retryable. Get the
  slide with `figma.getSlideGrid().flat()[N-1]` and the root with
  `slide.findOne(x => x.name.startsWith('viz (native'))`. For every SOLID fill or stroke on
  non-text nodes:
  1. Pick the token from this table using the hex value, ignoring opacity.
  2. Import it with `figma.variables.importVariableByKeyAsync`.
  3. Bind it with `figma.variables.setBoundVariableForPaint`, and **keep the paint's opacity**.
  4. Match paints by index, not by object identity. `node.fills` returns a new array on every
     read.

  Return `{ slide, bound, unmatched: [hex…] }`.

  | Slide | Hex → token |
  |---|---|
  | all | `#e1e0d9`, `#e0e0d9` → neutral `grid`. `#c2c2b8` → neutral `axis`. |
  | 96 seasonal | `#2e59b8` → `season/winter`. `#6f8f52` → `season/spring`. `#d9a441` → `season/summer`. `#b8925f` → `season/fall`. `#e07b39` → `emphasis`. `#73706b` → neutral `reference`. |
  | 97 elevation | `#b8925f` → `land/ground` (at opacity 20%: neutral `surface`, opacity set to 100%). `#e07b39` → `emphasis`. `#2e59b8` → Categorical `slot-1-cobalt`. |
  | 98 precip | `#2e59b8` → `water/rain`. `#e07b39` → `emphasis`. `#4d4d47` → neutral `reference`. |
  | 99 storm | `#2e59b8` → `water/flow`. `#e07b39` → `emphasis`. `#c0392b` → `alert`. |
  | 100 runoff | `#2e59b8` → `water/rain`. `#6f8f52` → `land/permeable`. |
  | 101 sankey | `#2e59b8` → `water/flow`. `#6b9edb` → `water/rain`. `#6f8f52` → `land/permeable`. `#8fad70` → `land/permeable`, with paint opacity 60% (R2's lighter partner). `#e07b39` → `emphasis`. |

  Any `unmatched` hex: stop, record it, and choose a token by the spec's meaning table. Rerun until
  `unmatched` is empty.

- [ ] **Step 3: Assign the text styles.** In the same frames, classify each TEXT node, then apply
  the style with `setRangeTextStyleIdAsync` across the whole text. If the font won't load,
  fall back to `setTextStyleIdAsync`, the same way the earlier JetBrains Mono SemiBold nodes were
  handled.
  - The sibling node named `viz-title` → title.
  - Bold text whose characters match `/^[~≈]?[\d.,%/ ]+(gal|in|d|ft)?$/i` → value.
  - Other Bold or SemiBold text → note.
  - Regular text → label.

  Return the counts per role.

- [ ] **Step 4: Check.**
  1. Rerun Step 2 in read-only mode. Expected: 0 unbound SOLID paints in the six frames.
  2. Screenshot slides 96–101 with `get_screenshot` at `maxDimension` 1000.
  3. Look for label overlap or clipping. Text now uses caps and the role sizes. Fix overlaps by
     nudging the label position, never by reducing size.
  4. Run the clip check from the deck text work: find text bounds that extend past a clipping
     ancestor.

- [ ] **Step 5: Log and commit.** Log the result in the spec's `## Shipped` section, then:

  ```bash
  git add site-plan/specs/2026-10-14-chart-tokens-design.md
  git commit -m "Chart tokens: deck native charts bound to library chart tokens"
  ```

### Task 8: Deck sun charts, slides 48 and 50

**Precondition:** Andrew has published PDC Pro Vision after Task 2.

**Files:**
- Figma deck, slides 48 (`1890:1731`) and 50 (`2014:1987`). Confirm with
  `getSlideGrid().flat()[47]` and `[49]`.

- [ ] **Step 1: Check what's on the slides.** These are vector shapes; the earlier inventory found
  104 and 147 shapes. Confirm with a read-only script: count IMAGE fills on the chart nodes.
  - If the chart is an image, skip to Step 3's alternative.

- [ ] **Step 2: Bind the season colors.** Using the Task 7 Step 2 method:
  - `#2a78d6`, `#2a78e5` → `season/winter`
  - `#008300` → `season/spring`
  - `#e87ba4`, `#e87ba3` → `season/summer`
  - `#eda100`, `#eda000` → `season/fall`
  - `#e1e0d9` → neutral `grid`
  - `#c3c2b7` → neutral `axis`
  - `#66665c` → neutral `label/muted`

  Leave white and black, plus `#fcfcfb` and `#ffffff` backgrounds, unbound.

- [ ] **Step 3: Apply text roles,** using the Task 7 Step 3 rules. The Inter 9–11px chart labels
  become `Mono Caps/16/Regular` labels. If the chart's layout can't fit 16px labels (labels
  overlap after the change), revert that slide's text with the Edit-forward approach: re-apply the
  original font size as a range override. Log the slide as an exception in the spec, with the
  reason.

  **Alternative, if the chart is an image:** export the matching chart from the site at 2× after
  Task 5, using a Chrome screenshot of the chart node. Replace the image fill. Log the swap.

- [ ] **Step 4: Check.** Screenshot both slides and run the clip check.

- [ ] **Step 5: Log and commit.**

  ```bash
  git add site-plan/specs/2026-10-14-chart-tokens-design.md
  git commit -m "Chart tokens: deck sun charts use season tokens"
  ```

### Task 9: Housekeeping

**Files:**
- Modify: `site-plan/specs/2026-10-11-map-tokens-v3-design.md`, the "Out of scope" list near the
  end.
- Modify: `site-plan/specs/2026-10-14-chart-tokens-design.md`
- Modify: `CLAUDE.md`, the "Site Microsite" section.

- [ ] **Step 1: Close the v3 item.** In the v3 spec's Out of scope list, replace the line
  `- Re-pointing \`Chart Categorical\` to Color Roles.` with
  `- ~~Re-pointing \`Chart Categorical\` to Color Roles.~~ Closed 2026-10-14: kept on Ramps for its Dark mode; see \`2026-10-14-chart-tokens-design.md\`.`

- [ ] **Step 2: Finish the chart spec.**
  - Change `**Status:**` to `Shipped 2026-10-14 (tasks 1–8).`
  - Add the four rulings R1–R4 under a `## Rulings during implementation` heading, copied from
    this plan.

- [ ] **Step 3: Add a CLAUDE.md convention.** Add a bullet under "Site Microsite":

  ```markdown
  **Chart colors and chart text come from `docs/assets/chart-tokens.css`** (mirrors the PDC Pro
  Vision chart collections; spec `site-plan/specs/2026-10-14-chart-tokens-design.md`). A new
  chart's prefixed variables must reference `--chart-*` tokens, not raw hex; its SVG text uses
  `font: var(--chart-font-<role>)`. Run `python3 scripts/check_chart_tokens.py page <file>
  <prefixes…>` before committing a chart page, and `… tokens` after any palette change.
  ```

- [ ] **Step 4: Run every check.**

  ```bash
  python3 scripts/check_chart_tokens.py tokens && \
  python3 scripts/check_chart_tokens.py page docs/water.html precip runoff wbal elev flow storm shed wuse && \
  python3 scripts/check_chart_tokens.py page docs/sun-solar.html spc sp3d spo && \
  python3 scripts/check_chart_tokens.py page docs/climate.html wind
  ```

  Expected: four `OK` lines.

- [ ] **Step 5: Commit.**

  ```bash
  git add site-plan/specs/2026-10-11-map-tokens-v3-design.md site-plan/specs/2026-10-14-chart-tokens-design.md CLAUDE.md
  git commit -m "Chart tokens: close v3 item, finalize spec, document convention"
  ```

  Don't push. Report to Andrew and wait for "push".

## Review Focus

1. **Labels overflow or overlap after the font change.**
   - Monospace in caps is wider than `system-ui`, and value text grows from 10.5 to 13px. Expect
     dense axes to collide: the precip months, the storm return periods and the 12 month labels in
     the sun polar chart.
   - Expected behavior: every label stays readable and inside the chart, at 360px viewport width
     too.
   - Covered by Task 4 Step 6, Task 5 Step 6 and Task 6 Step 5. Add a 360px-wide pass with
     `resize_window`.
2. **Dark mode resolves through the tokens.**
   - Removing per-chart dark blocks relies on `--chart-*` resolving on the same `.viz-root`.
   - Expected behavior: forced `data-theme="dark"` and the system preference both show the dark
     palette, and forced `data-theme="light"` on a dark-preference system shows light.
   - Covered by the visual steps. Also toggle `data-theme="light"` while the OS is in dark mode.
3. **The font fails to load (offline or blocked).**
   - Expected behavior: chart text falls back to `ui-monospace` without layout breakage.
   - Check once by blocking `fonts.googleapis.com` with DevTools in Task 4 Step 6.
4. **`color-mix` support.**
   - Old browsers drop the declaration, so translucent bands vanish.
   - Expected behavior: the bands show in current Chrome, Safari and Firefox. That's acceptable for
     this site.
   - Covered by the visual check. Logged as a known limitation in the spec.
5. **Deck charts keep their raw colors where a hex value wasn't in the mapping table.**
   - Expected behavior: there are zero unbound SOLID paints in chart frames.
   - Covered by Task 7 Step 4's re-scan and Task 8 Step 4.
