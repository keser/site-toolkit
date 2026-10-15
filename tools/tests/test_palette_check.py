import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from palette_check import check, contrast, delta_e, hex_to_rgb, simulate

RAMPS = {"a/500": "#476de7", "b/500": "#698436", "c/500": "#ef5c58", "k/900": "#000000", "w/0": "#ffffff"}


def palette(tokens, **checks):
    base = {"floor_de": 10, "contrast_min": 3.0, "distinct": [], "adjacent": [], "edges": [],
            "surfaces": {"light": ["#ffffff"], "dark": ["#000000"]}}
    base.update(checks)
    return {"tokens": tokens, "checks": base}


def test_contrast_black_on_white_is_21():
    assert round(contrast("#000000", "#ffffff"), 1) == 21.0


def test_delta_e_of_a_color_with_itself_is_zero():
    assert delta_e("#698436", "#698436") == 0


def test_simulation_keeps_white_white():
    for kind in ("deutan", "protan", "tritan"):
        assert all(abs(c - 1) < 0.01 for c in simulate(hex_to_rgb("#ffffff"), kind))


def test_deuteranopia_collapses_red_green():
    assert delta_e("#ff0000", "#00b000", "deutan") < delta_e("#ff0000", "#00b000") / 2


def test_distinct_pair_below_floor_is_reported():
    p = palette({"x": {"light": "a/500", "dark": "a/500"}, "y": {"light": "a/500", "dark": "a/500"}},
                distinct=[["x", "y"]])
    assert any("x" in f and "y" in f for f in check(RAMPS, p))


def test_adjacent_checks_only_neighbors():
    t = {n: {"light": s, "dark": s} for n, s in (("p", "a/500"), ("q", "b/500"), ("r", "a/500"))}
    assert check(RAMPS, palette(t, adjacent=[["p", "q", "r"]])) == []


def test_low_contrast_edge_is_reported():
    p = palette({"e": {"light": "w/0", "dark": "k/900"}}, edges=["e"])
    assert len(check(RAMPS, p)) == 2


def test_unknown_ramp_step_is_reported():
    p = palette({"x": {"light": "a/550", "dark": "a/500"}})
    assert any("a/550" in f for f in check(RAMPS, p))
