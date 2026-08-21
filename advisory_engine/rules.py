def irrigation_rule(soil_moisture, rain_probability=None):
    """
    Decides whether irrigation is required based on
    soil moisture and expected rainfall.
    """

    if soil_moisture < 30:

        if rain_probability is not None and rain_probability >= 60:
            return {
                "type": "irrigation",
                "priority": "MEDIUM",
                "message": "Soil moisture is low, but rainfall is likely. Recheck before irrigating."
            }

        return {
            "type": "irrigation",
            "priority": "HIGH",
            "message": "Soil moisture is low. Irrigation is recommended."
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


def disease_rule(disease_name, confidence):
    """
    Generates an advisory based on disease prediction
    and model confidence.
    """

    if not disease_name or disease_name.lower() == "healthy":
        return {
            "type": "disease",
            "priority": "LOW",
            "message": "No significant disease detected."
        }

    if confidence >= 0.80:
        return {
            "type": "disease",
            "priority": "HIGH",
            "message": f"{disease_name} detected with high confidence. "
                       "Inspect affected plants and follow recommended disease-management practices."
        }

    if confidence >= 0.50:
        return {
            "type": "disease",
            "priority": "MEDIUM",
            "message": f"Possible {disease_name} detected. "
                       "Further inspection is recommended."
        }

    return {
        "type": "disease",
        "priority": "LOW",
        "message": "Disease prediction confidence is low. Further inspection is recommended."
    }


def weather_rule(temperature, humidity):
    """
    Generates weather-related crop advisories.
    """

    recommendations = []

    if temperature >= 35:
        recommendations.append(
            "High temperature detected. Increase heat and water-stress monitoring."
        )

    if humidity >= 80:
        recommendations.append(
            "High humidity detected. Monitor the crop for fungal disease development."
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