from pydantic import BaseModel
from typing import Optional


class DiseaseData(BaseModel):
    name: Optional[str] = None
    confidence: float = 0.0
    severity: Optional[str] = None


class SoilData(BaseModel):
    moisture: float
    ph: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None


class WeatherData(BaseModel):
    temperature: float
    humidity: float
    rain_probability: Optional[float] = None


class MarketData(BaseModel):
    crop_name: Optional[str] = None
    region: Optional[str] = None
    current_price: Optional[float] = None
    trend: Optional[str] = None
    demand_indicator: Optional[str] = None
    forecast_price: Optional[float] = None


class AdvisoryRequest(BaseModel):
    crop: str
    crop_stage: Optional[str] = None
    farm_id: Optional[str] = None
    crop_id: Optional[str] = None
    disease_id: Optional[str] = None
    farm_health_score: Optional[int] = None
    persist_to_forge: bool = False
    disease: DiseaseData
    soil: SoilData
    weather: WeatherData
    market: Optional[MarketData] = None
