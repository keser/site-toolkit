# Map Tokens v2 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Also load the `figma:figma-use` skill before any `use_figma` call.

**Goal:** Replace the two-step Shade/Tint map palette with Shade/Base/Tint roles, 50 fill styles (90 before 2026-10-11)
fill styles, a 6-tier stroke-weight scale, component bindings, and a line-treatment reference sheet
in the PDC Pro Vision Figma file. No map should change color as a side effect.

**Architecture:** All work happens in Figma through `use_figma` (Plugin API JavaScript). This plan
file is the only repo artifact: its checkboxes and **State ledger** record progress and the IDs that
later tasks need. Each task has the same shape:

1. Run a read-only verification script and see it fail.
2. Run the build script.
3. Re-run the verification and see it pass.
4. Record IDs in the ledger and commit.

**Tech Stack:** Figma Plugin API via the Figma MCP `use_figma` tool (`skillNames: "figma-use"`);
`get_screenshot` for visual checks; git for plan-file commits.

**Spec:** [`site-plan/specs/2026-10-10-map-tokens-v2-design.md`](../specs/2026-10-10-map-tokens-v2-design.md)

> **2026-10-11:** the `Map Overlay` collection was renamed `Color Roles` (v3 plan Task 1); code below uses the new name.

## Global Constraints

- File key: `aF9SVeTLwFN8PCEiU2OSBQ`. Pages: Keys `222:2275`, Styles `699:2080`. Styles section `701:2`.
- **One page per `use_figma` call.** Each call switches pages with `await figma.setCurrentPageAsync(page)`
  at most once. Multi-page reads run as parallel calls in one message.
- **Never edit** the Base Map page or the Sector Analysis page. Read-only access is fine.
- **Color roles:** Shade = ramp step 700. Base = step 500. Tint = violet 300, teal 300, magenta 400,
  slate 200, cobalt 200, coral 200, charcoal 300, gold 100, sage 400, amber 300.
- **Hues, in order:** sage, cobalt, coral, gold, magenta, charcoal, slate, teal, violet, amber.
- **Variable names:** `<hue>/Shade`, `<hue>/Base`, `<hue>/Tint` in `Map Overlay`, scoped
  `ALL_FILLS, STROKE_COLOR`.
