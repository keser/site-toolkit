#!/usr/bin/env python3
"""Fetch a site's CT ECO imagery, elevation, and building layers into one folder.

Usage:
    python3 tools/fetch_ct_eco.py --lat 41.5728 --lon -72.6344 --out <dir>
        [--radius-ft 300] [--year 2023] [--only surface-ft.tif ground-ft.tif]
        [--width-ft 2640 --height-ft 1485] [--pixel-ft 0.6875]

--width-ft/--height-ft fetch a rectangle instead of the square, and --pixel-ft coarsens every
layer, for wide context views (a neighborhood) that would exceed the server's 4100 px limit.

Every raster covers the same square box in CT State Plane feet (EPSG:6434), centered on the
site, so the layers stack pixel for pixel. Writes manifest.json with each file's source,
request, fetch date, and citation. Connecticut only: CT ECO serves the state's flights.

The box should reach past the lot: a tall tree's low-sun shadow is about twice its height.
"""
import argparse
import json
import math
from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

SR = 6434  # NAD83(2011) / Connecticut (ftUS)
MAX_SIDE = 4100  # CT ECO ImageServer maxImageHeight
CT_ECO = "https://cteco.uconn.edu/ctraster/rest/services"
BUILDINGS = ("https://services3.arcgis.com/3FL1kr7L4LvwA2Kb/ArcGIS/rest/services/"
             "CT_Buildings/FeatureServer/0")

# EPSG:6434 Lambert Conformal Conic (2SP) on GRS80.
_A = 6378137.0
_F = 1 / 298.257222101
_E = math.sqrt(_F * (2 - _F))
_FT = 1200 / 3937  # metres per US survey foot
_LAT1, _LAT2, _LAT0, _LON0 = map(math.radians, (41.2, 41 + 52 / 60, 40 + 50 / 60, -72.75))
_FE, _FN = 1_000_000.0, 500_000.0  # feet


def _m(phi):
    return math.cos(phi) / math.sqrt(1 - (_E * math.sin(phi)) ** 2)


def _t(phi):
    s = _E * math.sin(phi)
    return math.tan(math.pi / 4 - phi / 2) / ((1 - s) / (1 + s)) ** (_E / 2)


_N = (math.log(_m(_LAT1)) - math.log(_m(_LAT2))) / (math.log(_t(_LAT1)) - math.log(_t(_LAT2)))
_BIGF = _m(_LAT1) / (_N * _t(_LAT1) ** _N)
_R0 = _A * _BIGF * _t(_LAT0) ** _N


def latlon_to_ct_ft(lat, lon):
    """WGS84/NAD83 degrees to EPSG:6434 easting, northing in US survey feet."""
    phi, lam = math.radians(lat), math.radians(lon)
    r = _A * _BIGF * _t(phi) ** _N
    theta = _N * (lam - _LON0)
    x = r * math.sin(theta) / _FT + _FE
    y = (_R0 - r * math.cos(theta)) / _FT + _FN
    return x, y


def site_box(x, y, radius_ft):
    return (x - radius_ft, y - radius_ft, x + radius_ft, y + radius_ft)


def rect_box(x, y, width_ft, height_ft):
    return (x - width_ft / 2, y - height_ft / 2, x + width_ft / 2, y + height_ft / 2)


def export_url(service, box, pixel_ft, fmt, bands=None, pixel_type=None):
    w = round((box[2] - box[0]) / pixel_ft)
    h = round((box[3] - box[1]) / pixel_ft)
    if max(w, h) > MAX_SIDE:
        raise ValueError(f"{w}x{h} px exceeds the server limit of {MAX_SIDE} px; use a larger pixel")
    q = {
        "bbox": ",".join(f"{v:g}" for v in box),
        "bboxSR": SR, "imageSR": SR,
        "size": f"{w},{h}",
        "format": fmt,
        "f": "image",
    }
    if bands is not None:
        q["bandIds"] = ",".join(map(str, bands))
    if fmt == "tiff":
        q["compression"] = "None"
    if pixel_type:
        q["pixelType"] = pixel_type
        q["interpolation"] = "RSP_BilinearInterpolation"
    return f"{service}/exportImage?{urlencode(q)}"


def buildings_query_url(box):
    env = {"xmin": box[0], "ymin": box[1], "xmax": box[2], "ymax": box[3],
           "spatialReference": {"wkid": SR}}
    q = {
        "geometry": json.dumps(env), "geometryType": "esriGeometryEnvelope",
        "inSR": SR, "outSR": SR, "spatialRel": "esriSpatialRelIntersects",
        "outFields": "*", "f": "geojson",
    }
    return f"{BUILDINGS}/query?{urlencode(q)}"


