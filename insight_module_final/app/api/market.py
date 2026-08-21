"""
Market Intelligence Engine API.
Note: this uses the SQLAlchemy models (app/models/db_models.py), separate
from the sqlite-based CLI tool in app/main.py. Wire this up once you move
the CLI's data into the shared Cloud Backend DB.
"""
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.schemas import MarketQuery, MarketResponse
from app.services.market_service import ingest_government_prices, snapshot_from_db

router = APIRouter(prefix="/market", tags=["Market Intelligence Engine"])


@router.post("/snapshot", response_model=MarketResponse)
def market_snapshot(query: MarketQuery, db: Session = Depends(get_db)):  # noqa: B008
    if query.ingest:
        ingest_government_prices(db, query.crop_type, query.region)
    analysis = snapshot_from_db(db, query.crop_type, query.region, persist=query.persist_to_forge)
    return MarketResponse(
        crop_type=query.crop_type,
        region=query.region,
        current_price=analysis["current_price"],
        trend=analysis["trend"],
        demand_indicator=analysis["demand_indicator"],
        forecast_price=analysis.get("forecast_price"),
        observations=analysis.get("observations"),
        forge=analysis.get("forge") if isinstance(analysis.get("forge"), dict) else None,
    )
