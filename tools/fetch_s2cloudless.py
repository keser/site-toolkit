#!/usr/bin/env python3
"""Fetch EOX Sentinel-2 cloudless imagery (the 2016 layer) for a box in CT State Plane feet.

Usage:
    python3 tools/fetch_s2cloudless.py --box-ft XMIN YMIN XMAX YMAX --out <dir> [--px 4096]

For regional views past the state line, where CT ECO's NAIP stops: one seamless mosaic of land
and water at 10 m. Saves s2cloudless.jpg in EPSG:4326 (lon/lat) covering the box's every edge,
plus manifest.json with the request and credit; reproject it into the sheet frame when rendering.

The 2016 layer is CC BY 4.0. Later years are CC BY-NC-SA 4.0, so this tool asks only for 2016.
"""
import argparse
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from fetch_ct_eco import ct_ft_to_latlon

WMS = "https://tiles.maps.eox.at/wms"
LAYER = "s2cloudless"  # 2016
MAX_SIDE = 4096
CREDIT = ("Sentinel-2 cloudless – https://s2maps.eu by EOX IT Services GmbH "
          "(Contains modified Copernicus Sentinel data 2016)")
LICENSE = "CC BY 4.0"


def getmap_url(bbox, width, height):
    """WMS 1.1.1 GetMap for a (west, south, east, north) bbox in degrees."""
    if max(width, height) > MAX_SIDE:
        raise ValueError(f"{width}x{height} px exceeds {MAX_SIDE} px; fetch a smaller image")
    q = {"service": "WMS", "request": "GetMap", "version": "1.1.1", "layers": LAYER, "styles": "",
         "srs": "EPSG:4326", "bbox": ",".join(f"{v:g}" for v in bbox),
         "width": width, "height": height, "format": "image/jpeg"}
    return f"{WMS}?{urlencode(q)}"


def lonlat_bbox(box_ft, steps=16):
    """The smallest lon/lat bbox holding a State Plane box, sampled along its edges (they curve)."""
    x0, y0, x1, y1 = box_ft
    pts = []
    for i in range(steps + 1):
        t = i / steps
        for x, y in ((x0 + t * (x1 - x0), y0), (x0 + t * (x1 - x0), y1),
                     (x0, y0 + t * (y1 - y0)), (x1, y0 + t * (y1 - y0))):
            pts.append(ct_ft_to_latlon(x, y))
    lats, lons = zip(*pts)
    return min(lons), min(lats), max(lons), max(lats)


def fetch(box_ft, out, px=MAX_SIDE):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    w, s, e, n = lonlat_bbox(box_ft)
    pad_x, pad_y = (e - w) * 0.01, (n - s) * 0.01
    bbox = (w - pad_x, s - pad_y, e + pad_x, n + pad_y)
    aspect = (bbox[2] - bbox[0]) / (bbox[3] - bbox[1])
    width, height = (px, round(px / aspect)) if aspect >= 1 else (round(px * aspect), px)
    url = getmap_url(bbox, width, height)
    with urlopen(Request(url, headers={"User-Agent": "site-toolkit fetch_s2cloudless"}), timeout=180) as r:
        data, ctype = r.read(), r.headers.get("Content-Type", "")
    if not ctype.startswith("image/"):
        raise RuntimeError(f"expected an image, got {ctype}: {data[:300]!r}")
    (out / "s2cloudless.jpg").write_bytes(data)
    manifest = {"file": "s2cloudless.jpg", "srs": "EPSG:4326", "bbox_lonlat": bbox, "size": [width, height],
                "box_ft": list(box_ft), "layer": LAYER, "year": 2016, "url": url,
                "fetched": date.today().isoformat(), "credit": CREDIT, "license": LICENSE}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote s2cloudless.jpg ({width}x{height}) and manifest.json")
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--box-ft", type=float, nargs=4, required=True, metavar=("XMIN", "YMIN", "XMAX", "YMAX"))
    p.add_argument("--out", required=True)
    p.add_argument("--px", type=int, default=MAX_SIDE, help="longer side in pixels")
    a = p.parse_args()
    fetch(a.box_ft, a.out, a.px)


if __name__ == "__main__":
    main()