- **Paint style names:** `<hue>/<Role>/<opacity>`. **The set is 50 styles (trimmed 2026-10-11):**
  `Shade/100`, `Base/100`, `Tint/100`, `Tint/50`, `Tint/25` per hue. Only the Tint is used
  translucent (map overlays); solid fills serve captions, sector overlays, and lines. Opacity is
  stored on the paint as 0.25, 0.5, or 1. **/100 styles bind their color to the `Map Overlay` variable; /25 and /50
  styles hold a raw copied color** (revised 2026-10-11: Figma overwrites a variable-bound paint's
  opacity with the variable's alpha, so bound /25 and /50 styles render at 100%).
- **Stroke collection:** `Stroke`, one mode named `Value`. Variables `weight/xs`=1, `sm`=2, `md`=3,
  `lg`=4, `xl`=6, `2xl`=8, scoped `STROKE_FLOAT` only.
- **Renames keep IDs.** `Tint` variables are renamed to `Base`, and the 20 existing paint styles are
  renamed, never deleted and recreated.
- **Default hue** for component main components: `charcoal`.
- **No variant axis is removed** from any component set.
- **Every build script is idempotent.** It checks names before creating or renaming, so a re-run
  after a partial failure creates no duplicates.

### Prelude A — token lookups (paste at the top of every script that needs tokens)

```js
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const col = n => cols.find(c => c.name === n);
const colorVars = await figma.variables.getLocalVariablesAsync('COLOR');
const floatVars = await figma.variables.getLocalVariablesAsync('FLOAT');
const V = (cn, n) => { const c = col(cn); return c ? colorVars.find(v => v.variableCollectionId === c.id && v.name === n) || null : null; };
const W = tier => { const c = col('Stroke'); return c ? floatVars.find(v => v.variableCollectionId === c.id && v.name === 'weight/' + tier) || null : null; };
// Docs display order (2026-10-12): loosely the visible spectrum, then the greys. Neutral follows charcoal on the Ramps frame.
const HUES = ['magenta','coral','amber','gold','sage','teal','cobalt','violet','slate','charcoal'];
const TINT_STEP = { violet:'300', teal:'300', magenta:'400', slate:'200', cobalt:'200', coral:'200', charcoal:'300', gold:'100', sage:'400', amber:'300' };
const STEP = (hue, role) => role === 'Shade' ? '700' : role === 'Base' ? '500' : TINT_STEP[hue];
const ROLES = ['Tint','Base','Shade'];
const OPACITIES = [25, 50, 100];
// The fill-style set (trimmed 2026-10-11): every role solid, plus Tint at 50% and 25% for overlays.
const STYLE_SET = HUES.flatMap(h => [['Shade', 100], ['Base', 100], ['Tint', 100], ['Tint', 50], ['Tint', 25]].map(([r, o]) => [h, r, o]));
const TIERS = [['xs',1],['sm',2],['md',3],['lg',4],['xl',6],['2xl',8]];
const TIER_BY_WEIGHT = Object.fromEntries(TIERS.map(([t, w]) => [w, t]));
const styles = await figma.getLocalPaintStylesAsync();
const S = name => styles.find(s => s.name === name) || null;
const hex = c => '#' + [c.r, c.g, c.b].map(x => Math.round(x * 255).toString(16).padStart(2, '0')).join('');
const lin = x => x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
const lum = c => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
const contrast = (a, b) => (Math.max(lum(a), lum(b)) + 0.05) / (Math.min(lum(a), lum(b)) + 0.05);
const rampColor = (hue, step) => { const v = V('Ramps', hue + '/' + step); return v.valuesByMode[col('Ramps').modes[0].modeId]; };
```

### Prelude B — Styles-page doc helpers (paste after Prelude A in Task 7 scripts)

```js
await Promise.all([['Inter','Regular'],['Inter','Medium'],['JetBrains Mono','Regular']].map(([family, style]) => figma.loadFontAsync({ family, style })));
const WHITE = {r:1,g:1,b:1}, BLACK = {r:0,g:0,b:0}, GREY = {r:0x60/255,g:0x5f/255,b:0x5b/255}, CARD = {r:245/255,g:245/255,b:245/255}, AERIAL = {r:0xaf/255,g:0xab/255,b:0xa4/255};
const solid = c => [{ type: 'SOLID', color: c }];
const bound = v => [figma.variables.setBoundVariableForPaint({ type: 'SOLID', color: {r:0,g:0,b:0} }, 'color', v)];
function txt(parent, chars, o = {}) {
  const t = figma.createText(); t.fontName = { family: o.family || 'Inter', style: o.style || 'Regular' }; t.fontSize = o.size || 13; t.characters = chars; t.fills = solid(o.color || BLACK); t.name = o.name || chars.slice(0, 40);
  parent.appendChild(t); if (o.width) { t.resize(o.width, t.height); t.textAutoResize = 'HEIGHT'; } return t;
}
const section = await figma.getNodeByIdAsync('701:2');
function docFrame(name, title, desc, x) {
  section.children.filter(n => n.name === name).forEach(n => n.remove());
  const f = figma.createAutoLayout('VERTICAL', { name }); section.appendChild(f); f.fills = solid(WHITE);
  f.resize(1440, 100); f.primaryAxisSizingMode = 'AUTO'; f.counterAxisSizingMode = 'FIXED'; f.x = x; f.y = 64;
  const st = figma.createAutoLayout('HORIZONTAL', { name: '_Status' }); f.appendChild(st); st.resize(1440, 64); st.layoutSizingHorizontal = 'FILL'; st.primaryAxisAlignItems = 'SPACE_BETWEEN'; st.counterAxisAlignItems = 'CENTER'; st.paddingLeft = st.paddingRight = 32; st.fills = [];
  txt(st, 'DESIGN SYSTEM — PDC PRO VISION'); txt(st, 'OCTOBER 2026');
  const dv = figma.createAutoLayout('HORIZONTAL', { name: 'Divider' }); f.appendChild(dv); dv.layoutSizingHorizontal = 'FILL'; dv.paddingLeft = dv.paddingRight = 32; dv.fills = [];
  const ln = figma.createRectangle(); ln.name = 'Line'; ln.fills = solid(BLACK); dv.appendChild(ln); ln.resize(1376, 1); ln.layoutSizingHorizontal = 'FILL';
  const ct = figma.createAutoLayout('VERTICAL', { name: 'Content', itemSpacing: 24 }); f.appendChild(ct); ct.layoutSizingHorizontal = 'FILL'; ct.paddingTop = ct.paddingBottom = ct.paddingLeft = ct.paddingRight = 64; ct.fills = [];
  txt(ct, title, { size: 36, style: 'Medium' }); txt(ct, desc, { size: 18, width: 500 });
  f.paddingBottom = 64;
  return f;
}
function row(f, name, title, desc, gap = 12) {
  const r = figma.createAutoLayout('HORIZONTAL', { name, itemSpacing: 128 }); f.appendChild(r); r.layoutSizingHorizontal = 'FILL'; r.paddingLeft = r.paddingRight = 64; r.paddingTop = r.paddingBottom = 32; r.fills = [];
  const d = figma.createAutoLayout('VERTICAL', { name: 'Description', itemSpacing: 4 }); r.appendChild(d); d.fills = [];
  txt(d, title, { size: 18, style: 'Medium', width: 320 }); txt(d, desc, { size: 13, color: GREY, width: 320 });
  const body = figma.createAutoLayout('VERTICAL', { name: 'Body', itemSpacing: gap }); r.appendChild(body); body.fills = [];
  return body;
}
function note(f, title, body) {
  const n = figma.createAutoLayout('VERTICAL', { name: 'Note — ' + title, itemSpacing: 4 }); f.appendChild(n); n.layoutSizingHorizontal = 'FILL'; n.paddingLeft = n.paddingRight = 64; n.paddingBottom = 16; n.fills = [];
  txt(n, title, { style: 'Medium' }); txt(n, body, { color: GREY, width: 1312 });
  return n;
}
```

## Review Focus

1. **Instances that inherit a main component's paint change silently** when Task 5 edits that main
   component, on any page. Task 4 audits every page and Task 5 pins inheriting layers before
   anything changes.
2. **Re-running after a partial failure** must not rename `Base` again, duplicate `Tint`, or
   duplicate styles. Every build script checks names first, and the verifications assert exact
   counts (30 / 6 / 50).
3. **Stroke binding on Keys (Task 6)** must skip sublayers inside instances, so it creates no
   overrides. It must also skip strokes with mixed per-side weights, and report them.
4. **Opacity must live on the paint, not the color.** Ramp colors carry no alpha, so the Task 3
   verification asserts paint opacity is exactly 0.25 / 0.5 / 1. The /25 and /50 styles must stay
   unbound, and their copied color must match the current role color (drift check).
5. **Bindings survive the renames by ID.** The verifications compare against the IDs recorded in
   the State ledger in Tasks 1 and 3.

## State ledger

Fill this in as tasks run. Later tasks read IDs from here.

- Task 1, pre-rename `<hue>/Tint` variable IDs (these become `Base`): sage 638:568, cobalt 638:569, coral 638:570, gold 638:571, magenta 638:572, charcoal 638:573, slate 638:574, teal 638:575, violet 638:576, amber 638:577 (all `VariableID:`); collection had 20 variables, now 30. New `Tint` IDs: `VariableID:738:668`–`738:677` in hue order.
- Task 1, Keys-page binding counts before: `{ Shade:fills 76, Shade:strokes 41, Tint:fills 20 }`; after: `{ Shade:fills 76, Shade:strokes 41, Base:fills 20 }`.
- Task 2, `Stroke` collection `VariableCollectionId:740:2` (mode `Value`); `weight/xs,sm,md,lg,xl,2xl` = `VariableID:740:3`–`740:8` (1,2,3,4,6,8).
- Task 3, pre-rename paint style IDs, `<hue>/Shade` and `<hue>/Tint`: `{"sage/Shade":"S:ab6a44800f57ffeca1f0919ec66b8b56555bfd80,","sage/Tint":"S:8ab98dca9b134e7036e5e8014301f035388995b7,","cobalt/Shade":"S:e27522a5795ac4cecd7705e66146048194efcafb,","cobalt/Tint":"S:493499ef7a88ba7240ba3b444eb801ceac3f70b1,","coral/Shade":"S:a2d50fe247eb7f102656a29a51e55cfeee2a3020,","coral/Tint":"S:408e0f5a2e73ae8fa85bb14919ac91bfff1a88ce,","gold/Shade":"S:82101cc01790282f6a27bbd17c0802ec18d93da0,","gold/Tint":"S:b921044d79104cc509f7e83962270c38803816e2,","magenta/Shade":"S:02cf29e69acfce532f73177fb01b6af78685dcb1,","magenta/Tint":"S:a71540625568ebde439ad0ffafb1ac0173813ce9,","charcoal/Shade":"S:f36b0498863718e588ab3e65ac31f933a800fb90,","charcoal/Tint":"S:bebd9e9b3ebca830ad9f68e2be23da93eb2e1aac,","slate/Shade":"S:8ab1dcf74f7cfdea63c55b43549fd69314b983ea,","slate/Tint":"S:fa2f163bc4892ae2f6a7b60a8f1339ae4af0ed11,","teal/Shade":"S:77da7a085b31ee25caa80b09227430dcc04bc5b9,","teal/Tint":"S:9bcf0a81d69a6124b3653c0cc2667ed70be643d6,","violet/Shade":"S:049ac38c4dc73b8bc542427baebb544c503e048f,","violet/Tint":"S:c0a59bc518b7e1dbdc8bd7b4c85f5d452fa49546,","amber/Shade":"S:e9dae32e00041743e49bbe6949796d58dd396548,","amber/Tint":"S:b88ecf03c6aabeeab8468c1bce7fcf89cb1c70ba,"}`
- Task 4, inheriting-instance audit result per page: 11 pages audited. Keys (`222:2275`) 237 (Legend Row 198, Site Marker 33, caption 5, Line Sample 1; 12 nested-marker "1" layers appear under both Legend Row and Site Marker, 225 distinct node IDs). Water (`237:2275`) 6 (caption 6). Styles, Base Map, Zones & Microclimates, Sector Analysis, Soil, Site Data Visualizations, Mood Board, Permaculture Resources, Assets: 0. Total 243 rows (231 distinct IDs). Pins file: `.superpowers/sdd/2026-10-10-map-tokens-v2/tokens-v2-pins.json` (git-ignored). Decision: pin (controller ruling; plan default).
- Task 4 correction (found in Task 5): the 5 Keys and 6 Water `caption` pins are instances of a **remote library** caption set (`238:4172`), not local `640:4373`. They matched by name only, and local caption edits cannot reach them (0 restored on both pages).
- Task 5, caption mapping (Step 1): `640:4365` Dark/SM and `640:4367` Dark/LG (bg `#262626`, white text) stay **Dark**. `640:4369` and `640:4371`, formerly "Light" (bg `#ffffff`@0.85, black text, stroke bound to `VariableID:145:401`), become **White**. New variants: Light/SM `749:668`, Black/SM `749:670`, Light/LG `749:672`, Black/LG `749:674`. Grid: Dark/White/Light/Black at x 0/200/400/600, SM y 0, LG y 60; set is 797×130.
- Task 5, Legend Row Area: fill rect `480:868`, stroke rect `640:1176` (weight 2 → `weight/sm`, stored as four per-side bindings).
- Task 5, live pin counts (ruling 10, live snapshot instead of the pins file): Step 3 snapshotted 405 Keys instance layers, restored 53 (51 had variable-bound paints), residual 0, no stroke-weight changes, `unmatchedWeights` []. Step 4 snapshotted 405, restored 0, residual 0. Step 6 Water: 0 restored, 6 unchanged, 0 missing, 0 residual. Verification went from RED (32 problems) to GREEN.
- Task 5 Step 3b (fix round 1): skipped 2 in-main nested instances and snapshotted 400 outer layers. Cleared overrides on `480:874` and `480:881` (0 left). Restored 19 outer layers (`I…;480:874;472:852` and `I…;480:881;473:854`), residual 0, no stroke-weight changes. Main nested layers now resolve to the Line → `charcoal/Base/100` (+ `weight/sm`) and the Marker → `charcoal/Shade/100` (Numbered/Circle, per the Step 3 rule). Post-check of the 237 Keys pins: 235 match, 2 differ by design (the main nested layers above), 0 instance differs, 0 missing. Step 2 verification `ok: true`.
- Task 6, stroke-weight counts before and after: before == after == {1:23, 2:20, 3:1, 4:31, 5:13, 6:14, 8:27, 1.5:7, mixed:3} (139 stroked nodes). Bound 107 (unboundExact 107 -> 0). Skipped mixed (3): 168:1168, 168:1174, 168:1181. Skipped unmatched (20): 1.5 x7 (640:4369, 640:4371, 497:4601, 497:4608, 497:4615, 497:4622, 497:4629); 5 x13 (497:4398, 497:4405, 497:4361, 497:4368, 497:4462, 497:4518, 497:4525, 497:4532, 497:4539, 709:4528, 709:4531, 709:4542, 709:4544). Uses isWeightBound (per-side bindings, Ruling 13).
- Task 7, new Styles-page frame IDs: Semantic Tokens `758:2`, Fill Styles `758:263`, Stroke `758:4720`; Typography moved to x=6336 (`701:447`); Ramps `701:3`. Section `701:2` resized to 7840x4259. Ruling 14 resolved 2026-10-11: /25 and /50 styles now hold raw copied colors and render translucent; page copy on Semantic Tokens (`758:13`) and Fill Styles (`758:271`) describes the re-sync rule.
- Task 7, Copy/Paste-properties binding test result: _(deferred to Andrew)_

---

### Task 1: Color variables — rename `Tint` → `Base`, add new `Tint`

**Files:**
- Modify (Figma): `Map Overlay` collection (`VariableCollectionId:145:395`)
- Modify: `site-plan/plans/2026-10-10-map-tokens-v2.md` (ledger and checkboxes)

**Interfaces:**
- Consumes: Prelude A.
- Produces: 30 `Map Overlay` variables named `<hue>/{Shade,Base,Tint}`. `<hue>/Base` keeps the old
  `<hue>/Tint` IDs.

- [x] **Step 1: Record the pre-change state.** Run on any page (it reads variables only), then copy
  the result into the ledger.

```js
// Prelude A here
const ids = Object.fromEntries(HUES.map(h => { const v = V('Color Roles', h + '/Tint'); return [h, v ? v.id : null]; }));
return { tintIds: ids, count: col('Color Roles').variableIds.length };
```

- [x] **Step 2: Record Keys-page binding counts.** This gives a baseline for checking visual
  continuity.

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const byId = Object.fromEntries(colorVars.map(v => [v.id, v.name]));
const tally = {};
for (const n of page.findAll(n => 'fills' in n || 'strokes' in n)) for (const k of ['fills','strokes']) {
  const ps = n[k]; if (!Array.isArray(ps)) continue;
  for (const p of ps) { const id = p.boundVariables && p.boundVariables.color && p.boundVariables.color.id; const nm = id && byId[id]; if (!nm || !/\/(Tint|Base|Shade)$/.test(nm)) continue; const key = nm.split('/')[1] + ':' + k; tally[key] = (tally[key] || 0) + 1; }
}
return tally;
```

Expected (2026-10-10 audit): `{ "Shade:fills": 76, "Shade:strokes": 41, "Tint:fills": 20 }`.

- [x] **Step 3: Write and run the verification. It should fail.**

```js
// Prelude A here
const LEDGER_TINT_IDS = { /* paste the Step 1 tintIds object here */ };
const problems = [];
const mo = col('Color Roles'); const m = mo.modes[0].modeId;
for (const h of HUES) for (const role of ['Shade','Base','Tint']) {
  const v = V('Color Roles', h + '/' + role);
  if (!v) { problems.push('missing ' + h + '/' + role); continue; }
  const a = await figma.variables.getVariableByIdAsync(v.valuesByMode[m].id);
  if (!a || a.name !== h + '/' + STEP(h, role)) problems.push(h + '/' + role + ' aliases ' + (a && a.name));
  if (v.scopes.join(',') !== 'ALL_FILLS,STROKE_COLOR') problems.push(h + '/' + role + ' scopes ' + v.scopes);
  if (!v.description) problems.push(h + '/' + role + ' no description');
  if (role === 'Base' && LEDGER_TINT_IDS[h] && v.id !== LEDGER_TINT_IDS[h]) problems.push(h + '/Base id changed');
}
if (mo.variableIds.length !== 30) problems.push('count ' + mo.variableIds.length);
return { ok: problems.length === 0, problems };
```

Expected now: `ok: false`, with problems including `missing sage/Base` and `count 20`.

- [x] **Step 4: Run the build.**

```js
// Prelude A here
const mo = col('Color Roles'); const m = mo.modes[0].modeId;
const W_ = { r:1, g:1, b:1 }, K_ = { r:0, g:0, b:0 };
const renamed = [], created = [];
for (const h of HUES) {
  const oldTint = V('Color Roles', h + '/Tint'), base = V('Color Roles', h + '/Base');
  if (!base && oldTint) { oldTint.name = h + '/Base'; renamed.push(oldTint.id); }
  if (!V('Color Roles', h + '/Tint')) {
    const v = figma.variables.createVariable(h + '/Tint', mo, 'COLOR');
    v.scopes = ['ALL_FILLS', 'STROKE_COLOR'];
    v.setValueForMode(m, figma.variables.createVariableAlias(V('Ramps', h + '/' + TINT_STEP[h])));
    colorVars.push(v); created.push(v.id);
  }
  const t = rampColor(h, TINT_STEP[h]), b = rampColor(h, '500'), s = rampColor(h, '700');
  V('Color Roles', h + '/Tint').description = `${h} step ${TINT_STEP[h]} — light-theme fills; black text ${contrast(t, K_).toFixed(1)}:1.`;
  V('Color Roles', h + '/Base').description = `${h} step 500 — lines, strokes, and markers without text. Not for text-bearing fills (${contrast(b, K_).toFixed(1)}:1 black / ${contrast(b, W_).toFixed(1)}:1 white).`;
  V('Color Roles', h + '/Shade').description = `${h} step 700 — dark-theme fills and strong outlines; white text ${contrast(s, W_).toFixed(1)}:1. Validated >=3:1 vs aerial tone #afaba4.`;
}
return { renamed, created, count: mo.variableIds.length };
```

- [x] **Step 5: Re-run the Step 3 verification.** Expected: `ok: true, problems: []`.

- [x] **Step 6: Re-run the Step 2 tally.** Expected: `{ "Shade:fills": 76, "Shade:strokes": 41,
  "Base:fills": 20 }`. The 20 former-Tint fills now report as Base, and no `Tint:*` keys appear.
  Any difference means a binding moved. Stop and investigate before continuing.

- [x] **Step 7: Commit the ledger.**

```bash
git add site-plan/plans/2026-10-10-map-tokens-v2.md
git commit -m "Map tokens v2 Task 1: rename Tint to Base, add Tint variables"
```

---

### Task 2: Stroke weight variables

**Files:**
- Create (Figma): `Stroke` variable collection
- Modify: this plan (checkboxes)

**Interfaces:**
- Consumes: Prelude A.
- Produces: `Stroke` collection with `weight/{xs,sm,md,lg,xl,2xl}` (FLOAT). Later tasks find them
  with `W(tier)`.

- [x] **Step 1: Write and run the verification. It should fail.**

```js
// Prelude A here
const problems = []; const c = col('Stroke');
if (!c) return { ok: false, problems: ['no Stroke collection'] };
if (c.modes.length !== 1 || c.modes[0].name !== 'Value') problems.push('modes ' + c.modes.map(m => m.name));
for (const [t, w] of TIERS) {
  const v = W(t); if (!v) { problems.push('missing weight/' + t); continue; }
  if (v.valuesByMode[c.modes[0].modeId] !== w) problems.push('weight/' + t + ' = ' + v.valuesByMode[c.modes[0].modeId]);
  if (v.scopes.join(',') !== 'STROKE_FLOAT') problems.push('weight/' + t + ' scopes ' + v.scopes);
}
if (c.variableIds.length !== 6) problems.push('count ' + c.variableIds.length);
return { ok: problems.length === 0, problems };
```

Expected now: `ok: false, problems: ['no Stroke collection']`.

- [x] **Step 2: Run the build.**

```js
// Prelude A here
let c = col('Stroke');
if (!c) { c = figma.variables.createVariableCollection('Stroke'); c.renameMode(c.modes[0].modeId, 'Value'); }
const m = c.modes[0].modeId; const made = [];
for (const [t, w] of TIERS) {
  let v = W(t);
  if (!v) { v = figma.variables.createVariable('weight/' + t, c, 'FLOAT'); floatVars.push(v); made.push(v.id); }
  v.scopes = ['STROKE_FLOAT']; v.setValueForMode(m, w); v.description = `Stroke weight tier ${t} = ${w}px.`;
}
return { collectionId: c.id, made };
```

- [x] **Step 3: Re-run the verification.** Expected: `ok: true`.

- [x] **Step 4: Commit.**

```bash
git add site-plan/plans/2026-10-10-map-tokens-v2.md
git commit -m "Map tokens v2 Task 2: Stroke weight collection"
```

---

### Task 3: Fill styles (50; 90 before 2026-10-11)

**Files:**
- Modify (Figma): local paint styles
- Modify: this plan (ledger and checkboxes)

**Interfaces:**
- Consumes: Prelude A; Task 1 variables.
- Produces: 50 paint styles `<hue>/<Role>/<opacity>` (see `STYLE_SET` in Prelude A). Later tasks find them with `S(name)`.

- [x] **Step 1: Record the pre-rename style IDs in the ledger.**

```js
// Prelude A here
const out = {};
for (const h of HUES) for (const r of ['Shade','Tint']) { const s = S(h + '/' + r); out[h + '/' + r] = s ? s.id : null; }
return out;
```

- [x] **Step 2: Write and run the verification. It should fail.**

```js
// Prelude A here
const LEDGER_STYLE_IDS = { /* paste the Step 1 object here */ };
const problems = [];
for (const [h, r, o] of STYLE_SET) {
  const name = `${h}/${r}/${o}`, s = S(name);
  if (!s) { problems.push('missing ' + name); continue; }
  const p = s.paints;
  if (p.length !== 1 || p[0].type !== 'SOLID') { problems.push(name + ' paints'); continue; }
  const bv = p[0].boundVariables && p[0].boundVariables.color;
  if (o === 100) {
    const v = bv && await figma.variables.getVariableByIdAsync(bv.id);
    if (!v || v.name !== `${h}/${r}`) problems.push(name + ' bound to ' + (v && v.name));
    if (hex(p[0].color) !== hex(rampColor(h, STEP(h, r)))) problems.push(name + ' stored color ' + hex(p[0].color) + ' (thumbnail shows this)');
  } else {
    // /25 and /50: unbound raw color that must match the role's current color (drift check)
    if (bv) problems.push(name + ' is variable-bound (renders opaque)');
    if (hex(p[0].color) !== hex(rampColor(h, STEP(h, r)))) problems.push(name + ' drifted: ' + hex(p[0].color) + ' vs ' + hex(rampColor(h, STEP(h, r))));
  }
  if (Math.abs(p[0].opacity - o / 100) > 1e-6) problems.push(name + ' opacity ' + p[0].opacity);
}
for (const h of HUES) {
  if (LEDGER_STYLE_IDS[h + '/Shade'] && (S(h + '/Shade/100') || {}).id !== LEDGER_STYLE_IDS[h + '/Shade']) problems.push(h + '/Shade/100 is not the renamed style');
  if (LEDGER_STYLE_IDS[h + '/Tint'] && (S(h + '/Base/100') || {}).id !== LEDGER_STYLE_IDS[h + '/Tint']) problems.push(h + '/Base/100 is not the renamed style');
  if (S(h + '/Shade') || S(h + '/Tint')) problems.push(h + ' old-name style still present');
}
const mapStyles = styles.filter(s => HUES.some(h => s.name.startsWith(h + '/')));
if (mapStyles.length !== 50) problems.push('count ' + mapStyles.length);
return { ok: problems.length === 0, problems: problems.slice(0, 40), total: problems.length };
```

Expected now: `ok: false`, about 50 problems (missing names, old names present).

- [x] **Step 3: Run the build.**

```js
// Prelude A here
const renamed = [], created = [];
for (const h of HUES) {
  const oldShade = S(h + '/Shade'); if (oldShade && !S(h + '/Shade/100')) { oldShade.name = h + '/Shade/100'; renamed.push(oldShade.id); }
  const oldTint = S(h + '/Tint'); if (oldTint && !S(h + '/Base/100')) { oldTint.name = h + '/Base/100'; renamed.push(oldTint.id); }
}
// Remove map styles outside STYLE_SET (e.g. the Shade/Base 25/50 styles trimmed on 2026-10-11).
const keep = new Set(STYLE_SET.map(([h, r, o]) => `${h}/${r}/${o}`));
for (const st of styles.filter(st => HUES.some(h => st.name.startsWith(h + '/')) && !keep.has(st.name))) st.remove();
for (const [h, r, o] of STYLE_SET) {
  const name = `${h}/${r}/${o}`;
  let s = S(name);
  if (!s) { s = figma.createPaintStyle(); s.name = name; styles.push(s); created.push(s.id); }
  if (o === 100) {
    // Store the resolved color (not a black placeholder) so the style picker thumbnail shows the real color.
    const c = rampColor(h, STEP(h, r));
    s.paints = [figma.variables.setBoundVariableForPaint({ type: 'SOLID', color: { r: c.r, g: c.g, b: c.b } }, 'color', V('Color Roles', `${h}/${r}`))];
    s.description = `${h} ${r} (step ${STEP(h, r)}) at 100% opacity.`;
  } else {
    // Figma overwrites a variable-bound paint's opacity with the variable's alpha, so /25 and /50 hold a raw copied color.
    const c = rampColor(h, STEP(h, r));
    s.paints = [{ type: 'SOLID', color: { r: c.r, g: c.g, b: c.b }, opacity: o / 100 }];
    s.description = `${h} ${r} at ${o}% opacity. Raw color copied from ${h}/${r} (not variable-bound: Figma overwrites a bound paint's opacity). Re-sync after any ramp or Color Roles change.`;
  }
}
return { renamed: renamed.length, created: created.length };
```

Expected on first run: `renamed: 20, created: 30` (the 2026-10-10 run created 70 of the original 90-style set; 40 Shade/Base 25/50 styles were deleted on 2026-10-11 after confirming no layer used them).

**Re-sync rule (2026-10-11):** the /25 and /50 styles don't follow color changes on their own. After
any change to a Ramps value or a `Color Roles` alias, re-run this Step 3 script, then the Step 2
verification. Its drift check lists any /25 or /50 style whose color no longer matches its role.

- [x] **Step 4: Re-run the verification.** Expected: `ok: true`.

- [x] **Step 5: Commit the ledger.**

```bash
git add site-plan/plans/2026-10-10-map-tokens-v2.md
git commit -m "Map tokens v2 Task 3: fill styles"
```

---

### Task 4: Audit inheriting instances (read-only, every page)

Changing a main component's paint changes every instance layer that hasn't overridden that paint.
This task finds those layers before Task 5 touches anything.

**Files:**
- Create: `$SCRATCH/tokens-v2-pins.json`, where `$SCRATCH` is the session scratchpad directory.
  It holds pin snapshots and is not committed.
- Modify: this plan (ledger)

**Interfaces:**
- Consumes: nothing from earlier tasks. This task is read-only.
- Produces: per-page JSON `{ page, layers: [{ id, fills, strokes, strokeWeight, setName }] }` listing
  every instance sublayer whose fills or strokes are identical to its source layer in the main
  component, for the sets `Line Sample`, `Site Marker`, `Legend Row`, `caption`.

- [x] **Step 1: List the pages.** Run on any page:
  `return figma.root.children.map(p => ({ id: p.id, name: p.name }))`.

- [x] **Step 2: Run the audit on every page, as parallel calls in one message.** Replace `PAGE_ID`
  in each copy.

```js
const page = await figma.getNodeByIdAsync('PAGE_ID'); await figma.setCurrentPageAsync(page);
const TARGETS = ['Line Sample','Site Marker','Legend Row','caption'];
const setOf = inst => { const mc = inst.mainComponent; if (!mc) return null; const s = mc.parent && mc.parent.type === 'COMPONENT_SET' ? mc.parent.name : mc.name; return TARGETS.includes(s) ? s : null; };
const strip = ps => JSON.stringify((ps || []).map(p => ({ t: p.type, c: p.color, o: p.opacity, b: p.boundVariables && p.boundVariables.color && p.boundVariables.color.id })));
const layers = [];
for (const inst of page.findAllWithCriteria({ types: ['INSTANCE'] })) {
  const setName = setOf(inst); if (!setName) continue;
  for (const n of [inst, ...inst.findAll(() => true)]) {
    if (n !== inst && n.type === 'INSTANCE' && setOf(n)) continue; // nested target instances are audited on their own
    if (!('fills' in n) && !('strokes' in n)) continue;
    const srcId = n === inst ? inst.mainComponent.id : n.id.split(';').pop();
    const src = await figma.getNodeByIdAsync(srcId); if (!src) continue;
    const sameFill = 'fills' in n && Array.isArray(n.fills) && n.fills.length && strip(n.fills) === strip(src.fills);
    const sameStroke = 'strokes' in n && n.strokes.length && strip(n.strokes) === strip(src.strokes);
    if (sameFill || sameStroke) layers.push({ id: n.id, setName, name: n.name,
      fills: sameFill ? JSON.parse(JSON.stringify(n.fills)) : null,
      strokes: sameStroke ? JSON.parse(JSON.stringify(n.strokes)) : null,
      strokeWeight: typeof n.strokeWeight === 'number' ? n.strokeWeight : null });
  }
}
return { page: page.name, pageId: page.id, count: layers.length, layers };
```

- [x] **Step 3: Save every page's result** into `$SCRATCH/tokens-v2-pins.json`, keyed by page ID.
  Write per-page counts in the ledger.

- [x] **Step 4: Decision gate.** If every count is 0, write "no inheriting layers, no pins needed"
  in the ledger and skip pinning in Task 5. If any count is above 0, show Andrew the per-page,
  per-set counts and ask: **pin** (keep today's colors as instance overrides) or **accept** (let
  those instances follow the new defaults). Record the answer in the ledger. The default
  recommendation is pin.

- [x] **Step 5: Commit the ledger.**

```bash
git add site-plan/plans/2026-10-10-map-tokens-v2.md
git commit -m "Map tokens v2 Task 4: inheriting-instance audit"
```

---

### Task 5: Component updates

**Files:**
- Modify (Figma): component sets `Line Sample` `472:867`, `Site Marker` `473:862`,
  `Legend Row` `480:889`, `caption` `640:4373` (all on Keys)
- Modify: this plan (checkboxes)

**Interfaces:**
- Consumes: Prelude A; Tasks 1–3 tokens; Task 4 pins file and decision.
- Produces: main components bound to styles and weight tiers. `caption` has `Style` values
  Light/Dark/White/Black × `Size` SM/LG (8 variants).

- [x] **Step 1: Inventory `caption` and the `Legend Row` Area variant (read-only).** The caption
  result decides the variant mapping in Step 4. Run this second read too, and confirm the Area
  variant has a filled rectangle (and, if split, a separate stroked one) before Step 3:
  `const a = (await figma.getNodeByIdAsync('480:889')).children.find(v => v.variantProperties['Swatch Type'] === 'Area'); return a.findAll(n => n.type === 'RECTANGLE').map(n => ({ id: n.id, name: n.name, fills: n.fills.length, strokes: n.strokes.length }));`
  (switch to the Keys page first).

```js
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const set = await figma.getNodeByIdAsync('640:4373');
const hex = c => '#' + [c.r, c.g, c.b].map(x => Math.round(x * 255).toString(16).padStart(2, '0')).join('');
return set.children.map(v => {
  const bg = (v.fills && v.fills.length) ? v : v.findOne(n => n.type !== 'TEXT' && 'fills' in n && n.fills.length);
  const t = v.findOne(n => n.type === 'TEXT');
  const f = bg && bg.fills[0];
  return { id: v.id, name: v.name, bgNode: bg && bg.id, bg: f && f.type === 'SOLID' ? hex(f.color) + '@' + f.opacity : null,
           stroke: bg && bg.strokes[0] && bg.strokes[0].type === 'SOLID' ? hex(bg.strokes[0].color) : null, text: t && t.fills[0] ? hex(t.fills[0].color) : null };
});
```

Classify each existing variant. A white background (`#ffffff`, any opacity) maps to **White**.
Black or near-black (every channel below `#1a`) maps to **Black**. A colored background with
white text maps to **Dark**. A colored background with black text maps to **Light**. Write the
mapping in the ledger. If any variant doesn't fit one rule, stop and ask Andrew.

- [x] **Step 2: Write and run the component verification. It should fail.**

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const problems = [];
const styleName = async (n, kind) => { const id = n[kind === 'fill' ? 'fillStyleId' : 'strokeStyleId']; if (!id || typeof id !== 'string') return null; const s = await figma.getStyleByIdAsync(id); return s && s.name; };
// Binding 'strokeWeight' on a RECTANGLE is stored as four per-side bindings
// (strokeTopWeight/Right/Bottom/Left), not boundVariables.strokeWeight — accept those when all four agree.
const wName = async n => { const bv = n.boundVariables || {}; let b = bv.strokeWeight; if (!b) { const sides = ['strokeTopWeight','strokeRightWeight','strokeBottomWeight','strokeLeftWeight'].map(k => bv[k] && bv[k].id); if (sides[0] && sides.every(s => s === sides[0])) b = bv.strokeTopWeight; } if (!b) return null; const v = await figma.variables.getVariableByIdAsync(b.id); return v && v.name; };
// Line Sample
const ls = await figma.getNodeByIdAsync('472:867');
const LS_TIER = { Thin: 'weight/xs', Standard: 'weight/sm', Heavy: 'weight/md' };
for (const v of ls.children) {
  const n = v.findOne(x => x.type !== 'TEXT' && 'strokes' in x && x.strokes.length);
  const weight = v.variantProperties.Weight;
  if (await wName(n) !== LS_TIER[weight]) problems.push('Line Sample ' + v.name + ' weight');
  if (await styleName(n, 'stroke') !== 'charcoal/Base/100') problems.push('Line Sample ' + v.name + ' stroke style');
}
// Site Marker
const sm = await figma.getNodeByIdAsync('473:862');
for (const v of sm.children) {
  const shape = v.findOne(x => !x.id.startsWith('I') && x.type !== 'TEXT' && x.type !== 'INSTANCE' && 'fills' in x && x.fills.length);
  const want = v.variantProperties.Style === 'Numbered' ? 'charcoal/Shade/100' : 'charcoal/Base/100';
  if (await styleName(shape, 'fill') !== want) problems.push('Site Marker ' + v.name + ' fill');
  if (v.variantProperties.Style === 'Numbered') for (const t of v.findAll(x => x.type === 'TEXT')) { const f = t.fills[0]; if (!f || f.color.r < 0.99) problems.push('Site Marker ' + v.name + ' text not white'); }
  for (const x of v.findAll(x => !x.id.startsWith('I') && x.type !== 'INSTANCE' && 'strokes' in x && x.strokes.length && typeof x.strokeWeight === 'number')) if (!(await wName(x))) problems.push('Site Marker ' + v.name + ' stroke weight unbound');
}
// Legend Row Area
const lr = await figma.getNodeByIdAsync('480:889');
const area = lr.children.find(v => v.variantProperties['Swatch Type'] === 'Area');
const fillNode = area.findOne(x => x.type === 'RECTANGLE' && x.fills.length);
const strokeNode = area.findOne(x => x.type === 'RECTANGLE' && x.strokes.length) || fillNode;
if (await styleName(fillNode, 'fill') !== 'charcoal/Tint/100') problems.push('Legend Row Area fill');
if (await styleName(strokeNode, 'stroke') !== 'charcoal/Base/100') problems.push('Legend Row Area stroke');
if (!(await wName(strokeNode))) problems.push('Legend Row Area weight unbound');
// caption
const cap = await figma.getNodeByIdAsync('640:4373');
const combos = cap.children.map(v => v.variantProperties.Style + '/' + v.variantProperties.Size).sort();
const want = ['Black/LG','Black/SM','Dark/LG','Dark/SM','Light/LG','Light/SM','White/LG','White/SM'];
if (JSON.stringify(combos) !== JSON.stringify(want)) problems.push('caption variants ' + combos);
return { ok: problems.length === 0, problems };
```

Expected now: `ok: false`, with Line Sample, Site Marker, Legend Row, and caption problems.

- [x] **Step 3: Update `Line Sample`, `Site Marker`, and `Legend Row`.** Keys-page instances are
  pinned live (controller ruling 10), not from the Task 4 pins file. Each Keys build script
  snapshots every fill and stroke of every instance layer of the four sets before it mutates. After
  the mutation, it re-sets only the paints that actually changed, then re-checks that nothing still
  differs. Paste these two snippets where the scripts below say so. Other pages are restored in Step 6.

**Live pin snapshot** (paste after the page switch, before any mutation):

```js
const TARGETS = ['Line Sample','Site Marker','Legend Row','caption'];
const setOf = inst => { const mc = inst.mainComponent; if (!mc) return null; const s = mc.parent && mc.parent.type === 'COMPONENT_SET' ? mc.parent.name : mc.name; return TARGETS.includes(s) ? s : null; };
const strip = ps => JSON.stringify((Array.isArray(ps) ? ps : []).map(p => ({ t: p.type, c: p.color, o: p.opacity, b: p.boundVariables && p.boundVariables.color && p.boundVariables.color.id })));
const snap = []; const seen = new Set();
for (const inst of page.findAllWithCriteria({ types: ['INSTANCE'] })) {
  if (!setOf(inst)) continue;
  for (const n of [inst, ...inst.findAll(() => true)]) {
    if (seen.has(n.id)) continue; seen.add(n.id);
    if (!('fills' in n) && !('strokes' in n)) continue;
    snap.push({ n, fills: Array.isArray(n.fills) ? JSON.parse(JSON.stringify(n.fills)) : null, strokes: 'strokes' in n ? JSON.parse(JSON.stringify(n.strokes)) : null, sw: typeof n.strokeWeight === 'number' ? n.strokeWeight : null });
  }
}
```

**Live pin restore** (paste after the mutation; `residual` must be 0 and `swChanged` empty):

```js
const loadFonts = async n => { if (n.type === 'TEXT') for (const seg of n.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(seg.fontName); };
let restored = 0; const restoredIds = []; const swChanged = [];
for (const s of snap) {
  let changed = false;
  if (s.fills && strip(s.n.fills) !== strip(s.fills)) { await loadFonts(s.n); s.n.fills = s.fills; changed = true; }
  if (s.strokes && strip(s.n.strokes) !== strip(s.strokes)) { await loadFonts(s.n); s.n.strokes = s.strokes; changed = true; }
  if (s.sw !== null && typeof s.n.strokeWeight === 'number' && s.n.strokeWeight !== s.sw) swChanged.push(s.n.id);
  if (changed) { restored++; restoredIds.push(s.n.id); }
}
let residual = 0; // the strip() compare includes the bound variable id, so this also confirms restored bindings
for (const s of snap) if ((s.fills && strip(s.n.fills) !== strip(s.fills)) || (s.strokes && strip(s.n.strokes) !== strip(s.strokes))) residual++;
```

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
// Live pin snapshot here
const bindTier = (n, tier) => n.setBoundVariable('strokeWeight', W(tier));
const report = { line: 0, marker: 0, area: 0, unmatchedWeights: [] };
// Line Sample
const LS_TIER = { Thin: 'xs', Standard: 'sm', Heavy: 'md' };
for (const v of (await figma.getNodeByIdAsync('472:867')).children) {
  const n = v.findOne(x => x.type !== 'TEXT' && 'strokes' in x && x.strokes.length);
  await n.setStrokeStyleIdAsync(S('charcoal/Base/100').id); bindTier(n, LS_TIER[v.variantProperties.Weight]); report.line++;
}
// Site Marker
for (const v of (await figma.getNodeByIdAsync('473:862')).children) {
  const shape = v.findOne(x => !x.id.startsWith('I') && x.type !== 'TEXT' && x.type !== 'INSTANCE' && 'fills' in x && x.fills.length);
  const numbered = v.variantProperties.Style === 'Numbered';
  await shape.setFillStyleIdAsync(S(numbered ? 'charcoal/Shade/100' : 'charcoal/Base/100').id);
  if (numbered) for (const t of v.findAll(x => x.type === 'TEXT')) {
    for (const seg of t.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(seg.fontName);
    t.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
  }
  for (const x of v.findAll(x => !x.id.startsWith('I') && x.type !== 'INSTANCE' && 'strokes' in x && x.strokes.length && typeof x.strokeWeight === 'number')) {
    const tier = TIER_BY_WEIGHT[x.strokeWeight]; if (tier) bindTier(x, tier); else report.unmatchedWeights.push(v.name + ':' + x.strokeWeight);
  }
  report.marker++;
}
// Legend Row Area
const area = (await figma.getNodeByIdAsync('480:889')).children.find(v => v.variantProperties['Swatch Type'] === 'Area');
const fillNode = area.findOne(x => x.type === 'RECTANGLE' && x.fills.length);
const strokeNode = area.findOne(x => x.type === 'RECTANGLE' && x.strokes.length) || fillNode;
await fillNode.setFillStyleIdAsync(S('charcoal/Tint/100').id); await strokeNode.setStrokeStyleIdAsync(S('charcoal/Base/100').id);
const at = TIER_BY_WEIGHT[typeof strokeNode.strokeWeight === 'number' ? strokeNode.strokeWeight : 2] || 'sm'; bindTier(strokeNode, at); report.area = 1;
// Live pin restore here
return { ...report, snapshotLayers: snap.length, restored, residual, swChanged };
```

- [x] **Step 3b: Pin Legend Row at outer instances, keep charcoal main defaults** (fix round 1,
  revised ruling 11). Step 3's live snapshot also caught the Legend Row main's own nested
  instances. Line Sample `480:874` and Site Marker `480:881` sit inside the Legend Row main
  component, so Step 3 restored grey overrides there (`I480:874;472:852` `strokeStyleId`,
  `I480:881;473:854` `fillStyleId|fills`). New Legend Rows would then start grey. This script
  snapshots only the *outer* instances, clears the main's nested overrides (those two were the only
  overrides present on them, so `removeOverrides()` is safe), and pins at the outer layers.

```js
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const SET_IDS = ['472:867','473:862','480:889','640:4373'];
const inMainSet = n => { let p = n.parent; while (p && p.type !== 'PAGE') { if (SET_IDS.includes(p.id)) return true; p = p.parent; } return false; };
// Live pin snapshot here, with `if (inMainSet(inst)) continue;` added after the setOf() check
for (const id of ['480:874', '480:881']) (await figma.getNodeByIdAsync(id)).removeOverrides();
// Live pin restore here
return { snapshotLayers: snap.length, restored, residual, swChanged };
```

Then post-check every Keys pin from the Task 4 pins file against the live paint (type, color,
opacity, bound variable id). Pins inside the main sets are expected to differ, and all others must
match. Re-run the Step 2 verification as well.

- [x] **Step 4: Update `caption`.** Use the Step 1 mapping. `MAPPING` maps each existing variant
  ID to its new `Style` value. Keys-page caption instances are covered by the live pin snippets in
  this script, and other pages by Step 6. New variants are stacked under the White column and then
  laid out as a grid, one column per Style (Dark, White, Light, Black at x 0/200/400/600) and one
  row per Size (SM y 0, LG y 60). The set is then resized to fit with its original 37/25 px
  right/bottom margins.

```js
// Prelude A here
const MAPPING = { '640:4365': 'Dark', '640:4367': 'Dark', '640:4369': 'White', '640:4371': 'White' }; // Step 1 result (ledger)
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const set = await figma.getNodeByIdAsync('640:4373');
// Live pin snapshot here
const bgOf = v => (v.fills && v.fills.length) ? v : v.findOne(n => n.type !== 'TEXT' && 'fills' in n && n.fills.length);
const setText = async (v, c) => { for (const t of v.findAll(n => n.type === 'TEXT')) { for (const seg of t.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(seg.fontName); t.fills = [{ type: 'SOLID', color: c }]; } };
// 1. rename existing variants per mapping (instances follow, since the node ID is kept)
for (const [id, style] of Object.entries(MAPPING)) { const v = await figma.getNodeByIdAsync(id); const nm = `Style=${style}, Size=${v.variantProperties.Size}`; if (v.name !== nm) v.name = nm; }
// 2. White variants: outline -> charcoal/Base/100
for (const v of set.children.filter(v => v.variantProperties.Style === 'White')) await bgOf(v).setStrokeStyleIdAsync(S('charcoal/Base/100').id);
// 3. create any missing Style x Size combos by cloning that Size's White variant
const created = [];
for (const size of ['SM', 'LG']) {
  const base = set.children.find(v => v.variantProperties.Style === 'White' && v.variantProperties.Size === size);
  for (const style of ['Light', 'Dark', 'Black']) {
    if (set.children.find(v => v.variantProperties.Style === style && v.variantProperties.Size === size)) continue;
    const c = base.clone(); set.appendChild(c); c.name = `Style=${style}, Size=${size}`;
    const colKids = set.children.filter(v => v !== c && Math.abs(v.x - base.x) < 1);
    c.x = base.x; c.y = Math.max(...colKids.map(v => v.y + v.height)) + 24; // temporary; grid layout below
    const bg = bgOf(c); bg.strokes = [];
    if (style === 'Light') { await bg.setFillStyleIdAsync(S('charcoal/Tint/100').id); await setText(c, { r: 0, g: 0, b: 0 }); }
    if (style === 'Dark')  { await bg.setFillStyleIdAsync(S('charcoal/Shade/100').id); await setText(c, { r: 1, g: 1, b: 1 }); }
    if (style === 'Black') { await bg.setFillStyleIdAsync(''); bg.fills = [{ type: 'SOLID', color: { r: 0, g: 0, b: 0 } }]; await setText(c, { r: 1, g: 1, b: 1 }); }
    created.push(c.id);
  }
}
// 4. existing Light/Dark variants (if any were mapped as such): apply the role style
for (const v of set.children.filter(v => Object.keys(MAPPING).includes(v.id))) {
  if (v.variantProperties.Style === 'Light') await bgOf(v).setFillStyleIdAsync(S('charcoal/Tint/100').id);
  if (v.variantProperties.Style === 'Dark') await bgOf(v).setFillStyleIdAsync(S('charcoal/Shade/100').id);
}
// 5. grid layout: Style -> column, Size -> row; grow the (non-auto-layout) set to fit
const COLX = { Dark: 0, White: 200, Light: 400, Black: 600 }, ROWY = { SM: 0, LG: 60 };
for (const v of set.children) { v.x = COLX[v.variantProperties.Style]; v.y = ROWY[v.variantProperties.Size]; }
set.resizeWithoutConstraints(Math.max(...set.children.map(v => v.x + v.width)) + 37, Math.max(...set.children.map(v => v.y + v.height)) + 25);
// Live pin restore here
return { variants: set.children.map(v => v.name), created, snapshotLayers: snap.length, restored, residual, swChanged };
```

- [x] **Step 5: Re-run the Step 2 verification.** Expected: `ok: true`.

- [x] **Step 6: Restore pins on the other pages** (skip if Task 4 found none or Andrew chose
  accept). Run one call per page with pins, in parallel. Paste that page's `layers` array (only
  `id`, `fills`, `strokes` are used). Re-set a pinned paint only where the live paint now differs.

