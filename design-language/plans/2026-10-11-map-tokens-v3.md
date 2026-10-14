# Map Tokens v3 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Also load the `figma:figma-use` skill before any `use_figma` call.

**Goal:** Rename `Map Overlay` to `Color Roles`, add casing-line effect styles, extend `Line Sample`
(Fine/Medium/Coarse dashes, a Bold weight, a Casing axis), clean up `Site Marker` and `caption`,
update the Styles page, and generate Andrew's migration checklist. No existing map should change
appearance.

**Architecture:** Same as v2. All work happens in the PDC Pro Vision Figma file through `use_figma`.
This plan file is the repo artifact: its checkboxes and **State ledger** record progress and IDs.
Each task:

1. Run a read-only verification and see it fail.
2. Run the build.
3. Re-run the verification and see it pass.
4. Record results in the ledger and commit.

**Tech Stack:** Figma Plugin API via the Figma MCP `use_figma` tool (`skillNames: "figma-use"`);
`get_screenshot` for visual checks; git for plan-file commits.

**Spec:** [`site-plan/specs/2026-10-11-map-tokens-v3-design.md`](../specs/2026-10-11-map-tokens-v3-design.md)
(extends [`2026-10-10-map-tokens-v2-design.md`](../specs/2026-10-10-map-tokens-v2-design.md)).

## Global Constraints

- File key: `aF9SVeTLwFN8PCEiU2OSBQ`. Pages: Keys `222:2275`, Styles `699:2080`. Styles section
  `701:2`.
- **One page per `use_figma` call**; switch with `await figma.setCurrentPageAsync(page)` at most once.
- **Never edit** the Base Map or Sector Analysis pages. Read-only access is fine.
- **Collection names after Task 1:** `Ramps`, `Color Roles` (formerly `Map Overlay`), `Chart
  Categorical`, `Stroke`. Variable names inside `Color Roles` stay `<hue>/{Shade,Base,Tint}`.
- **Fill styles:** 50, per hue `Shade/100`, `Base/100`, `Tint/100`, `Tint/50`, `Tint/25`
  (unchanged by this plan). Translucent fills are always Tint at 25 or 50%.
- **Casing effect styles:** `<hue>/Casing`, one `DROP_SHADOW`, offset (0, 4), radius 1, spread 0,
  blend `NORMAL`, color bound to `Color Roles` `<hue>/Shade`, alpha 1.
- **Dash set:** Fine `[2,2]`, Medium `[8,8]`, Coarse `[16,9]` (plus Solid `[]`).
- **Line Sample weights:** Thin = `weight/xs`, Standard = `weight/sm`, Heavy = `weight/md`,
  Bold = `weight/xl` (was `weight/lg` until 2026-10-13).
- **Default hue** for main components: `charcoal`.
- **No variant axis is removed.** Renamed variant values keep their component node, so instances
  follow.
- **No existing instance may change appearance:** Keys-page component edits use Prelude C's
  snapshot/restore and must report `residual: 0`.
- **Known Figma behaviors (from v2):**
  - `setBoundVariableForPaint` / variable resolution overwrite a paint's opacity with the variable's
    alpha. Never rely on paint opacity on a variable-bound paint.
  - Rectangles and frames store a stroke-weight binding per side (`strokeTopWeight`…).
