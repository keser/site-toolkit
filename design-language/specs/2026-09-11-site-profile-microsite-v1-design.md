# Site Profile Microsite — V1 Design

Status: approved, pending implementation.

## Goal

A published "microsite" — `docs/` on `main`, served via GitHub Pages — that profiles
Lot #86 (58 Freestone Avenue, Portland, CT) in enough depth to be a real working
reference when designing the property's permaculture future: climate, solar, wind,
hazard risk to start, with watershed/water, species inventory, and zones/design to
follow in later phases.

This is a new subsystem for `permaculture-site-plan`, not a change to an existing one —
hence the full brainstorming-skill treatment rather than jumping straight to
implementation.

## Non-goals (this phase)

- The Water suite (9 reports, Lesson 5) — V2.
- Species Inventory (georeferenced aerial map, GPS-pinned observations) — V3. Already
  decided the exact-location policy extends to it (2026-09-11), but it's out of scope
  for V1 regardless — bigger port, deserves its own pass.
- A new Zones & Design page — V3. Unlike the other content, Lesson 4's zones/
  microclimates material (`pdc-pro-2026/lesson-04-design/work/*.md`) has never been built
  as an HTML report; this would be new content authoring, not a port. Bigger lift,
  deferred.
- A Phase Plan / Progress page duplicating `project-plan-overview.md` as HTML. That file
  already warns its own denormalized copy (`project-plan-overview.md` vs. the 5 phase
  files) needs updating in lockstep or it drifts — a third HTML copy triples that risk.
  If a progress-facing page is wanted later, it should link out to the GitHub-rendered
  markdown rather than duplicate the data.

## Architecture

```
permaculture-site-plan/
├── docs/                       — GitHub Pages root (serves as-is; .nojekyll disables Jekyll)
│   ├── .nojekyll
│   ├── index.html              — Home/Overview (new content)
│   ├── climate.html            — ported: lesson-01-climate/assets/climate-survey-charts.html
│   ├── sun-solar.html          — hub page (new, thin) linking the 3 sun-path reports
│   ├── sun-path-charts.html    — ported: lesson-03-site-analysis/assets/sun-path-charts.html
│   ├── sun-path-3d.html        — ported: lesson-03-site-analysis/assets/sun-path-3d.html
│   ├── sun-path-overlay.html   — ported: lesson-03-site-analysis/assets/sun-path-overlay.html
│   ├── wind.html               — ported: lesson-03-site-analysis/assets/wind-roses.html
│   ├── flood-hazard.html       — ported: lesson-03-site-analysis/assets/flood-risk-report.html
│   └── _partials/
│       ├── nav.html            — shared header/nav, source of truth
│       └── footer.html         — shared footer, source of truth
└── scripts/
    └── build-nav.py            — stamps _partials/* into every docs/*.html between marker comments
```

No subfolders under `docs/` for V1 — flat, matching the flat pattern already used in
`pdc-pro-2026`'s lesson asset folders. `sun-solar.html` is a lightweight hub (mirrors the
precedent set by `lesson-05-water/assets/index.html`), not a merge of the 3 reports —
each stays a full, independently-linkable page.

## Nav/footer mechanism

No generator, so no free templating — but hand-duplicating nav markup across 6+ pages is
real maintenance debt for a site that's about to grow to 15+ pages across V2/V3. Middle
ground: `docs/_partials/nav.html` and `footer.html` are edited once; every content page
carries `<!-- NAV:START -->…<!-- NAV:END -->` and `<!-- FOOTER:START -->…<!-- FOOTER:END -->`
marker comments; `scripts/build-nav.py` (plain Python, no dependencies) rewrites the
content between those markers from the partials. Output is still fully static — GitHub
Pages does zero processing at serve time — this only saves authoring effort, and only
runs locally, before a commit. **Must be re-run after any nav/footer edit or new page
before committing**, since nothing enforces freshness automatically.

## Content plan

| Page | Source | Notes |
|---|---|---|
| `index.html` | New — synthesized from `site-plan/site-profile.md` + `CLAUDE.md` | Address, coordinates, 0.43 ac, elevation range, Köppen class, hardiness zone, frost-free window, FEMA zone teaser, nav cards to each section (+ ghosted "coming soon" cards for Water/Species/Zones to signal the roadmap) |
| `climate.html` | `pdc-pro-2026/lesson-01-climate/assets/climate-survey-charts.html` | Temp, precip, wind (survey-level), frost-free/hardiness |
| `sun-solar.html` | New (thin hub) | Links to the 3 sun-path pages below |
| `sun-path-charts.html` | `.../lesson-03-site-analysis/assets/sun-path-charts.html` | |
| `sun-path-3d.html` | `.../lesson-03-site-analysis/assets/sun-path-3d.html` | |
| `sun-path-overlay.html` | `.../lesson-03-site-analysis/assets/sun-path-overlay.html` | |
| `wind.html` | `.../lesson-03-site-analysis/assets/wind-roses.html` | Deeper 10-yr KHFD station data; `climate.html` links here for the full picture |
| `flood-hazard.html` | `.../lesson-03-site-analysis/assets/flood-risk-report.html` | FEMA zone, First Street data |

Each ported page keeps its `.viz-root`-scoped CSS and inline SVG exactly as built —
no visual redesign, just: (1) wrap in the shared nav/footer via the marker comments,
(2) swap the address/coordinates in per the new public-location policy (most of these
were already written generically for the course deck, so this is often an addition
rather than a redaction), (3) spot-check for any third-party names before publishing —
unlikely in data/chart reports, but not yet verified.

## GitHub Pages

Enable via repo Settings → Pages → Source: `main` / `/docs`. **This is the step that
actually makes the site live and publicly reachable — do it as an explicit, confirmed
action once V1 content is ready, not automatically on first push to `docs/`.**

## Later phases (not designed yet)

- **V2 — Water suite:** port the 9 Lesson 5 reports + adapt their existing `index.html`
  hub. Bigger port, no new content-authoring risk.
- **V3 — Species Inventory + Zones & Design:** Species Inventory ports the georeferenced
  aerial/GPS map (policy already settled: publish as-is). Zones & Design is genuinely new
  content, authored from `pdc-pro-2026/lesson-04-design/work/*.md` rather than ported —
  bigger lift, gets its own design pass when it comes up.

Each later phase gets its own short spec in this folder before implementation, per the
brainstorming skill.