```js
const PAGE_PINS = []; // this page's layers array
const page = await figma.getNodeByIdAsync('PAGE_ID'); await figma.setCurrentPageAsync(page);
const strip = ps => JSON.stringify((Array.isArray(ps) ? ps : []).map(p => ({ t: p.type, c: p.color, o: p.opacity, b: p.boundVariables && p.boundVariables.color && p.boundVariables.color.id })));
const differs = (n, p) => (p.fills && strip(n.fills) !== strip(p.fills)) || (p.strokes && strip(n.strokes) !== strip(p.strokes));
let restored = 0, missing = 0, unchanged = 0;
for (const p of PAGE_PINS) {
  const n = await figma.getNodeByIdAsync(p.id); if (!n) { missing++; continue; }
  if (!differs(n, p)) { unchanged++; continue; }
  if (n.type === 'TEXT') for (const seg of n.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(seg.fontName);
  if (p.fills) n.fills = p.fills; if (p.strokes) n.strokes = p.strokes; restored++;
}
let residual = 0; for (const p of PAGE_PINS) { const n = await figma.getNodeByIdAsync(p.id); if (n && differs(n, p)) residual++; }
return { page: page.name, restored, unchanged, missing, residual };
```

Expected: `missing: 0` and `residual: 0` on every page. `restored + unchanged` equals that page's
Task 4 count.

