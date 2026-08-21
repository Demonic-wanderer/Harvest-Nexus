from datetime import datetime, date
from typing import Optional


def _clamp(val, low, high):
    try:
        return max(low, min(high, float(val)))
    except (TypeError, ValueError):
        return low


def irrigation_rule(soil_moisture, rain_probability=None, crop_stage=None):
    """
    Decides whether irrigation is required based on
    soil moisture, expected rainfall, and crop growth stage.
    """
    moisture = _clamp(soil_moisture, 0, 100)
    rain_prob = _clamp(rain_probability, 0, 100) if rain_probability is not None else None

    threshold = 30
    # Flowering and Fruiting stages require more water
    if crop_stage and crop_stage.lower() in ["flowering", "fruiting", "reproductive", "grain_filling"]:
        threshold = 40

    if moisture < threshold:
        if rain_prob is not None and rain_prob >= 60:
            return {
                "type": "irrigation",
                "priority": "MEDIUM",
                "message": (
                    f"Soil moisture is low ({moisture:.0f}%) during {crop_stage or 'critical'} stage, "
                    f"but rain probability is {rain_prob:.0f}%. Hold irrigation for 12–24h to avoid waterlogging."
                ),
            }

        return {
            "type": "irrigation",
            "priority": "HIGH",
            "message": f"Soil moisture is critically low ({moisture:.0f}%). Immediate irrigation is recommended for the {crop_stage or 'current'} stage.",
        }

    if moisture >= 60:
        return {
            "type": "irrigation",
            "priority": "LOW",
            "message": f"Soil moisture is sufficient ({moisture:.0f}%). Irrigation is not currently required.",
        }

    return {
        "type": "irrigation",
        "priority": "LOW",
        "message": f"Soil moisture is moderate ({moisture:.0f}%). Continue routine field monitoring.",
    }


def nutrient_rule(nitrogen, phosphorus, potassium):
    """
    Checks NPK levels and identifies nutrient deficiencies with ICAR dosage caps.
    """
    deficiencies = []
    advisories = []

    if nitrogen is not None:
        n_val = float(nitrogen)
        if n_val < 30:
            deficiencies.append("Nitrogen")
            advisories.append("Apply Neem-coated Urea in split doses (max 30-40 kg/acre) to prevent fertilizer leaf burn")

    if phosphorus is not None:
        p_val = float(phosphorus)
        if p_val < 20:
            deficiencies.append("Phosphorus")
            advisories.append("Apply Single Super Phosphate (SSP) or DAP near root zone")

    if potassium is not None:
        k_val = float(potassium)
        if k_val < 20:
            deficiencies.append("Potassium")
            advisories.append("Apply Muriate of Potash (MOP) to improve disease resistance")

    if deficiencies:
        return {
            "type": "nutrient",
            "priority": "MEDIUM",
            "message": f"Low nutrient level detected ({', '.join(deficiencies)}). ICAR Action: {'; '.join(advisories)}.",
        }

    return {
        "type": "nutrient",
        "priority": "LOW",
        "message": "No major NPK deficiency detected. Maintain standard basal fertilization.",
    }


def ph_rule(ph):
    """
    Checks soil pH and generates a soil acidity/alkalinity advisory.
    """
    if ph is None:
        return None

    ph_val = _clamp(ph, 0, 14)

    if ph_val < 5.5:
        return {
            "type": "soil_ph",
            "priority": "MEDIUM",
            "message": f"Soil pH is acidic ({ph_val:.1f}). Apply agricultural lime (calcium carbonate) or dolomite to normalize soil pH.",
        }

    if ph_val > 7.8:
        return {
            "type": "soil_ph",
            "priority": "MEDIUM",
            "message": f"Soil pH is alkaline ({ph_val:.1f}). Apply agricultural gypsum or composted organic matter to improve micronutrient availability.",
        }

    return {
        "type": "soil_ph",
        "priority": "LOW",
        "message": f"Soil pH is optimal ({ph_val:.1f}) for nutrient absorption.",
    }


def chemical_safety_rule(disease_name, severity=None, rain_probability=None):
    """
    Prevents pesticide spraying before heavy rainfall (protects against chemical runoff & human hazard).
    """
    if not disease_name or "healthy" in disease_name.lower():
        return None

    rain_prob = _clamp(rain_probability, 0, 100) if rain_probability is not None else 0

    if rain_prob >= 60:
        return {
            "type": "safety",
            "priority": "HIGH",
            "message": (
                f"SAFETY WARNING: High rainfall probability ({rain_prob:.0f}%). "
                "Do NOT apply foliar chemical sprays today. Rain will wash off active ingredients, "
                "wasting chemicals and causing aquatic runoff pollution. Apply post-rain."
            ),
        }

    return None


