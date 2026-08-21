import os
import shutil
import sys
import tempfile
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from disease_detection import predict_disease
from multimodel import analyze_multimodal, forecast_harvest_volume

app = FastAPI(title="Harvest Nexus Oracle - AI & Disease Intelligence Engine")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    image_path: str
    crop_id: Optional[str] = None


class YieldForecastRequest(BaseModel):
    crop: str = "Tomato"
    land_size_acres: float = 1.0
    farm_health_score: int = 100
    growth_stage: Optional[str] = "Vegetative"
    disease_severity: Optional[str] = "none"


class MultimodalRequest(BaseModel):
    image_path: str
    crop: str = "Tomato"
    growth_stage: Optional[str] = "Vegetative"
    land_size_acres: Optional[float] = 1.0
    soil_moisture: float
    soil_temperature: Optional[float] = None
    soil_ph: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    air_temperature: Optional[float] = None
    humidity: Optional[float] = None
    rain_expected: Optional[str] = None
    crop_id: Optional[str] = None
    persist_to_forge: bool = False


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "oracle",
        "modules": ["disease_vision_mobilenetv2", "multimodal_health_score", "harvest_yield_forecaster"],
    }


@app.post("/predict")
def predict(req: PredictRequest):
    try:
        return predict_disease(req.image_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/predict-upload")
async def predict_upload(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename or "leaf.jpg")[1] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        path = tmp.name
    try:
        return predict_disease(path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        if os.path.exists(path):
            os.remove(path)


@app.post("/forecast-yield")
def yield_forecast_endpoint(req: YieldForecastRequest):
    return forecast_harvest_volume(
        crop=req.crop,
        land_size_acres=req.land_size_acres,
        farm_health_score=req.farm_health_score,
        growth_stage=req.growth_stage,
        disease_severity=req.disease_severity,
    )


@app.post("/assess")
def assess(req: MultimodalRequest):
    try:
        return analyze_multimodal(
            image_path=req.image_path,
            crop=req.crop,
            growth_stage=req.growth_stage or "Vegetative",
            soil_moisture=req.soil_moisture,
            soil_temperature=req.soil_temperature,
            soil_ph=req.soil_ph,
            nitrogen=req.nitrogen,
            phosphorus=req.phosphorus,
            potassium=req.potassium,
            air_temperature=req.air_temperature,
            humidity=req.humidity,
            rain_expected=req.rain_expected,
            land_size_acres=req.land_size_acres or 1.0,
            crop_id=req.crop_id,
            persist_to_forge=req.persist_to_forge,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/assess-upload")
async def assess_upload(
    file: UploadFile = File(...),
    crop: str = Form("Tomato"),
    growth_stage: str = Form("Vegetative"),
    land_size_acres: float = Form(1.0),
    soil_moisture: float = Form(30.0),
    soil_temperature: Optional[float] = Form(None),
    soil_ph: Optional[float] = Form(None),
    nitrogen: Optional[float] = Form(None),
    phosphorus: Optional[float] = Form(None),
    potassium: Optional[float] = Form(None),
    air_temperature: Optional[float] = Form(None),
    humidity: Optional[float] = Form(None),
    rain_expected: Optional[str] = Form(None),
    crop_id: Optional[str] = Form(None),
    persist_to_forge: bool = Form(False),
):
    """Convenience multipart endpoint for mobile uploads combining image + field telemetry."""
    suffix = os.path.splitext(file.filename or "leaf.jpg")[1] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        path = tmp.name

    try:
        return analyze_multimodal(
            image_path=path,
            crop=crop,
            growth_stage=growth_stage,
            soil_moisture=soil_moisture,
            soil_temperature=soil_temperature,
            soil_ph=soil_ph,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            air_temperature=air_temperature,
            humidity=humidity,
            rain_expected=rain_expected,
            land_size_acres=land_size_acres,
            crop_id=crop_id,
            persist_to_forge=persist_to_forge,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        if os.path.exists(path):
            os.remove(path)
