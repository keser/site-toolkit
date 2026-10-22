#!/usr/bin/env python3
"""Terrain and canopy views from lidar rasters.

- hillshade: relief shading of a bare-earth grid, so the ground under tree canopy reads.
- contour_segments: marching-squares contour line segments at one level, in fractional grid
  (row, col) coordinates. Segments are not stitched; draw them as one path per level.
- canopy_height: height of whatever stands on the ground (surface minus bare earth), with
  CT ECO's "0 = no lidar return" cells treated as bare ground.

Grids are north-up (row 0 is the north edge). Uses numpy only.
"""
import math

import numpy as np


def hillshade(dem, cell, az=315, alt=45):
    """0..1 shading for a sun at azimuth az (clockwise from north) and altitude alt."""
    dem = np.asarray(dem, float)
    d_row, d_col = np.gradient(dem, cell)
    dz_east, dz_north = d_col, -d_row
    slope = np.arctan(np.hypot(dz_east, dz_north))
    aspect = np.arctan2(-dz_east, -dz_north)  # direction the slope faces, clockwise from north
    a, h = math.radians(az), math.radians(alt)
    shade = math.sin(h) * np.cos(slope) + math.cos(h) * np.sin(slope) * np.cos(a - aspect)
    return np.clip(shade, 0, 1)


def contour_segments(z, level):
    """[((r0, c0), (r1, c1)), ...] where the surface crosses `level`."""
    z = np.asarray(z, float)
    tl, tr, bl, br = z[:-1, :-1], z[:-1, 1:], z[1:, :-1], z[1:, 1:]
    rows, cols = np.mgrid[0:z.shape[0] - 1, 0:z.shape[1] - 1]

    def edge(a, b):
        crossed = (a < level) != (b < level)
        with np.errstate(invalid="ignore", divide="ignore"):
            t = np.where(crossed, (level - a) / (b - a), 0.0)
        return crossed, t

    top_x, top_t = edge(tl, tr)
    right_x, right_t = edge(tr, br)
    bottom_x, bottom_t = edge(bl, br)
    left_x, left_t = edge(tl, bl)
    pts = {  # each edge's crossing point in (row, col)
        "top": (rows, cols + top_t), "right": (rows + right_t, cols + 1),
        "bottom": (rows + 1, cols + bottom_t), "left": (rows + left_t, cols),
    }
    crossed = {"top": top_x, "right": right_x, "bottom": bottom_x, "left": left_x}
    count = top_x.astype(int) + right_x + bottom_x + left_x
    segs = []
    names = ["top", "right", "bottom", "left"]
    two = count == 2
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            sel = two & crossed[a] & crossed[b]
            for r, c in zip(*np.nonzero(sel)):
                segs.append(((float(pts[a][0][r, c]), float(pts[a][1][r, c])),
                             (float(pts[b][0][r, c]), float(pts[b][1][r, c]))))
    # saddles: pair edges by the cell-centre value
    for r, c in zip(*np.nonzero(count == 4)):
        centre_high = (tl[r, c] + tr[r, c] + bl[r, c] + br[r, c]) / 4 >= level
        tl_high = tl[r, c] >= level
        pairs = [("top", "left"), ("bottom", "right")] if tl_high != centre_high else [("top", "right"), ("bottom", "left")]
        for a, b in pairs:
            segs.append(((float(pts[a][0][r, c]), float(pts[a][1][r, c])),
                         (float(pts[b][0][r, c]), float(pts[b][1][r, c]))))
    return segs


def canopy_height(surface, ground):
    """Surface minus bare earth, floored at 0; surface 0 means no lidar return."""
    surface = np.asarray(surface, float)
    ground = np.asarray(ground, float)
    return np.maximum(np.where(surface <= 0, ground, surface) - ground, 0.0)


def stitch(segments, ndigits=3):
    """Join segments that share endpoints into polylines (lists of points)."""
    key = lambda p: (round(p[0], ndigits), round(p[1], ndigits))
    ends = {}
    for i, (a, b) in enumerate(segments):
        ends.setdefault(key(a), []).append(i)
        ends.setdefault(key(b), []).append(i)
    used = [False] * len(segments)
    lines = []

    def extend(line):
        while True:
            nxt = [i for i in ends.get(key(line[-1]), []) if not used[i]]
            if not nxt:
                return
            i = nxt[0]
            used[i] = True
            a, b = segments[i]
            line.append(tuple(b) if key(a) == key(line[-1]) else tuple(a))

    for i, (a, b) in enumerate(segments):
        if used[i]:
            continue
        used[i] = True
        line = [tuple(a), tuple(b)]
        extend(line)
        line.reverse()
        extend(line)
        lines.append(line)
    return lines


def simplify(line, tol):
    """Douglas-Peucker: drop points closer than tol to the simplified line."""
    if len(line) < 3:
        return list(line)
    p = np.asarray(line, float)
    a, b = p[0], p[-1]
    ab = b - a
    n = np.hypot(*ab)
    d = (np.abs(ab[0] * (p[:, 1] - a[1]) - ab[1] * (p[:, 0] - a[0])) / n) if n else np.hypot(*(p - a).T)
    i = int(np.argmax(d))
    if d[i] <= tol:
        return [tuple(line[0]), tuple(line[-1])]
    return simplify(line[:i + 1], tol)[:-1] + simplify(line[i:], tol)
