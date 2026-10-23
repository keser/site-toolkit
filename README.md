# site-toolkit

Tools, a design language, and a workspace template for permaculture site analysis and
design. Built so the same analysis can be run on any site, not just one.

**Demo:** the `docs/` folder is a published example microsite for one real property
(Lot #86, Portland, CT — the author's family home and PDC Pro course site, public by the author's
decision). It is the reference for what a finished site profile looks like. Images in the demo
are labeled checkerboard placeholders, not real site imagery.

## How work flows

The toolkit sits at the end of a three-step path:

1. **Coursework** (`pdc-pro-2026`, private). Lessons for the PDC Pro certificate course, shaped by
   its rubric and submitted as slides on Canvas.
2. **Site plan** (`~/Code/keser/site-plans/<site>/`, private). Lesson work that's useful beyond
   the course graduates into a site plan. There it's rewritten as project plan and site analysis,
   not as a course deliverable. Lot 86 is the first site.
3. **Toolkit** (this repo, public). Each graduated lesson becomes a template section that works
   for any address.

The toolkit also feeds back into steps 1 and 2. Coursework and site plans use its tools and design
language, so the output stays consistent and maintainable as it grows. Beyond the course, the same
assets serve new site plans, analyses and stakeholder presentations.

**Sections first, tools later.** Once a lesson has worked on a real site, its structure goes into
`template/`: headings, the questions to answer and the data to collect. Tools and pages are
generalized only when a second site actually needs them.

The whole setup is also a portfolio piece for andrewkeser.com. It documents the process of using
AI to support this kind of workflow, and how that work draws on design-systems practice.

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

### Later: kickoff research lookups

To design when the deep-research phase of starting a new site gets focus. That phase needs a
set of location-based lookups to run for every new site. The first one found so far:

- **Native plant nurseries near the site.** It came up while sourcing plants for the demo
  site's Lesson 8 plant system design. A state extension list is a good starting source. In
  Connecticut it's UConn's
  [native plant availability and nursery list](https://ipm.cahnr.uconn.edu/native-plant-availability-nurseries/),
  which gives each nursery's town and marks retail or wholesale. Filter it by distance from the
  site, then check each nursery's season and hours.

Add more lookups here as other lessons turn them up.
