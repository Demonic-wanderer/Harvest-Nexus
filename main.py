from weather.weather_api import get_weather
from advisory_engine.schemas import AdvisoryRequest
from advisory_engine.advisory import generate_advisory


# Get live weather for Indore
weather_data = get_weather(22.7196, 75.8577)

print("Live weather:", weather_data)


# Create advisory request
request = AdvisoryRequest(
    crop="wheat",
    disease={
        "name": "Early Blight",
        "confidence": 0.85
    },

    soil={
        "moisture": 30,
        "ph": 6.5,
        "nitrogen": 20,
        "phosphorus": 35,
        "potassium": 40
    },

    weather={
        "temperature": weather_data["temperature"],
        "humidity": weather_data["humidity"],
        "rain_probability": weather_data["rain_probability"]
    }
)


# Generate advisory
result = generate_advisory(request)

print("\n===== LIVE FARM ADVISORY =====")
print(result)