import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import imagery  # noqa: E402


def test_ndvi_is_normalized_difference_of_nir_and_red():
    red = np.array([[50, 100, 0]], dtype=np.uint8)
    nir = np.array([[150, 100, 0]], dtype=np.uint8)
    out = imagery.ndvi(red, nir)
    assert np.allclose(out, [[0.5, 0.0, 0.0]])


def test_ndvi_does_not_overflow_uint8_bands():
    red = np.array([[200]], dtype=np.uint8)
    nir = np.array([[250]], dtype=np.uint8)
    assert np.isclose(imagery.ndvi(red, nir)[0, 0], 50 / 450)


def test_stretch_maps_percentiles_to_the_full_range():
    band = np.arange(101, dtype=float)
    out = imagery.stretch(band, 10, 90)
    assert out[10] == 0 and out[90] == 255 and out[0] == 0 and out[100] == 255
    assert out.dtype == np.uint8


def test_cir_puts_nir_in_red_red_in_green_and_green_in_blue():
    r = np.tile(np.arange(100.0), (2, 1))
    g, nir = r * 0, r * 0
    out = imagery.cir(r, g, nir)
    assert out.shape == (2, 100, 3)
    assert out[..., 1].max() == 255 and out[..., 0].max() == 0 and out[..., 2].max() == 0


def test_classify_returns_the_bin_index_for_each_value():
    out = imagery.classify(np.array([-0.2, 0.05, 0.2, 0.45, 0.8]), [0.1, 0.3, 0.5])
    assert out.tolist() == [0, 0, 1, 2, 3]
