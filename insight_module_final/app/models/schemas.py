import typing

from pydantic import BaseModel


class MarketQuery(BaseModel):
    crop_type: str
    region: str


class MarketResponse(BaseModel):
    crop_type: str
    region: str
    current_price: float
    trend: str
    demand_indicator: str


class BuyerQuery(BaseModel):
    crop_type: str
    location: str


class BuyerOut(BaseModel):
    name: str
    contact_number: typing.Optional[str]
    distance_km: typing.Optional[float] = None

    class Config:
        from_attributes = True


class MandiOut(BaseModel):
    name: str
    location: str
    contact_number: typing.Optional[str]

    class Config:
        from_attributes = True


class BuyerLinkageResponse(BaseModel):
    crop_type: str
    location: str
    nearby_buyers: list[BuyerOut]
    nearby_mandis: list[MandiOut]


class InsightSummary(BaseModel):
    market: MarketResponse
    buyer_linkage: BuyerLinkageResponse
