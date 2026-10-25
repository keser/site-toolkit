# Site profile

What the site is today: its context, climate, energies, landform, water, soil, and living
systems. This is the as-is record. What the site should become goes in `design-brief.md`.

Fill sections in any order, but observe before deciding: a season of watching beats a guess.
Each finished section ends with **Findings for design**: its strengths, weaknesses,
opportunities, and threats, naming any tasks they affect by ID. Leave a quadrant as "none
identified yet" rather than padding it. The strongest findings roll up into `synthesis.md`.

Each section lists:
- **Answers:** the questions the section must settle.
- **Collect:** the data and observations to gather.
- **Watch for:** mistakes the demo site made, so the next site doesn't.
- **Toolkit:** tools, map sheets, and the demo page that shows a finished version.

Sources go in the table at the end. Note each source's license before anything from it is
published.

---

## 1. Location and history

**Answers**
- Where does the site sit, from region down to parcel? Which bioregion and ecoregion?
- How has the land changed over time: clearing, buildings, earthworks, regrowth?
- What exactly are the boundaries, and how sure are we?

**Collect**
- Regional-to-parcel context views, north up, each with a scale bar.
- Historic aerials (timeline imagery, state archives) at a few points in time.
- The parcel record: assessor card, deed, survey or permit plans, the state GIS parcel layer.
- Ground photos from each corner and from repeatable reference points (a gate, a tree, a building
  corner), so later photos can be compared.

**Watch for**
- Parcel sources can disagree. The demo lot is 0.43 ac by the survey and assessor, and 0.57 ac by
  the GIS polygon. Record both, use the surveyed plan until it's disproved, and find the pins.
- Historic imagery often has no clear reuse terms. Keep it private until the license is checked.
- A screenshot has no coordinates. To place points on one: derive feet per pixel from a traced
  shape of known length, anchor it with a geocoded address, then check both the traced area and
  where known features land.

