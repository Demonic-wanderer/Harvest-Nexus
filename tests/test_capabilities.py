import os
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "AI Engines"))
sys.path.insert(0, str(ROOT / "insight_module_final"))

from advisory_engine.advisory import generate_advisory
from advisory_engine.schemas import AdvisoryRequest
from disease_detection import predict_disease
from disease_mapping import severity_from_prediction
from multimodel import analyze_multimodal, compute_farm_health_score
from shared.geo import geocode_location, haversine_km
from app.services.logistics_service import quote_route
from app.services.market_analytics import analyze_price_series


def _green_leaf(path):
    Image.new("RGB", (224, 224), (30, 170, 40)).save(path)


def test_severity_mapping():
    assert severity_from_prediction("Tomato___healthy", 99) == "none"
    assert severity_from_prediction("Tomato___Early_blight", 90) == "high"
    assert severity_from_prediction("Tomato___Early_blight", 70) == "medium"
    print("severity mapping ok")


def test_disease_predict_without_checkpoint():
    with tempfile.TemporaryDirectory() as tmp:
        image_path = os.path.join(tmp, "leaf.png")
        _green_leaf(image_path)
        result = predict_disease(image_path)
        assert "disease" in result
        assert "severity" in result
        assert "treatments" in result
        assert result["confidence"] > 0
        print("disease predict ok", result["source"], result["severity"])


def test_multimodal_score_not_hardcoded_healthy():
    vision = {"severity": "high", "display_name": "Early blight", "confidence": 90}
    score, deductions = compute_farm_health_score(vision, 10, 4.5, 10, 10, 10, 38, 90, True)
    assert score < 60
    assert deductions
    with tempfile.TemporaryDirectory() as tmp:
        image_path = os.path.join(tmp, "leaf.png")
        _green_leaf(image_path)
        result = analyze_multimodal(
            image_path, "Tomato", "Vegetative", 12, 28, 6.8, 40, 35, 40, 30, 50, "no"
        )
        assert "farm_health_score" in result
        assert result["crop_health_status"] in {"healthy", "watch", "stressed"}
    print("multimodal score ok", score)


def test_advisory_market_and_health_score():
    request = AdvisoryRequest(
        crop="Tomato",
        crop_stage="Vegetative",
        disease={"name": "Early Blight", "confidence": 0.9, "severity": "high"},
        soil={"moisture": 12, "ph": 6.5, "nitrogen": 20, "phosphorus": 35, "potassium": 40},
        weather={"temperature": 36, "humidity": 85, "rain_probability": 10},
        market={"crop_name": "Tomato", "region": "Indore", "current_price": 1800, "trend": "Falling", "demand_indicator": "Low", "forecast_price": 1700},
    )
    result = generate_advisory(request)
    categories = [item["category"] for item in result["recommendations"]]
    assert "market" in categories
    assert result["farm_health_score"] < 70
    print("advisory market+score ok", result["farm_health_score"])


def test_market_forecast_not_two_price_only():
    rising = analyze_price_series([100, 110, 125, 140, 160])
    falling = analyze_price_series([200, 190, 170, 150, 130])
    assert rising["trend"] == "Rising"
    assert falling["trend"] == "Falling"
    assert rising["forecast_price"] > rising["current_price"]
    print("market forecast ok", rising["forecast_price"])


def test_buyer_distance_and_logistics_quotes():
    km = haversine_km(22.7196, 75.8577, 23.2599, 77.4126)
    assert 150 < km < 220
    assert geocode_location("Indore") == (22.7196, 75.8577)
    quote = quote_route(quantity_quintals=20, origin="Indore", destination="Bhopal")
    assert quote["distance_km"] > 0
    assert quote["quotes"]
    assert quote["quotes"][0]["estimated_cost"] > 0
    print("geo+logistics ok", quote["distance_km"], len(quote["quotes"]))


from datetime import date, timedelta
from multimodel import forecast_harvest_volume


def test_harvest_yield_forecast():
    forecast = forecast_harvest_volume(
        crop="Tomato",
        land_size_acres=2.0,
        farm_health_score=85,
        growth_stage="Fruiting",
        disease_severity="low",
    )
    assert forecast["estimated_yield_total_quintals"] > 0
    assert forecast["base_yield_per_acre_q"] == 120.0
    assert forecast["yield_range_max_quintals"] >= forecast["estimated_yield_total_quintals"]
    print("yield forecast ok:", forecast["summary"])


def test_chemical_safety_and_harvest_sync():
    # 1. Chemical safety rain alert
    rain_request = AdvisoryRequest(
        crop="Tomato",
        disease={"name": "Early Blight", "confidence": 0.85, "severity": "high"},
        soil={"moisture": 35, "nitrogen": 40},
        weather={"temperature": 28, "humidity": 85, "rain_probability": 75},
    )
    rain_advisory = generate_advisory(rain_request)
    categories = [item["category"] for item in rain_advisory["recommendations"]]
    assert "safety" in categories

    # 2. Harvest market sync opportunity
    near_harvest = (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")
    sync_request = AdvisoryRequest(
        crop="Tomato",
        crop_stage="Fruiting",
        expected_harvest_date=near_harvest,
        disease={"name": "healthy", "confidence": 0.95},
        soil={"moisture": 45, "nitrogen": 40},
        weather={"temperature": 26, "humidity": 60, "rain_probability": 10},
        market={"crop_name": "Tomato", "region": "Indore", "current_price": 2300, "trend": "Rising", "demand_indicator": "High", "forecast_price": 2500},
    )
    sync_advisory = generate_advisory(sync_request)
    assert any("HARVEST LINKAGE" in item["action"] for item in sync_advisory["recommendations"])
    print("chemical safety & harvest sync ok")


if __name__ == "__main__":
    test_severity_mapping()
    test_disease_predict_without_checkpoint()
    test_multimodal_score_not_hardcoded_healthy()
    test_advisory_market_and_health_score()
    test_market_forecast_not_two_price_only()
    test_buyer_distance_and_logistics_quotes()
    test_harvest_yield_forecast()
    test_chemical_safety_and_harvest_sync()
    print("\n===== ALL CAPABILITY TESTS PASSED WITH 100% SUCCESS =====")
