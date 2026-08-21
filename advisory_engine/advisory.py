from .schemas import AdvisoryRequest
from .rules import (
    chemical_safety_rule,
    disease_rule,
    harvest_market_sync_rule,
    irrigation_rule,
    market_rule,
    nutrient_rule,
    ph_rule,
    weather_rule,
)
from .priority import calculate_priority as prioritize, get_highest_priority
from .formatter import format_action_plan

try:
    from shared.forge_client import ForgeClientError, submit_advisory
except ImportError:  # script executed from repo subfolders
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from shared.forge_client import ForgeClientError, submit_advisory


def _confidence_as_ratio(confidence):
    if confidence is None:
        return 0.0
    return confidence / 100.0 if confidence > 1 else confidence


def compute_farm_health_score(request: AdvisoryRequest, recommendations):
    if request.farm_health_score is not None:
        return max(0, min(100, int(request.farm_health_score)))

    score = 100
    disease_name = (request.disease.name or "").lower()
    confidence = _confidence_as_ratio(request.disease.confidence)
    if request.disease.severity == "high" or (disease_name and "healthy" not in disease_name and confidence >= 0.8):
        score -= 40
    elif request.disease.severity == "medium" or (disease_name and "healthy" not in disease_name and confidence >= 0.5):
        score -= 25
    elif disease_name and "healthy" not in disease_name:
        score -= 10

    if request.soil.moisture < 30:
        score -= 15
    elif request.soil.moisture > 80:
        score -= 10

    if request.soil.ph is not None and (request.soil.ph < 5.5 or request.soil.ph > 7.8):
        score -= 10

    if request.soil.nitrogen is not None and request.soil.nitrogen < 30:
        score -= 8
    if request.soil.phosphorus is not None and request.soil.phosphorus < 20:
        score -= 8
    if request.soil.potassium is not None and request.soil.potassium < 20:
        score -= 8

    if request.weather.temperature >= 35:
        score -= 8
    if request.weather.humidity >= 80:
        score -= 6

    high_count = sum(1 for item in recommendations if item.get("priority") == "HIGH")
    score -= 5 * max(0, high_count - 1)
    return max(0, min(100, score))


def _advice_text(plan, category):
    matches = [item["action"] for item in plan["recommendations"] if item["category"] == category]
    return " ".join(matches) if matches else None


def generate_advisory(request: AdvisoryRequest):
    recommendations = []

    # 1. Chemical Spray & Weather Safety Guardrail
    safety_result = chemical_safety_rule(
        disease_name=request.disease.name,
        severity=request.disease.severity,
        rain_probability=request.weather.rain_probability,
    )
    if safety_result:
        recommendations.append(safety_result)

    # 2. Disease Pathology Advisory
    if request.disease.name:
        disease_result = disease_rule(
            request.disease.name,
            _confidence_as_ratio(request.disease.confidence),
            crop=request.crop,
            severity=request.disease.severity,
        )
        recommendations.append(disease_result)

    # 3. Precision Irrigation Rule
    irrigation_result = irrigation_rule(
        request.soil.moisture,
        request.weather.rain_probability,
        crop_stage=request.crop_stage,
    )
    recommendations.append(irrigation_result)

    # 4. NPK Soil Nutrition Rule
    if request.soil.nitrogen is not None:
        nutrient_result = nutrient_rule(
            request.soil.nitrogen,
            request.soil.phosphorus,
            request.soil.potassium,
        )
        recommendations.append(nutrient_result)

    # 5. Soil pH Balance Rule
    ph_result = ph_rule(request.soil.ph)
    if ph_result:
        recommendations.append(ph_result)

    # 6. Microclimate & Weather Rule
    weather_result = weather_rule(
        request.weather.temperature,
        request.weather.humidity,
        crop=request.crop,
    )
    if weather_result:
        recommendations.append(weather_result)

    # 7. Harvest-to-Mandi Linkage Sync Rule (SIH Core Deliverable)
    harvest_sync_result = harvest_market_sync_rule(
        crop=request.crop,
        expected_harvest_date=request.expected_harvest_date,
        crop_stage=request.crop_stage,
        market=request.market,
    )
    if harvest_sync_result:
        recommendations.append(harvest_sync_result)

    # 8. General Market Price & Demand Rule
    market_result = market_rule(request.market)
    if market_result and not harvest_sync_result:
        recommendations.append(market_result)

    prioritized = prioritize(recommendations)
    farm_health_score = compute_farm_health_score(request, prioritized)
    plan = format_action_plan(prioritized)
    highest = get_highest_priority(prioritized)
    plan["farm_health_score"] = farm_health_score
    plan["priority_level"] = highest["priority"] if highest else "LOW"

    if request.persist_to_forge and request.farm_id:
        payload = {
            "farm_id": request.farm_id,
            "crop_id": request.crop_id,
            "disease_id": request.disease_id,
            "irrigation_advice": _advice_text(plan, "irrigation"),
            "fertilizer_advice": _advice_text(plan, "nutrient"),
            "treatment_plan": _advice_text(plan, "disease"),
            "priority_level": plan["priority_level"],
            "farm_health_score": farm_health_score,
        }
        try:
            plan["forge"] = submit_advisory(payload)
            plan["forge_persisted"] = True
        except ForgeClientError as exc:
            plan["forge_persisted"] = False
            plan["forge_error"] = str(exc)

    return plan