- **Every build script is idempotent:** it checks names before creating, renaming, or cloning.
- **Git safety (absolute):** never run `git reset`, `git checkout -- <path>`, `git restore`,
  `git stash`, or `git clean`. Fix mistakes forward. Edit plan/spec files with exact-string edits,
  never whole-file scripted rewrites. Stage files by explicit path; never stage `CLAUDE.md` or
  `site-plan/3d/`.

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
const ROLES_COL = 'Color Roles';
const effectStyles = await figma.getLocalEffectStylesAsync();
const CASING = h => (effectStyles.find(s => s.name === h + '/Casing') || null);
```

### Prelude B — Styles-page doc helpers (paste after Prelude A in Task 5 scripts)

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

### Prelude C — instance snapshot/restore (paste in Tasks 3 and 4, after the Keys page switch)

```js
const PIN_SETS = ['Line Sample', 'Site Marker', 'Legend Row', 'caption'];
const setOf = async inst => { const mc = await inst.getMainComponentAsync(); if (!mc) return null; const s = mc.parent && mc.parent.type === 'COMPONENT_SET' ? mc.parent.name : mc.name; return PIN_SETS.includes(s) ? s : null; };
const sig = ps => JSON.stringify((Array.isArray(ps) ? ps : []).map(p => ({ t: p.type, c: p.color, o: p.opacity, x: p.offset, r: p.radius, s: p.spread, v: p.visible, b: p.boundVariables && p.boundVariables.color && p.boundVariables.color.id })));
async function snapshot(page) {
  const snap = [];
  for (const inst of page.findAllWithCriteria({ types: ['INSTANCE'] })) {
    if (!(await setOf(inst))) continue;
    for (const n of [inst, ...inst.findAll(() => true)]) {
      const e = { n };
      if ('fills' in n && Array.isArray(n.fills)) e.fills = JSON.parse(JSON.stringify(n.fills));
      if ('strokes' in n) e.strokes = JSON.parse(JSON.stringify(n.strokes));
      if ('effects' in n) e.effects = JSON.parse(JSON.stringify(n.effects));
      snap.push(e);
    }
  }
  return snap;
}
async function restore(snap) {
  let restored = 0, residual = 0;
  for (const e of snap) {
    let changed = false;
    for (const k of ['fills', 'strokes', 'effects']) {
      if (!e[k] || sig(e.n[k]) === sig(e[k])) continue;
      if (e.n.type === 'TEXT') for (const seg of e.n.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(seg.fontName);
      e.n[k] = e[k]; changed = true;
    }
    if (changed) restored++;
  }
  for (const e of snap) for (const k of ['fills', 'strokes', 'effects']) if (e[k] && sig(e.n[k]) !== sig(e[k])) residual++;
  return { snapshot: snap.length, restored, residual };
}
```

## Review Focus

1. **Variant renames must keep instances on the same component.** `Coarse → Medium`, `Light →
   Tint`, and `Dark → Shade` rename variant values in place. Tasks 3 and 4 count instances per
   variant before and after, and the counts must match.
2. **Bound effect color alpha.** Task 2 asserts every `<hue>/Casing` shadow reads alpha 1 after
   binding. Paints showed Figma overwriting opacity on binding; effects are checked, not assumed.
3. **Re-runs must not duplicate clones** (Coarse `[16,9]`, Bold/Shadow, caption) or effect styles.
   Verifications assert exact variant and style counts.
4. **The rename must not strand v2 scripts.** Task 1 updates every `'Map Overlay'` literal in the v2
   plan, because v2 Task 3 is Andrew's re-sync script.
5. **Deleting the `Icon` property** must not detach or break existing `Site Marker` instances.
   Task 4 counts instances and their variant names before and after.

## State ledger

- Task 1, collection ID and variable count after rename: `VariableCollectionId:145:395`, 30 variables (done 2026-10-11)
- Task 2, casing effect style IDs: sage S:7bafddbf28d97370ac42962aca8f3cdf285f22f4; cobalt S:d4377f5b23cc88dbd16a34c6ab14a2712c717be1; coral S:42b7c1916080feec7c6613d854f9f8aebcf8152e; gold S:c20ee9f321db2c4d3af87bec315fb3f3229abd46; magenta S:93aa166d2514baa8357a9a922f216d76ebc8e666; charcoal S:699ee51e2bac5bcf31fd655b25ab158ce9b6472b; slate S:b0a2fb7fe058b96ed7879a1889bb3b6662d0023e; teal S:162c31fb89bf8c52c0d2de6db09eab757cff53dc; violet S:60566efcea852b606ab7860380e228216c45c8f8; amber S:9a112dbb7fdb8dddb60125341bb10dd71671d53c (all alpha 1)
- Task 3, Line Sample instance counts per variant before/after (Keys page; keyed by node ID): 472:851 0/0, 472:853 0/0 (Coarse renamed Medium), 472:855 0/0, 472:857 0/0, 472:859 0/0, 472:861 0/0, 472:863 1/1, 472:865 14/14; new 791:664 (Standard/Coarse [16,9]) 0, 791:666 (Bold/Solid/Shadow) 0. Snapshot/restore: snapshot 479, restored 0, residual 0. 10 variants, set 540×108 (done 2026-10-11)
- Task 4, Site Marker and caption instance counts before/after (identical; keyed by variant ID): Site Marker 473:853 13/13, 473:860 5/5, 641:1198/641:1206/641:1225/641:1231 0/0; caption all 8 variants 0/0 (640:4365 and 640:4367 now Shade, 749:668 and 749:672 now Tint). `Icon#473:4` deleted; Dot/Hexagon polygon on charcoal/Base/100 + charcoal/Shade/100. Snapshot/restore: snapshot 479, restored 0, residual 0 (done 2026-10-11)
- Task 5, Styles-page frame IDs and counts: Stroke Documentation `796:2` (x=4768); 17 text nodes renamed to Color Roles; 72 line-treatment samples, 10 casing samples, 2 region cards; section 701:2 resized 7840x4259; GREEN ok:true.
- Task 6, checklist counts per category: translucent 32, rebind 0, dash 11, casing 13 (Keys page; fill-inventory scan 16/0/5/0 is a subset) (done 2026-10-11)

---

### Task 1: Rename `Map Overlay` → `Color Roles`

**Files:**
- Modify (Figma): collection `VariableCollectionId:145:395`
- Modify: `site-plan/plans/2026-10-10-map-tokens-v2.md` (every `'Map Overlay'` literal in code)
- Modify: `/Users/andrewkeser/.claude/projects/-Users-andrewkeser-Code-keser-permaculture-site-plan/memory/figma_styles_page_sync.md`
- Modify: this plan (ledger, checkboxes)

**Interfaces:**
- Consumes: Prelude A.
- Produces: collection `Color Roles` with the same 30 variables and IDs. Later tasks use
  `V('Color Roles', …)`.

- [x] **Step 1: Write and run the verification. It should fail.**

```js
// Prelude A here
const problems = [];
const c = col('Color Roles');
if (!c) problems.push('no Color Roles collection');
if (col('Map Overlay')) problems.push('Map Overlay still exists');
if (c && c.id !== 'VariableCollectionId:145:395') problems.push('unexpected id ' + c.id);
if (c && c.variableIds.length !== 30) problems.push('count ' + c.variableIds.length);
if (c) for (const h of HUES) for (const r of ROLES) if (!V('Color Roles', `${h}/${r}`)) problems.push('missing ' + h + '/' + r);
return { ok: problems.length === 0, problems };
```

Expected now: `ok: false` with `no Color Roles collection` and `Map Overlay still exists`.

- [x] **Step 2: Run the build.**

```js
const cols = await figma.variables.getLocalVariableCollectionsAsync();
const c = cols.find(c => c.id === 'VariableCollectionId:145:395');
const before = c.name;
if (c.name !== 'Color Roles') c.name = 'Color Roles';
return { before, after: c.name, vars: c.variableIds.length };
```

- [x] **Step 3: Re-run the Step 1 verification.** Expected: `ok: true`.

- [x] **Step 4: Update the v2 plan's code.** In `site-plan/plans/2026-10-10-map-tokens-v2.md`,
  replace every `'Map Overlay'` string literal (in `V(...)` and `col(...)` calls) with
  `'Color Roles'`, using exact-string edits. Then add this line directly under that plan's
  `**Spec:**` line:
  `> **2026-10-11:** the \`Map Overlay\` collection was renamed \`Color Roles\` (v3 plan Task 1); code below uses the new name.`
  Check: `grep -c "'Map Overlay'" site-plan/plans/2026-10-10-map-tokens-v2.md` returns `0`.

- [x] **Step 5: Update the memory note.** In `figma_styles_page_sync.md`, change `Map Overlay` to
  `Color Roles` wherever it names the collection.

- [x] **Step 6: Commit.**

```bash
git add site-plan/plans/2026-10-11-map-tokens-v3.md site-plan/plans/2026-10-10-map-tokens-v2.md
git commit -m "Map tokens v3 Task 1: rename Map Overlay to Color Roles"
```

---

### Task 2: Casing effect styles (10)

**Files:**
- Modify (Figma): local effect styles
- Modify: this plan (ledger, checkboxes)

**Interfaces:**
- Consumes: Prelude A; Task 1.
- Produces: effect styles `<hue>/Casing`. Later tasks find them with `CASING(hue)`.

- [x] **Step 1: Write and run the verification. It should fail.**

```js
// Prelude A here
const problems = [];
for (const h of HUES) {
  const s = CASING(h);
  if (!s) { problems.push('missing ' + h + '/Casing'); continue; }
  if (s.effects.length !== 1) { problems.push(h + ' effects ' + s.effects.length); continue; }
  const e = s.effects[0];
  if (e.type !== 'DROP_SHADOW') problems.push(h + ' type ' + e.type);
  if (e.offset.x !== 0 || e.offset.y !== 4 || e.radius !== 1 || (e.spread || 0) !== 0) problems.push(h + ' geometry');
  if (Math.abs(e.color.a - 1) > 1e-6) problems.push(h + ' alpha ' + e.color.a);
  const b = e.boundVariables && e.boundVariables.color;
  const v = b && await figma.variables.getVariableByIdAsync(b.id);
  if (!v || v.name !== h + '/Shade' || v.variableCollectionId !== col('Color Roles').id) problems.push(h + ' bound to ' + (v && v.name));
  if (hex(e.color) !== hex(rampColor(h, '700'))) problems.push(h + ' stored color ' + hex(e.color));
}
const extra = effectStyles.filter(s => s.name.endsWith('/Casing') && !HUES.includes(s.name.split('/')[0]));
if (extra.length) problems.push('extra ' + extra.map(s => s.name));
return { ok: problems.length === 0, problems };
```

Expected now: `ok: false`, 10 `missing` problems.

- [x] **Step 3: Run the build.** The shadow's stored color is set to the resolved Shade color, so
  the style picker thumbnail matches (the v2 lesson for paint styles).

```js
// Prelude A here
const made = [];
for (const h of HUES) {
  let s = CASING(h);
  if (!s) { s = figma.createEffectStyle(); s.name = h + '/Casing'; effectStyles.push(s); made.push(s.id); }
  const c = rampColor(h, '700');
  const base = { type: 'DROP_SHADOW', color: { r: c.r, g: c.g, b: c.b, a: 1 }, offset: { x: 0, y: 4 }, radius: 1, spread: 0, visible: true, blendMode: 'NORMAL', showShadowBehindNode: false };
  s.effects = [figma.variables.setBoundVariableForEffect(base, 'color', V('Color Roles', h + '/Shade'))];
  s.description = `Casing shadow for ${h} lines: drop shadow (0, 4), blur 1, color ${h}/Shade. Pair with a ${h}/Base/100 stroke at weight/lg.`;
}
return { made: made.length, alphas: effectStyles.filter(s => s.name.endsWith('/Casing')).map(s => s.name + ' a=' + s.effects[0].color.a) };
```

- [x] **Step 4: Re-run the verification.** Expected: `ok: true`. If any alpha reads other than 1,
  stop: record it in the ledger and report BLOCKED. Don't work around it.

- [x] **Step 5: Record the 10 style IDs in the ledger and commit.**

```bash
git add site-plan/plans/2026-10-11-map-tokens-v3.md
git commit -m "Map tokens v3 Task 2: casing effect styles"
```

---

### Task 3: `Line Sample` — dash set, Bold weight, Casing axis

**Files:**
- Modify (Figma): component set `Line Sample` `472:867` (Keys)
- Modify: this plan (ledger, checkboxes)

**Interfaces:**
- Consumes: Preludes A and C; Tasks 1–2.
- Produces: `Line Sample` with `Weight` Thin|Standard|Heavy|Bold, `Dash` Solid|Fine|Medium|Coarse,
  `Cap` None|Single|Double, `Casing` None|Shadow; 10 variants.

- [x] **Step 1: Record instance counts per variant (read-only).**

```js
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const set = await figma.getNodeByIdAsync('472:867');
const ids = new Set(set.children.map(v => v.id));
const counts = {};
for (const inst of page.findAllWithCriteria({ types: ['INSTANCE'] })) { const mc = await inst.getMainComponentAsync(); if (mc && ids.has(mc.id)) counts[mc.id] = (counts[mc.id] || 0) + 1; }
return set.children.map(v => ({ id: v.id, name: v.name, instances: counts[v.id] || 0 }));
```

Record it in the ledger as "before". The instance counts are keyed by variant node ID, which
renames don't change.

- [x] **Step 2: Write and run the verification. It should fail.**

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const set = await figma.getNodeByIdAsync('472:867');
const problems = [];
const defs = set.componentPropertyDefinitions;
const want = { Weight: ['Thin','Standard','Heavy','Bold'], Dash: ['Solid','Fine','Medium','Coarse'], Cap: ['None','Single','Double'], Casing: ['None','Shadow'] };
for (const [k, vals] of Object.entries(want)) { const d = defs[k]; if (!d) { problems.push('no axis ' + k); continue; } for (const v of vals) if (!d.variantOptions.includes(v)) problems.push(k + ' lacks ' + v); }
const DASH = { Solid: [], Fine: [2, 2], Medium: [8, 8], Coarse: [16, 9] };
const WT = { Thin: 'weight/xs', Standard: 'weight/sm', Heavy: 'weight/md', Bold: 'weight/xl' };
for (const v of set.children) {
  const p = v.variantProperties; const n = v.findOne(x => x.type === 'VECTOR');
  if (!n) { problems.push(v.name + ' no vector'); continue; }
  if (DASH[p.Dash] && JSON.stringify(n.dashPattern) !== JSON.stringify(DASH[p.Dash])) problems.push(v.name + ' dash ' + JSON.stringify(n.dashPattern));
  const b = n.boundVariables && n.boundVariables.strokeWeight; const wv = b && await figma.variables.getVariableByIdAsync(b.id);
  if (!wv || wv.name !== WT[p.Weight]) problems.push(v.name + ' weight ' + (wv && wv.name));
  const ss = typeof n.strokeStyleId === 'string' && n.strokeStyleId ? await figma.getStyleByIdAsync(n.strokeStyleId) : null;
  if (!ss || ss.name !== 'charcoal/Base/100') problems.push(v.name + ' stroke style ' + (ss && ss.name));
  const es = typeof n.effectStyleId === 'string' && n.effectStyleId ? await figma.getStyleByIdAsync(n.effectStyleId) : null;
  if (p.Casing === 'Shadow' && (!es || es.name !== 'charcoal/Casing')) problems.push(v.name + ' effect ' + (es && es.name));
  if (p.Casing === 'None' && n.effects.length) problems.push(v.name + ' has effects');
}
if (set.children.length !== 10) problems.push('variants ' + set.children.length);
for (const name of ['Weight=Standard, Dash=Coarse, Cap=None, Casing=None', 'Weight=Bold, Dash=Solid, Cap=None, Casing=Shadow'])
  if (!set.children.find(v => v.name === name)) problems.push('missing ' + name);
return { ok: problems.length === 0, problems };
```

Expected now: `ok: false` (no Casing axis, no Bold, no Medium/Coarse `[16,9]`, 8 variants).

- [x] **Step 3: Run the build.**

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
// Prelude C here
const snap = await snapshot(page);
const set = await figma.getNodeByIdAsync('472:867');
const vname = p => `Weight=${p.Weight}, Dash=${p.Dash}, Cap=${p.Cap}, Casing=${p.Casing}`;
// 1. rename in place: add Casing=None, Coarse([8,8]) -> Medium.
//    Compute every new name first, then assign in one pass: reading variantProperties after the
//    first rename throws "Component set for node has existing errors" (ran 2026-10-11).
if (!set.componentPropertyDefinitions.Casing) {
  const renames = set.children.map(v => { const p = { ...v.variantProperties }; if (p.Dash === 'Coarse') p.Dash = 'Medium'; p.Casing = 'None'; return [v, vname(p)]; });
  for (const [v, name] of renames) v.name = name;
}
const find = name => set.children.find(v => v.name === name);
const right = () => Math.max(...set.children.map(v => v.x + v.width));
const created = [];
// 2. Coarse [16,9] from the Medium variant
if (!find('Weight=Standard, Dash=Coarse, Cap=None, Casing=None')) {
  const c = find('Weight=Standard, Dash=Medium, Cap=None, Casing=None').clone(); set.appendChild(c);
  c.name = 'Weight=Standard, Dash=Coarse, Cap=None, Casing=None'; c.x = right() + 40;
  c.findOne(x => x.type === 'VECTOR').dashPattern = [16, 9]; created.push(c.id);
}
// 3. Bold + Shadow from Standard/Solid/None
if (!find('Weight=Bold, Dash=Solid, Cap=None, Casing=Shadow')) {
  const c = find('Weight=Standard, Dash=Solid, Cap=None, Casing=None').clone(); set.appendChild(c);
  c.name = 'Weight=Bold, Dash=Solid, Cap=None, Casing=Shadow'; c.x = right() + 40;
  const vec = c.findOne(x => x.type === 'VECTOR');
  vec.setBoundVariable('strokeWeight', W('lg'));
  await vec.setStrokeStyleIdAsync(S('charcoal/Base/100').id);
  await vec.setEffectStyleIdAsync(CASING('charcoal').id);
  created.push(c.id);
}
// 4. fit the set around its children
const minX = Math.min(...set.children.map(v => v.x)), minY = Math.min(...set.children.map(v => v.y));
for (const v of set.children) { v.x -= minX - 20; v.y -= minY - 20; }
set.resizeWithoutConstraints(Math.max(...set.children.map(v => v.x + v.width)) + 20, Math.max(...set.children.map(v => v.y + v.height)) + 20);
const pins = await restore(snap);
return { created, variants: set.children.map(v => v.name), pins };
```

Expected: `pins.residual: 0`.

- [x] **Step 4: Re-run the Step 2 verification** (expected `ok: true`) **and the Step 1 count**.
  Every original variant ID must keep its instance count. The two new variants have 0.

- [x] **Step 5: Screenshot the set** (`get_screenshot` on `472:867`) and confirm the casing
  variant shows the shadow under the line.

- [x] **Step 6: Record before/after counts and the pin result in the ledger and commit.**

```bash
git add site-plan/plans/2026-10-11-map-tokens-v3.md
git commit -m "Map tokens v3 Task 3: Line Sample dash set, Bold weight, Casing axis"
```

---

### Task 4: `Site Marker` and `caption` cleanup

**Files:**
- Modify (Figma): `Site Marker` `473:862`, `caption` `640:4373` (Keys)
- Modify: this plan (ledger, checkboxes)

**Interfaces:**
- Consumes: Preludes A and C; Task 1.
- Produces: `Site Marker` without the `Icon` property and with `Dot / Hexagon` on styles; `caption`
  `Style` values Shade|White|Tint|Black.

- [x] **Step 1: Record instance counts per variant for both sets (read-only).**

```js
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const out = {};
for (const sid of ['473:862', '640:4373']) {
  const set = await figma.getNodeByIdAsync(sid); const ids = new Set(set.children.map(v => v.id)); const counts = {};
  for (const inst of page.findAllWithCriteria({ types: ['INSTANCE'] })) { const mc = await inst.getMainComponentAsync(); if (mc && ids.has(mc.id)) counts[mc.id] = (counts[mc.id] || 0) + 1; }
  out[set.name] = set.children.map(v => ({ id: v.id, name: v.name, instances: counts[v.id] || 0 }));
}
return out;
```

- [x] **Step 2: Write and run the verification. It should fail.**

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const problems = [];
const sm = await figma.getNodeByIdAsync('473:862');
if (Object.keys(sm.componentPropertyDefinitions).some(k => k.startsWith('Icon'))) problems.push('Site Marker still has Icon property');
const dh = sm.children.find(v => v.variantProperties.Style === 'Dot' && v.variantProperties.Shape === 'Hexagon');
const poly = dh && dh.findOne(x => x.type === 'POLYGON');
const st = async id => (typeof id === 'string' && id ? ((await figma.getStyleByIdAsync(id)) || {}).name : null);
if (!poly) problems.push('Dot/Hexagon polygon missing');
else {
  if (await st(poly.fillStyleId) !== 'charcoal/Base/100') problems.push('Dot/Hexagon fill ' + await st(poly.fillStyleId));
  if (poly.strokes.length && await st(poly.strokeStyleId) !== 'charcoal/Shade/100') problems.push('Dot/Hexagon stroke ' + await st(poly.strokeStyleId));
}
const cap = await figma.getNodeByIdAsync('640:4373');
const capStyles = [...new Set(cap.children.map(v => v.variantProperties.Style))].sort().join('|');
if (capStyles !== 'Black|Shade|Tint|White') problems.push('caption Style values ' + capStyles);
if (cap.children.length !== 8) problems.push('caption variants ' + cap.children.length);
return { ok: problems.length === 0, problems };
```

Expected now: `ok: false` (Icon property present, raw Dot/Hexagon, caption values
`Black|Dark|Light|White`).

- [x] **Step 3: Run the build.** `Dot / Hexagon`'s current raw fill `#7a7975` and stroke `#474644`
  equal `charcoal/Base` and `charcoal/Shade` exactly, so binding the styles changes nothing visually.

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
// Prelude C here
const snap = await snapshot(page);
const sm = await figma.getNodeByIdAsync('473:862');
const iconKey = Object.keys(sm.componentPropertyDefinitions).find(k => k.startsWith('Icon'));
if (iconKey) sm.deleteComponentProperty(iconKey);
const dh = sm.children.find(v => v.variantProperties.Style === 'Dot' && v.variantProperties.Shape === 'Hexagon');
const poly = dh.findOne(x => x.type === 'POLYGON');
await poly.setFillStyleIdAsync(S('charcoal/Base/100').id);
if (poly.strokes.length) await poly.setStrokeStyleIdAsync(S('charcoal/Shade/100').id);
const cap = await figma.getNodeByIdAsync('640:4373');
const MAP = { Light: 'Tint', Dark: 'Shade' };
for (const v of cap.children) { const p = v.variantProperties; if (MAP[p.Style]) v.name = `Style=${MAP[p.Style]}, Size=${p.Size}`; }
const pins = await restore(snap);
return { iconDeleted: iconKey || null, captionVariants: cap.children.map(v => v.name), pins };
```

Expected: `pins.residual: 0`.

- [x] **Step 4: Re-run the Step 2 verification** (expected `ok: true`) **and the Step 1 counts**.
  Every variant ID must keep its instance count.

- [x] **Step 5: Record before/after counts and the pin result in the ledger and commit.**

```bash
git add site-plan/plans/2026-10-11-map-tokens-v3.md
git commit -m "Map tokens v3 Task 4: Site Marker and caption cleanup"
```

---

### Task 5: Styles page — Color Roles naming, Stroke frame, casing, region recipe

**Files:**
- Modify (Figma): Styles page `699:2080`, section `701:2`. Rename text in Semantic Tokens
  (`758:2`). Rebuild `Stroke Documentation` (at x=4768).
- Modify: this plan (ledger, checkboxes)

**Interfaces:**
- Consumes: Preludes A and B; Tasks 1–3.
- Produces: no text in section `701:2` says "Map Overlay"; the Stroke frame has 72 line-treatment
  samples, 10 casing samples, and 2 region recipe cards.

- [x] **Step 1: Write and run the verification. It should fail.**

```js
const page = await figma.getNodeByIdAsync('699:2080'); await figma.setCurrentPageAsync(page);
const sec = await figma.getNodeByIdAsync('701:2');
const problems = [];
const mo = sec.findAll(n => n.type === 'TEXT' && n.characters.includes('Map Overlay'));
if (mo.length) problems.push(mo.length + ' text nodes still say Map Overlay');
const st = sec.children.find(c => c.name === 'Stroke Documentation');
if (!st) problems.push('no Stroke frame');
else {
  const lt = st.findAll(n => n.type === 'VECTOR' && / · (xs|sm|md|lg|xl|2xl) \(/.test(n.name)).length;
  if (lt !== 72) problems.push('line treatment samples ' + lt);
  const cs = st.findAll(n => n.type === 'VECTOR' && n.name.startsWith('Casing — ')).length;
  if (cs !== 10) problems.push('casing samples ' + cs);
  const rc = st.findAll(n => n.name.startsWith('Region — ')).length;
  if (rc !== 2) problems.push('region cards ' + rc);
  if (Math.round(st.x) !== 4768) problems.push('Stroke x ' + Math.round(st.x));
}
return { ok: problems.length === 0, problems };
```

Expected now: `ok: false` (Map Overlay text present, 54 samples, no casing or region).

- [x] **Step 2: Rename "Map Overlay" text across the section.**

```js
const page = await figma.getNodeByIdAsync('699:2080'); await figma.setCurrentPageAsync(page);
const sec = await figma.getNodeByIdAsync('701:2');
let changed = 0;
for (const t of sec.findAll(n => n.type === 'TEXT' && (n.characters.includes('Map Overlay') || n.characters === 'Semantic Color Tokens'))) {
  for (const seg of t.getStyledTextSegments(['fontName'])) await figma.loadFontAsync(seg.fontName);
  t.characters = t.characters === 'Semantic Color Tokens' ? 'Color Roles' : t.characters.split('Map Overlay').join('Color Roles');
  changed++;
}
return { changed };
```

- [x] **Step 3: Rebuild the Stroke frame.**

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('699:2080'); await figma.setCurrentPageAsync(page);
// Prelude B here
const f = docFrame('Stroke Documentation', 'Stroke', 'Stroke weights from the Stroke collection, line treatments, casing lines, and region borders. Dash patterns and line ends can’t be variables or styles, so the Line Treatments grid is their canonical record: copy properties from a sample (⌥⌘C), paste them onto a map path (⌥⌘V), then pick a color style. Strokes use the same Color Roles paint styles as fills.', 4768);
const strokeStyle = S('charcoal/Base/100').id;
// o.h = sample height, o.inset = gap at each end (room for arrowheads), o.y = line position (2026-10-12 sizing).
async function line(parent, name, len, dash, caps, tier, styleId, effectId, o = {}) {
  const h = o.h || 48, inset = o.inset ?? 8;
  const box = figma.createFrame(); box.name = 'Sample'; parent.appendChild(box); box.resize(len, h); box.fills = []; box.clipsContent = false;
  const v = figma.createVector(); v.name = name; box.appendChild(v);
  await v.setVectorNetworkAsync({ vertices: [{ x: 0, y: 0, strokeCap: caps[0] }, { x: len - 2 * inset, y: 0, strokeCap: caps[1] }], segments: [{ start: 0, end: 1 }], regions: [] });
  v.x = inset; v.y = o.y ?? h / 2; v.dashPattern = dash;
  await v.setStrokeStyleIdAsync(styleId || strokeStyle); v.setBoundVariable('strokeWeight', W(tier));
  if (effectId) await v.setEffectStyleIdAsync(effectId);
  return v;
}
function card(parent, name) {
  const c = figma.createAutoLayout('HORIZONTAL', { name, itemSpacing: 24 }); parent.appendChild(c); c.resize(864, 80); c.primaryAxisSizingMode = 'FIXED'; c.counterAxisSizingMode = 'AUTO';
  c.paddingTop = c.paddingBottom = c.paddingLeft = c.paddingRight = 16; c.counterAxisAlignItems = 'CENTER'; c.cornerRadius = 13; c.fills = solid(CARD);
  return c;
}
// Weights
const wb = row(f, 'Section — Weights', 'Weights', 'Six tiers. Bind a stroke’s weight to a tier instead of typing a number, so retuning a tier updates every map.');
for (const [t, w] of TIERS) {
  const c = card(wb, 'weight/' + t);
  await line(c, `Weight ${t} (${w})`, 120, [], ['NONE', 'NONE'], t);
  const info = figma.createAutoLayout('VERTICAL', { name: 'Info', itemSpacing: 2 }); c.appendChild(info); info.fills = [];
  txt(info, 'weight/' + t, { style: 'Medium' }); txt(info, `${w}px  ·  STROKE_FLOAT`, { size: 11, color: GREY, family: 'JetBrains Mono' });
}
// Line treatments
const DASH = { Solid: [], Fine: [2, 2], Medium: [8, 8], Coarse: [16, 9] };
const CAP = { None: ['NONE', 'NONE'], Single: ['NONE', 'ARROW_LINES'], Double: ['ARROW_LINES', 'ARROW_LINES'] };
const tb = row(f, 'Section — Line Treatments', 'Line Treatments', 'Every Dash × Cap combination at every weight tier, stroked charcoal/Base/100. Three dashes: Fine [2,2], Medium [8,8], Coarse [16,9]. Dash lengths are fixed, so Fine reads as dense bars at the heaviest tiers.', 16);
let samples = 0;
for (const [d, dash] of Object.entries(DASH)) for (const [c, caps] of Object.entries(CAP)) {
  const r = figma.createAutoLayout('HORIZONTAL', { name: `${d} · ${c}`, itemSpacing: 16 }); tb.appendChild(r); r.counterAxisAlignItems = 'CENTER'; r.fills = []; r.clipsContent = false;
  const label = `${d}${dash.length ? ' [' + dash.join(',') + ']' : ''} · ${c}`;
  txt(r, label, { size: 11, family: 'JetBrains Mono', width: 160 });
  for (const [t, w] of TIERS) {
    const cell = figma.createAutoLayout('VERTICAL', { name: t, itemSpacing: 2 }); r.appendChild(cell); cell.fills = []; cell.clipsContent = false; cell.counterAxisAlignItems = 'CENTER';
    // 96x72 box with a 64px line: 2xl arrowheads fit without clipping or touching the label.
    await line(cell, `${label} · ${t} (${w})`, 96, dash, caps, t, null, null, { h: 72, inset: 16 });
    txt(cell, `${t} (${w})`, { size: 10, color: GREY }); samples++;
  }
}
// Casing
const cb = row(f, 'Section — Casing', 'Casing Lines', 'A Base stroke at weight lg with the hue’s Casing effect style: a drop shadow (0, 4), blur 1, in the hue’s Shade. Matches Line Sample → Casing = Shadow.', 16);
const cgrid = figma.createAutoLayout('HORIZONTAL', { name: 'Casing grid', itemSpacing: 16 }); cb.appendChild(cgrid); cgrid.fills = []; cgrid.layoutWrap = 'WRAP'; cgrid.resize(864, cgrid.height); cgrid.counterAxisSpacing = 16;
let casing = 0;
for (const h of HUES) {
  // Fixed 160px columns (5 per row in 864) so both rows align; the line spans the cell so its left edge meets the label.
  const cell = figma.createAutoLayout('VERTICAL', { name: h, itemSpacing: 2 }); cgrid.appendChild(cell); cell.fills = []; cell.clipsContent = false;
  await line(cell, `Casing — ${h}`, 160, [], ['NONE', 'NONE'], 'lg', S(`${h}/Base/100`).id, CASING(h).id, { inset: 0, y: 22 });
  txt(cell, `${h}/Base/100\n+ ${h}/Casing`, { size: 10, color: GREY, width: 160 });
  cell.counterAxisSizingMode = 'FIXED'; cell.resize(160, cell.height); casing++;
}
// Region recipe
const rb = row(f, 'Section — Region Recipe', 'Region Borders', 'Strokes also outline shapes. A region overlay is a Tint 50% or 25% fill plus a Base border at weight xl or 2xl with a named dash.', 16);
const RECIPES = [['Region — sage Tint 50 + Base xl Medium', 'sage', 50, 'xl', [8, 8]], ['Region — cobalt Tint 25 + Base 2xl Coarse', 'cobalt', 25, '2xl', [16, 9]]];
for (const [name, h, o, tier, dash] of RECIPES) {
  const c = card(rb, name);
  const bg = figma.createFrame(); bg.name = 'Region container'; c.appendChild(bg); bg.resize(160, 96); bg.cornerRadius = 4; bg.fills = [];
  const shape = figma.createRectangle(); shape.name = 'Region'; bg.appendChild(shape); shape.resize(128, 64); shape.x = 16; shape.y = 16; shape.cornerRadius = 8;
  await shape.setFillStyleIdAsync(S(`${h}/Tint/${o}`).id); await shape.setStrokeStyleIdAsync(S(`${h}/Base/100`).id);
  shape.strokeAlign = 'INSIDE'; shape.dashPattern = dash;
  for (const side of ['strokeTopWeight', 'strokeRightWeight', 'strokeBottomWeight', 'strokeLeftWeight']) shape.setBoundVariable(side, W(tier));
  const info = figma.createAutoLayout('VERTICAL', { name: 'Info', itemSpacing: 2 }); c.appendChild(info); info.fills = [];
  txt(info, name.replace('Region — ', ''), { style: 'Medium' });
  txt(info, `fill ${h}/Tint/${o}  ·  stroke ${h}/Base/100  ·  weight/${tier}  ·  dash [${dash.join(',')}]  ·  inside`, { size: 11, color: GREY, family: 'JetBrains Mono' });
}
note(f, 'Paste-properties binding test', 'Not yet run. See Task 7 Step 6 of site-plan/plans/2026-10-10-map-tokens-v2.md.');
return { frameId: f.id, samples, casing, regions: RECIPES.length };
```

Expected: `samples: 72, casing: 10, regions: 2`.

- [x] **Step 4: Fit the section and screenshot.**

```js
const page = await figma.getNodeByIdAsync('699:2080'); await figma.setCurrentPageAsync(page);
const s = await figma.getNodeByIdAsync('701:2');
const typo = s.children.find(c => c.name === 'Typography Documentation'); if (typo) { typo.x = 6336; typo.y = 64; }
const right = Math.max(...s.children.map(k => k.x + k.width)), bottom = Math.max(...s.children.map(k => k.y + k.height));
s.resizeWithoutConstraints(right + 64, bottom + 64);
const st = s.children.find(c => c.name === 'Stroke Documentation');
await st.screenshot({ scale: 0.25 });
return { w: Math.round(s.width), h: Math.round(s.height), frames: s.children.map(k => k.name + ' @' + Math.round(k.x)) };
```

Look for clipped text, overlapping arrowheads, and casing shadows that render. Then re-run the
Step 1 verification. Expected: `ok: true`.

- [x] **Step 5: Record frame IDs and counts in the ledger and commit.**

```bash
git add site-plan/plans/2026-10-11-map-tokens-v3.md
git commit -m "Map tokens v3 Task 5: Styles page Color Roles, Stroke frame, casing, region recipe"
```

---

### Task 6: Migration checklist (read-only scan)

**Files:**
- Modify: this plan (append under "Migration checklist (Andrew)")

**Interfaces:**
- Consumes: Prelude A; Tasks 1–3.
- Produces: four lists with node IDs.

- [x] **Step 1: Scan the Keys page** (`222:2275`), skipping component-set definitions and the
  `sector-analysis-comparison` frame (`724:4690`, deliberately raw), including instance sublayers.

```js
// Prelude A here
const page = await figma.getNodeByIdAsync('222:2275'); await figma.setCurrentPageAsync(page);
const ROOT = page; const SKIP = new Set(['724:4690']);
const roleOf = c => { for (const h of HUES) for (const r of ROLES) if (hex(rampColor(h, STEP(h, r))) === hex(c)) return `${h}/${r}`; return null; };
const nearestHueTint = c => { let best = null, d = 9; for (const h of HUES) for (const step of ['50','100','200','300','400','500','600','700','800']) { const v = rampColor(h, step); const dd = Math.hypot(v.r - c.r, v.g - c.g, v.b - c.b); if (dd < d) { d = dd; best = h; } } return best; };
const inSkip = n => { for (let p = n; p && p.type !== 'PAGE'; p = p.parent) { if (SKIP.has(p.id) || p.type === 'COMPONENT_SET') return true; } return false; };
const where = n => { let p = n, top = n; while (p.parent && p.parent.type !== 'PAGE') { if (p.type === 'INSTANCE') top = p; p = p.parent; } return (top !== n ? top.name + ' › ' : '') + p.name; };
const DASH_OK = ['[]', '[2,2]', '[8,8]', '[16,9]'];
const DASH_MAP = { '[4,4]': 'Fine', '[12,8]': 'Coarse', '[14,8]': 'Coarse' };
const out = { translucent: [], rebind: [], dash: [], casing: [] };
for (const n of ROOT.findAll(n => 'fills' in n || 'strokes' in n)) {
  if (inSkip(n)) continue;
  const styleName = async id => (typeof id === 'string' && id ? ((await figma.getStyleByIdAsync(id)) || {}).name : null);
  const fs = await styleName(n.fillStyleId);
  for (const p of (Array.isArray(n.fills) ? n.fills : [])) {
    if (p.type !== 'SOLID' || p.visible === false) continue;
    const bound = p.boundVariables && p.boundVariables.color;
    if (p.opacity < 0.999 && !(fs && /\/Tint\/(25|50)$/.test(fs))) { const h = nearestHueTint(p.color); out.translucent.push(`${n.id} · ${hex(p.color)} @${Math.round(p.opacity * 100)}% → ${h}/Tint/${p.opacity < 0.375 ? 25 : 50} (in ${where(n)})`); }
    else if (!bound && !fs && p.opacity >= 0.999) { const r = roleOf(p.color); if (r) out.rebind.push(`${n.id} · fill ${hex(p.color)} → ${r}/100 (in ${where(n)})`); }
  }
  const ss = await styleName(n.strokeStyleId);
  for (const p of (n.strokes || [])) {
    if (p.type !== 'SOLID') continue;
    if (!(p.boundVariables && p.boundVariables.color) && !ss) { const r = roleOf(p.color); if (r) out.rebind.push(`${n.id} · stroke ${hex(p.color)} → ${r}/100 (in ${where(n)})`); }
  }
  if (n.strokes && n.strokes.length && Array.isArray(n.dashPattern)) { const k = JSON.stringify(n.dashPattern); if (!DASH_OK.includes(k)) out.dash.push(`${n.id} · dash ${k} → ${DASH_MAP[k] || 'nearest of Fine/Medium/Coarse'} (in ${where(n)})`); }
  if (n.strokes && n.strokes.length && n.strokeWeight === 5 && (n.effects || []).some(e => e.type === 'DROP_SHADOW')) out.casing.push(`${n.id} · weight-5 line with shadow → Line Sample Casing=Shadow (in ${where(n)})`);
}
return { counts: Object.fromEntries(Object.entries(out).map(([k, v]) => [k, v.length])), out };
```

- [x] **Step 2: Run the same script on the Keys page** (`fill-inventory` lives there, section `Components`, not the Styles page), scoped to `fill-inventory`: change the
  first two lines to switch to `699:2080` and set `const ROOT = await figma.getNodeByIdAsync('699:2103');`.
  Keep everything else.

- [x] **Step 3: Append the results** under "Migration checklist (Andrew)" below as `- [ ]` items,
  grouped by category, then by the `(in …)` frame. Keep every ID. Fill in the "Generated" line with
  the date and per-category counts. Record the counts in the ledger.

- [x] **Step 4: Commit.**

```bash
git add site-plan/plans/2026-10-11-map-tokens-v3.md
git commit -m "Map tokens v3 Task 6: migration checklist"
```

---

### Task 7: Close-out

**Files:**
- Modify: `site-plan/specs/2026-10-11-map-tokens-v3-design.md` (Status line)
- Modify: the memory note `figma_styles_page_sync.md`
- Modify: this plan (checkboxes)

- [x] **Step 1: Update the spec Status line** to: `Status: built YYYY-MM-DD — see
  site-plan/plans/2026-10-11-map-tokens-v3.md; migration checklist listed there.`
- [x] **Step 2: Update the memory note.** Mention the `<hue>/Casing` effect styles, the Stroke
  frame's casing and region sections, and that `Line Sample` has `Casing` and `Bold`.
- [x] **Step 3: Commit, then ask Andrew before pushing.**

```bash
git add site-plan/plans/2026-10-11-map-tokens-v3.md site-plan/specs/2026-10-11-map-tokens-v3-design.md
git commit -m "Map tokens v3 Task 7: close-out"
```

---

## Migration checklist (Andrew)

Generated: 2026-10-11 — 32 translucent fills, 0 raw role-matching colors, 11 off-set dashes, 13 casing lines. (The `fill-inventory` scan (frame `699:2103`, on the Keys page, section `Components`) returned 16 translucent + 5 dash items, all already in the Keys-page results, so the lists below are the deduplicated union.)

Remaps change appearance by design: under the 'always Tint 25/50' rule, darker or more opaque fills (e.g. `#233c94` cobalt/700 @ 50%, the 80% fills) become lighter; 10% fills become 25%. Items under fill-inventory (`699:*`, `709:*`) mirror `497:*` originals in the example keys — fix the originals; the inventory copies follow or can be deleted.

**Translucent fills to remap to Tint 25/50 (32)**

In `label › Components`:
- [ ] I222:2288;168:1446 · #b3ede5 @40% → teal/Tint/50
- [ ] I222:2289;168:1446 · #e748c1 @30% → magenta/Tint/25
- [ ] I222:2290;168:1446 · #cbad42 @40% → gold/Tint/50
- [ ] I222:2291;168:1446 · #d2383b @40% → coral/Tint/50
- [ ] I222:2292;168:1446 · #8e5aca @40% → violet/Tint/50
- [ ] I222:2374;138:1446 · #233c94 @50% → cobalt/Tint/50
- [ ] I222:2375;138:1446 · #ff8780 @50% → coral/Tint/50
- [ ] I222:2376;138:1446 · #b09100 @50% → gold/Tint/50
- [ ] I222:2377;138:1446 · #e748c1 @50% → magenta/Tint/50

In `Components`:
- [ ] 497:4336 · #233c94 @50% → cobalt/Tint/50
- [ ] 497:4342 · #ff8780 @80% → coral/Tint/50
- [ ] 497:4348 · #ffabe5 @80% → magenta/Tint/50
- [ ] 497:4455 · #233c94 @50% → cobalt/Tint/50
- [ ] 497:4475 · #e748c1 @50% → magenta/Tint/50
- [ ] 497:4495 · #b09100 @50% → gold/Tint/50
- [ ] 497:4586 · #ff73da @10% → magenta/Tint/25
- [ ] 699:2081 · #b3ede5 @40% → teal/Tint/50
- [ ] 699:2082 · #cbad42 @40% → gold/Tint/50
- [ ] 699:2083 · #8e5aca @40% → violet/Tint/50
- [ ] 699:2084 · #e748c1 @30% → magenta/Tint/25
- [ ] 699:2094 · #d2383b @40% → coral/Tint/50
- [ ] 699:2098 · #233c94 @50% → cobalt/Tint/50
- [ ] 699:2099 · #ff8780 @50% → coral/Tint/50
- [ ] 699:2100 · #b09100 @50% → gold/Tint/50
- [ ] 699:2101 · #e748c1 @50% → magenta/Tint/50
- [ ] 699:2143 · #233c94 @50% → cobalt/Tint/50
- [ ] 699:2144 · #ff8780 @80% → coral/Tint/50
- [ ] 699:2149 · #ffabe5 @80% → magenta/Tint/50
- [ ] 709:4553 · #e748c1 @50% → magenta/Tint/50
- [ ] 709:4564 · #b09100 @50% → gold/Tint/50
- [ ] 709:4552 · #233c94 @50% → cobalt/Tint/50
- [ ] 709:4588 · #ff73da @10% → magenta/Tint/25

**Raw colors that match a role exactly (rebind to the style) (0)**

None found.

**Dashes outside Fine/Medium/Coarse (11)**

In `Components`:
- [ ] 497:4645 · dash [4,4] → Fine
- [ ] 497:4562 · dash [12,8] → Coarse
- [ ] 497:4568 · dash [14,8] → Coarse
- [ ] 497:4574 · dash [12,8] → Coarse
- [ ] 497:4580 · dash [4,4] → Fine
- [ ] 497:4586 · dash [12,8] → Coarse
- [ ] 709:4576 · dash [4,4] → Fine
- [ ] 709:4579 · dash [14,8] → Coarse
- [ ] 709:4582 · dash [12,8] → Coarse
- [ ] 709:4583 · dash [12,8] → Coarse
- [ ] 709:4588 · dash [12,8] → Coarse

**Casing lines to swap for Line Sample → Casing = Shadow (13)**

In `Components`:
- [ ] 497:4398 · weight-5 line with shadow
- [ ] 497:4405 · weight-5 line with shadow
- [ ] 497:4361 · weight-5 line with shadow
- [ ] 497:4368 · weight-5 line with shadow
- [ ] 497:4462 · weight-5 line with shadow
- [ ] 497:4518 · weight-5 line with shadow
- [ ] 497:4525 · weight-5 line with shadow
- [ ] 497:4532 · weight-5 line with shadow
- [ ] 497:4539 · weight-5 line with shadow
- [ ] 709:4528 · weight-5 line with shadow
- [ ] 709:4531 · weight-5 line with shadow
- [ ] 709:4542 · weight-5 line with shadow
- [ ] 709:4544 · weight-5 line with shadow
