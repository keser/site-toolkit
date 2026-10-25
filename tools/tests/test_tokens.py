import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tokens


def write_root(tmp_path, ramps, **collections):
    d = tmp_path / "design-language/tokens"
    d.mkdir(parents=True)
    (d / "ramps.json").write_text(json.dumps(ramps))
    for name, toks in collections.items():
        (d / f"{name}.json").write_text(json.dumps({"tokens": toks}))
    return tmp_path


def test_single_mode_token_resolves_through_ramps_in_every_mode(tmp_path):
    root = write_root(tmp_path, {"gold/100": "#f2dfa1"}, map={"sun/full-sun": "gold/100"})
    assert tokens.rgb("map", "sun/full-sun", root=root) == (0xF2, 0xDF, 0xA1)
    assert tokens.rgb("map", "sun/full-sun", "dark", root=root) == (0xF2, 0xDF, 0xA1)


def test_two_mode_token_picks_the_mode(tmp_path):
    root = write_root(tmp_path, {"sage/400": "#849f55", "sage/500": "#698436"},
                      species={"layer/shrub": {"light": "sage/500", "dark": "sage/400"}})
    assert tokens.hex("species", "layer/shrub", root=root) == "#698436"
    assert tokens.hex("species", "layer/shrub", "dark", root=root) == "#849f55"


def test_unknown_token_names_itself(tmp_path):
    root = write_root(tmp_path, {}, map={})
    with pytest.raises(KeyError, match="map: no token sun/nope"):
        tokens.rgb("map", "sun/nope", root=root)


def test_token_pointing_off_the_ramps_names_the_step(tmp_path):
    root = write_root(tmp_path, {}, map={"terrain/high": "gold/950"})
    with pytest.raises(KeyError, match="gold/950"):
        tokens.rgb("map", "terrain/high", root=root)


def test_every_map_token_resolves():
    for name in json.loads((tokens.ROOT / "design-language/tokens/map.json").read_text())["tokens"]:
        assert len(tokens.rgb("map", name)) == 3


def test_map_tokens_match_the_rasters_they_replaced():
    assert tokens.hex("map", "sun/shade") == "#414655"  # slate/700, shade_build's old SHADOW_RGB
    assert tokens.hex("map", "vigor/dense") == "#516920"  # sage/600
    assert tokens.hex("map", "terrain/contour-index") == "#595e72"  # slate/600, as on the terrain sheet
