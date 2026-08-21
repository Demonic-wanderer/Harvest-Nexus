from typing import Optional

from sqlalchemy.orm import Session

from app.models.db_models import Buyer, Mandi
from app.models.schemas import BuyerLinkageResponse, BuyerOut, MandiOut

try:
    from shared.geo import geocode_location, haversine_km
except ImportError:
    import os
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
    from shared.geo import geocode_location, haversine_km


def _coords_for(entity, fallback_location: Optional[str] = None):
    lat = getattr(entity, "latitude", None)
    lon = getattr(entity, "longitude", None)
    if lat is not None and lon is not None:
        return float(lat), float(lon)
    return geocode_location(getattr(entity, "location", None) or fallback_location)


def find_buyers_and_mandis(
    db: Session,
    crop_type: str,
    location: str,
    origin_lat: Optional[float] = None,
    origin_lon: Optional[float] = None,
    radius_km: float = 150,
) -> BuyerLinkageResponse:
    origin = (origin_lat, origin_lon) if origin_lat is not None and origin_lon is not None else geocode_location(location)

    matched_buyers = (
        db.query(Buyer)
        .filter(Buyer.crop_types.ilike(f"%{crop_type}%"))
        .limit(50)
        .all()
    )
    matched_mandis = db.query(Mandi).limit(50).all()

    buyers_out = []
    for buyer in matched_buyers:
        coords = _coords_for(buyer)
        distance = haversine_km(origin[0], origin[1], coords[0], coords[1]) if origin and coords else None
        if distance is not None and distance > radius_km:
            continue
        if distance is None and location and location.lower() not in (buyer.location or "").lower():
            continue
        item = BuyerOut.model_validate(buyer)
        item.distance_km = distance
        buyers_out.append(item)

    mandis_out = []
    for mandi in matched_mandis:
        coords = _coords_for(mandi)
        distance = haversine_km(origin[0], origin[1], coords[0], coords[1]) if origin and coords else None
        if distance is not None and distance > radius_km:
            continue
        if distance is None and location and location.lower() not in (mandi.location or "").lower():
            continue
        item = MandiOut.model_validate(mandi)
        item.distance_km = distance
        mandis_out.append(item)

    buyers_out.sort(key=lambda item: item.distance_km if item.distance_km is not None else 10_000)
    mandis_out.sort(key=lambda item: item.distance_km if item.distance_km is not None else 10_000)

    return BuyerLinkageResponse(
        crop_type=crop_type,
        location=location,
        origin_lat=origin[0] if origin else None,
        origin_lon=origin[1] if origin else None,
        nearby_buyers=buyers_out[:10],
        nearby_mandis=mandis_out[:10],
    )
