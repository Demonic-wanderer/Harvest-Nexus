import requests


def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation",
        "hourly": "precipitation_probability",
        "forecast_days": 1
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    current = data["current"]
    hourly = data["hourly"]

    # Get current hour's rain probability
    rain_probability = hourly["precipitation_probability"][0]

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "rain_probability": rain_probability
    }


if __name__ == "__main__":
    # Example: Indore coordinates
    weather = get_weather(22.7196, 75.8577)

    print("=== LIVE WEATHER ===")
    print("Temperature:", weather["temperature"], "°C")
    print("Humidity:", weather["humidity"], "%")
    print("Rain Probability:", weather["rain_probability"], "%")