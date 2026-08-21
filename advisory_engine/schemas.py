from pydantic import BaseModel
from typing import Optional


class DiseaseData(BaseModel):
    name: Optional[str] = None
    confidence: float = 0.0


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


class AdvisoryRequest(BaseModel):
    crop: str
    crop_stage: Optional[str] = None
    disease: DiseaseData
    soil: SoilData
    weather: WeatherData