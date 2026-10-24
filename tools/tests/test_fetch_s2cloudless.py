import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fetch_ct_eco  # noqa: E402
import fetch_s2cloudless as f  # noqa: E402


def test_getmap_url_asks_the_2016_layer_in_lon_lat_order():
    q = parse_qs(urlparse(f.getmap_url((-73.0, 41.0, -72.0, 42.0), 2000, 1000)).query)
    assert q["layers"] == ["s2cloudless"]  # the 2016 layer, CC BY 4.0
    assert q["srs"] == ["EPSG:4326"]
    assert q["bbox"] == ["-73,41,-72,42"]
    assert q["width"] == ["2000"] and q["height"] == ["1000"]
    assert q["request"] == ["GetMap"] and q["format"] == ["image/jpeg"]


def test_getmap_url_rejects_sizes_over_the_limit():
    with pytest.raises(ValueError, match="4096"):
        f.getmap_url((-73.0, 41.0, -72.0, 42.0), 5000, 1000)


def test_lonlat_bbox_encloses_every_edge_of_a_state_plane_box():
    box = (900000.0, 600000.0, 1100000.0, 800000.0)
    w, s, e, n = f.lonlat_bbox(box)
    for x in (box[0], (box[0] + box[2]) / 2, box[2]):
        for y in (box[1], (box[1] + box[3]) / 2, box[3]):
            lat, lon = fetch_ct_eco.ct_ft_to_latlon(x, y)
            assert w <= lon <= e and s <= lat <= n


def test_credit_names_eox_and_copernicus_2016():
    assert "EOX IT Services GmbH" in f.CREDIT and "Copernicus Sentinel data 2016" in f.CREDIT
