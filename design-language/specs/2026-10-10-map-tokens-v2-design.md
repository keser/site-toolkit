# Map Tokens v2 — Shade / Base / Tint, Fill Styles, Stroke Weights

Status: built 2026-10-11 — see site-plan/plans/2026-10-10-map-tokens-v2.md; manual follow-ups and open decisions listed there. Extends
[2026-09-28-map-design-system-design.md](2026-09-28-map-design-system-design.md), which is
complete. That spec's Phase 6 ("Layer Styles") introduced the two-step `Shade`/`Tint` tone
axis that this spec replaces.

## Goal

Give every key element on the maps of the PDC Pro Vision Figma file
(`aF9SVeTLwFN8PCEiU2OSBQ`) a predefined fill, outline, and stroke weight to pick from, instead of
hand-set values:

- Three semantic color roles per hue, each with a clear job and a validated text pairing.
- Fill styles for every role as a solid, plus translucent Tint styles for map overlays.
- A fixed stroke-weight scale bound to variables.
- A written, copyable record of the line treatments Figma can't store as tokens (dash
  patterns, line ends).

## Why now

Andrew compared the current tokens against the colors he hand-picked for the Sector Analysis
maps (frame `sector-analysis-comparison`, `724:4690`, on the Keys page). His picks are lighter
than both current tokens. They sit between steps 100 and 400, chosen per hue. Every pick
passes WCAG AA for normal text with black text (6.1–15.8:1), which is how Sector Analysis uses
them. The current `Tint` (step 500) is borderline for text either way (4.0–5.2:1), so it suits
lines and markers better than text-bearing fills.

The Keys page also uses eight stroke weights (1, 1.5, 2, 3, 4, 5, 6, 8), but `Line Sample`
defines only three (1, 2, 3).

## Decisions (resolved 2026-10-10)

| Fork | Options considered | Chosen | Why |
|---|---|---|---|
| Role structure | Two roles (repoint Tint) · three roles | **Shade / Base / Tint** | Lines and textless markers need a mid-strength color. Step 500 is the only step neither too pale nor too dark over the aerial base. |
| Fill-style set | Tint+Shade × opacity + Base solid (70) · full set (90) · solid only (30) | **Full set, 90 → trimmed to 50 on 2026-10-11** | Built as 90. After testing, Andrew found only the Tint is used translucent (map overlays); solid fills serve captions, sector overlays, and lines. The 40 Shade/Base 25/50 styles were deleted. |
| Stroke scale | Keep all 8 · consolidate to 6 · keep 3 | **6: 1 / 2 / 3 / 4 / 6 / 8** | Drops the near-duplicates 1.5 and 5 while the keys are being restyled anyway. |
| Weight names | Literal (`weight/4`) · tiers | **Tiers (`xs`–`2xl`)** | A value can be retuned without the name becoming wrong. |
| Theme mechanism | Component variants · variable modes | **Variants on `caption.Style`** | Matches the existing `Mode = Light \| Dark` variants on `Sector Compass Key` and `Sector Diagram`. Can be backed by modes later without breaking instances. |
| Migration | Repoint `Tint` in place · rename `Tint` → `Base`, add new `Tint` | **Rename, then add** | No map changes color until Andrew chooses. Existing bindings keep their variable IDs. |
| Translucent styles (revised 2026-10-11) | Variable-bound (renders opaque) · RGBA variables (static copies + re-sync) · raw-color /25 /50 styles | **Raw-color /25 and /50** | Bound styles render at 100% in Figma. RGBA variables can't alias the ramps, so they need the same re-sync with 60 extra variables. |
| Translucent styles (revised 2026-10-25) | Keep raw /25 /50 · bind to Ramps alpha copies | **Bind to Color Roles `<hue>/Tint/<25|50>`, which alias `alpha/<hue>-<step>-<25|50>`** | Reverses 2026-10-11. The role layer keeps the chain Ramps → Color Roles → style, the same as the /100 styles, so a Tint step change is made once in Color Roles plus its two alpha copies. Only 20 styles remain (not 60), Ramps already holds alpha steps for the Page tokens, and `check_chart_tokens.py tokens` now flags alpha drift from the repo. The copies still need a manual re-sync after a ramp change. Rendering verified: Tint 50 samples at the expected 50% blend. |
| Amber Tint | amber/200 · amber/300 | **amber/300** | amber/200 matches coral/200's contrast exactly (12.5:1), and coral and amber are already the closest hue pair (23.3°). amber/300 (9.3:1) separates them by lightness. |

