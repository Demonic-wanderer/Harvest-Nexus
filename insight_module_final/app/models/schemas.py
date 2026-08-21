import typing

from pydantic import BaseModel


class MarketQuery(BaseModel):
    crop_type: str
    region: str
    ingest: bool = False
    persist_to_forge: bool = False


class MarketResponse(BaseModel):
    crop_type: str
    region: str
    current_price: float
    trend: str
    demand_indicator: str
    forecast_price: typing.Optional[float] = None
    observations: typing.Optional[int] = None
    forge: typing.Optional[dict] = None


class BuyerQuery(BaseModel):
    crop_type: str
    location: str
    origin_lat: typing.Optional[float] = None
    origin_lon: typing.Optional[float] = None
    radius_km: float = 150


class BuyerOut(BaseModel):
    name: str
    contact_number: typing.Optional[str] = None
    location: typing.Optional[str] = None
    distance_km: typing.Optional[float] = None

    class Config:
        from_attributes = True


class MandiOut(BaseModel):
    name: str
    location: str
    contact_number: typing.Optional[str] = None
    distance_km: typing.Optional[float] = None

    class Config:
        from_attributes = True


class BuyerLinkageResponse(BaseModel):
    crop_type: str
    location: str
    origin_lat: typing.Optional[float] = None
    origin_lon: typing.Optional[float] = None
    nearby_buyers: list[BuyerOut]
    nearby_mandis: list[MandiOut]


class InsightSummary(BaseModel):
    market: MarketResponse
    buyer_linkage: BuyerLinkageResponse
