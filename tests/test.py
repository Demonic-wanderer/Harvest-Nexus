import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from advisory_engine.advisory import generate_advisory
from advisory_engine.schemas import AdvisoryRequest


def make_request(
    disease_name=None,
    confidence=0.0,
    moisture=50,
    ph=6.5,
    nitrogen=50,
    phosphorus=50,
    potassium=50,
    temperature=25,
    humidity=60,
    rain_probability=20
):
    return AdvisoryRequest(
        crop="Tomato",
        crop_stage="Vegetative",
        disease={
            "name": disease_name,
            "confidence": confidence
        },
        soil={
            "moisture": moisture,
            "ph": ph,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium
        },
        weather={
            "temperature": temperature,
            "humidity": humidity,
            "rain_probability": rain_probability
        }
    )


# TEST 1: High-confidence disease
def test_high_confidence_disease():
    request = make_request(
        disease_name="Early Blight",
        confidence=0.90
    )

    result = generate_advisory(request)

    categories = [item["category"] for item in result["recommendations"]]

    assert "disease" in categories
    assert result["farm_health_score"] <= 100
    print("TEST 1 PASSED")


# TEST 2: Low soil moisture + high rainfall
def test_low_moisture_high_rain():
    request = make_request(
        moisture=10,
        rain_probability=100
    )

    result = generate_advisory(request)

    irrigation = [
        item for item in result["recommendations"]
        if item["category"] == "irrigation"
    ]

    assert len(irrigation) > 0
    assert irrigation[0]["priority"] == "MEDIUM"

    print("TEST 2 PASSED")


# TEST 3: Low nitrogen
def test_low_nitrogen():
    request = make_request(
        nitrogen=20,
        phosphorus=35,
        potassium=40
    )

    result = generate_advisory(request)

    nutrient = [
        item for item in result["recommendations"]
        if item["category"] == "nutrient"
    ]

    assert len(nutrient) > 0

    print("TEST 3 PASSED")


# TEST 4: Normal soil pH
def test_normal_ph():
    request = make_request(
        ph=6.5
    )

    result = generate_advisory(request)

    ph_results = [
        item for item in result["recommendations"]
        if item["category"] == "soil_ph"
    ]

    assert len(ph_results) > 0
    assert ph_results[0]["priority"] == "LOW"

    print("TEST 4 PASSED")


# TEST 5: Priority ordering
def test_priority_order():
    request = make_request(
        disease_name="Early Blight",
        confidence=0.90,
        moisture=10,
        nitrogen=20
    )

    result = generate_advisory(request)

    recommendations = result["recommendations"]

    priorities = [item["priority"] for item in recommendations]

    priority_value = {
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    values = [priority_value[p] for p in priorities]

    assert values == sorted(values)

    print("TEST 5 PASSED")


# Run all tests
if __name__ == "__main__":
    test_high_confidence_disease()
    test_low_moisture_high_rain()
    test_low_nitrogen()
    test_normal_ph()
    test_priority_order()

    print("\n===== ALL TESTS PASSED =====")