# Site Profile Microsite — V3b Design (Zones & Design)

Status: approved, pending implementation.

## Goal

Add the Zones & Design section to the live microsite. Unlike every prior phase, there is
no existing HTML report to port — the source is three markdown files
(`pdc-pro-2026/lesson-04-design/work/{microclimates,current-zones,zones-brainstorm}.md`,
516 lines total) plus 9 raw Figma-export PNGs (~13MB). This is new content authoring,
using the same visual pattern as every other page, not a mechanical port.

## Scope split: hub + 3 sub-pages

Same shape as Water (V2) and Sun & Solar (V1) — a topic with multiple distinct pieces
gets a thin hub linking to full pages, rather than one long page:

| Page | Source | Content |
|---|---|---|
| `docs/zones-design.html` (hub) | new | 3 cards linking to the sub-pages below |
| `docs/microclimates.html` | `microclimates.md` | 4 microclimate types, 2 images, 61-species list (27 native / 34 introduced), observations & ideas |
| `docs/current-zones.html` | `current-zones.md` | 5 current zones, existing-conditions matrix, 5 images (map + 4 photos), SWOT |
| `docs/zones-brainstorm.html` | `zones-brainstorm.md` | 6 brainstorm Q&A, 6 zone-1 photos with annotations, brainstorm map + per-zone callouts, proposed future-state matrix |

Every page carries all text verbatim from its source markdown (this is a permaculture
course record — the content is Andrew's own analysis, not something to paraphrase or
"improve"). `zones-brainstorm.html` keeps the source's own framing that it's a brainstorm,
not committed design — same "this is exploratory" note the markdown itself carries.

**Verbatim policy, precise:** typo and subject/verb-agreement corrections are permitted
without being individually flagged (e.g. the source's own `[sic]` markers, or an obvious
slide-transcription slip). Wording, voice, and grammatical person are never altered —
first-person "I"/"we" stays first-person, an active sentence stays active. Any content
change beyond typo-fixing (e.g. the neighbor-privacy rewordings this phase needed) must
be called out explicitly in the plan, with its own verification check, not folded
silently into a "transcription." This line exists because the implementation phase
violated it once — a review caught several sentences silently rewritten from first
person to passive/impersonal voice, which got reverted — and the rule wasn't written
down anywhere until after that happened.

## Images: compress before embedding

9 source PNGs, raw Figma slide exports, 368KB–2.5MB each (~13MB total) — un-web-optimized.
Recompress each via `sips` (built into macOS, no new dependency): resize to max width
1200px, convert to JPEG at quality 65. Tested on 3 representative files: 1.4MB→166KB,
2.5MB→290KB, 368KB→140KB — comparable to the site's existing image sizes (V1/V2's
thumbnails run 100–175KB). Store at `docs/assets/zones-design/` (a subfolder, since this
is 9 files versus the 1–7 files other pages needed — keeps `docs/assets/` from becoming a
flat pile of 16+ unrelated images).

| Source file | New filename |
|---|---|
| `slide-64-microclimates-aerial-drone-photo.png` | `docs/assets/zones-design/microclimates-aerial.jpg` |
| `slide-65-current-microclimate-map.png` | `docs/assets/zones-design/microclimates-map.jpg` |
| `slide-69-current-zones-map.png` | `docs/assets/zones-design/current-zones-map.jpg` |
| `slide-71-current-zone-strengths-1.png` | `docs/assets/zones-design/current-zones-strengths-1.jpg` |
| `slide-72-current-zone-strengths-2.png` | `docs/assets/zones-design/current-zones-strengths-2.jpg` |
| `slide-77-zone-01-nw-side-yard-1.png` | `docs/assets/zones-design/brainstorm-zone1-nw-1.jpg` |
| `slide-78-zone-01-nw-side-yard-2.png` | `docs/assets/zones-design/brainstorm-zone1-nw-2.jpg` |
| `slide-79-zone-01-se-side-yard.png` | `docs/assets/zones-design/brainstorm-zone1-se.jpg` |
| `slide-80-zone-brainstorm-map.png` | `docs/assets/zones-design/brainstorm-map.jpg` |

## Visual pattern (unchanged)

Same `.viz-root` CSS system as every hand-authored page (`index.html`, `sun-solar.html`,
`water.html`'s hub styling) — light/dark aware, `body { margin: 0; }` (see the CLAUDE.md
checklist item this repo already has for hand-authored pages), inline styling, no
framework. Tables for the zone matrices (matching the markdown tables' structure exactly).
Photo credits ("PHOTO BY ANDREW KESER, ...") kept as captions, matching how ported pages
already cite sources.

## Privacy

Content already scrubbed at the source (the markdown files use "neighbors" / "the
neighbors driveway" generically, never a name — consistent with this repo's privacy
convention). No new redaction needed. Exact address/coordinates permitted as usual.

## Relative links

Same bar as every prior phase: `grep -rn 'href="/' docs/` and `grep -rn 'src="/' docs/`
must both return nothing.

## Nav / Home page

Nav gains one link: Zones & Design → `zones-design.html`, last position (after Species
Inventory). Home page's remaining "Coming later" card (currently tagged `V3b`) moves to
"Available now" — after this ships, "Coming later" is empty; the whole section (heading +
divider before it, if visually needed) should be removed from the Home page rather than
left as an empty section header with no cards under it.