- [x] **Step 7: Visual check.** Run `get_screenshot` on each of the four component set IDs. Confirm
  that the caption shows 8 variants with readable text, that Numbered markers have white numbers
  on dark fills, and that line samples still render.

- [x] **Step 8: Commit.**

```bash
git add site-plan/plans/2026-10-10-map-tokens-v2.md
git commit -m "Map tokens v2 Task 5: component bindings and caption styles"
```

---

### Task 6: Bind exact-match stroke weights on the Keys page

**Files:**
- Modify (Figma): Keys page `222:2275` nodes that are not inside instances
- Modify: this plan (ledger)

**Interfaces:**
- Consumes: Prelude A; Task 2 variables.
- Produces: strokes weighing exactly 1/2/3/4/6/8 bound to their tier. 1.5, 5, and mixed weights
  stay untouched and are listed for Task 9.

- [x] **Step 1: Write and run the count verification. It should fail.**

```js
// Prelude A here
// Per-side bindings on rectangles/frames are stored as stroke{Top,Right,Bottom,Left}Weight (Ruling 13)
const isWeightBound = n => { const b = n.boundVariables || {}; return !!(b.strokeWeight || (b.strokeTopWeight && b.strokeRightWeight && b.strokeBottomWeight && b.strokeLeftWeight)); };
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const nodes = page.findAll(n => !n.id.startsWith('I') && 'strokes' in n && n.strokes.length);
const unboundExact = nodes.filter(n => typeof n.strokeWeight === 'number' && TIER_BY_WEIGHT[n.strokeWeight] && !isWeightBound(n));
const byWeight = {}; for (const n of nodes) { const k = typeof n.strokeWeight === 'number' ? n.strokeWeight : 'mixed'; byWeight[k] = (byWeight[k] || 0) + 1; }
return { ok: unboundExact.length === 0, unboundExact: unboundExact.length, byWeight };
```

