import os
import sys
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from disease_detection import predict_disease
from multimodel import analyze_multimodal

app = FastAPI(title="Harvest Nexus Oracle")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    image_path: str
    crop_id: Optional[str] = None


class MultimodalRequest(BaseModel):
    image_path: str
    crop: str = "Tomato"
    growth_stage: Optional[str] = None
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
    return {"status": "ok", "service": "oracle"}


@app.post("/predict")
def predict(req: PredictRequest):
    try:
        return predict_disease(req.image_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/predict-upload")
async def predict_upload(file: UploadFile = File(...)):
    import shutil
    import tempfile

    suffix = os.path.splitext(file.filename or "leaf.jpg")[1] or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        path = tmp.name
    try:
        return predict_disease(path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    finally:
        if os.path.exists(path):
            os.remove(path)


@app.post("/assess")
def assess(req: MultimodalRequest):
    try:
        return analyze_multimodal(
            req.image_path,
            req.crop,
            req.growth_stage,
            req.soil_moisture,
            req.soil_temperature,
            req.soil_ph,
            req.nitrogen,
            req.phosphorus,
            req.potassium,
            req.air_temperature,
            req.humidity,
            req.rain_expected,
            crop_id=req.crop_id,
            persist_to_forge=req.persist_to_forge,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
