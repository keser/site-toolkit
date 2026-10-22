import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import shade  # noqa: E402

# Grids are north-up: row 0 is the north edge, column 0 the west edge. Cells are 1 ft.


def wall_ew(height=10.0, row=20, size=50):
    """Flat ground at 0 with an east-west wall one cell thick."""
    surface = np.zeros((size, size))
    surface[row, :] = height
    return surface


def test_south_sun_at_45_degrees_casts_a_shadow_as_long_as_the_wall_is_tall():
    surface = wall_ew()
    shaded = shade.shadow_mask(surface, np.zeros_like(surface), 1.0, az=180, alt=45)
    col = shaded[:, 25]
    assert col[10:20].all()          # 1 to 10 ft north of the wall
    assert not col[:9].any()          # beyond 11 ft north
    assert not col[21:].any()         # the sunny side


def test_low_sun_lengthens_the_shadow():
    surface = wall_ew()
    shaded = shade.shadow_mask(surface, np.zeros_like(surface), 1.0, az=180, alt=26.57)  # tan = 0.5
    col = shaded[:, 25]
    assert col[1:20].all()            # 1 to 19 ft north, inside the 20 ft shadow
    assert not col[21:].any()


def test_east_sun_shades_west_of_a_north_south_wall():
    surface = np.zeros((50, 50))
    surface[:, 30] = 10.0
    shaded = shade.shadow_mask(surface, np.zeros_like(surface), 1.0, az=90, alt=45)
    row = shaded[25]
    assert row[20:30].all()
    assert not row[31:].any()
    assert not row[:19].any()


def test_a_receptor_above_the_obstacle_stays_in_sun():
    surface = wall_ew()
    roof = np.full_like(surface, 12.0)
    shaded = shade.shadow_mask(surface, roof, 1.0, az=180, alt=45)
    assert not shaded.any()


def test_sun_below_the_horizon_shades_everything():
    surface = np.zeros((10, 10))
    assert shade.shadow_mask(surface, surface, 1.0, az=180, alt=-1).all()


def test_sun_hours_on_open_ground_count_every_step_with_the_sun_up():
    surface = np.zeros((20, 20))
    positions = [(90, 10), (135, 30), (180, 45), (225, 30), (270, 10), (300, -2)]
    hours = shade.sun_hours(surface, surface, 1.0, positions, step_minutes=60)
    assert np.allclose(hours, 5.0)


def test_sun_hours_drop_behind_a_wall():
    surface = wall_ew()
    positions = [(180, 45)] * 4
    hours = shade.sun_hours(surface, np.zeros_like(surface), 1.0, positions, step_minutes=30)
    assert hours[15, 25] == 0.0
    assert hours[30, 25] == 2.0