Expected now: `ok: false`. Record `byWeight` in the ledger as the "before" counts.

- [x] **Step 2: Run the build.**

```js
// Prelude A here
// Per-side bindings on rectangles/frames are stored as stroke{Top,Right,Bottom,Left}Weight (Ruling 13)
const isWeightBound = n => { const b = n.boundVariables || {}; return !!(b.strokeWeight || (b.strokeTopWeight && b.strokeRightWeight && b.strokeBottomWeight && b.strokeLeftWeight)); };
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
let bound = 0; const skipped = { mixed: [], unmatched: [] };
for (const n of page.findAll(n => !n.id.startsWith('I') && 'strokes' in n && n.strokes.length)) {
  if (isWeightBound(n)) continue;
  if (typeof n.strokeWeight !== 'number') { skipped.mixed.push(n.id); continue; }
  const tier = TIER_BY_WEIGHT[n.strokeWeight];
  if (!tier) { skipped.unmatched.push(n.id + '@' + n.strokeWeight); continue; }
  n.setBoundVariable('strokeWeight', W(tier)); bound++;
}
return { bound, skipped };
```

- [x] **Step 3: Re-run the Step 1 verification.** Expected: `ok: true`, and `byWeight` identical to
  the "before" counts (binding changed no values). Record the "after" counts and the skipped lists
  in the ledger.

