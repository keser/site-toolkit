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
