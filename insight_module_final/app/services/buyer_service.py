from sqlalchemy.orm import Session

from app.models.db_models import Buyer, Mandi
from app.models.schemas import BuyerLinkageResponse, BuyerOut, MandiOut


def find_buyers_and_mandis(db: Session, crop_type: str, location: str) -> BuyerLinkageResponse:
    matched_buyers = (
        db.query(Buyer)
        .filter(Buyer.location.ilike(f"%{location}%"))
        .filter(Buyer.crop_types.ilike(f"%{crop_type}%"))
        .limit(10)
        .all()
    )

    matched_mandis = (
        db.query(Mandi)
        .filter(Mandi.location.ilike(f"%{location}%"))
        .limit(10)
        .all()
    )

    return BuyerLinkageResponse(
        crop_type=crop_type,
        location=location,
        nearby_buyers=[BuyerOut.model_validate(b) for b in matched_buyers],
        nearby_mandis=[MandiOut.model_validate(m) for m in matched_mandis],
    )