- [x] **Step 4: Commit.**

```bash
git add site-plan/plans/2026-10-10-map-tokens-v2.md
git commit -m "Map tokens v2 Task 6: bind exact-match stroke weights on Keys"
```

---

### Task 7: Styles page — tokens, fill styles, stroke, and line treatments

> **Superseded in part (2026-10-11):** v3 Task 5 (site-plan/plans/2026-10-11-map-tokens-v3.md) renamed the Semantic Tokens title to "Color Roles" and rebuilt the Stroke frame (Fine/Medium/Coarse dashes, casing row, region recipe). Don't run Steps 1 and 4 below as written — they rebuild the old v2 Stroke frame. To refresh the page: run Steps 2–3 here, then v3 Task 5 Steps 2–4.

**Files:**
- Modify (Figma): Styles page `699:2080`, section `701:2`. Rebuild
  `Color Documentation — Semantic Tokens`. Add `Fill Styles Documentation` and
  `Stroke Documentation`. Move `Typography Documentation`.
- Modify: this plan (ledger)

**Interfaces:**
- Consumes: Preludes A and B; Tasks 1–3 tokens.
- Produces: frame order at y=64 is Ramps x=64, Semantic Tokens x=1632, Fill Styles x=3200,
  Stroke x=4768, Typography x=6336.

- [x] **Step 1: Write and run the page verification. It should fail.**

```js
const page = await figma.getNodeByIdAsync('699:2080'); await figma.setCurrentPageAsync(page);
const sec = await figma.getNodeByIdAsync('701:2');
const want = [['Color Documentation — Ramps',64],['Color Documentation — Semantic Tokens',1632],['Fill Styles Documentation',3200],['Stroke Documentation',4768],['Typography Documentation',6336]];
const problems = [];
for (const [n, x] of want) { const f = sec.children.find(c => c.name === n); if (!f) problems.push('missing ' + n); else if (Math.round(f.x) !== x) problems.push(n + ' x=' + Math.round(f.x)); }
const sem = sec.children.find(c => c.name === 'Color Documentation — Semantic Tokens');
if (sem) for (const g of ['Tint','Base','Shade']) if (!sem.findOne(n => n.name === 'Section — Map Overlay ' + g)) problems.push('semantic group ' + g);
const fs = sec.children.find(c => c.name === 'Fill Styles Documentation');
if (fs && fs.findAll(n => n.name.startsWith('Style — ')).length !== 50) problems.push('fill style cells');
const st = sec.children.find(c => c.name === 'Stroke Documentation');
if (st && st.findAll(n => n.type === 'VECTOR' && n.name.includes(' · ')).length !== 54) problems.push('line treatment samples');
return { ok: problems.length === 0, problems };
```

Expected now: `ok: false` (missing frames, no Base group).

- [x] **Step 2: Rebuild Semantic Tokens.**

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('699:2080'); await figma.setCurrentPageAsync(page);
// Prelude B here
const f = docFrame('Color Documentation — Semantic Tokens', 'Semantic Color Tokens', 'Aliases that map keys and charts bind to. Each hue has three roles: Tint (light-theme fills, black text), Base (lines and textless markers), and Shade (dark-theme fills, white text). Every Color Roles token has a solid paint style; Tint also has 50% and 25% styles for translucent overlays.', 1632);
note(f, 'Contrast audit', 'Tint picks pass WCAG AA normal text with black (6.1–15.8:1); Shade passes with white (9.1–10.4:1); Base (step 500) is borderline either way (4.0–5.2:1) and is for textless use. Every Shade is validated >=3:1 against the sampled aerial tone (#afaba4). All ramps fail AA-large on dark backgrounds, which matters only if reused on the dark-mode microsite. Amber Tint uses step 300 so it separates from coral/200 by lightness. Spec: site-plan/specs/2026-10-10-map-tokens-v2-design.md. Tint 50 and Tint 25 paint styles hold copied raw colors and need a re-sync after color changes — see the Fill Styles frame.');
function card(body, name, swatches, sub) {
  const c = figma.createAutoLayout('HORIZONTAL', { name, itemSpacing: 24 }); body.appendChild(c); c.resize(864, 80); c.primaryAxisSizingMode = 'FIXED'; c.counterAxisSizingMode = 'AUTO';
  c.paddingTop = c.paddingBottom = c.paddingLeft = c.paddingRight = 16; c.counterAxisAlignItems = 'CENTER'; c.cornerRadius = 13; c.fills = solid(CARD);
  const sws = figma.createAutoLayout('HORIZONTAL', { name: 'Swatches', itemSpacing: 8 }); c.appendChild(sws); sws.fills = [];
  const made = []; for (const v of swatches) { const s = figma.createFrame(); s.name = 'Swatch'; sws.appendChild(s); s.resize(48, 48); s.cornerRadius = 8; s.fills = bound(v); made.push(s); }
  const info = figma.createAutoLayout('VERTICAL', { name: 'Info', itemSpacing: 2 }); c.appendChild(info); info.fills = [];
  txt(info, name, { style: 'Medium' }); txt(info, sub, { size: 11, color: GREY, family: 'JetBrains Mono' });
  return made;
}
const GROUP_DESC = {
  Tint: 'Per-hue step chosen from Sector Analysis. Light-theme fills; black text passes (6.1–15.8:1).',
  Base: 'Step 500. Lines, strokes, and markers without text. Borderline for text either way.',
  Shade: 'Step 700. Dark-theme fills and strong outlines; white text passes (9.1–10.4:1).'
};
let cards = 0;
for (const role of ROLES) {
  const body = row(f, 'Section — Map Overlay ' + role, 'Color Roles — ' + role, GROUP_DESC[role]);
  for (const h of HUES) {
    const v = V('Color Roles', `${h}/${role}`), step = STEP(h, role);
    const roleStyles = STYLE_SET.filter(([hh, rr]) => hh === h && rr === role);
    const styleOk = roleStyles.every(([hh, rr, o]) => S(`${hh}/${rr}/${o}`));
    const label = role === 'Tint' ? 'styles /100 /50 /25' : 'style /100';
    card(body, v.name, [v], `→ ${h}/${step}  ·  ${hex(rampColor(h, step))}  ·  ${label}${styleOk ? '' : ' —'}`); cards++;
  }
}
const cc = col('Chart Categorical'); const L = cc.modes.find(m => m.name === 'Light'), D = cc.modes.find(m => m.name === 'Dark');
const body = row(f, 'Section — Chart Categorical', 'Chart Categorical', 'Seven slots for the HTML dataviz reports in pdc-pro-2026. Each card shows Light then Dark. Order is validated for color-vision-deficiency adjacency — don’t reorder.');
for (const id of cc.variableIds) {
  const v = await figma.variables.getVariableByIdAsync(id);
  const al = await figma.variables.getVariableByIdAsync(v.valuesByMode[L.modeId].id), ad = await figma.variables.getVariableByIdAsync(v.valuesByMode[D.modeId].id);
  const [sl, sd] = card(body, v.name, [v, v], `Light → ${al.name}  ·  Dark → ${ad.name}`);
  sl.setExplicitVariableModeForCollection(cc, L.modeId); sd.setExplicitVariableModeForCollection(cc, D.modeId); cards++;
}
return { frameId: f.id, cards };
```

Expected: `cards: 37`.

- [x] **Step 3: Build Fill Styles.**

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('699:2080'); await figma.setCurrentPageAsync(page);
// Prelude B here
const f = docFrame('Fill Styles Documentation', 'Fill Styles', '50 paint styles, five per hue: Shade, Base, and Tint as solid fills (captions, sector overlays, lines), plus Tint at 50% and 25% for translucent map overlays. The solid styles are bound to their Color Roles variable. Tint 50 and Tint 25 hold a copied raw color, because Figma overwrites a variable-bound paint’s opacity — re-sync them after any ramp or Color Roles change (plan Task 3).', 3200);
let cells = 0;
for (const h of HUES) {
  const body = row(f, 'Section Fill Styles — ' + h, h[0].toUpperCase() + h.slice(1), `${h}/{Shade,Base,Tint}/100 + Tint/{50,25}`);
  const grid = figma.createAutoLayout('HORIZONTAL', { name: 'Grid', itemSpacing: 32 }); body.appendChild(grid); grid.fills = [];
  for (const role of ['Shade', 'Base', 'Tint']) {
    const grp = figma.createAutoLayout('HORIZONTAL', { name: role, itemSpacing: 8 }); grid.appendChild(grp); grp.fills = [];
    for (const [, , o] of STYLE_SET.filter(([hh, rr]) => hh === h && rr === role)) {
      const cell = figma.createAutoLayout('VERTICAL', { name: `Style — ${h}/${role}/${o}`, itemSpacing: 4 }); grp.appendChild(cell); cell.fills = [];
      // No background (2026-10-12): swatches never sit on the aerial tone in practice, so it skewed how they read.
      const bg = figma.createFrame(); bg.name = 'Swatch container'; cell.appendChild(bg); bg.resize(56, 48); bg.cornerRadius = 4; bg.fills = [];
      const sw = figma.createRectangle(); sw.name = 'Swatch'; bg.appendChild(sw); sw.resize(56, 48); sw.x = 0; sw.y = 0; sw.cornerRadius = 2;
      await sw.setFillStyleIdAsync(S(`${h}/${role}/${o}`).id);
      txt(cell, `${role} ${o}`, { size: 11, color: GREY });
      cells++;
    }
  }
}
return { frameId: f.id, cells };
```

