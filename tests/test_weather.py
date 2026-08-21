import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from weather.weather_api import rain_probability_for_current_hour


def test_uses_matching_hour_not_first_slot():
    hourly = {
        "time": [
            "2026-08-21T00:00",
            "2026-08-21T01:00",
            "2026-08-21T14:00",
            "2026-08-21T15:00",
        ],
        "precipitation_probability": [5, 10, 80, 20],
    }
    now = datetime(2026, 8, 21, 14, 12, tzinfo=timezone.utc)
    assert rain_probability_for_current_hour(hourly, now=now) == 80


def test_empty_hourly_returns_zero():
    assert rain_probability_for_current_hour({}, now=datetime.now(timezone.utc)) == 0


if __name__ == "__main__":
    test_uses_matching_hour_not_first_slot()
    test_empty_hourly_returns_zero()
    print("weather tests passed")