## 1. Color tokens — `Map Overlay` collection

`Ramps` (92 primitives) is unchanged. `Map Overlay` grows from 20 to 30 aliases:

| Token | Step | Use | Text on it |
|---|---|---|---|
| `<hue>/Shade` | 700 (unchanged) | Dark-theme fills, strong outlines | White, 9.1–10.4:1 |
| `<hue>/Base` | 500 | Lines, strokes, markers without text | None. 4.0–5.2:1 either way. |
| `<hue>/Tint` | Per hue, below | Light-theme fills | Black, 6.1–15.8:1 |

Tint steps: violet 300, teal 300, magenta 400, slate 200, cobalt 200, coral 200, charcoal 300,
gold 100, sage 400, amber 300.

- The 10 current `<hue>/Tint` variables are **renamed** to `<hue>/Base`. Their IDs and their
  step-500 aliases are kept.
- The 10 new `<hue>/Tint` variables are created, scoped `ALL_FILLS, STROKE_COLOR` like the rest
  of the collection.
- Every variable's description states its role, its step, and its validated text pairing.
- `Chart Categorical` is out of scope. It serves the HTML charts, not the maps.

## 2. Fill styles (50 paint styles)

- Five per hue (revised 2026-10-11): `Shade/100`, `Base/100`, `Tint/100`, `Tint/50`, `Tint/25`.
  Named `<hue>/<Role>/<opacity>`, for example `sage/Tint/25` or `amber/Shade/100`. The style
  picker nests them as hue › role › opacity.
- Each style is one solid paint with opacity 25, 50, or 100% set on the paint. Opacity lives in
  styles for two reasons:
  - paint opacity can't be bound to a variable;
  - layer opacity would fade a layer's stroke along with its fill.
- **/100 styles bind their color to the `Map Overlay` variable. Tint /50 and /25 styles hold a raw copied
  color** (revised 2026-10-11). Figma overwrites a variable-bound paint's opacity with the variable's
  alpha, so bound /25 and /50 styles rendered at 100%. The cost: after any Ramps or `Map Overlay`
  change, the 20 translucent styles must be re-synced (plan Task 3 re-sync rule, with a drift
  check).
- The 20 existing paint styles are **renamed**, not recreated, so anything using them keeps its
  style ID:
  - `<hue>/Shade` becomes `<hue>/Shade/100`;
  - `<hue>/Tint` becomes `<hue>/Base/100`, since it is bound to the variable being renamed to
    Base.
- The other 70 were new; on 2026-10-11 the 40 Shade/Base 25/50 styles were deleted, leaving 50.
- The same styles apply to strokes.

## 3. Stroke weights — new `Stroke` collection

One mode, six number variables, scoped to `STROKE_FLOAT` only:

| Variable | Value |
|---|---|
| `weight/xs` | 1 |
| `weight/sm` | 2 |
| `weight/md` | 3 |
| `weight/lg` | 4 |
| `weight/xl` | 6 |
| `weight/2xl` | 8 |

No opacity variables (styles carry opacity) and no effect or halo styles (nothing in the keys
uses them yet).

## 4. Components

No variant axis is removed, so no existing instance loses its variant.

- **`Line Sample`** (`472:867`):
  - The Weight axis stays. Each variant's weight is bound to a tier: Thin → `xs`, Standard →
    `sm`, Heavy → `md`.
  - The heavier tiers (`lg`, `xl`, `2xl`) are set by overriding the bound variable on an
    instance, not by adding variants. The full cross would be 54 variants.
  - Default stroke color is `charcoal/Base/100`.