def disease_rule(disease_name, confidence, crop=None, severity=None):
    """
    Generates an advisory based on disease prediction,
    model confidence, and specific crop.
    """
    crop_info = f" on {crop}" if crop else ""
    healthy = not disease_name or "healthy" in disease_name.lower()

    if healthy:
        return {
            "type": "disease",
            "priority": "LOW",
            "message": f"No significant crop pathogen detected{crop_info}. Foliage health is normal.",
        }

    if confidence < 0.60:
        return {
            "type": "disease",
            "priority": "LOW",
            "message": (
                f"Diagnosis confidence is low ({confidence*100:.0f}%) for potential {disease_name}{crop_info}. "
                "Retake photo in natural daylight or consult your local KVK agronomist before spraying."
            ),
        }

    if (severity and severity.lower() == "high") or confidence >= 0.80:
        return {
            "type": "disease",
            "priority": "HIGH",
            "message": (
                f"{disease_name} detected{crop_info} with high confidence ({confidence*100:.0f}%). "
                "Prune infected foliage immediately and apply recommended ICAR-approved fungicide rotation."
            ),
        }

    return {
        "type": "disease",
        "priority": "MEDIUM",
        "message": (
            f"Moderate symptoms of {disease_name} detected{crop_info} ({confidence*100:.0f}%). "
            "Inspect underside of leaves and implement preventative biocontrol measures."
        ),
    }


def weather_rule(temperature, humidity, crop=None):
    """
    Generates weather-related crop advisories.
    """
    recommendations = []
    crop_prefix = f"For {crop}: " if crop else ""

    temp_val = float(temperature) if temperature is not None else 25.0
    hum_val = float(humidity) if humidity is not None else 50.0

    if temp_val >= 35:
        recommendations.append(
            f"{crop_prefix}High ambient temperature ({temp_val:.0f}°C) detected. Mulch soil and increase heat-stress monitoring."
        )

    if hum_val >= 80:
        recommendations.append(
            f"{crop_prefix}High relative humidity ({hum_val:.0f}%) creates favorable conditions for fungal spores. Ensure canopy ventilation."
        )

    if not recommendations:
        return {
            "type": "weather",
            "priority": "LOW",
            "message": "Weather conditions are currently within the optimal vegetative range.",
        }

    return {
        "type": "weather",
        "priority": "MEDIUM",
        "message": " ".join(recommendations),
    }


def harvest_market_sync_rule(crop, expected_harvest_date=None, crop_stage=None, market=None):
    """
    SIH Requirement: Links farm harvest schedules with local mandi demand & price peaks.
    """
    if not market or not market.current_price:
        return None

    trend = (market.trend or "Stable").capitalize()
    mandi = market.region or "nearby"
    price = market.current_price
    forecast = market.forecast_price or price

    days_to_harvest = None
    if expected_harvest_date:
        try:
            today = date.today()
            if isinstance(expected_harvest_date, str):
                parsed = datetime.strptime(expected_harvest_date.split("T")[0], "%Y-%m-%d").date()
                days_to_harvest = (parsed - today).days
            elif isinstance(expected_harvest_date, date):
                days_to_harvest = (expected_harvest_date - today).days
        except Exception:
            days_to_harvest = None

    stage_ready = crop_stage and crop_stage.lower() in ["harvest_ready", "maturity", "fruiting", "mature"]

    if days_to_harvest is not None:
        if days_to_harvest <= 7 and trend == "Rising":
            return {
                "type": "market",
                "priority": "OPPORTUNITY",
                "message": (
                    f"HARVEST LINKAGE: {crop} matures in {days_to_harvest} days. "
                    f"{mandi} Mandi prices are RISING at ₹{price:.0f}/q (near-term peak forecast: ₹{forecast:.0f}/q). "
                    "Pre-book transporter now to capture the price upswing."
                ),
            }
        elif days_to_harvest <= 7 and trend == "Falling":
            return {
                "type": "market",
                "priority": "MEDIUM",
                "message": (
                    f"HARVEST ALERT: {crop} matures in {days_to_harvest} days, but {mandi} Mandi prices are FALLING (₹{price:.0f}/q). "
                    "Consider early harvest or secure local cold storage / direct buyer contract."
                ),
            }

    if stage_ready and trend == "Rising":
        return {
            "type": "market",
            "priority": "OPPORTUNITY",
            "message": (
                f"MARKET LINKAGE: Crop is harvest-ready and {mandi} Mandi prices are RISING at ₹{price:.0f}/q. "
                "Optimal selling window is within 48-72 hours."
            ),
        }

    return None


def market_rule(market):
    if market is None or market.current_price is None:
        return None

    trend = (market.trend or "Stable").capitalize()
    demand = market.demand_indicator or "Unknown"
    crop = market.crop_name or "the crop"
    mandi = market.region or "local"
    forecast = ""
    if market.forecast_price:
        forecast = f" Near-term forecast: ₹{market.forecast_price:.0f}/q."

    if trend.lower() == "falling" and (demand.lower() in {"low", "unknown"}):
        return {
            "type": "market",
            "priority": "MEDIUM",
            "message": (
                f"{crop} prices in {mandi} Mandi are falling at ₹{market.current_price:.0f}/q "
                f"with {demand.lower()} demand. Consider holding if storage is available.{forecast}"
            ),
        }

    if trend.lower() == "rising":
        return {
            "type": "market",
            "priority": "LOW",
            "message": (
                f"{crop} prices in {mandi} Mandi are rising at ₹{market.current_price:.0f}/q "
                f"({demand} demand). Selling in the next window may capture the upswing.{forecast}"
            ),
        }

    return {
        "type": "market",
        "priority": "LOW",
        "message": (
            f"{crop} market in {mandi} Mandi is {trend.lower()} at ₹{market.current_price:.0f}/q "
            f"with {demand.lower()} demand.{forecast}"
        ),
    }