# Site Profile Microsite V3a Implementation Plan (Species Inventory)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Species Inventory page to the live microsite, reachable from nav and Home.

**Architecture:** No new tooling — reuses `scripts/port_report.py` and `scripts/build_nav.py` unchanged. One port, one path fix (parcel-aerial.jpg, reusing the asset already copied in V1), one nav+Home edit.

**Tech Stack:** Same as V1/V2.

**Spec:** `site-plan/specs/2026-09-11-site-profile-microsite-v3a-design.md`

## Global Constraints

- No changes to `port_report.py` or `build_nav.py`.
- Every internal link relative, never root-absolute — `grep -rn 'href="/' docs/` and `grep -rn 'src="/' docs/` must both return nothing, every task.
- iNaturalist S3 photo URLs (`https://inaturalist-open-data.s3.amazonaws.com/...`) are expected external references — do not flag or try to localize them.
- Exact address/coordinates/GPS map data permitted; third-party names never permitted.
- `build_nav.py` re-run (and output committed) after any partial edit or new page.

---

### Task 1: Port Species Inventory, fix the parcel-aerial.jpg path

**Files:**
- Create: `docs/species-inventory.html`

**Interfaces:**
- Consumes: `scripts/port_report.py` and `scripts/build_nav.py` CLIs, unchanged. Consumes the existing `docs/assets/parcel-aerial.jpg` (from V1) — do not re-copy it.

- [ ] **Step 1: Port**

```bash
python3 scripts/port_report.py /Users/andrewkeser/Code/keser/pdc-pro-2026/lesson-08-gardens-animals/assets/species-inventory.html docs/species-inventory.html
```

- [ ] **Step 2: Fix the image path**

Find `<img src="parcel-aerial.jpg"` in the ported file (there should be exactly one) and
change it to `<img src="assets/parcel-aerial.jpg"`. Confirm `docs/assets/parcel-aerial.jpg`
already exists (it does, from V1) — do not copy a new one.

- [ ] **Step 3: Stamp and verify**

```bash
python3 scripts/build_nav.py
```

Expected: `docs/species-inventory.html` reported stamped.

```bash
grep -c 'src="assets/parcel-aerial.jpg"' docs/species-inventory.html   # expect: 1
grep -c 'src="parcel-aerial.jpg"' docs/species-inventory.html   # expect: 0 (the un-fixed path should be gone)
grep -rn 'href="/' docs/species-inventory.html   # expect: nothing
grep -rn 'src="/' docs/species-inventory.html   # expect: nothing
```

Confirm exactly one NAV region and one FOOTER region, both stamped. Confirm content
fidelity against the source (diff the post-split body against the source's `<div
class="viz-root">` content, accounting for the one intentional path-fix line). Read
through the visible text for any third-party name (species/taxonomy data — low risk,
check anyway). You likely don't have a browser tool — substitute reading the file
structurally as in prior tasks.

- [ ] **Step 4: Commit**

```bash
git add docs/species-inventory.html
git commit -m "Port Species Inventory report"
```

---

### Task 2: Add Species Inventory to the nav and move its Home page card

**Files:**
- Modify: `docs/_partials/nav.html`
- Modify: `docs/index.html`

**Interfaces:**
- Consumes: `docs/species-inventory.html` (Task 1).

- [ ] **Step 1: Add to the nav partial**

In `docs/_partials/nav.html`, the `.site-nav__links` div currently reads:

```html
  <div class="site-nav__links">
    <a href="climate.html">Climate</a>
    <a href="water.html">Water</a>
    <a href="sun-solar.html">Sun &amp; Solar</a>
    <a href="wind.html">Wind</a>
    <a href="flood-hazard.html">Flood &amp; Hazard</a>
  </div>
```

Add `<a href="species-inventory.html">Species Inventory</a>` as the last link (after
Flood & Hazard):

```html
  <div class="site-nav__links">
    <a href="climate.html">Climate</a>
    <a href="water.html">Water</a>
    <a href="sun-solar.html">Sun &amp; Solar</a>
    <a href="wind.html">Wind</a>
    <a href="flood-hazard.html">Flood &amp; Hazard</a>
    <a href="species-inventory.html">Species Inventory</a>
  </div>
```

- [ ] **Step 2: Move the Home page card**

In `docs/index.html`, the "Coming later" section currently reads:

```html
    <h2 class="section-head">Coming later</h2>
    <div class="card-grid">
      <div class="nav-card soon">
        <h3>Species Inventory</h3>
        <p>A georeferenced site map of observed species, from iNaturalist field data.</p>
        <span class="tag">V3</span>
      </div>
      <div class="nav-card soon">
        <h3>Zones &amp; Design</h3>
        <p>Current permaculture zones and the design brainstorm for their future.</p>
        <span class="tag">V3</span>
      </div>
    </div>
```

Remove the Species Inventory `<div class="nav-card soon">` block (leaving only Zones &
Design in "Coming later"), and add a real linked card to the end of "Available now":

```html
      <a class="nav-card" href="species-inventory.html">
        <h3>Species Inventory</h3>
        <p>A georeferenced site map of observed species, from iNaturalist field data.</p>
      </a>
```

(append it after the existing last card in "Available now" — read the current file to
find the exact insertion point, the "Available now" grid's closing `</div>` tag.)

- [ ] **Step 3: Re-stamp and verify**

```bash
python3 scripts/build_nav.py
```

Expected: every `docs/*.html` page reports stamped (nav partial changed).

```bash
grep -c 'species-inventory.html' docs/_partials/nav.html   # expect: 1
grep -c 'nav-card soon' docs/index.html   # expect: 1 (only Zones & Design left)
grep -rn 'href="/' docs/   # expect: nothing
```

- [ ] **Step 4: Commit**

```bash
git add docs/_partials/nav.html docs/index.html
git commit -m "Add Species Inventory to the nav and move its Home page card to Available now"
```

Note: this commit's diff will show every `docs/*.html` file changed (re-stamped nav) —
expected, stage and commit all of it.

---

### Task 3: Final verification

**Files:** none created — verification only.

- [ ] **Step 1: Test suite**

```bash
python3 -m pytest scripts/tests/ -v
```

Expected: 16/16 pass.

- [ ] **Step 2: build_nav.py no-op**

```bash
python3 scripts/build_nav.py
```

Expected: `0 file(s) updated`.

- [ ] **Step 3: Site-wide link crawl**

```bash
ls docs/*.html | wc -l
```

Expected: 18 (17 from V1+V2, plus this task's 1 new page).

For every file, extract every internal `href`/`src` and confirm targets exist. Confirm
zero root-absolute references anywhere (`grep -rn 'href="/' docs/` and `grep -rn 'src="/'
docs/`). Confirm `docs/species-inventory.html` is reachable from nav (all 18 pages) and
from `docs/index.html`'s "Available now" grid. Confirm no third-party names anywhere in
the new page.

- [ ] **Step 4: Commit if anything needed fixing**

If Step 3 found and you fixed something, commit with a clear message. Otherwise no
commit — report the clean result.

## Self-Review Notes

- **Spec coverage:** port + path fix (Task 1), nav + Home wiring (Task 2), verification
  (Task 3) — matches the spec's full scope.
- **Placeholder scan:** none found; every step has concrete commands or exact text.
- **Consistency:** Task 2's "before" text captured from the live files at plan-writing
  time; if either file has since changed, the implementer should stop and report
  NEEDS_CONTEXT rather than guess.