Expected: `cells: 50`.

- [x] **Step 4: Build Stroke (weights plus line treatments).**

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('699:2080'); await figma.setCurrentPageAsync(page);
// Prelude B here
const f = docFrame('Stroke Documentation', 'Stroke', 'Stroke weights from the Stroke collection, and line treatments. Dash patterns and line ends can’t be variables or styles, so the Line Treatments grid is their canonical record: copy properties from a sample (⌥⌘C), paste them onto a map path (⌥⌘V), then pick a color style.', 4768);
const strokeStyle = S('charcoal/Base/100').id;
async function line(parent, name, len, dash, caps, tier) {
  const box = figma.createFrame(); box.name = 'Sample'; parent.appendChild(box); box.resize(len, 48); box.fills = []; box.clipsContent = false;
  const v = figma.createVector(); v.name = name; box.appendChild(v);
  await v.setVectorNetworkAsync({ vertices: [{ x: 0, y: 0, strokeCap: caps[0] }, { x: len - 16, y: 0, strokeCap: caps[1] }], segments: [{ start: 0, end: 1 }], regions: [] });
  v.x = 8; v.y = 24; v.dashPattern = dash;
  await v.setStrokeStyleIdAsync(strokeStyle); v.setBoundVariable('strokeWeight', W(tier));
  return v;
}
// Weights
const wb = row(f, 'Section — Weights', 'Weights', 'Six tiers. Bind a stroke’s weight to a tier instead of typing a number, so retuning a tier updates every map.');
for (const [t, w] of TIERS) {
  const c = figma.createAutoLayout('HORIZONTAL', { name: 'weight/' + t, itemSpacing: 24 }); wb.appendChild(c); c.resize(864, 80); c.primaryAxisSizingMode = 'FIXED'; c.counterAxisSizingMode = 'AUTO';
  c.paddingTop = c.paddingBottom = c.paddingLeft = c.paddingRight = 16; c.counterAxisAlignItems = 'CENTER'; c.cornerRadius = 13; c.fills = solid(CARD);
  await line(c, `Weight ${t} (${w})`, 120, [], ['NONE', 'NONE'], t);
  const info = figma.createAutoLayout('VERTICAL', { name: 'Info', itemSpacing: 2 }); c.appendChild(info); info.fills = [];
  txt(info, 'weight/' + t, { style: 'Medium' }); txt(info, `${w}px  ·  STROKE_FLOAT`, { size: 11, color: GREY, family: 'JetBrains Mono' });
}
// Line treatments
const DASH = { Solid: [], Coarse: [8, 8], Fine: [2, 2] };
const CAP = { None: ['NONE', 'NONE'], Single: ['NONE', 'ARROW_LINES'], Double: ['ARROW_LINES', 'ARROW_LINES'] };
const tb = row(f, 'Section — Line Treatments', 'Line Treatments', 'Every Dash × Cap combination at every weight tier, stroked charcoal/Base/100. Dash lengths are fixed, so Fine reads as dots at the heaviest tiers.', 16);
let samples = 0;
for (const [d, dash] of Object.entries(DASH)) for (const [c, caps] of Object.entries(CAP)) {
  const r = figma.createAutoLayout('HORIZONTAL', { name: `${d} · ${c}`, itemSpacing: 16 }); tb.appendChild(r); r.counterAxisAlignItems = 'CENTER'; r.fills = [];
  txt(r, `${d}${dash.length ? ' [' + dash.join(',') + ']' : ''} · ${c}`, { size: 11, family: 'JetBrains Mono', width: 160 });
  for (const [t, w] of TIERS) {
    const cell = figma.createAutoLayout('VERTICAL', { name: t, itemSpacing: 2 }); r.appendChild(cell); cell.fills = [];
    await line(cell, `${d}${dash.length ? ' [' + dash.join(',') + ']' : ''} · ${c} · ${t} (${w})`, 96, dash, caps, t);
    txt(cell, `${t} (${w})`, { size: 10, color: GREY }); samples++;
  }
}
note(f, 'Paste-properties binding test', 'Not yet run. See Task 7 Step 6 of site-plan/plans/2026-10-10-map-tokens-v2.md.');
return { frameId: f.id, samples };
```

Expected: `samples: 54`.

- [x] **Step 5: Move Typography, fit the section, and screenshot.**

```js
const page = await figma.getNodeByIdAsync('699:2080'); await figma.setCurrentPageAsync(page);
const s = await figma.getNodeByIdAsync('701:2');
const typo = s.children.find(c => c.name === 'Typography Documentation'); typo.x = 6336; typo.y = 64;
const right = Math.max(...s.children.map(k => k.x + k.width)), bottom = Math.max(...s.children.map(k => k.y + k.height));
s.resizeWithoutConstraints(right + 64, bottom + 64);
await s.screenshot({ scale: 0.15 });
return { w: Math.round(s.width), h: Math.round(s.height), frames: s.children.map(k => k.name + ' @' + Math.round(k.x)) };
```

Then re-run the Step 1 verification. Expected: `ok: true`. Record the frame IDs in the ledger.

- [ ] **Step 6: Paste-properties binding test (manual, Andrew).** In Figma:
  1. Select the `Medium [8,8] · Single · lg (4)` sample.
  2. Copy properties (⌥⌘C).
  3. Paste properties (⌥⌘V) onto any scratch path.
  4. In the right panel, check whether the stroke weight shows the `weight/lg` variable chip and
     the stroke shows the `charcoal/Base/100` style.

  Then delete the scratch path. Record the result in the ledger, and have Claude update the
  `Note — Paste-properties binding test` text to "Tested 2026-MM-DD: bindings
  [carry over | do not carry over]".

- [x] **Step 7: Commit.**

```bash
git add site-plan/plans/2026-10-10-map-tokens-v2.md
git commit -m "Map tokens v2 Task 7: Styles page tokens, fill styles, stroke"
```

---

### Task 8: Comparison frame — amber replaces the duplicate cobalt row

**Files:**
- Modify (Figma): `sector-analysis-comparison` `724:4690` (Keys)

**Interfaces:**
- Consumes: Prelude A; Task 1 variables.
- Produces: the bottom row (y=837 in each column) bound to `amber/Shade`, `amber/Tint`, and
  `amber/Base`.

- [x] **Step 1: Write and run the verification. It should fail.**

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const fr = await figma.getNodeByIdAsync('724:4690');
const byId = Object.fromEntries(colorVars.map(v => [v.id, v.name]));
const last = fr.findAll(n => 'fills' in n && Array.isArray(n.fills) && n.fills[0] && Math.round(n.y) === 837);
const names = last.map(n => byId[n.fills[0].boundVariables && n.fills[0].boundVariables.color && n.fills[0].boundVariables.color.id]);
return { ok: names.length > 0 && names.every(n => n && n.startsWith('amber/')), names };
```

Expected now: `ok: false`, names like `cobalt/400`, `cobalt/50`, `cobalt/Base`.

- [x] **Step 2: Run the build.** The left column is Shade, the middle is the Sector Analysis pick
  (now Tint), and the right is the former Tint (now Base). Detect the column from the current
  binding.

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const fr = await figma.getNodeByIdAsync('724:4690');
const byId = Object.fromEntries(colorVars.map(v => [v.id, v.name]));
const TARGET = { 'cobalt/400': 'amber/Shade', 'cobalt/50': 'amber/Tint', 'cobalt/Base': 'amber/Base' };
let changed = 0;
for (const n of fr.findAll(n => 'fills' in n && Array.isArray(n.fills) && n.fills[0] && Math.round(n.y) === 837)) {
  const cur = byId[n.fills[0].boundVariables && n.fills[0].boundVariables.color && n.fills[0].boundVariables.color.id];
  const to = TARGET[cur]; if (!to) continue;
  n.fills = [figma.variables.setBoundVariableForPaint(n.fills[0], 'color', V('Color Roles', to))]; changed++;
}
await fr.screenshot();
return { changed };
```

- [x] **Step 3: Re-run the verification.** Expected: `ok: true`.

- [x] **Step 4: Commit.**

```bash
git add site-plan/plans/2026-10-10-map-tokens-v2.md
git commit -m "Map tokens v2 Task 8: amber row in sector comparison"
```

---

### Task 9: Manual follow-up checklist and close-out

**Files:**
- Modify: this plan (append the checklist under "Manual follow-ups")
- Modify: `site-plan/specs/2026-10-10-map-tokens-v2-design.md` (Status line)
- Modify: `/Users/andrewkeser/.claude/projects/-Users-andrewkeser-Code-keser-permaculture-site-plan/memory/figma_styles_page_sync.md`
  (add the new frames)

**Interfaces:**
- Consumes: Prelude A; results of all previous tasks.
- Produces: node-ID checklists for Andrew's three design calls.

- [x] **Step 1: Generate the checklists (read-only, Keys page).**

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const byId = Object.fromEntries(colorVars.map(v => [v.id, v.name]));
// Instance sublayers are included on purpose: most real colors on Keys are Legend Row overrides.
// Label each with its outermost INSTANCE and the key frame directly under the page.
const where = n => { let outer = null, p = n.parent, q = n; while (p && p.type !== 'PAGE') { if (p.type === 'INSTANCE') outer = p; q = p; p = p.parent; } return `${outer ? 'in instance ' + outer.id + ' ' + outer.name + ', ' : ''}frame ${q.name}`; };
const base = [], shadeStrokes = [], oddWeights = [];
for (const n of page.findAll(n => 'fills' in n || 'strokes' in n)) {
  for (const p of (Array.isArray(n.fills) ? n.fills : [])) { const nm = byId[p.boundVariables && p.boundVariables.color && p.boundVariables.color.id]; if (nm && nm.endsWith('/Base')) base.push(`${n.id} · ${nm} · ${n.name} (${where(n)})`); }
  for (const p of (n.strokes || [])) { const nm = byId[p.boundVariables && p.boundVariables.color && p.boundVariables.color.id]; if (nm && nm.endsWith('/Shade')) shadeStrokes.push(`${n.id} · ${nm} · ${n.name} (${where(n)})`); }
  if (n.strokes && n.strokes.length && (n.strokeWeight === 1.5 || n.strokeWeight === 5)) oddWeights.push(`${n.id} · ${n.strokeWeight} · ${n.name} (${where(n)})`);
}
return { base, shadeStrokes, oddWeights };
```

