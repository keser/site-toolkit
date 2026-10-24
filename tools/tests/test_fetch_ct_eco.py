import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fetch_ct_eco as f  # noqa: E402


def test_latlon_to_ct_ft_matches_ct_eco_server_projection():
    # Reference: CT ECO's Statewide2023 ImageServer projecting this point to EPSG:6434.
    x, y = f.latlon_to_ct_ft(41.5728, -72.6344)
    assert x == pytest.approx(1031631.09, abs=1.0)
    assert y == pytest.approx(769456.67, abs=1.0)


def test_site_box_is_square_around_center():
    assert f.site_box(1000.0, 2000.0, 300) == (700.0, 1700.0, 1300.0, 2300.0)


def test_export_url_sizes_image_from_pixel_size():
    url = f.export_url("https://h/ImageServer", (0, 0, 600, 600), pixel_ft=0.25, fmt="png", bands=[0, 1, 2])
    q = parse_qs(urlparse(url).query)
    assert url.startswith("https://h/ImageServer/exportImage?")
    assert q["size"] == ["2400,2400"]
    assert q["bboxSR"] == ["6434"] and q["imageSR"] == ["6434"]
    assert q["bbox"] == ["0,0,600,600"]
    assert q["bandIds"] == ["0,1,2"]
    assert q["format"] == ["png"]


def test_export_url_omits_band_ids_when_not_given():
    q = parse_qs(urlparse(f.export_url("https://h/ImageServer", (0, 0, 600, 600), 2, "tiff")).query)
    assert "bandIds" not in q


def test_export_url_rejects_images_over_server_limit():
    with pytest.raises(ValueError, match="4100"):
        f.export_url("https://h/ImageServer", (0, 0, 2000, 2000), pixel_ft=0.25, fmt="png")


def test_layers_for_year_point_at_that_years_services():
    names = {layer["file"]: layer["service"] for layer in f.layers(2026)}
    assert names["ortho-rgb.png"].endswith("/images/Ortho_2026/ImageServer")
    assert names["ground-ft.tif"].endswith("/elevation/Statewide2026/ImageServer")
    assert names["surface-ft.tif"].endswith("/elevation/MaxSurfaceHeight_2026/ImageServer")


def test_buildings_query_url_uses_box_in_state_plane():
    q = parse_qs(urlparse(f.buildings_query_url((0, 0, 600, 600))).query)
    assert q["inSR"] == ["6434"] and q["outSR"] == ["6434"]
    assert q["f"] == ["geojson"]
    assert '"xmax": 600' in q["geometry"][0]


def test_surface_layer_says_zero_is_no_data():
    surface = next(layer for layer in f.layers(2023) if layer["file"] == "surface-ft.tif")
    assert "0 = no lidar return" in surface["what"]


def test_select_layers_keeps_only_the_named_files():
    picked = f.select_layers(2023, ["surface-ft.tif", "ground-ft.tif"])
    assert [layer["file"] for layer in picked] == ["surface-ft.tif", "ground-ft.tif"]


def test_select_layers_with_no_filter_returns_every_layer():
    assert f.select_layers(2023, None) == f.layers(2023)


def test_select_layers_rejects_an_unknown_file():
    with pytest.raises(ValueError, match="ortho.jpg"):
        f.select_layers(2023, ["ortho.jpg"])


def test_rect_box_is_centered_with_given_width_and_height():
    assert f.rect_box(1000.0, 2000.0, 2640, 1485) == (-320.0, 1257.5, 2320.0, 2742.5)


def test_select_layers_overrides_pixel_size_for_wide_views():
    picked = f.select_layers(2023, ["ortho-rgb.png"], pixel_ft=0.6875)
    assert [layer["pixel_ft"] for layer in picked] == [0.6875]
    assert f.select_layers(2023, ["ortho-rgb.png"])[0]["pixel_ft"] == 0.25  # default untouched
