from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.logistics_service import (
    book_transport,
    estimate_transport_cost,
    is_worth_transporting,
    load_transporters,
    quote_route,
)

router = APIRouter(prefix="/logistics", tags=["Logistics"])


class TransportEstimateRequest(BaseModel):
    distance_km: float
    quantity_quintals: float
    rate_per_km_quintal: Optional[float] = None


class TransportEstimateResponse(BaseModel):
    estimated_cost: float


@router.post("/transport-cost", response_model=TransportEstimateResponse)
def transport_cost(req: TransportEstimateRequest):
    rate = req.rate_per_km_quintal if req.rate_per_km_quintal is not None else 2.5
    cost = estimate_transport_cost(req.distance_km, req.quantity_quintals, rate)
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


class RouteQuoteRequest(BaseModel):
    quantity_quintals: float
    origin: Optional[str] = None
    destination: Optional[str] = None
    origin_lat: Optional[float] = None
    origin_lon: Optional[float] = None
    dest_lat: Optional[float] = None
    dest_lon: Optional[float] = None


@router.get("/transporters")
def transporters():
    return {"transporters": load_transporters()}


@router.post("/quote")
def quote(req: RouteQuoteRequest):
    try:
        return quote_route(
            quantity_quintals=req.quantity_quintals,
            origin_lat=req.origin_lat,
            origin_lon=req.origin_lon,
            dest_lat=req.dest_lat,
            dest_lon=req.dest_lon,
            origin=req.origin,
            destination=req.destination,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


class BookTransportRequest(BaseModel):
    transaction_id: str
    transporter_name: str
    contact_phone: Optional[str] = None
    pickup_location: str
    drop_location: str
    estimated_cost: Optional[float] = None
    persist_to_forge: bool = True


@router.post("/book")
def book(req: BookTransportRequest):
    quote = {
        "transporter_name": req.transporter_name,
        "contact_phone": req.contact_phone,
        "estimated_cost": req.estimated_cost,
    }
    return book_transport(
        req.transaction_id,
        quote,
        req.pickup_location,
        req.drop_location,
        persist=req.persist_to_forge,
    )
