# Page tokens and Ramps-only color — design

Status: built, 2026-10-25. Scope mode: personal project (HLSD), opinionated.

## Goal

Every color the microsite uses resolves to a Ramps color. Page chrome gets a Figma collection
("Page", Light/Dark) like the chart tokens already have. Amber is the accent.

## Audit

### Figma (Site Toolkit Design Language file)

Every color variable in every collection aliases a Ramps variable. No collection holds a raw
value.

| Collection | Color values | Aliases to Ramps | Raw |
|---|---|---|---|
| Color Roles | 30 | 30 | 0 |
| Chart Semantic | 24 | 24 | 0 |
| Chart Neutral | 12 | 12 | 0 |
| Chart Categorical | 14 | 14 | 0 |
| Species | 40 | 40 | 0 |
| Sheet | 14 | 14 | 0 |
| Map Semantic | 13 | 13 | 0 |

Chart Neutral is a semantic layer over the charcoal ramp (grid → charcoal/100 light,
charcoal/700 dark, and so on). Stroke and Map display hold no colors.

Paint styles: 30 are bound to variables. The other 20 are the `<hue>/Tint/25` and `/Tint/50`
styles. They hold copied hex plus paint opacity, because an alias can't carry its own alpha.

### Microsite (`docs/`)

The off-system colors all live in the HTML, not in Figma.

1. **Page chrome.** 10 variables, copied into all 11 pages, plus the nav and footer partials
   (9 hex values). None reference Ramps.
2. **Page-specific variables.** 48 definitions, 19 distinct values, on 6 pages. The earlier
   "~300" estimate counted every hex occurrence; most were the copied chrome.
3. **Inline hex in scripts.** `sun-solar.html` colors its 3D scene objects in JS (house, camper,
   coop, pool, tree).

## Findings that touch chart and semantic tokens

| Variable | Pages | Today | Problem | Proposal |
|---|---|---|---|---|
| `--scale-100/450/700` | flood-hazard, synthesis | blue, ΔE 4–16 off cobalt | A sequential chart scale outside `--chart-*` | Chart Semantic `flood/depth-1..3` → cobalt/100, 400, 700 (light); cobalt/200, 400, 700 (dark) |
| `--status-good`, `--status-done` | flood-hazard, synthesis, project-plan | `#0ca30c`, `#4fd44f`, ΔE 43+ off sage | Saturated green that matches nothing in the system | Page `status/good` → sage ramp |
| `--status-serious` | flood-hazard, synthesis | `#ec835a`, near amber | Collides with the new amber accent and chart emphasis | Page `status/serious` → coral ramp |
| `--status-active`, `--status-hold` | project-plan | off cobalt, off gold | Off-ramp | `status/active` → cobalt, `status/hold` → gold |
| `--runoff-on-bar`, `--shed-on-water` | water | `#1a1a19` | Text on a bar, hard-coded | Page `text/on-fill` |
| `--site-fill` | species-inventory | near charcoal | Off-ramp | charcoal/50 / charcoal/900 |
| `--gsa-roof-1..4` | sun-solar | exact Ramps values | Fine, but copied as hex | Alias in CSS; no change in look |
| 3D scene colors | sun-solar (JS) | 5 raw hex | Off-system | Read from Map Semantic CSS variables (structure, water, vegetation) |

Amber now means "accent and emphasis" everywhere. Status colors must not use it.

## Decisions (Andrew, 2026-10-25)

1. **Light surfaces are pure white.** Page and raised panels both use neutral/White; borders
   separate them. The old off-white (#f9f9f7) had no Ramps step.
2. **Serious status moves to coral.** Amber now means accent and emphasis only.
3. **Chart emphasis fill becomes translucent amber.** Water's ad hoc `color-mix()` fills (14, 16,
   18%) now use `--chart-emphasis-fill`. The elevation profile's blue lot band was the same idea
   in cobalt, so it became a new pair: `--chart-focus` and `--chart-focus-fill`.

## Calls made while building

- **Status chips use opaque tints**, not alpha: the hue's 600 on its 50 (light) and 200 on its 800
  (dark). Every chip measures at least 5.5:1. This kept the alpha steps to six.
- **Dark muted text is charcoal/300, not 400.** charcoal/400 measured 4.48:1 on the dark badge
  background, under AA.
- **`text/on-fill` is charcoal/900 in both modes.** It labels mid-tone bars that stay mid-tone in
  dark mode, so white text would lose contrast.
- **Page tokens sit on `:root`**, not `.viz-root`, so the nav and footer partials share them.
- `--status-done` was renamed `--status-good`; `--scale-*` became `--chart-flood-depth-1..3`.
- The check now fails when a page lacks `page-tokens.css`, or uses `--chart-*` without linking
  `chart-tokens.css`. The flood-factor gradient vanished during migration for that reason: the
  page had never loaded the chart tokens.

