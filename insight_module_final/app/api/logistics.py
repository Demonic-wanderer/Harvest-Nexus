from fastapi import APIRouter
from pydantic import BaseModel

from app.services.logistics_service import (
    estimate_transport_cost,
    is_worth_transporting,
)

router = APIRouter(prefix="/logistics", tags=["Logistics"])


class TransportEstimateRequest(BaseModel):
    distance_km: float
    quantity_quintals: float


class TransportEstimateResponse(BaseModel):
    estimated_cost: float


@router.post("/transport-cost", response_model=TransportEstimateResponse)
def transport_cost(req: TransportEstimateRequest):
    cost = estimate_transport_cost(req.distance_km, req.quantity_quintals)
    return TransportEstimateResponse(estimated_cost=cost)


class WorthTransportingRequest(BaseModel):
    local_price: float
    remote_price: float
    transport_cost: float
    quantity_quintals: float


class WorthTransportingResponse(BaseModel):
    recommended: bool


@router.post("/worth-transporting", response_model=WorthTransportingResponse)
def worth_transporting(req: WorthTransportingRequest):
    recommended = is_worth_transporting(
        req.local_price, req.remote_price, req.transport_cost, req.quantity_quintals
    )
    return WorthTransportingResponse(recommended=recommended)
