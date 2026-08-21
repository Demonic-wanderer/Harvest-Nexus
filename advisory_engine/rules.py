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
                "message_hi": (
                    f"मिट्टी की नमी कम ({moisture:.0f}%) है, लेकिन बारिश की संभावना {rain_prob:.0f}% है। "
                    "जलभराव से बचने के लिए 12-24 घंटे सिंचाई रोकें।"
                ),
            }

        return {
            "type": "irrigation",
            "priority": "HIGH",
            "message": f"Soil moisture is critically low ({moisture:.0f}%). Immediate irrigation is recommended for the {crop_stage or 'current'} stage.",
            "message_hi": f"मिट्टी की नमी बहुत कम ({moisture:.0f}%) है। {crop_stage or 'वर्तमान'} अवस्था के लिए तुरंत हल्की सिंचाई करें।",
        }

    if moisture >= 60:
        return {
            "type": "irrigation",
            "priority": "LOW",
            "message": f"Soil moisture is sufficient ({moisture:.0f}%). Irrigation is not currently required.",
            "message_hi": f"मिट्टी में पर्याप्त नमी ({moisture:.0f}%) उपलब्ध है। अभी अतिरिक्त सिंचाई की आवश्यकता नहीं है।",
        }

    return {
        "type": "irrigation",
        "priority": "LOW",
        "message": f"Soil moisture is moderate ({moisture:.0f}%). Continue routine field monitoring.",
        "message_hi": f"मिट्टी की नमी सामान्य ({moisture:.0f}%) है। नियमित निगरानी बनाए रखें।",
    }


