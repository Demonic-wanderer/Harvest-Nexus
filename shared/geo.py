"""Haversine distance helpers used by Insight and Forge-facing Python services."""

from __future__ import annotations

import math
from typing import Optional

EARTH_RADIUS_KM = 6371.0

CITY_COORDINATES = {
    "indore": (22.7196, 75.8577),
    "bhopal": (23.2599, 77.4126),
    "ujjain": (23.1765, 75.7885),
    "gwalior": (26.2183, 78.1828),
    "jabalpur": (23.1815, 79.9864),
    "delhi": (28.6139, 77.2090),
    "lucknow": (26.8467, 80.9462),
    "patna": (25.5941, 85.1376),
    "jaipur": (26.9124, 75.7873),
    "nagpur": (21.1458, 79.0882),
    "pune": (18.5204, 73.8567),
    "hyderabad": (17.3850, 78.4867),
}


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return round(EARTH_RADIUS_KM * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)


def geocode_location(location: Optional[str]) -> Optional[tuple[float, float]]:
    if not location:
        return None
    key = location.strip().lower()
    if key in CITY_COORDINATES:
        return CITY_COORDINATES[key]
    for city, coords in CITY_COORDINATES.items():
        if city in key:
            return coords
    return None
