import argparse
from weather.weather_api import get_weather
from advisory_engine.schemas import AdvisoryRequest
from advisory_engine.advisory import generate_advisory


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Harvest Nexus - Farm Advisory Demo")
    parser.add_argument("--lat", type=float, default=22.7196, help="Latitude (default: Indore)")
    parser.add_argument("--lon", type=float, default=75.8577, help="Longitude (default: Indore)")
    args = parser.parse_args()

    # Get live weather
    weather_data = get_weather(args.lat, args.lon)

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