from datetime import datetime, timezone

import httpx
from sqlalchemy import desc
from sqlalchemy.orm import Session

from db.database import add_market_price, get_market_prices


def save_price(crop_type, region, price_per_quintal):
    recorded_at = datetime.now(timezone.utc).isoformat()
    add_market_price(crop_type, region, price_per_quintal, recorded_at)


def list_prices():
    return get_market_prices()


def snapshot_from_db(db: Session, crop_type: str, region: str, persist: bool = False) -> dict:
    rows = (
        db.query(MarketPrice)
        .filter(MarketPrice.crop_type == crop_type, MarketPrice.region == region)
        .order_by(desc(MarketPrice.recorded_at))
        .limit(14)
        .all()
    )
    prices = list(reversed([row.price_per_quintal for row in rows]))
    analysis = analyze_price_series(prices)
    analysis.update({"crop_type": crop_type, "region": region})
    forge = persist_snapshot_to_forge(crop_type, region, analysis, persist=persist)
    if forge:
        analysis["forge"] = forge
    return analysis


def ingest_government_prices(db: Session, crop_type: str, region: str) -> dict:
    if not settings.MARKET_PRICE_API_KEY:
        return {"ingested": 0, "source": "none", "reason": "MARKET_PRICE_API_KEY is not configured"}

    params = {
        "api-key": settings.MARKET_PRICE_API_KEY,
        "format": "json",
        "limit": 50,
        "filters[commodity]": crop_type,
    }
    try:
        response = httpx.get(settings.GOV_AGRI_DATA_API_URL, params=params, timeout=20)
        response.raise_for_status()
        payload = response.json()
    except httpx.HTTPError as exc:
        return {"ingested": 0, "source": settings.GOV_AGRI_DATA_API_URL, "error": str(exc)}

    records = payload.get("records") or payload.get("data") or []
    ingested = 0
    for record in records:
        market = (record.get("market") or record.get("district") or region or "").lower()
        if region.lower() not in market and market not in region.lower():
            continue
        price_raw = record.get("modal_price") or record.get("price") or record.get("modalPrice")
        try:
            price = float(str(price_raw).replace(",", ""))
        except (TypeError, ValueError):
            continue
        db.add(MarketPrice(crop_type=crop_type, region=region, price_per_quintal=price))
        ingested += 1

    if ingested:
        db.commit()
    return {"ingested": ingested, "source": settings.GOV_AGRI_DATA_API_URL}
