# Site Profile Microsite — V3a Design (Species Inventory)

Status: approved, pending implementation.

## Goal

Add the Species Inventory page to the live microsite. No hub needed — a single page,
linked directly from nav and Home, same pattern as Climate/Wind/Flood & Hazard.

## Source

`pdc-pro-2026/lesson-08-gardens-animals/assets/species-inventory.html` (52.8K). Data
(observation points, composition stats, photo catalog) is fully embedded as JS arrays —
no live API calls. Photo thumbnails hotlink to iNaturalist's own public open-data S3
bucket (`inaturalist-open-data.s3.amazonaws.com`) — leave these as external references,
that's iNaturalist's sanctioned public CDN for exactly this use, not a private hotlink.

One local asset dependency: `<img src="parcel-aerial.jpg" ...>` for the site map. Already
available at `docs/assets/parcel-aerial.jpg` (copied there in V1's Sun Path Overlay fix) —
reuse it, don't re-copy.

(`species-inventory-slide.html`, the 12K static Figma-slide export version, is out of
scope — the interactive page is the real content; the slide version is a course-slide
artifact, not something a site visitor needs.)

## Architecture (unchanged from V1/V2)

- `docs/species-inventory.html` via `port_report.py` + `build_nav.py`.
- Nav gains a 6th link: Species Inventory → `species-inventory.html`, positioned after
  Water (chronological: Climate L1, Water L5, Sun/Wind/Flood L3 — actually current order
  is Climate/Water/Sun/Wind/Flood, not strictly chronological; place Species Inventory
  last since it's Lesson 8, latest in course order).
- Home page: move its card from "Coming later" to "Available now" (last position, matching
  nav order), same mechanic as V2's Water card move.

## Privacy / content checks

GPS/exact-location policy already settled (2026-09-11, same day as the general address
policy): publish the georeferenced map as-is. Standard checks apply: no third-party names
in visible text (the photo catalog and observation data are all species/taxonomy, not
people — low risk, verify anyway).

## The parcel-aerial.jpg path needs fixing on port (same as V1's Task 7b)

The source's `<img src="parcel-aerial.jpg" ...>` is a bare relative path that worked in
the source repo's own folder (image sat alongside the HTML). It does **not** resolve in
`docs/`, where the image lives at `docs/assets/parcel-aerial.jpg`. Fix the `src` to
`assets/parcel-aerial.jpg` after porting — same mechanical fix as V1's Sun Path Overlay,
except this time the destination asset already exists, so no copy step is needed, only
the path edit.

## Relative links (the V1 lesson, still binding)

Same bar: `grep -rn 'href="/' docs/` must return nothing after this change, and
`grep -rn 'src="/' docs/` likewise, including the fixed parcel-aerial reference above.

## Out of scope

Zones & Design is V3b — separate spec (new content authoring, not a port).
