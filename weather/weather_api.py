from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import requests

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def parse_hourly_time(value: str, tz: timezone) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=tz)
    return parsed.astimezone(tz)


def rain_probability_for_current_hour(
    hourly: dict[str, Any],
    now: Optional[datetime] = None,
    utc_offset_seconds: int = 0,
) -> float:
    """Pick precipitation probability for the current hour, not the first forecast slot."""
    times = hourly.get("time") or []
    values = hourly.get("precipitation_probability") or []
    if not times or not values:
        return 0.0

    tz = timezone(timedelta(seconds=int(utc_offset_seconds or 0)))
    moment = now or datetime.now(timezone.utc)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    target = moment.astimezone(tz).replace(minute=0, second=0, microsecond=0)

    best_index = 0
    best_delta = None
    for index, stamp in enumerate(times):
        if index >= len(values):
            break
        hour = parse_hourly_time(stamp, tz).replace(minute=0, second=0, microsecond=0)
        delta = abs((hour - target).total_seconds())
        if best_delta is None or delta < best_delta:
            best_delta = delta
            best_index = index
            if delta == 0:
                break

    probability = values[best_index]
    return float(probability if probability is not None else 0.0)


def get_weather(latitude, longitude, now: Optional[datetime] = None):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation",
        "hourly": "precipitation_probability",
        "forecast_days": 1,
        "timezone": "auto",
    }

    response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data["current"]
    rain_probability = rain_probability_for_current_hour(
        data.get("hourly") or {},
        now=now,
        utc_offset_seconds=data.get("utc_offset_seconds") or 0,
    )

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "rain_probability": rain_probability,
        "precipitation": current.get("precipitation"),
        "observed_at": current.get("time"),
    }


if __name__ == "__main__":
    weather = get_weather(22.7196, 75.8577)
    print("=== LIVE WEATHER ===")
    print("Temperature:", weather["temperature"], "°C")
    print("Humidity:", weather["humidity"], "%")
    print("Rain Probability:", weather["rain_probability"], "%")