- **`Site Marker`** (`473:862`):
  - Dot and Icon fill with `Base/100`, since they carry no text.
  - Numbered fills with `Shade/100` with white text, because Base fails text contrast both ways.
  - Marker strokes are bound to weight tiers.
- **`Legend Row`** (`480:889`), `Area` variant. The outline is one step darker than the fill:

  | Fill | Outline |
  |---|---|
  | Tint | Base |
  | Base | Shade |
  | Shade | Shade |

  Fills use the opacity styles. This replaces the 2026-09-29 "same hue, darker step" rule with
  a specific mapping.
- **`caption`** (`640:4373`). `Style` grows from Light/Dark to four values. `Size` (SM/LG) is
  unchanged.

  | Style | Fill | Text | Outline |
  |---|---|---|---|
  | Light | `<hue>/Tint/100` | Black | — |
  | Dark | `<hue>/Shade/100` | White | — |
  | White | White at 85% (the 2026-09-29 documented default) | Black | `<hue>/Base/100` |
  | Black | Black | White | — |

  The hue is chosen by rebinding the fill or outline on each instance.

## 5. Line-treatment reference sheet

A new frame on the Styles page (`699:2080`):

- **Layout:** one row per Dash × Cap combination, one column per weight tier.
- **Samples:** each is bound to its weight variable, stroked `charcoal/Base/100`, and labeled
  with its exact values, for example "Fine [2,2] · Single · sm (2)".
- **Purpose:** it is the only written record of dash patterns and line ends, which can't be
  variables or styles. The sheet is the canonical source for those values.
- **Workflow:**
  1. Copy properties (⌥⌘C) from a sample.
  2. Paste properties (⌥⌘V) onto a map path.
  3. Pick a color style.
- **Unverified:** whether pasted properties carry variable bindings. Test this on one path
  during the build and record the result on the sheet.
- **Known issue, not solved here:** dash patterns are fixed lengths, so `Fine [2,2]` reads as
  dots at `2xl` (8). The sheet makes this visible. Scaling dashes per tier is a possible
  follow-up.

## 6. Build order and verification

Each step is safe to re-run and is checked before the next starts.

1. **Color variables:** rename the 10 `Tint` variables to `Base`, then add the 10 new `Tint`
   variables. *Check:* the 20 fills previously bound to Tint keep their exact color, now bound
   to Base. The collection has 30 variables.
2. **Stroke weights:** create the `Stroke` collection and its 6 variables. *Check:* values and
   scopes.
3. **Paint styles:** rename the 20 existing styles, then create the other 70. *Check:* 50
   styles at the right opacity; /100 bound to the right variable, /25 and /50 holding the role's
   current color.
4. **Components:** update the four component sets. *Check:* a screenshot of each, plus a count
   showing existing instances still point at the same variants.
5. **Bind exact-match weights on the Keys page:** strokes of exactly 1, 2, 3, 4, 6, or 8 get
   bound to their tier, with no visual change. Strokes of 1.5 and 5 are left alone. *Check:*
   before and after counts by weight.
6. **Styles page sync:**
   - Rebuild the Semantic Tokens frame with three groups (Tint, Base, Shade).
   - Add a Fill Styles frame: hue rows × nine role/opacity columns, on a mid-grey background
     so the 25% and 50% styles read. (Background removed 2026-10-12; see the v3 spec's
     "Styles page revisions".)
   - Add a Stroke frame, after the website file's Dimension frame.
   - Add the line-treatment sheet.
7. **Comparison frame** (`724:4690`): replace the duplicate cobalt row with amber.

## Manual follow-ups (Andrew's design calls)

The plan produces a checklist of node IDs for each:

- Which former-Tint fills, now Base, should switch to the new lighter Tint.
- Which of the 41 Shade-colored strokes on the Keys page should move to Base.
- Whether each of the seven 1.5 strokes goes to 1 or 2, and each of the thirteen 5 strokes to
  4 or 6.

## Out of scope

- The Base Map retrofit (deferred indefinitely 2026-09-29) and the Sector Analysis page.
- `Chart Categorical` and the HTML dataviz palette.
- Variable modes for theming.
- Effect and halo styles.
- Per-tier dash scaling.
