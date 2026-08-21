import os
import sys
import tempfile
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(ENGINE_DIR)
load_dotenv(os.path.join(REPO_ROOT, ".env"))
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from disease_detection import ModelUnavailableError, predict_disease
from multimodel import analyze_multimodal, forecast_harvest_volume

app = FastAPI(title="Harvest Nexus Oracle - AI & Disease Intelligence Engine")
MAX_IMAGE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
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
    farm_id: Optional[str] = None
    persist_to_forge: bool = False


def _api_error(status_code: int, code: str, message: str):
    raise HTTPException(status_code=status_code, detail={"code": code, "message": message})


def _model_ready() -> bool:
    """Verify the checkpoint exists without paying the model-load cost on health checks."""
    return os.path.exists(os.path.join(ENGINE_DIR, "mobilenetv2_disease.pth"))


async def _save_image_upload(file: UploadFile) -> str:
    if file.content_type and file.content_type.lower() not in ALLOWED_IMAGE_TYPES:
        _api_error(415, "unsupported_image_type", "Use a JPEG, PNG, or WebP leaf photograph.")

    payload = await file.read(MAX_IMAGE_BYTES + 1)
    if not payload:
        _api_error(400, "empty_image", "The selected image is empty. Choose another leaf photograph.")
    if len(payload) > MAX_IMAGE_BYTES:
        _api_error(413, "image_too_large", "Image must be 10 MB or smaller.")

    suffix = os.path.splitext(file.filename or "leaf.jpg")[1].lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        suffix = ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(payload)
        return tmp.name


def _raise_scan_error(exc: Exception):
    if isinstance(exc, ModelUnavailableError):
        _api_error(503, "model_unavailable", str(exc))
    if isinstance(exc, ValueError):
        _api_error(400, "invalid_image", "This is not a readable leaf image. Retake a clear photo and try again.")
    if isinstance(exc, FileNotFoundError):
        _api_error(404, "image_not_found", str(exc))
    raise exc


@app.get("/health")
def health():
    return {
        "status": "ok" if _model_ready() else "degraded",
        "service": "oracle",
        "model_ready": _model_ready(),
        "max_upload_mb": MAX_IMAGE_BYTES // (1024 * 1024),
        "modules": ["disease_vision_mobilenetv2", "multimodal_health_score", "harvest_yield_forecaster"],
    }


@app.post("/predict")
def predict(req: PredictRequest):
    try:
        return predict_disease(req.image_path)
    except (FileNotFoundError, ValueError, ModelUnavailableError) as exc:
        _raise_scan_error(exc)


@app.post("/predict-upload")
async def predict_upload(file: UploadFile = File(...)):
    path = await _save_image_upload(file)
    try:
        return predict_disease(path)
    except (FileNotFoundError, ValueError, ModelUnavailableError) as exc:
        _raise_scan_error(exc)
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
            farm_id=req.farm_id,
            persist_to_forge=req.persist_to_forge,
        )
    except (FileNotFoundError, ValueError, ModelUnavailableError) as exc:
        _raise_scan_error(exc)


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
    farm_id: Optional[str] = Form(None),
    persist_to_forge: bool = Form(False),
):
    """Convenience multipart endpoint for mobile uploads combining image + field telemetry."""
    path = await _save_image_upload(file)

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
            farm_id=farm_id,
            persist_to_forge=persist_to_forge,
        )
    except (FileNotFoundError, ValueError, ModelUnavailableError) as exc:
        _raise_scan_error(exc)
    finally:
        if os.path.exists(path):
            os.remove(path)