def nutrient_rule(nitrogen, phosphorus, potassium):
    """
    Checks NPK levels and identifies nutrient deficiencies with ICAR dosage caps.
    """
    deficiencies = []
    deficiencies_hi = []
    advisories = []
    advisories_hi = []

    if nitrogen is not None:
        n_val = float(nitrogen)
        if n_val < 30:
            deficiencies.append("Nitrogen")
            deficiencies_hi.append("नाइट्रोजन")
            advisories.append("Apply Neem-coated Urea in split doses (max 30-40 kg/acre)")
            advisories_hi.append("नीम लेपित यूरिया (30-40 किग्रा/एकड़) किस्तों में दें")

    if phosphorus is not None:
        p_val = float(phosphorus)
        if p_val < 20:
            deficiencies.append("Phosphorus")
            deficiencies_hi.append("फास्फोरस")
            advisories.append("Apply Single Super Phosphate (SSP) or DAP near root zone")
            advisories_hi.append("जड़ क्षेत्र के पास सिंगल सुपर फॉस्फेट (SSP) या DAP डालें")

    if potassium is not None:
        k_val = float(potassium)
        if k_val < 20:
            deficiencies.append("Potassium")
            deficiencies_hi.append("पोटाश")
            advisories.append("Apply Muriate of Potash (MOP) to improve disease resistance")
            advisories_hi.append("रोग प्रतिरोधक क्षमता बढ़ाने के लिए म्यूटरेट ऑफ पोटाश (MOP) दें")

    if deficiencies:
        return {
            "type": "nutrient",
            "priority": "MEDIUM",
            "message": f"Low nutrient level detected ({', '.join(deficiencies)}). ICAR Action: {'; '.join(advisories)}.",
            "message_hi": f"पोषक तत्वों की कमी पाई गई ({', '.join(deficiencies_hi)})। ICAR सलाह: {'; '.join(advisories_hi)}।",
        }

    return {
        "type": "nutrient",
        "priority": "LOW",
        "message": "No major NPK deficiency detected. Maintain standard basal fertilization.",
        "message_hi": "NPK पोषक तत्व संतुलित हैं। मानक पोषण कार्यक्रम जारी रखें।",
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
            "message_hi": f"मिट्टी अम्लीय ({ph_val:.1f}) है। pH सामान्य करने के लिए कृषि चूना या डोलोमाइट का प्रयोग करें।",
        }

    if ph_val > 7.8:
        return {
            "type": "soil_ph",
            "priority": "MEDIUM",
            "message": f"Soil pH is alkaline ({ph_val:.1f}). Apply agricultural gypsum or composted organic matter to improve micronutrient availability.",
            "message_hi": f"मिट्टी क्षारीय ({ph_val:.1f}) है। सूक्ष्म पोषक तत्व बढ़ाने के लिए जिप्सम या जैविक खाद डालें।",
        }

    return {
        "type": "soil_ph",
        "priority": "LOW",
        "message": f"Soil pH is optimal ({ph_val:.1f}) for nutrient absorption.",
        "message_hi": f"मिट्टी का pH ({ph_val:.1f}) फसलों के पोषक तत्व अवशोषण के लिए अनुकूल है।",
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
            "message_hi": (
                f"⚠️ सुरक्षा चेतावनी: भारी वर्षा की संभावना ({rain_prob:.0f}%) है। "
                "आज कीटनाशक/फफूंदनाशक का छिड़काव न करें। बारिश से रसायन बह जाएगा। बारिश रुकने के बाद स्प्रे करें।"
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
            "message_hi": f"फसल पर किसी हानिकारक रोग के लक्षण नहीं मिले। पत्तियां पूर्णतः स्वस्थ हैं।",
        }

    if confidence < 0.60:
        return {
            "type": "disease",
            "priority": "LOW",
            "message": (
                f"Diagnosis confidence is low ({confidence*100:.0f}%) for potential {disease_name}{crop_info}. "
                "Retake photo in natural daylight or consult your local KVK agronomist before spraying."
            ),
            "message_hi": (
                f"रोग पहचान का विश्वास स्तर कम ({confidence*100:.0f}%) है। "
                "साफ रोशनी में फोटो पुनः लें या छिड़काव से पहले कृषि विज्ञान केंद्र (KVK) से सलाह लें।"
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
            "message_hi": (
                f"उच्च विश्वास स्तर ({confidence*100:.0f}%) के साथ {disease_name} के लक्षण मिले। "
                "संक्रमित पत्तियों को काटकर नष्ट करें और अनुमोदित फफूंदनाशक का छिड़काव करें।"
            ),
        }

    return {
        "type": "disease",
        "priority": "MEDIUM",
        "message": (
            f"Moderate symptoms of {disease_name} detected{crop_info} ({confidence*100:.0f}%). "
            "Inspect underside of leaves and implement preventative biocontrol measures."
        ),
        "message_hi": (
            f"{disease_name} के मध्यम लक्षण दिखे ({confidence*100:.0f}%)। "
            "पत्तियों के नीचे जांचें और जैविक सुरक्षा उपाय अपनाएं।"
        ),
    }


def weather_rule(temperature, humidity, crop=None):
    """
    Generates weather-related crop advisories.
    """
    recommendations = []
    recommendations_hi = []
    crop_prefix = f"For {crop}: " if crop else ""

    temp_val = float(temperature) if temperature is not None else 25.0
    hum_val = float(humidity) if humidity is not None else 50.0

    if temp_val >= 35:
        recommendations.append(
            f"{crop_prefix}High ambient temperature ({temp_val:.0f}°C) detected. Mulch soil and increase heat-stress monitoring."
        )
        recommendations_hi.append(
            f"उच्च तापमान ({temp_val:.0f}°C) दर्ज हुआ। मिट्टी की नमी बनाए रखने के लिए मल्चिंग करें।"
        )

    if hum_val >= 80:
        recommendations.append(
            f"{crop_prefix}High relative humidity ({hum_val:.0f}%) creates favorable conditions for fungal spores. Ensure canopy ventilation."
        )
        recommendations_hi.append(
            f"अधिक नमी ({hum_val:.0f}%) से फफूंद रोग का खतरा बढ़ सकता है। फसल में हवा का संचार सुनिश्चित करें।"
        )

    if not recommendations:
        return {
            "type": "weather",
            "priority": "LOW",
            "message": "Weather conditions are currently within the optimal vegetative range.",
            "message_hi": "मौसम की स्थिति फसल वृद्धि के लिए अनुकूल है।",
        }

    return {
        "type": "weather",
        "priority": "MEDIUM",
        "message": " ".join(recommendations),
        "message_hi": " ".join(recommendations_hi),
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

    if "bull" in trend.lower() or "rising" in trend.lower() or forecast > price:
        if days_to_harvest is not None and days_to_harvest <= 7:
            return {
                "type": "market",
                "priority": "HIGH",
                "message": (
                    f"MARKET PEAK OPPORTUNITY: {mandi} {crop} price is rising (₹{price:.0f}/q, trend: {trend}). "
                    f"Harvest in {days_to_harvest}d aligns with high demand. Book transport early to lock in peak margins."
                ),
                "message_hi": (
                    f"बाज़ार अवसर: {mandi} में {crop} के भाव बढ़ रहे हैं (₹{price:.0f}/क्विंटल)। "
                    f"आगामी {days_to_harvest} दिनों में तुड़ाई करके बेहतर दाम प्राप्त करें।"
                ),
            }

    return None


def market_rule(market):
    """
    General market rule for price and trend signals.
    """
    if not market or not market.current_price:
        return None

    price = market.current_price
    trend = (market.trend or "Stable").capitalize()
    mandi = market.region or "local mandi"

    return {
        "type": "market",
        "priority": "LOW",
        "message": f"{mandi} price: ₹{price:.0f}/q ({trend}). Check transportation booking before dispatch.",
        "message_hi": f"{mandi} भाव: ₹{price:.0f}/क्विंटल ({trend})। माल भेजने से पहले वाहन उपलब्धता सुनिश्चित करें।",
    }