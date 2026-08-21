"""
Market Intelligence Engine API.
Note: this uses the SQLAlchemy models (app/models/db_models.py), separate
from the sqlite-based CLI tool in app/main.py. Wire this up once you move
the CLI's data into the shared Cloud Backend DB.
"""
from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.db_models import MarketPrice
from app.models.schemas import MarketQuery, MarketResponse

router = APIRouter(prefix="/market", tags=["Market Intelligence Engine"])


def _calculate_trend(prices: list[MarketPrice]) -> str:
    if len(prices) < 2:
        return "Stable"
    latest, previous = prices[0].price_per_quintal, prices[1].price_per_quintal
    if previous == 0:
        return "Stable"
    pct_change = ((latest - previous) / previous) * 100
    if pct_change >= settings.RISING_TREND_THRESHOLD_PCT:
        return "Rising"
    if pct_change <= settings.FALLING_TREND_THRESHOLD_PCT:
        return "Falling"
    return "Stable"


def _estimate_demand(trend: str) -> str:
    return {
        "Rising": "High", "Stable": "Medium",
        "Falling": "Low", "Unknown": "Unknown",
    }[trend]


@router.post("/snapshot", response_model=MarketResponse)
def market_snapshot(query: MarketQuery, db: Session = Depends()):
    """
    Input: crop_type + region
    Output: current price, expected trend, demand indicator
    """
    recent_prices = (
        db.query(MarketPrice)
        .filter(MarketPrice.crop_type == query.crop_type, MarketPrice.region == query.region)
        .order_by(desc(MarketPrice.recorded_at))
        .limit(2)
        .all()
    )

    if not recent_prices:
        return MarketResponse(
            crop_type=query.crop_type, region=query.region,
            current_price=0.0, trend="Unknown", demand_indicator="Unknown",
        )

    trend = _calculate_trend(recent_prices)
    return MarketResponse(
        crop_type=query.crop_type,
        region=query.region,
        current_price=recent_prices[0].price_per_quintal,
        trend=trend,
        demand_indicator=_estimate_demand(trend),
    )
