import math
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sun_arcs as s  # noqa: E402

LAT, LON, TZ = 41.5728, -72.6344, "America/New_York"


def test_noon_altitude_matches_latitude_and_declination():
    winter = max(p["alt"] for p in s.day_arc(date(2026, 12, 21), LAT, LON, TZ))
    summer = max(p["alt"] for p in s.day_arc(date(2026, 6, 21), LAT, LON, TZ))
    assert winter == pytest.approx(90 - LAT - 23.44, abs=0.2)
    assert summer == pytest.approx(90 - LAT + 23.44, abs=0.2)


def test_solar_noon_is_due_south_and_before_clock_noon_in_winter():
    noon = s.solar_noon(date(2026, 12, 21), LAT, LON, TZ)
    assert noon["az"] == pytest.approx(180, abs=0.5)
    # 72.63°W is 9.5 min east of the EST meridian; equation of time adds about 1.7 min.
    assert (noon["time"].hour, noon["time"].minute) in [(11, 48), (11, 49)]


def test_summer_hours_use_daylight_time():
    noon = s.solar_noon(date(2026, 6, 21), LAT, LON, TZ)
    assert noon["time"].hour == 12 and 50 <= noon["time"].minute <= 53


def test_hour_marks_are_whole_clock_hours_with_sun_up():
    marks = s.hour_marks(date(2026, 12, 21), LAT, LON, TZ)
    assert [m["time"].hour for m in marks] == list(range(8, 17))
    assert all(m["time"].minute == 0 and m["alt"] > 0 for m in marks)


def test_polar_offset_puts_zenith_at_center_and_horizon_at_radius():
    assert s.polar_offset(180, 90, 100) == pytest.approx((0, 0), abs=1e-9)
    east, north = s.polar_offset(90, 0, 100)
    assert (east, north) == pytest.approx((100, 0), abs=1e-9)
    east, north = s.polar_offset(180, 45, 100)
    assert (east, north) == pytest.approx((0, -50), abs=1e-9)


def test_camera_projects_its_target_to_image_center():
    cam = s.Camera(heading=180, tilt=50, range_m=250, fov_h=60, width=2000, height=1000)
    assert cam.project((0, 0, 0)) == pytest.approx((1000, 500), abs=1e-6)


def test_camera_looking_south_sees_points_further_south_higher_in_frame():
    cam = s.Camera(heading=180, tilt=50, range_m=250, fov_h=60, width=2000, height=1000)
    _, y_near = cam.project((0, 20, 0))
    _, y_far = cam.project((0, -20, 0))
    assert y_far < 500 < y_near


def test_camera_looking_south_puts_east_on_the_left():
    cam = s.Camera(heading=180, tilt=50, range_m=250, fov_h=60, width=2000, height=1000)
    x_east, _ = cam.project((20, 0, 0))
    assert x_east < 1000


def test_sunrise_and_sunset_include_refraction():
    rise, sset = s.sunrise_sunset(date(2026, 12, 21), LAT, LON, TZ)
    arc = s.day_arc(date(2026, 12, 21), LAT, LON, TZ, step_min=1)
    early = (arc[0]["time"] - rise).total_seconds() / 60
    late = (sset - arc[-1]["time"]).total_seconds() / 60
    assert 2 <= early <= 8 and 2 <= late <= 8


def test_sunrise_sunset_is_none_in_polar_night():
    assert s.sunrise_sunset(date(2026, 12, 21), 78.2, 15.6, "Arctic/Longyearbyen") == (None, None)


def test_solar_noon_is_found_outside_the_old_10_to_15_window():
    # Far western China keeps Beijing time, so solar noon falls after 15:00 on the clock.
    noon = s.solar_noon(date(2026, 6, 21), 39.5, 73.5, "Asia/Shanghai")
    assert noon["time"].hour >= 15
