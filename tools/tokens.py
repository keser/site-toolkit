#!/usr/bin/env python3
"""Read design-token colors for raster renders, resolved through the Ramps.

    import tokens
    tokens.rgb("map", "sun/full-sun")              # (242, 223, 161)
    tokens.hex("species", "layer/shrub", "dark")   # "#849f55"

A collection is design-language/tokens/<name>.json: {"tokens": {name: step}} for one mode, or
{name: {"light": step, "dark": step}} for two. Each step is a key in ramps.json, which mirrors
the Figma Ramps collection. Figma is the source of truth; these files mirror it so Python rasters
and Figma keys share one color per meaning instead of copying hex.
"""
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=None)
def _load(root, name):
    return json.loads((Path(root) / "design-language/tokens" / f"{name}.json").read_text())


def hex(collection, name, mode="light", root=ROOT):
    toks = _load(root, collection)["tokens"]
    if name not in toks:
        raise KeyError(f"{collection}: no token {name}")
    step = toks[name] if isinstance(toks[name], str) else toks[name][mode]
    ramps = _load(root, "ramps")
    if step not in ramps:
        raise KeyError(f"{collection}: {name} points to {step}, which is not in ramps.json")
    return ramps[step]


def rgb(collection, name, mode="light", root=ROOT):
    h = hex(collection, name, mode, root)
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