## Page collection

Light / Dark. Ramps aliases only.

| Token (CSS name kept) | Light | Dark | Note |
|---|---|---|---|
| `surface/page` (`--page`) | neutral/White | neutral/Black | was #f9f9f7 / #0d0d0d |
| `surface/raised` (`--surface-1`) | neutral/White | **charcoal/900** (new) | dark was #1a1a19 |
| `surface/badge` (`--badge-bg`) | charcoal/50 | charcoal/800 | |
| `text/primary` | neutral/Black | neutral/White | |
| `text/secondary` | charcoal/700 | charcoal/200 | |
| `text/muted` | **charcoal/600** | charcoal/300 | fixes WCAG 1.4.3 (was 3.41:1, now 6.39:1) |
| `text/on-fill` | charcoal/900 | charcoal/900 | text on mid-tone chart bars |
| `line/grid` | charcoal/100 | charcoal/800 | |
| `line/baseline` | charcoal/200 | charcoal/700 | |
| `line/border` | **neutral/Black-a10** (new) | **neutral/White-a10** (new) | was rgba 10% |
| `accent` | amber/500 | amber/400 | non-text only (4.04:1 / 7.12:1) |
| `status/good`, `active`, `hold`, `serious` | sage, cobalt, gold, coral steps | | steps chosen at build time by contrast |

The nav label (`#6b6a65` / `#a3a29a`) folds into `text/muted`.

## Ramps additions

1. **charcoal/900 = #1a1a19.** No step exists between charcoal/800 (#2e2e2c) and Black. The dark
   raised surface needs one.
2. **Alpha steps:** `neutral/Black-a10`, `neutral/White-a10` for borders, and `amber/500-a20`,
   `amber/400-a30` for emphasis fills, and `cobalt/500-a20`, `cobalt/400-a30` for focus fills. Named `alpha/<hue>-<step>-<percent>` in Figma. Figma color variables hold RGBA, so other collections can
   alias them.

## Emphasis fill (translucent amber)

Andrew likes the look of a translucent fill. Checked for accessibility on the page surfaces:

| Mode | Fill | Label text on fill | Emphasis line on fill |
|---|---|---|---|
| Light | amber/500 at 20% | 16.2:1 | 3.1:1 |
| Dark, today | amber/800 opaque | 10.4:1 | 4.7:1 |
| Dark, proposed | amber/400 at 30% | ~8:1 | ~3.6:1 |

A translucent fill passes. On a dark surface it reads as a warm glow, not a muddy brown block,
because the surface shows through. Opacity alone can't make it lighter than amber/800; the
higher alpha (30%) does that. Above about 40%, the emphasis line drops under 3:1 against the
fill.

`--chart-emphasis-fill` changes to the alpha steps. That's a change to Chart Semantic, so it is
listed here, not slipped in.

## Files

- Figma: Ramps additions; new Page collection with codeSyntax `--<css-name>`; Chart Semantic
  `flood/depth-1..3`, emphasis-fill re-aliased.
- `design-language/tokens/page.json` (same shape as `chart.json`); `ramps.json` additions.
- `docs/assets/page-tokens.css`, linked from every page. Per-page chrome blocks removed.
  Nav and footer partials use the variables.
- `tools/check_chart_tokens.py`: also checks `page.json` against `page-tokens.css` and fails on
  any raw hex in `docs/*.html` styles outside an allowlist.

## Follow-up: sun-solar 3D scene (2026-10-25)

The scene's raw colors now resolve to tokens. House, camper, and coop share a new Chart Semantic
`land/structure` (charcoal/200 light, charcoal/600 dark): the legend keys only the sun arcs, so the
three tans and blues were variety, not meaning. The pool is `water/body`, trees
`species layer/canopy`, hedgerows `species layer/shrub`. The JS `shade()` parsed hex, which a
`var()` can't give it. Each face now draws the token color plus a white or black overlay at the
old strength, so the scene follows a theme toggle with no script read.

## Deferred

- The sun-solar month colors (`monthColors`, annual sun-path chart): 8 of 12 months are raw hex.
- `--gsa-roof-1..4` on sun-solar equal Map Semantic `sun/*` exactly but are copied as hex. Map
  tokens have no CSS mirror yet.
- Labels over the aerial photo on sun-solar stay fixed dark-on-white-halo in both modes; they
  sit on a photo, not the page.

- Repurpose the 20 Tint/25, /50 paint styles to bind to alpha variables. Only if the alpha steps
  prove out.
- Any Ramps step beyond those listed.