**Toolkit:** `fetch_ct_eco.py` (Connecticut imagery, lidar, buildings), `fetch_s2cloudless.py`
(regional imagery). Sheets 01–04 (regional), 07 (base map).
Demo: [Site profile](https://keser.github.io/site-toolkit/index.html), [Base map](https://keser.github.io/site-toolkit/base-map.html).

## 2. Climate

**Answers**
- What is the climate type and hardiness zone?
- When are the wet and dry seasons? When does winter start and end? When are the frost dates?
- How strong and how consistent is the wind, and does it change by season?
- What is the worst-case storm (24-hour, 100-year rainfall)?

**Collect**
- Monthly temperature and precipitation normals from the nearest reliable station.
- Snow totals, frost-free period, hardiness zone.
- Hourly wind records, ideally 10 years, summarized by season.
- Design-storm depths from NOAA precipitation frequency data (or the local equivalent).

**Watch for**
- An annual wind rose can hide the real pattern. The demo site's annual rose read "W/SW." By
  season it's north in winter and south the rest of the year.
- If a number was read off a chart image, label it as an estimate. Prefer the higher-precision
  source when two cover the same thing.

**Toolkit:** Demo: [Climate](https://keser.github.io/site-toolkit/climate.html).

## 3. Sun and solar

**Answers**
- Where does the sun rise and set, and how high does it get, at each solstice and equinox?
- Which spots get enough direct sun for growing, by season?
- What casts shade: buildings, on-site trees, neighbors' trees? What would pruning change?
- Is the roof worth solar panels?

**Collect**
- Sun positions for the site's latitude and longitude.
- A surface model (lidar) or measured heights for buildings and trees.
- On-site shadow checks near the winter solstice.

**Watch for**
- A spot in full sun in July can be in shade all December. Check the low winter arc before
  counting on winter gain.
- Model the trees the site can't control (neighbors') separately from the ones it can.

**Toolkit:** `sun_arcs.py`, `shade.py`. Sheets 09 (sun paths), 24 (shadow study), 25 (sun hours).
Demo: [Sun & solar](https://keser.github.io/site-toolkit/sun-solar.html).

## 4. Sectors

**Answers**
- Which outside energies cross the site, and from which direction: sun, wind, fire, noise,
  views, wildlife, water, pollution, social and community influences?
- For each one: **use** it, **amplify** it, or **deflect** it, and why?

**Collect**
- Directions and seasons for each sector, drawn over the base map, which stays visible beneath.
- One sentence per sector on the response and the reason for it.

**Watch for**
- Social sectors (neighbors, roads, community resources) count as much as natural ones.
  Name neighbors by role only.

**Toolkit:** Sheets 05, 06 (community and neighborhood compasses), 08 (compass on the base map).
Demo: [Sectors](https://keser.github.io/site-toolkit/sectors.html).

## 5. Hazards and regional challenges

**Answers**
- Which natural hazards are realistic here: flood, fire, wind, ice, heat, drought, earthquake?
- What are the site's weakest points, and what has kept them from being fixed?
- What does doing nothing cost?
- Which community resources can the site lean on?

**Collect**
- FEMA flood maps and the National Risk Index (US), state wildfire and other hazard maps.
- A list of community resources: nurseries, compost and mulch sources, tool rental, extension
  services.

**Watch for**
- Look up native plant nurseries near the site early. A state extension list is a good start.

**Toolkit:** Sheet 23 (resilience brainstorm). Demo: [Flood risk](https://keser.github.io/site-toolkit/flood-hazard.html).

## 6. Landform and base map

**Answers**
- What is on the site today: structures, paths, utilities, trees, beds, landforms?
- Where are the high and low points, and which way does the ground fall?
- What does a section through the site show that a plan can't?

**Collect**
- A scaled, north-up base map of the whole site with a scale bar, built from the survey and aerial
  imagery and checked on the ground.
- Contours: 1 m bare-earth elevation data (USGS 3DEP in the US) or the state lidar.
- A transect for an elevation profile that shows terrain, structures, and vegetation layers.

**Watch for**
- Run the transect along the lot's true axis. A line held at one longitude runs due north, which
  is off-axis on most lots; the demo site's first profile was 25° off and reversed the conclusion
  about which end is high.
- Keep the base map grayscale so every overlay reads on top of it.

**Toolkit:** `terrain.py` (hillshade, contours, canopy height). Sheets 07 (base map), 28 (terrain
under canopy). Demo: [Base map](https://keser.github.io/site-toolkit/base-map.html), [elevation profile](https://keser.github.io/site-toolkit/water.html#elevation).

## 7. Water

**Answers**
- Where does water come from: rain, municipal supply, a well? How much does the household use, by
  season?
- Which watershed is the site in, and how much land drains onto it?
- Where does water enter, pool, move, and leave, including in a design storm?
- How much runs off roofs and paving in an average year and in a 100-year, 24-hour event?
- Where does wastewater go?

**Collect**
- Rainfall normals and the 24-hour record or design storm (from section 2).
- Watershed and catchment maps, from the regional basin down to the site's own catchment.
- Roof and surface areas, with runoff coefficients.
- Water bills for seasonal use. Never record the account number.
- The owner's on-site account of where water actually goes in heavy rain.

**Watch for**
- Check the model against what people have seen. The demo site's elevation data suggested one
  drainage story; the owner's on-site account corrected it.

**Toolkit:** Sheets 03, 04 (watersheds), 10 (site water flow), 11 (catchment area).
Demo: [Water](https://keser.github.io/site-toolkit/water.html).

## 8. Soil

**Answers**
- Which soil types are mapped on the site, and what do they mean for drainage, depth, and
  flooding?
- What does the soil actually look like where we dig?
- Where are the compaction, erosion, waterlogging, and signs of life?
- What compost and mulch resources exist on and off site?

**Collect**
- The USDA Web Soil Survey map for the site (US), or the local equivalent. For each soil type:
  farmland class, typical profile, drainage, depth to bedrock and water table, flood frequency,
  hydric rating.
- At least one test pit (three on larger sites), marked on the map. For each: jar texture test,
  texture by feel, profile photo with a ruler, percolation or infiltration test, and a soil
  health assessment (the NRCS in-field guide).
- Optional lab chemistry.

**Watch for**
- In frozen ground, run the tests as practice and repeat them after thaw.

**Toolkit:** Sheet 15 (soil sample locations).

## 9. Vegetation, species, and succession

**Answers**
- What grows and lives here now, and which species are native, introduced, or invasive here?
- What is the current successional stage, and what is the region's mature state?
- Where are the canopy, understory, and ground layers?

**Collect**
- A species inventory from on-site observation. Logging to iNaturalist gives photos, dates, and
  location through a public API.
- A plant list with an ID, position, layer, and status for each mapped plant.
- Canopy height from lidar; color-infrared and NDVI imagery for vigor.

**Watch for**
- Establishment data can be right in surprising ways. iNaturalist lists Eastern cottontail as
  introduced in Connecticut, and it is: it displaced the native New England cottontail. Check the
  regional ecology before "fixing" a status.
- How a plant behaves on this site beats a state list. A plant can be invasive here without being
  listed.

**Toolkit:** `imagery.py` (NDVI, color-infrared), `terrain.py` (canopy height). Sheets 16–19
(species maps, plant inventory), 20 (succession), 26, 27 (infrared, vegetation index), 29
(canopy height). Demo: [Species inventory](https://keser.github.io/site-toolkit/species-inventory.html).

## 10. Microclimates

**Answers**
- Which distinct pockets does the site have: hot and dry, cool and shaded, wet, sheltered,
  exposed?
- Which plants already thrive in each one? They hint at what else will.

**Collect**
- Mapped areas by sun, temperature, moisture, wind, and ground cover, each with at least one
  plant growing there.

**Toolkit:** Sheet 13. Demo: [Zones & design](https://keser.github.io/site-toolkit/zones-design.html#microclimates).

## 11. Current zones and access

**Answers**
- How is the site used today? Which areas get visited daily, weekly, seasonally, rarely?
- Which paths carry the most traffic?

**Collect**
- A map putting every part of the site in a zone of use, 1 to 5, with access paths by type and
  frequency.
- A table of what sits in each zone and what upkeep it gets.

**Watch for**
- This records how the site is used now, not the design. Proposed zones go in `design-brief.md`.
- On a small lot, the five zones may not all exist. Say so instead of forcing them.

**Toolkit:** Sheets 12 (zones), 14 (circulation). Demo:
[Zones & design](https://keser.github.io/site-toolkit/zones-design.html#current-zones).

---

## Sources

| Source | What it gave | Date | License / reuse terms | Where the original lives |
|---|---|---|---|---|
| | | | | |
