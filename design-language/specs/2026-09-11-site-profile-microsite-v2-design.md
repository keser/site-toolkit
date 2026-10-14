# Site Profile Microsite — V2 Design (Water Suite)

Status: approved, pending implementation.

## Goal

Add the Water section to the live microsite (https://keser.github.io/permaculture-site-plan/):
the 8 Lesson 5 water reports plus their hub page, reachable from Home and the shared nav.

No new architecture — V1 settled platform, tooling, and the relative-link requirement (the
Critical finding from V1's final review). V2 is content scope only, using the exact same
`scripts/port_report.py` / `scripts/build_nav.py` pipeline unchanged.

## Source inventory

`pdc-pro-2026/lesson-05-water/assets/`:

| File | Size | Notes |
|---|---|---|
| `precipitation-by-month.html` | 7.9K | |
| `runoff-by-surface.html` | 8.4K | |
| `water-balance.html` | 6.6K | |
| `elevation-sections.html` | 7.8K | |
| `site-flow-schematic.html` | 10.6K | |
| `design-storm-frequency.html` | 6.9K | |
| `macro-watershed-scale.html` | 9.3K | |
| `water-use-by-season.html` | 8.8K | Added later than the others — **not yet linked from the hub** (see below) |
| `index.html` | 6.1K | Hub page: JS-rendered card grid + 7 thumbnail `<img>`s. Hand-authored, not a plain `.viz-root` fragment split target the same way, but still splits cleanly on `<div class="viz-root">` |
| `thumb-*.png` (×7) | ~150K each | One per report **except** `water-use-by-season` |

**Known source defect to fix on port, not reproduce:** `index.html`'s `CARDS` array lists
only 7 of the 8 reports — `water-use-by-season.html` has never been wired into the hub. Fix
here (not upstream in `pdc-pro-2026` — out of scope for this repo to touch that one).

## Architecture (unchanged from V1)

- 8 reports → `docs/*.html` via `port_report.py` + `build_nav.py`, flat, same as V1.
- Hub → `docs/water.html` via `port_report.py`, then hand-edited to add the missing 8th
  card. Card renderer needs a small tweak to handle a card with no thumbnail image (render
  the `.thumb` div only when `c.img` is set, instead of assuming every card has one).
- 7 thumbnails → `docs/assets/thumb-*.png` (alongside V1's `parcel-aerial.jpg`), hub's
  `img src="thumb-X.png"` → `img src="assets/thumb-X.png"`.
- `docs/_partials/nav.html` gains a 5th link: Water → `water.html` (relative, per V1's fix).
- `docs/index.html` (Home): the "Watersheds & Water" card moves from the "Coming later"
  section (`<div class="nav-card soon">`, `V2` tag) to "Available now" (`<a class="nav-card">`,
  linking to `water.html`).

## Privacy / content checks (same bar as V1)

Exact address/coordinates expected and fine. Check each ported page + the hub for any
third-party name (unlikely — data/chart reports, same genre as V1's sources).

One redaction made: `water-use-by-season.html`'s source data included a real Town of
Portland water-utility account number, present in the subhead's "four consecutive bills"
mention and in the "Source:" citation line. Stripped from the ported `docs/` copy on the
grounds that an account number is identifying/sensitive in a way an address alone isn't
(the number itself isn't repeated here — see the note in this repo's `CLAUDE.md` for why);
the upstream `pdc-pro-2026` source file still has it and always will, so a future re-port
of this file needs to redact it again.

## Relative links (the V1 lesson)

Every internal link — in the 8 ported reports (none expected, they're standalone), the hub's
8 card `href`s, the nav addition, and the Home page edit — must be relative, never
root-absolute (`water.html`, not `/water.html`). Verify explicitly: `grep -rn 'href="/'
docs/` must return nothing, same bar as V1's final review.

## Out of scope (unchanged from V1's phasing)

Species Inventory and Zones & Design remain V3.
