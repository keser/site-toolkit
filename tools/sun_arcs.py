#!/usr/bin/env python3
"""Sun positions for a site, and two ways to draw them over imagery.

- day_arc / hour_marks / solar_noon: sun azimuth and altitude through a day, in local clock time
  (NOAA solar position equations; geometric altitude, no refraction).
- polar_offset: a top-down sun-path projection. Zenith sits at the site, the horizon at `radius`,
  and distance from the site grows as the sun drops (r = radius * (90 - alt) / 90). Direction is
  the true azimuth.
- Camera: a pinhole camera matching a Google Earth LookAt (heading, tilt, range, horizontal field
  of view), for drawing a sky dome over a tilted capture. Points are east, north, up in metres from
  the LookAt target.

Site values (latitude, longitude, time zone, camera) are inputs; nothing here is site-specific.
"""
import math
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


def _sun(dt_utc, lat, lon):
    """Azimuth (deg clockwise from north) and altitude (deg) at a UTC datetime."""
    jd = dt_utc.timestamp() / 86400 + 2440587.5
    t = (jd - 2451545.0) / 36525
    l0 = (280.46646 + t * (36000.76983 + t * 0.0003032)) % 360
    m = 357.52911 + t * (35999.05029 - 0.0001537 * t)
    e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    mr = math.radians(m)
    c = (math.sin(mr) * (1.914602 - t * (0.004817 + 0.000014 * t))
         + math.sin(2 * mr) * (0.019993 - 0.000101 * t) + math.sin(3 * mr) * 0.000289)
    omega = 125.04 - 1934.136 * t
    lam = l0 + c - 0.00569 - 0.00478 * math.sin(math.radians(omega))
    eps0 = 23 + (26 + (21.448 - t * (46.815 + t * (0.00059 - t * 0.001813))) / 60) / 60
    eps = math.radians(eps0 + 0.00256 * math.cos(math.radians(omega)))
    decl = math.asin(math.sin(eps) * math.sin(math.radians(lam)))
    y = math.tan(eps / 2) ** 2
    l0r = math.radians(l0)
    eot = 4 * math.degrees(y * math.sin(2 * l0r) - 2 * e * math.sin(mr)
                           + 4 * e * y * math.sin(mr) * math.cos(2 * l0r)
                           - 0.5 * y * y * math.sin(4 * l0r) - 1.25 * e * e * math.sin(2 * mr))
    minutes = dt_utc.hour * 60 + dt_utc.minute + dt_utc.second / 60
    ha = math.radians(((minutes + eot + 4 * lon) / 4) - 180)
    phi = math.radians(lat)
    cos_z = math.sin(phi) * math.sin(decl) + math.cos(phi) * math.cos(decl) * math.cos(ha)
    zen = math.acos(max(-1.0, min(1.0, cos_z)))
    az = math.degrees(math.atan2(math.sin(ha),
                                 math.cos(ha) * math.sin(phi) - math.tan(decl) * math.cos(phi))) + 180
    return az % 360, 90 - math.degrees(zen)


def _at(day, minutes, lat, lon, tz):
    local = datetime.combine(day, time(), ZoneInfo(tz)) + timedelta(minutes=minutes)
    az, alt = _sun(local.astimezone(timezone.utc), lat, lon)
    return {"time": local, "az": az, "alt": alt}


def day_arc(day, lat, lon, tz, step_min=5):
    """Sun positions every step_min minutes while the sun is above the horizon."""
    pts = (_at(day, m, lat, lon, tz) for m in range(0, 24 * 60 + 1, step_min))
    return [p for p in pts if p["alt"] > 0]


def hour_marks(day, lat, lon, tz):
    """Sun positions on whole clock hours while the sun is up."""
    pts = (_at(day, h * 60, lat, lon, tz) for h in range(24))
    return [p for p in pts if p["alt"] > 0]


def sunrise_sunset(day, lat, lon, tz, horizon=-0.833):
    """Almanac sunrise and sunset to the minute: sun's centre 0.833° below the horizon
    (refraction plus the sun's radius)."""
    up = [_at(day, m, lat, lon, tz) for m in range(0, 24 * 60)]
    up = [p for p in up if p["alt"] > horizon]
    return up[0]["time"], up[-1]["time"]


def solar_noon(day, lat, lon, tz):
    """Highest sun of the day, to the minute."""
    return max((_at(day, m, lat, lon, tz) for m in range(10 * 60, 15 * 60)), key=lambda p: p["alt"])


def polar_offset(az, alt, radius):
    """(east, north) offset from the site for a top-down sun-path diagram."""
    r = radius * (90 - alt) / 90
    a = math.radians(az)
    return r * math.sin(a), r * math.cos(a)


def sky_point(az, alt, radius):
    """(east, north, up) on a dome of the given radius."""
    a, h = math.radians(az), math.radians(alt)
    return radius * math.cos(h) * math.sin(a), radius * math.cos(h) * math.cos(a), radius * math.sin(h)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _norm(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


class Camera:
    """Pinhole camera for a Google Earth LookAt. heading = direction looked, tilt from straight down."""

    def __init__(self, heading, tilt, range_m, fov_h, width, height):
        h, t = math.radians(heading), math.radians(tilt)
        look = (math.sin(h), math.cos(h), 0.0)
        self.pos = (-range_m * math.sin(t) * look[0], -range_m * math.sin(t) * look[1],
                    range_m * math.cos(t))
        self.fwd = _norm(tuple(-c for c in self.pos))
        self.right = _norm(_cross(self.fwd, (0.0, 0.0, 1.0)))
        self.up = _cross(self.right, self.fwd)
        self.f = (width / 2) / math.tan(math.radians(fov_h) / 2)
        self.cx, self.cy = width / 2, height / 2

    def project(self, p):
        d = tuple(a - b for a, b in zip(p, self.pos))
        z = _dot(d, self.fwd)
        return self.cx + self.f * _dot(d, self.right) / z, self.cy - self.f * _dot(d, self.up) / z