def layers(year):
    ortho = f"{CT_ECO}/images/Ortho_{year}/ImageServer"
    naip = f"{CT_ECO}/images/NAIP_{year}/ImageServer"
    return [
        {"file": "ortho-rgb.png", "service": ortho, "pixel_ft": 0.25, "fmt": "png", "bands": [0, 1, 2],
         "what": f"{year} orthoimagery, true color, leaf-off spring flight"},
        {"file": "ortho-4band.tif", "service": ortho, "pixel_ft": 0.25, "fmt": "tiff", "bands": [0, 1, 2, 3],
         "what": f"{year} orthoimagery, bands R, G, B, near-infrared"},
        {"file": "naip-4band.tif", "service": naip, "pixel_ft": 1, "fmt": "tiff", "bands": [0, 1, 2, 3],
         "what": f"NAIP {year}, bands R, G, B, near-infrared"},
        {"file": "surface-ft.tif", "service": f"{CT_ECO}/elevation/MaxSurfaceHeight_{year}/ImageServer",
         "pixel_ft": 2, "fmt": "tiff", "pixel_type": "F32",
         "what": f"{year} lidar max surface elevation (treetops, roofs), feet; "
                 "0 = no lidar return (water, dark roofs)"},
        {"file": "ground-ft.tif", "service": f"{CT_ECO}/elevation/Statewide{year}/ImageServer",
         "pixel_ft": 2, "fmt": "tiff", "pixel_type": "F32",
         "what": f"{year} lidar bare-earth elevation, feet"},
    ]


def select_layers(year, only, pixel_ft=None):
    """The layers whose file names are in `only` (all layers when `only` is None), at `pixel_ft`
    instead of each layer's own pixel size when given."""
    every = layers(year)
    if pixel_ft is not None:
        every = [{**layer, "pixel_ft": pixel_ft} for layer in every]
    if only is None:
        return every
    known = {layer["file"] for layer in every} | {"buildings.geojson"}
    unknown = [name for name in only if name not in known]
    if unknown:
        raise ValueError(f"unknown layer file(s) {', '.join(unknown)}; choose from {', '.join(sorted(known))}")
    return [layer for layer in every if layer["file"] in only]


def _get(url):
    with urlopen(url, timeout=120) as r:
        data, ctype = r.read(), r.headers.get("Content-Type", "")
    if "json" in ctype or "html" in ctype:
        raise RuntimeError(f"expected an image, got {ctype}: {data[:300]!r}")
    return data


def fetch(lat, lon, out, radius_ft=300, year=2023, only=None, width_ft=None, height_ft=None, pixel_ft=None):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    x, y = latlon_to_ct_ft(lat, lon)
    box = rect_box(x, y, width_ft, height_ft) if width_ft else site_box(x, y, radius_ft)
    citation = f"CT State GIS Office. ({year}). {year} Aerial imagery and elevation. CT ECO, UConn."
    manifest = {"center": {"lat": lat, "lon": lon, "x_ft": round(x, 2), "y_ft": round(y, 2)},
                "box_ft": [round(v, 2) for v in box], "sr": f"EPSG:{SR}", "year": year,
                "fetched": date.today().isoformat(), "citation": citation, "files": []}
    for layer in select_layers(year, only, pixel_ft):
        url = export_url(layer["service"], box, layer["pixel_ft"], layer["fmt"],
                         layer.get("bands"), layer.get("pixel_type"))
        (out / layer["file"]).write_bytes(_get(url))
        manifest["files"].append({"file": layer["file"], "what": layer["what"],
                                  "pixel_ft": layer["pixel_ft"], "url": url})
        print(f"wrote {layer['file']}")
    if only is None or "buildings.geojson" in only:
        url = buildings_query_url(box)
        with urlopen(url, timeout=120) as r:
            geo = json.load(r)
        (out / "buildings.geojson").write_text(json.dumps(geo))
        manifest["files"].append({"file": "buildings.geojson", "url": url,
                                  "what": f"{len(geo.get('features', []))} building footprints from the 2023 "
                                          "lidar, 2D only; take heights from surface-ft minus ground-ft"})
        print(f"wrote buildings.geojson ({len(geo.get('features', []))} footprints)")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("wrote manifest.json")
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lon", type=float, required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--radius-ft", type=float, default=300)
    p.add_argument("--year", type=int, default=2023)
    p.add_argument("--width-ft", type=float, help="rectangle width (with --height-ft) instead of the square")
    p.add_argument("--height-ft", type=float)
    p.add_argument("--pixel-ft", type=float, help="pixel size for every layer, for wide views")
    p.add_argument("--only", nargs="+", metavar="FILE",
                   help="fetch only these files, e.g. surface-ft.tif ground-ft.tif (for a wide shade box)")
    a = p.parse_args()
    if (a.width_ft is None) != (a.height_ft is None):
        p.error("--width-ft and --height-ft go together")
    fetch(a.lat, a.lon, a.out, a.radius_ft, a.year, a.only, a.width_ft, a.height_ft, a.pixel_ft)


if __name__ == "__main__":
    main()
