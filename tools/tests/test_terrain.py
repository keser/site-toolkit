import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import terrain  # noqa: E402


def test_flat_ground_hillshade_equals_sine_of_sun_altitude():
    out = terrain.hillshade(np.zeros((5, 5)), 1.0, az=315, alt=45)
    assert np.allclose(out, np.sin(np.radians(45)))


def test_slope_facing_the_sun_is_brighter_than_slope_facing_away():
    x = np.tile(np.arange(10.0), (10, 1))      # rises to the east
    east_up = terrain.hillshade(x, 1.0, az=270, alt=45)       # sun in the west: slope faces it
    east_up_sun_east = terrain.hillshade(x, 1.0, az=90, alt=45)
    assert east_up[5, 5] > east_up_sun_east[5, 5]


def test_contour_of_an_east_rising_plane_is_a_north_south_line():
    z = np.tile(np.arange(6.0), (4, 1))        # z = column index
    segs = terrain.contour_segments(z, 2.5)
    assert len(segs) == 3                     # one per row gap
    for (r0, c0), (r1, c1) in segs:
        assert c0 == c1 == 2.5
        assert abs(r1 - r0) == 1


def test_contour_level_outside_the_grid_range_has_no_segments():
    assert terrain.contour_segments(np.zeros((3, 3)), 5) == []


def test_canopy_height_never_goes_below_zero_and_fills_no_returns():
    surface = np.array([[0.0, 110.0], [95.0, 130.0]])   # 0 = no lidar return
    ground = np.array([[100.0, 100.0], [100.0, 100.0]])
    assert terrain.canopy_height(surface, ground).tolist() == [[0.0, 10.0], [0.0, 30.0]]


def test_stitch_joins_segments_that_share_endpoints_into_one_line():
    segs = [((0, 0), (0, 1)), ((0, 2), (0, 1)), ((5, 5), (5, 6))]
    lines = sorted(terrain.stitch(segs), key=len)
    assert len(lines) == 2
    assert lines[1] in ([(0, 0), (0, 1), (0, 2)], [(0, 2), (0, 1), (0, 0)])


def test_simplify_drops_points_within_tolerance_of_the_line():
    line = [(0, 0), (1, 0.05), (2, 0), (3, 2)]
    assert terrain.simplify(line, 0.1) == [(0, 0), (2, 0), (3, 2)]
