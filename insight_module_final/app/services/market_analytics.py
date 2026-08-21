from typing import Iterable, Optional

try:
    from shared.forge_client import ForgeClientError, submit_market_snapshot
except ImportError:
    import os
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
    from shared.forge_client import ForgeClientError, submit_market_snapshot


def _linear_forecast(prices: list[float]) -> tuple[str, Optional[float], str]:
    if not prices:
        return "Unknown", None, "Unknown"
    if len(prices) == 1:
        return "Stable", round(prices[0], 2), "Medium"

    n = len(prices)
    xs = list(range(n))
    mean_x = sum(xs) / n
    mean_y = sum(prices) / n
    denom = sum((x - mean_x) ** 2 for x in xs) or 1
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, prices)) / denom
    forecast = prices[-1] + slope
    pct = (slope / prices[-1]) * 100 if prices[-1] else 0

    if pct >= 3:
        trend = "Rising"
    elif pct <= -3:
        trend = "Falling"
    else:
        trend = "Stable"

    demand = {"Rising": "High", "Stable": "Medium", "Falling": "Low"}[trend]
    return trend, round(forecast, 2), demand


def analyze_price_series(prices: Iterable[float]) -> dict:
    series = [float(p) for p in prices]
    trend, forecast, demand = _linear_forecast(series)
    current = series[-1] if series else 0.0
    return {
        "current_price": current,
        "trend": trend,
        "forecast_price": forecast,
        "demand_indicator": demand,
        "observations": len(series),
    }


def persist_snapshot_to_forge(crop_type, region, snapshot, persist=True):
    if not persist:
        return None
    payload = {
        "crop_name": crop_type,
        "region": region,
        "current_price": snapshot["current_price"],
        "trend": snapshot["trend"],
        "demand_indicator": snapshot["demand_indicator"],
        "forecast_price": snapshot.get("forecast_price"),
    }
    try:
        return submit_market_snapshot(payload)
    except ForgeClientError as exc:
        return {"error": str(exc)}
