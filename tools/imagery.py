#!/usr/bin/env python3
"""Vegetation views from 4-band imagery (red, green, blue, near-infrared).

- ndvi: normalized difference vegetation index, (NIR - red) / (NIR + red), from -1 to 1. Healthy
  leaves reflect near-infrared strongly and absorb red, so dense green growth reads high (about 0.5
  and up), bare soil and pavement near 0, and water below 0.
- cir: the standard color-infrared composite (NIR as red, red as green, green as blue), where
  living vegetation shows red and evergreens show darker red than broadleaf.
- stretch / classify: display helpers.

CT ECO's 4-band TIFFs open in Pillow as RGBA; the "alpha" channel is near-infrared.
"""
import numpy as np


def ndvi(red, nir):
    red = np.asarray(red, float)
    nir = np.asarray(nir, float)
    total = nir + red
    with np.errstate(invalid="ignore", divide="ignore"):
        out = (nir - red) / total
    return np.where(total > 0, out, 0.0)


def stretch(band, lo_pct=2, hi_pct=98):
    """Linear stretch so the lo/hi percentiles map to 0 and 255."""
    band = np.asarray(band, float)
    lo, hi = np.percentile(band, [lo_pct, hi_pct])
    scaled = (band - lo) / (hi - lo) if hi > lo else np.zeros_like(band)
    return (np.clip(scaled, 0, 1) * 255).round().astype(np.uint8)


def cir(red, green, nir, lo_pct=2, hi_pct=98):
    """Color-infrared composite as an RGB uint8 array."""
    return np.dstack([stretch(nir, lo_pct, hi_pct), stretch(red, lo_pct, hi_pct), stretch(green, lo_pct, hi_pct)])


def classify(values, breaks):
    """Index of the bin each value falls in: below breaks[0] is 0, at or above breaks[-1] is len(breaks)."""
    return np.digitize(np.asarray(values, float), breaks)
