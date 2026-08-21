from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.schemas import BuyerLinkageResponse, BuyerQuery
from app.services.buyer_service import find_buyers_and_mandis

router = APIRouter(prefix="/buyers", tags=["Buyer Linkage Engine"])


@router.post("/nearby", response_model=BuyerLinkageResponse)
def nearby_buyers(query: BuyerQuery, db: Session = Depends(get_db)):  # noqa: B008
    """
    Input: crop_type + location
    Output: nearby buyers, nearby mandis, contact information
    """
    return find_buyers_and_mandis(db, query.crop_type, query.location)
