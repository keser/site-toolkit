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


def test_horizon_profile_sees_a_wall_at_its_angular_height():
    surface = wall_ew()                       # 10 ft wall at row 20
    angles = shade.horizon_profile(surface, 1.0, 30, 25, 0.0, [180, 0], max_dist_ft=60)
    assert np.isclose(angles[0], 0.0)         # looking south: open
    assert np.isclose(angles[1], np.degrees(np.arctan(10 / 10)))   # wall 10 ft north, 10 ft tall


def test_plane_factor_is_one_facing_the_sun_and_zero_edge_on():
    assert np.isclose(shade.plane_factor(180, 45, slope=45, aspect=180), 1.0)
    assert np.isclose(shade.plane_factor(180, 45, slope=45, aspect=0), 0.0, atol=1e-9)
    assert np.isclose(shade.plane_factor(90, 90, slope=0, aspect=0), 1.0)


def test_solar_access_of_open_ground_is_one_and_falls_behind_a_wall():
    surface = wall_ew()
    positions = [(180, 30), (180, 60)]
    acc = shade.solar_access(surface, np.zeros_like(surface), 1.0, positions)
    assert np.isclose(acc[40, 25], 1.0)
    assert np.isclose(acc[2, 25], 1.0)        # 18 ft north: beyond both shadows (17.3 and 5.8 ft)
    assert 0 < acc[13, 25] < 1                # 7 ft north: shaded at 30 deg, sunny at 60


def test_horizon_profile_can_skip_obstacles_closer_than_a_minimum_distance():
    surface = wall_ew()                       # wall 10 ft north of row 30
    angles = shade.horizon_profile(surface, 1.0, 30, 25, 0.0, [0], max_dist_ft=60, min_dist_ft=12)
    assert np.isclose(angles[0], 0.0)


def test_clear_sky_dni_is_zero_below_the_horizon_and_rises_with_the_sun():
    assert shade.clear_sky_dni(0) == 0.0
    assert shade.clear_sky_dni(-5) == 0.0
    assert abs(shade.clear_sky_dni(90) - 1353 * 0.7) < 1e-6  # air mass 1
    assert shade.clear_sky_dni(10) < shade.clear_sky_dni(30) < shade.clear_sky_dni(60)
