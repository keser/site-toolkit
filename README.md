# site-toolkit

Tools, a design language, and a workspace template for permaculture site analysis and
design. Built so the same analysis can be run on any site, not just one.

**Demo:** the `docs/` folder is a published example microsite for one real property
(Lot #86, Portland, CT — the author's own, public by his decision). It is the reference
for what a finished site profile looks like. Images in the demo are labeled checkerboard
placeholders, not real site imagery.

## What's here

| Folder | What it is |
|---|---|
| `docs/` | Demo microsite (plain static HTML, GitHub Pages source). |
| `tools/` | Python helpers: `build_nav.py` stamps shared nav/footer into pages; `port_report.py` wraps a `.viz-root` report fragment into a page. Tests in `tools/tests/`. |
| `design-language/` | How maps, diagrams, and report pages share one visual system. Figma is the source of truth; this folder documents it and keeps the history. |
| `template/` | Starting point for a new site workspace. Copy it into a new **private** repo per site. |

## Starting a new site

1. Create a new private repo at `~/Code/keser/site-plans/<site-name>/` and copy `template/` into it.
   Every site repo lives in that one folder.
2. Fill in `CLAUDE.md` and `site-plan/phases.md`: phases are defined per site from its design
   goals and constraints; they are not fixed.
3. Keep private data (parcel records, survey scans, photos, utility details) out of git. The
   template's `.gitignore` excludes images, PDFs, and raw media by default.

## Privacy

Everything is private unless the owner has explicitly said otherwise. The demo property is the
only exception here. Never commit another site's address, parcel data, photos, or household
details to this repo. Never name neighbors or other private third parties.

## Status

Early. Tools and docs were extracted from the demo site's own repo. The analyses in the demo
are written for one property and have not yet been parameterized for other addresses.
