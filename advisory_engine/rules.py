def irrigation_rule(soil_moisture, rain_probability=None, crop_stage=None):
    """
    Decides whether irrigation is required based on
    soil moisture, expected rainfall, and crop growth stage.
    """
    threshold = 30
    # Flowering and Fruiting stages require more water
    if crop_stage and crop_stage.lower() in ["flowering", "fruiting", "reproductive"]:
        threshold = 40

    if soil_moisture < threshold:

        if rain_probability is not None and rain_probability >= 60:
            return {
                "type": "irrigation",
                "priority": "MEDIUM",
                "message": f"Soil moisture is low ({soil_moisture}%) during critical stage ({crop_stage or 'monitored'}), but rainfall is likely. Recheck before irrigating."
            }

        return {
            "type": "irrigation",
            "priority": "HIGH",
            "message": f"Soil moisture is low ({soil_moisture}%). Irrigation is recommended for the {crop_stage or 'current'} stage."
        }

    if soil_moisture >= 60:
        return {
            "type": "irrigation",
            "priority": "LOW",
            "message": "Soil moisture is sufficient. Irrigation is not currently required."
        }

    return {
        "type": "irrigation",
        "priority": "LOW",
        "message": "Soil moisture is moderate. Continue monitoring."
    }


def nutrient_rule(nitrogen, phosphorus, potassium):
    """
    Checks NPK levels and identifies nutrient deficiencies.
    """

    deficiencies = []

    if nitrogen is not None and nitrogen < 30:
        deficiencies.append("Nitrogen")

    if phosphorus is not None and phosphorus < 20:
        deficiencies.append("Phosphorus")

    if potassium is not None and potassium < 20:
        deficiencies.append("Potassium")

    if deficiencies:
        return {
            "type": "nutrient",
            "priority": "MEDIUM",
            "message": "Low nutrient level detected: "
                       + ", ".join(deficiencies)
                       + ". Follow the recommended nutrient management plan."
        }

    return {
        "type": "nutrient",
        "priority": "LOW",
        "message": "No major NPK deficiency detected."
    }


def ph_rule(ph):
    """
    Checks soil pH and generates a soil acidity/alkalinity advisory.
    """

    if ph is None:
        return None

    if ph < 5.5:
        return {
            "type": "soil_ph",
            "priority": "MEDIUM",
            "message": "Soil pH is low and indicates acidic soil. Consider appropriate soil correction based on crop requirements."
        }

    if ph > 7.5:
        return {
            "type": "soil_ph",
            "priority": "MEDIUM",
            "message": "Soil pH is high and indicates alkaline soil. Consider appropriate soil correction based on crop requirements."
        }

    return {
        "type": "soil_ph",
        "priority": "LOW",
        "message": "Soil pH is within the monitored range."
    }


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
            "message": f"No significant disease detected{crop_info}."
        }

    if (severity and severity.lower() == "high") or confidence >= 0.80:
        return {
            "type": "disease",
            "priority": "HIGH",
            "message": f"{disease_name} detected{crop_info} with high confidence. "
                       "Inspect affected plants and follow recommended disease-management practices."
        }

    if confidence >= 0.50:
        return {
            "type": "disease",
            "priority": "MEDIUM",
            "message": f"Possible {disease_name} detected{crop_info}. "
                       "Further inspection is recommended."
        }

    return {
        "type": "disease",
        "priority": "LOW",
        "message": f"Disease prediction confidence is low for potential {disease_name}{crop_info}. Further inspection is recommended."
    }


def weather_rule(temperature, humidity, crop=None):
    """
    Generates weather-related crop advisories.
    """
    recommendations = []
    crop_prefix = f"For {crop}: " if crop else ""

    if temperature >= 35:
        recommendations.append(
            f"{crop_prefix}High temperature detected. Increase heat and water-stress monitoring."
        )

    if humidity >= 80:
        recommendations.append(
            f"{crop_prefix}High humidity detected. Monitor the crop for fungal disease development."
        )

    if not recommendations:
        return {
            "type": "weather",
            "priority": "LOW",
            "message": "Weather conditions are currently within the monitored range."
        }

    return {
        "type": "weather",
        "priority": "MEDIUM",
        "message": " ".join(recommendations)
    }


def market_rule(market):
    if market is None or market.current_price is None:
        return None

    trend = (market.trend or "Stable").capitalize()
    demand = market.demand_indicator or "Unknown"
    crop = market.crop_name or "the crop"
    forecast = ""
    if market.forecast_price:
        forecast = f" Near-term forecast is ₹{market.forecast_price:.0f}/quintal."

    if trend.lower() == "falling" and (demand.lower() in {"low", "unknown"}):
        return {
            "type": "market",
            "priority": "MEDIUM",
            "message": (
                f"{crop} prices are {trend.lower()} at ₹{market.current_price:.0f}/quintal "
                f"with {demand.lower()} demand. Consider holding if storage is available.{forecast}"
            ),
        }

    if trend.lower() == "rising":
        return {
            "type": "market",
            "priority": "LOW",
            "message": (
                f"{crop} prices are rising at ₹{market.current_price:.0f}/quintal "
                f"({demand} demand). Selling in the next window may capture the upswing.{forecast}"
            ),
        }

    return {
        "type": "market",
        "priority": "LOW",
        "message": (
            f"{crop} market is {trend.lower()} at ₹{market.current_price:.0f}/quintal "
            f"with {demand.lower()} demand.{forecast}"
        ),
    }