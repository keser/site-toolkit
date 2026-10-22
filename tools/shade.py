#!/usr/bin/env python3
"""Shadows and hours of direct sun from a lidar surface model.

- shadow_mask: which cells a given sun position leaves in shadow. A cell is shaded when, looking
  from it toward the sun, any surface along the ray rises above the line of sight.
- sun_hours: hours of direct sun per cell over a list of sun positions (from sun_arcs.day_arc).

Grids are north-up (row 0 is the north edge, column 0 the west edge), in feet. `surface` is the
first-return or max surface (roofs, canopy); `receptor` is the height to test at each cell, such
as bare earth plus a foot for plants, or the surface itself for roofs. Anything outside the grid
casts no shadow, so give the grid a margin of about twice the tallest nearby object's height.

Uses numpy only. Leaf-off lidar still records most branches, so deciduous canopy shades here as
if in leaf; treat winter results under deciduous trees as a lower bound on sun.
"""
import math

import numpy as np


def _shift(a, dr, dc):
    """out[r, c] = a[r + dr, c + dc], -inf outside the grid."""
    out = np.full(a.shape, -np.inf)
    h, w = a.shape
    r0, r1 = max(0, -dr), min(h, h - dr)
    c0, c1 = max(0, -dc), min(w, w - dc)
    if r0 < r1 and c0 < c1:
        out[r0:r1, c0:c1] = a[r0 + dr:r1 + dr, c0 + dc:c1 + dc]
    return out


def shadow_mask(surface, receptor, cell_ft, az, alt, max_dist_ft=None):
    """True where the sun at (az, alt) is blocked. az is degrees clockwise from north."""
    surface = np.asarray(surface, float)
    receptor = np.asarray(receptor, float)
    if alt <= 0:
        return np.ones(surface.shape, bool)
    tan = math.tan(math.radians(alt))
    rise = float(np.nanmax(surface) - np.nanmin(receptor))
    reach = rise / tan if rise > 0 else 0.0
    diagonal = math.hypot(*surface.shape) * cell_ft
    reach = min(reach, diagonal if max_dist_ft is None else max_dist_ft)
    east, north = math.sin(math.radians(az)), math.cos(math.radians(az))
    shaded = np.zeros(surface.shape, bool)
    seen = set()
    for k in range(1, int(math.ceil(reach / cell_ft)) + 1):
        dr, dc = -round(k * north), round(k * east)
        if (dr, dc) in seen:
            continue
        seen.add((dr, dc))
        dist = math.hypot(dr, dc) * cell_ft
        shaded |= _shift(surface, dr, dc) - receptor >= dist * tan
    return shaded


def sun_hours(surface, receptor, cell_ft, positions, step_minutes, max_dist_ft=None):
    """Hours of direct sun per cell; each (az, alt) position stands for step_minutes."""
    hours = np.zeros(np.shape(surface))
    for az, alt in positions:
        if alt <= 0:
            continue
        hours += ~shadow_mask(surface, receptor, cell_ft, az, alt, max_dist_ft)
    return hours * step_minutes / 60


def horizon_profile(surface, cell_ft, row, col, z0, azimuths, max_dist_ft=600, min_dist_ft=0):
    """Skyline seen from grid cell (row, col) at height z0: the highest elevation angle (degrees,
    floored at 0) of the surface along each azimuth. min_dist_ft skips the near field, such as a
    garden's own fence, which lidar records as solid."""
    surface = np.asarray(surface, float)
    h, w = surface.shape
    out = []
    for az in azimuths:
        east, north = math.sin(math.radians(az)), math.cos(math.radians(az))
        best = 0.0
        for k in range(1, int(max_dist_ft / cell_ft) + 1):
            r, c = round(row - k * north), round(col + k * east)
            if not (0 <= r < h and 0 <= c < w):
                break
            dist = math.hypot(r - row, c - col) * cell_ft
            if dist and dist >= min_dist_ft:
                best = max(best, math.degrees(math.atan2(surface[r, c] - z0, dist)))
        out.append(best)
    return out


def plane_factor(az, alt, slope=0.0, aspect=180.0):
    """Cosine of the sun's angle of incidence on a plane (slope degrees from horizontal, aspect the
    direction it faces, clockwise from north), floored at 0. Works on arrays of slope/aspect."""
    a, h = math.radians(az), math.radians(alt)
    s, asp = np.radians(slope), np.radians(aspect)
    return np.maximum(math.sin(h) * np.cos(s) + math.cos(h) * np.sin(s) * np.cos(a - asp), 0.0)


def clear_sky_dni(alt):
    """Direct normal irradiance on a clear day, W/m², Meinel's air-mass model. A weighting, not a
    forecast: real yield also depends on clouds, which this ignores."""
    if alt <= 0:
        return 0.0
    air_mass = 1 / math.sin(math.radians(alt))
    return 1353 * 0.7 ** (air_mass ** 0.678)


def solar_access(surface, receptor, cell_ft, positions, slope=0.0, aspect=180.0, max_dist_ft=None):
    """Share of the direct sun a surface would get unshaded (0..1), each sun position weighted by
    clear-sky DNI times its incidence on the surface (flat by default; pass slope/aspect arrays for
    roofs)."""
    got = np.zeros(np.shape(surface))
    total = np.zeros(np.shape(surface))
    for az, alt in positions:
        if alt <= 0:
            continue
        wgt = clear_sky_dni(alt) * plane_factor(az, alt, slope, aspect)
        total = total + wgt
        got = got + wgt * ~shadow_mask(surface, receptor, cell_ft, az, alt, max_dist_ft)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(total > 0, got / total, 0.0)
