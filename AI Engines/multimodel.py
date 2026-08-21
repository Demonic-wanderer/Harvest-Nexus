import os
import sys

from PIL import Image

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(ENGINE_DIR)
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from disease_detection import predict_disease
from disease_mapping import get_crop_base_yield
from shared.forge_client import ForgeClientError, submit_disease_prediction
from advisory_engine.advisory import generate_advisory
from advisory_engine.schemas import AdvisoryRequest


def _clamp(value, low=0, high=100):
    return max(low, min(high, value))


def _to_float(value, default=None):
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _boolish(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def forecast_harvest_volume(
    crop: str,
    land_size_acres: float = 1.0,
    farm_health_score: int = 100,
    growth_stage: str = "Vegetative",
    disease_severity: str = "none",
) -> dict:
    """
    Time-series & agronomic harvest yield estimation (Quintals)
    Combines ICAR benchmark crop productivity with current farm health score and growth phase.
    """
    acres = max(0.1, _to_float(land_size_acres, 1.0))
    score = _clamp(_to_float(farm_health_score, 100), 0, 100)
    base_yield_per_acre = get_crop_base_yield(crop)

    # Health factor scales potential yield: 100 score -> 100% potential, 50 score -> 70%
    health_factor = 0.40 + (0.60 * (score / 100.0))

    # Stage modifier: earlier stages have wider estimation intervals
    stage_key = (growth_stage or "Vegetative").strip().lower()
    if "seedling" in stage_key:
        variance_pct = 0.20
        stage_weight = 0.95
    elif "vegetative" in stage_key:
        variance_pct = 0.15
        stage_weight = 1.00
    elif "flower" in stage_key or "reproduct" in stage_key:
        variance_pct = 0.10
        stage_weight = 1.02
    elif "fruit" in stage_key or "grain" in stage_key:
        variance_pct = 0.08
        stage_weight = 1.03
    elif "matur" in stage_key or "harvest" in stage_key:
        variance_pct = 0.04
        stage_weight = 1.00
    else:
        variance_pct = 0.12
        stage_weight = 1.00

    estimated_per_acre = round(base_yield_per_acre * health_factor * stage_weight, 2)
    total_estimated_yield = round(estimated_per_acre * acres, 2)

    # Potential loss if disease is untreated
    loss_multiplier = {
        "high": 0.45,
        "medium": 0.25,
        "low": 0.10,
        "uncertain": 0.15,
        "none": 0.0,
    }.get((disease_severity or "none").lower(), 0.0)

    potential_loss_quintals = round(total_estimated_yield * loss_multiplier, 2)
    min_yield = round(max(0.0, total_estimated_yield * (1 - variance_pct)), 2)
    max_yield = round(total_estimated_yield * (1 + variance_pct), 2)

    return {
        "crop": crop,
        "land_size_acres": acres,
        "base_yield_per_acre_q": base_yield_per_acre,
        "estimated_yield_total_quintals": total_estimated_yield,
        "estimated_yield_per_acre_quintals": estimated_per_acre,
        "yield_range_min_quintals": min_yield,
        "yield_range_max_quintals": max_yield,
        "health_score_factor": round(health_factor, 2),
        "potential_loss_if_untreated_q": potential_loss_quintals,
        "forecast_confidence": "High" if variance_pct <= 0.10 else "Medium",
        "summary": (
            f"Estimated harvest of {total_estimated_yield} quintals across {acres} acre(s) "
            f"(~{estimated_per_acre} q/acre). "
            + (f"Treat active pathogen to safeguard up to {potential_loss_quintals} q." if potential_loss_quintals > 0 else "Foliage health supports target harvest output.")
        ),
    }


def compute_farm_health_score(vision, soil_moisture, soil_ph, nitrogen, phosphorus, potassium,
                              air_temperature, humidity, rain_expected):
    score = 100
    deductions = []

    severity = (vision or {}).get("severity", "none")
    if severity == "high":
        score -= 40
        deductions.append("high_disease_severity")
    elif severity == "medium":
        score -= 25
        deductions.append("medium_disease_severity")
    elif severity == "low":
        score -= 12
        deductions.append("low_disease_severity")
    elif severity == "uncertain":
        score -= 15
        deductions.append("unverified_disease_risk")

    moisture = _to_float(soil_moisture)
    if moisture is not None:
        if moisture < 25:
            score -= 15
            deductions.append("low_moisture")
        elif moisture > 80:
            score -= 10
            deductions.append("excess_moisture")

    ph = _to_float(soil_ph)
    if ph is not None and (ph < 5.5 or ph > 7.8):
        score -= 10
        deductions.append("ph_out_of_range")

    for nutrient, threshold, name in (
        (nitrogen, 30, "low_nitrogen"),
        (phosphorus, 20, "low_phosphorus"),
        (potassium, 20, "low_potassium"),
    ):
        value = _to_float(nutrient)
        if value is not None and value < threshold:
            score -= 8
            deductions.append(name)

    temperature = _to_float(air_temperature)
    humidity_value = _to_float(humidity)
    if temperature is not None and temperature >= 35:
        score -= 8
        deductions.append("heat_stress")
    if humidity_value is not None and humidity_value >= 85:
        score -= 6
        deductions.append("high_humidity")
    if _boolish(rain_expected) and moisture is not None and moisture > 60:
        score -= 4
        deductions.append("wet_canopy_risk")

    return _clamp(score), deductions


def analyze_multimodal(image_path, crop, growth_stage, soil_moisture, soil_temperature, soil_ph,
                      nitrogen, phosphorus, potassium, air_temperature, humidity, rain_expected,
                      land_size_acres=1.0, crop_id=None, farm_id=None, persist_to_forge=False):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Crop image '{image_path}' not found.")

    with Image.open(image_path) as img:
        img.verify()

    vision = predict_disease(image_path)
    score, deductions = compute_farm_health_score(
        vision, soil_moisture, soil_ph, nitrogen, phosphorus, potassium,
        air_temperature, humidity, rain_expected,
    )

    if score >= 80:
        status = "healthy"
    elif score >= 55:
        status = "watch"
    else:
        status = "stressed"

    recommendations = list(vision.get("treatments") or [])
    moisture = _to_float(soil_moisture)
    if moisture is not None and moisture < 30:
        recommendations.append("Low soil moisture. Irrigation recommended.")
    n, p, k = _to_float(nitrogen), _to_float(phosphorus), _to_float(potassium)
    if any(value is not None and value < threshold for value, threshold in ((n, 30), (p, 20), (k, 20))):
        recommendations.append("Nutrient levels are low. Adjust fertilizer NPK ratios.")
    if not recommendations:
        recommendations.append("Crop health is optimal. No active intervention needed.")

    # Yield forecast integration
    yield_forecast = forecast_harvest_volume(
        crop=crop,
        land_size_acres=land_size_acres or 1.0,
        farm_health_score=score,
        growth_stage=growth_stage,
        disease_severity=vision.get("severity", "none"),
    )

    result = {
        "crop": crop,
        "growth_stage": growth_stage,
        "crop_health_status": status,
        "farm_health_score": score,
        "score_deductions": deductions,
        "vision": vision,
        "vision_check": (
            f"{vision['display_name']} ({vision['confidence']}%, severity={vision['severity']})"
        ),
        "sensor_verdict": "Sensor anomalies detected." if deductions else "Soil NPK and moisture levels are within acceptable bounds.",
        "yield_forecast": yield_forecast,
        "recommendations": recommendations,
        "soil_temperature": _to_float(soil_temperature),
    }

    disease_id = None
    if persist_to_forge and crop_id:
        try:
            forge_response = submit_disease_prediction({
                "crop_id": crop_id,
                "image_url": image_path,
                "disease_name": vision["disease"],
                "confidence": vision["confidence"],
                "severity": vision["severity"],
            })
            disease_id = (((forge_response or {}).get("data") or {}).get("record") or {}).get("id")
            result["forge_persisted"] = True
        except ForgeClientError as exc:
            result["forge_persisted"] = False
            result["forge_error"] = str(exc)

    # Akasha's rule engine turns the same scan and sensor context into the
    # dashboard advisory. When farm_id is supplied it also persists that row.
    advisory = generate_advisory(AdvisoryRequest(
        crop=crop,
        crop_stage=growth_stage,
        land_size_acres=land_size_acres or 1.0,
        farm_id=farm_id,
        crop_id=crop_id,
        disease_id=disease_id,
        persist_to_forge=persist_to_forge,
        disease={"name": vision["disease"], "confidence": vision["confidence"], "severity": vision["severity"]},
        soil={"moisture": soil_moisture, "ph": soil_ph, "nitrogen": nitrogen, "phosphorus": phosphorus, "potassium": potassium},
        weather={"temperature": air_temperature or 30, "humidity": humidity or 60, "rain_probability": 0},
    ))
    result["advisory"] = advisory
    result["advisory_forge_persisted"] = advisory.get("forge_persisted", False)

    return result


def collect_farm_data():
    print("================================")
    print("   Harvest Nexus multimodal AI")
    print("================================")

    image_path = input("Enter crop image path: ")
    if not os.path.exists(image_path):
        print(f"Error: Image path '{image_path}' does not exist.")
        return

    crop = input("Enter crop name (e.g. Tomato, Wheat): ")
    growth_stage = input("Enter growth stage (e.g. Seedling, Vegetative, Flowering): ")

    try:
        soil_moisture = float(input("Enter soil moisture (%): "))
        soil_temperature = float(input("Enter soil temperature (°C): "))
        soil_ph = float(input("Enter soil pH: "))
        nitrogen = float(input("Enter nitrogen (mg/kg): "))
        phosphorus = float(input("Enter phosphorus (mg/kg): "))
        potassium = float(input("Enter potassium (mg/kg): "))
        air_temperature = float(input("Enter air temperature (°C): "))
        humidity = float(input("Enter humidity (%): "))
    except ValueError:
        print("Error: All numerical values must be valid integers/floats.")
        return

    rain_expected = input("Is rain expected? (Yes/No): ")

    result = analyze_multimodal(
        image_path, crop, growth_stage, soil_moisture, soil_temperature, soil_ph,
        nitrogen, phosphorus, potassium, air_temperature, humidity, rain_expected,
    )

    print("Health Status:", result["crop_health_status"].upper())
    print("Farm health score:", result["farm_health_score"])
    print("Vision Check:", result["vision_check"])
    print("Sensor Verdict:", result["sensor_verdict"])
    print("Recommendations:")
    for rec in result["recommendations"]:
        print(" -", rec)


if __name__ == "__main__":
    collect_farm_data()