- [x] **Step 2: Append the three lists** under "Manual follow-ups" below, as `- [ ]` items grouped
  by heading. Fill in the "Generated" line.
- [x] **Step 3: Update the spec Status line** to: `Status: built YYYY-MM-DD — see
  site-plan/plans/2026-10-10-map-tokens-v2.md; manual follow-ups open.`
- [x] **Step 4: Update the memory note** `figma_styles_page_sync.md`. Add the Fill Styles and
  Stroke frames, and the rule that a token change means re-running Task 7.
- [x] **Step 5: Commit, then ask Andrew before pushing.**

```bash
git add site-plan/plans/2026-10-10-map-tokens-v2.md site-plan/specs/2026-10-10-map-tokens-v2-design.md
git commit -m "Map tokens v2 Task 9: follow-up checklists, mark spec built"
```

---

## Open decisions (Andrew)

- **~~Ruling 14: /25 and /50 fill styles render opaque~~ — resolved 2026-10-11 (option b).** Figma writes
  a bound color variable's alpha into the paint's opacity on bind, on style apply, and on variable
  change, so variable-bound /25 and /50 styles rendered at 100%. Andrew confirmed it in the UI, and
  confirmed that setting fill opacity by hand either fades the stroke (layer opacity) or detaches the
  style. Chosen: **/25 and /50 styles hold a raw copied color**; /100 stays variable-bound. Option (a),
  60 RGBA variables, was rejected (**reversed 2026-10-25**: the 20 remaining styles now bind
  `alpha/<hue>-<step>-<25|50>` Ramps copies; see the v2 design spec): those variables would be static copies too, so it needs the same
  re-sync step plus 60 extra variables. Upkeep: the Task 3 re-sync rule and drift check. On 2026-10-11 the set was trimmed to 50 styles: only Tint is used translucent, so the 40 Shade/Base 25/50 styles were deleted (no layer used them).
- **Paste-properties binding test (Task 7 Step 6): not yet run.** Steps are in Task 7 Step 6 above. Until it runs, the Styles page note stays "Not yet run".
- **Captions on maps use a remote library caption set (`238:4172`)**, not the local `caption` (`640:4373`) updated in Task 5. Local caption changes reach no current instance until instances are swapped.
- **Comparison frame swatch `724:4692`** (y=0, fourth column) is bound to `amber/Shade`. It read `violet/Tint` (now `violet/Base`) on 2026-10-10 and no task script touched it, so it is likely your own edit. Confirm.
- **New Legend Row instances** now default to charcoal lines and markers (Task 5 fix). Existing rows kept their colors as instance overrides.

## Manual follow-ups (Andrew)

Generated: 2026-10-11 — includes instance sublayers (read-only script over the Keys page `222:2275`; every item sits in the `Components` frame). Without instance sublayers the counts would be 27 / 2 / 20; with them 28 / 38 / 20.

- **Base fills that could become Tint** (former Tint, step 500, to the lighter pick): 28 nodes (27 direct, 1 instance sublayer). Only one is a real decision; the other 27 are annotated "keep Base".
  - **Real open decision (1):**
    - [ ] `I487:902;480:881;641:1230` amber/Base Triangle (instance 487:902 Legend Row). Keep Base or move to Tint?
  - **Keep Base: Site Marker main-component fills (8).** Spec §4 assigns Dot/Icon markers Base.
  - [ ] `473:857` charcoal/Base Ellipse
  - [ ] `473:861` charcoal/Base Ellipse
  - [ ] `641:1213` charcoal/Base Square
  - [ ] `641:1218` charcoal/Base Triangle
  - [ ] `641:1223` charcoal/Base Hexagon
  - [ ] `641:1227` charcoal/Base Square
  - [ ] `641:1230` charcoal/Base Triangle
  - [ ] `641:1233` charcoal/Base Hexagon
  - **Keep Base: `sector-analysis-comparison` swatches (19).** This column demonstrates the former-Tint/Base values.
  - [ ] `724:4669` violet/Base
  - [ ] `724:4670` teal/Base
  - [ ] `724:4671` magenta/Base
  - [ ] `724:4672` slate/Base
  - [ ] `724:4673` cobalt/Base
  - [ ] `724:4674` coral/Base
  - [ ] `724:4675` charcoal/Base
  - [ ] `724:4676` gold/Base
  - [ ] `724:4677` sage/Base
  - [ ] `724:4678` amber/Base
  - [ ] `724:4693` teal/Base
  - [ ] `724:4694` magenta/Base
  - [ ] `724:4695` slate/Base
  - [ ] `724:4696` cobalt/Base
  - [ ] `724:4697` coral/Base
  - [ ] `724:4698` charcoal/Base
  - [ ] `724:4699` gold/Base
  - [ ] `724:4700` sage/Base
  - [ ] `724:4701` amber/Base
- **Shade strokes that should become Base:** the spec's count of 41 included main-component strokes that Task 5 moved to `charcoal/Base` per spec §4, leaving 38 overrides to review. 38 nodes (2 direct, 36 Legend Row instance sublayers)
  - Direct:
    - [ ] `497:4422` slate/Shade
    - [ ] `709:4550` slate/Shade
  - Instance sublayers, grouped by the Legend Row instance's ID prefix. The main-component sublayers (`640:1176`, `480:874;472:852`) are where a change cascades to rows that do not override it, but these rows DO override, so each is its own decision.
  - Legend Row instances under `494:*` (11)
    - [ ] `I494:969;640:1176` sage/Shade
    - [ ] `I494:976;480:874;472:852` teal/Shade
    - [ ] `I494:983;480:874;472:852` sage/Shade
    - [ ] `I494:990;480:874;472:852` cobalt/Shade
    - [ ] `I494:997;480:874;472:852` violet/Shade
    - [ ] `I494:1004;640:1176` sage/Shade
    - [ ] `I494:1010;640:1176` sage/Shade
    - [ ] `I494:1016;480:874;472:852` cobalt/Shade
    - [ ] `I494:1023;480:874;472:852` violet/Shade
    - [ ] `I494:1030;480:874;472:852` gold/Shade
    - [ ] `I494:1037;480:874;472:852` magenta/Shade
  - Legend Row instances under `495:*` (6)
    - [ ] `I495:4209;640:1176` sage/Shade
    - [ ] `I495:4215;640:1176` sage/Shade
    - [ ] `I495:4221;640:1176` sage/Shade
    - [ ] `I495:4227;640:1176` sage/Shade
    - [ ] `I495:4233;480:874;472:852` cobalt/Shade
    - [ ] `I495:4240;480:874;472:852` magenta/Shade
  - Legend Row instances under `496:*` (11)
    - [ ] `I496:1071;640:1176` sage/Shade
    - [ ] `I496:1093;640:1176` sage/Shade
    - [ ] `I496:1107;640:1176` sage/Shade
    - [ ] `I496:1113;480:874;472:852` cobalt/Shade
    - [ ] `I496:1128;640:1176` sage/Shade
    - [ ] `I496:1134;480:874;472:864` cobalt/Shade
    - [ ] `I496:1150;640:1176` sage/Shade
    - [ ] `I496:1156;640:1176` sage/Shade
    - [ ] `I496:1162;640:1176` sage/Shade
    - [ ] `I496:1168;480:874;472:852` cobalt/Shade
    - [ ] `I496:1175;480:874;472:852` magenta/Shade
  - Legend Row instances under `487:*` (6)
    - [ ] `I487:867;640:1176` sage/Shade
    - [ ] `I487:873;640:1176` sage/Shade
    - [ ] `I487:879;640:1176` sage/Shade
    - [ ] `I487:913;640:1176` sage/Shade
    - [ ] `I487:919;640:1176` sage/Shade
    - [ ] `I487:925;640:1176` sage/Shade
  - Legend Row instances under `489:*` (2)
    - [ ] `I489:934;640:1176` sage/Shade
    - [ ] `I489:940;640:1176` sage/Shade
- **1.5 to 1 or 2, and 5 to 4 or 6:** 20 nodes (1.5px: 7, 5px: 13; none are instance sublayers)
  - [ ] `640:4369` 1.5px, Style=White, Size=SM
  - [ ] `640:4371` 1.5px, Style=White, Size=LG
  - [ ] `497:4398` 5px, Vector 2
  - [ ] `497:4405` 5px, Vector 2
  - [ ] `497:4361` 5px, Vector 2
  - [ ] `497:4368` 5px, Vector 2
  - [ ] `497:4462` 5px, Vector 2
  - [ ] `497:4518` 5px, Vector 2
  - [ ] `497:4525` 5px, Vector 2
  - [ ] `497:4532` 5px, Vector 2
  - [ ] `497:4539` 5px, Vector 2
  - [ ] `497:4601` 1.5px, waypoint: Front / driveway-side yard
  - [ ] `497:4608` 1.5px, goal-marker: ChipDrop drop-off
  - [ ] `497:4615` 1.5px, goal-marker: pawpaw understory + mushroom cultivation
  - [ ] `497:4622` 1.5px, waste-pit
  - [ ] `497:4629` 1.5px, goal-marker: compost system
  - [ ] `709:4528` 5px, line
  - [ ] `709:4531` 5px, line
  - [ ] `709:4542` 5px, line
  - [ ] `709:4544` 5px, line
