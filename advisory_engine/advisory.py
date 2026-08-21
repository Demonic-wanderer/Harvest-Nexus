from .schemas import AdvisoryRequest
from .rules import disease_rule, irrigation_rule, nutrient_rule, ph_rule, weather_rule
from .priority import calculate_priority as prioritize
from .formatter import format_action_plan


def generate_advisory(request: AdvisoryRequest):
    recommendations = []
    
  
    if request.disease.name:
        disease_result = disease_rule(
            request.disease.name,
            request.disease.confidence
        )
        recommendations.append(disease_result)

  
    irrigation_result = irrigation_rule(request.soil.moisture, request.weather.rain_probability)
    if irrigation_result:
        recommendations.append(irrigation_result)

    # Nutrient recommendation
    if request.soil.nitrogen is not None:
        nutrient_result = nutrient_rule(
            request.soil.nitrogen,
            request.soil.phosphorus,
            request.soil.potassium
        )

        if nutrient_result:
            recommendations.append(nutrient_result)


    # Soil pH recommendation
    ph_result = ph_rule(request.soil.ph)

    if ph_result:
     recommendations.append(ph_result)


    # Weather recommendation
    weather_result = weather_rule(
        request.weather.temperature,
        request.weather.humidity
    )

    if weather_result:
        recommendations.append(weather_result)

    # Arrange recommendations by priority
    prioritized = prioritize(recommendations)

    # Convert into farmer-friendly action plan
    return format_action_plan(prioritized)


