# Microsite patterns

Extracted from the demo site's conventions. The authoritative copy for rules is `../CLAUDE.md`;
this file is the rationale.

- **Plain static HTML.** Chosen over Jekyll/Docusaurus to match the self-contained `.viz-root`
  report pattern and avoid a build step. Pages serves `docs/` as committed (`docs/.nojekyll`).
- **Relative links only.** The site is project-scoped, not a domain root, so `/page.html` 404s.
- **`body { margin: 0; }`** on hand-authored pages, or a white border shows around `.viz-root`.
- **Prefix rule for long pages.** Several visualizations share one page, so every non-shared
  CSS identifier needs a per-section prefix, and each script gets its own IIFE.
- **Shared nav/footer without a generator.** Partials + marker comments + `tools/build_nav.py`.
- **Porting.** `tools/port_report.py` splits a report fragment at `<div class="viz-root">`
  (head above, body from there) and wraps it in a full page with empty NAV/FOOTER markers.
