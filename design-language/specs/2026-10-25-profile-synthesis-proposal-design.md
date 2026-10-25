# Site profile: current state, synthesis, proposal

**Date:** 2026-10-25 · **Status:** built (demo microsite and template)

## Why
The demo profile grew out of PDC course lessons, so it read like coursework: lesson citations,
rubric-required content, design brainstorms mixed into analysis. The owner wants the profile to
work as a handoff artifact for landscape architects, engineers, and other designers proposing
work to a property owner. It could be sold to owners or used to start the owner's own design
proposals. The course is moving from analysis into design, so the profile needs a clear line
between "what is" and "what could be."

## Decisions
1. **Three parts.**
   1. *Current state:* the snapshot, constraints, and history.
   2. *Synthesis:* findings and open questions that come before design.
   3. *Proposal:* for Lot 86, the owner's project plan; for a client site, a design brief with
      phases tied to the owner's goals.

   The nav groups pages under those labels.
2. **SWOT at two levels.** The course required a brainstorm and SWOT at each step as a learning
   device. The owner kept the method and moved it: every current-state page ends with "Findings
   for design" (strengths, weaknesses, opportunities, threats), and `synthesis.html` rolls up the
   strongest ones before design starts. Facet-level brainstorms (the zone brainstorm) stay on
   their page and feed the synthesis's "Design ideas to test."
3. **Findings come from the page.** No finding is added that the page's own content doesn't
   support. Empty quadrants say "None identified yet."
4. **Course framing removed where it doesn't serve the reader.**
   - Source notes cite the original data, not lesson numbers or private repo paths.
   - The annual wind rose digitized from a course slide is removed; the seasonal roses from 10
     years of KHFD station data stay.
5. **Settled site facts applied everywhere.** The lot is 0.43 ac (1993 plan outline), and
   elevation is 103–110 ft (2023 CT ECO lidar inside the outline; the
   centerline profile alone runs 103.6–107.5 ft).

## Known gaps
- Resolved 2026-10-25: the zone, microclimate, and brainstorm images were re-exported from the
  corrected Figma sheets (12a, 13a, C01). The low point question was settled by the owner: the
  back-east corner is the lowest ground but absorbs most runoff (turf, mature trees, a
  needle-mulched spruce grove); the street-side corner is the practical low point for runoff.
- Data the intended audience is likely to want (zoning and setbacks, easements, wetlands,
  utilities, soils, a tree inventory with trunk diameters) is deferred until audience
  conversations after the course (`~/Code/keser/ROADMAP.md`).

## Template
`template/site-plan/` mirrors the structure: `site-profile.md` sections end in findings,
`synthesis.md` is new, and `design-brief.md` holds goals, design layers, and phases.
