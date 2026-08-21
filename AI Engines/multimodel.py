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
from shared.forge_client import ForgeClientError, submit_disease_prediction


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
                      crop_id=None, persist_to_forge=False):
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
        "recommendations": recommendations,
        "soil_temperature": _to_float(soil_temperature),
    }

    if persist_to_forge and crop_id:
        try:
            submit_disease_prediction({
                "crop_id": crop_id,
                "image_url": image_path,
                "disease_name": vision["disease"],
                "confidence": vision["confidence"],
                "severity": vision["severity"],
            })
            result["forge_persisted"] = True
        except ForgeClientError as exc:
            result["forge_persisted"] = False
            result["forge_error"] = str(exc)

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
