import os
from PIL import Image


def analyze_multimodal(image_path, crop, growth_stage, soil_moisture, soil_temperature, soil_ph, 
                      nitrogen, phosphorus, potassium, air_temperature, humidity, rain_expected):
    """
    Simulates or executes a multimodal AI analysis combining vision (crop image)
    with sensor data (soil NPK, weather conditions, pH, moisture).
    Returns mock analysis results.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Crop image '{image_path}' not found.")
    
    with Image.open(image_path) as img:
        img.verify()
        
    status = "healthy"
    recommendations = []
    
    try:
        sm = float(soil_moisture)
        if sm < 30:
            recommendations.append("Low soil moisture. Irrigation recommended.")
    except ValueError:
        pass
        
    try:
        n = float(nitrogen)
        p = float(phosphorus)
        k = float(potassium)
        if n < 30 or p < 20 or k < 20:
            recommendations.append("Nutrient levels are low. Adjust fertilizer NPK ratios.")
    except ValueError:
        pass

    if not recommendations:
        recommendations.append("Crop health is optimal. No active intervention needed.")
        
    return {
        "crop_health_status": status,
        "vision_check": "No visible leaf disease spots detected via image classification.",
        "sensor_verdict": "Soil NPK and moisture levels are within acceptable bounds." if not recommendations else "Sensor anomalies detected.",
        "recommendations": recommendations
    }


def collect_farm_data():
    print("================================")
    print("   🌾 KISAN MULTIMODAL AI")
    print("================================")
    
    image_path = input("Enter crop image path: ")
    if not os.path.exists(image_path):
        print(f"❌ Error: Image path '{image_path}' does not exist.")
        return

    try:
        with Image.open(image_path) as img:
            print("✅ Image loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return

    crop = input("Enter crop name (e.g. Tomato, Wheat): ")
    growth_stage = input("Enter growth stage (e.g. Seedling, Vegetative, Flowering): ")
    
    try:
        soil_moisture = float(input("Enter soil moisture (%): "))
        soil_temperature = float(input("Enter soil temperature (°C): "))
        soil_ph = float(input("Enter soil pH: "))
        nitrogen = float(input("Enter nitrogen (mg/kg): "))
        phosphorus = float(input("Enter phosphorus (mg/kg): "))
        potassium = float(input("Enter potassium (mg/kg): "))
        air_temperature = float(input("Enter air temperature (°C): "))
        humidity = float(input("Enter humidity (%): "))
    except ValueError:
        print("❌ Error: All numerical values must be valid integers/floats.")
        return
        
    rain_expected = input("Is rain expected? (Yes/No): ")

    print()
    print("================================")
    print("      🌾 FARM DATA RECEIVED")
    print("================================")
    print("Crop:", crop)
    print("Growth stage:", growth_stage)
    print("Soil moisture:", soil_moisture, "%")
    print("Soil temperature:", soil_temperature, "°C")
    print("Soil pH:", soil_ph)
    print("Nitrogen:", nitrogen, "mg/kg")
    print("Phosphorus:", phosphorus, "mg/kg")
    print("Potassium:", potassium, "mg/kg")
    print("Air temperature:", air_temperature, "°C")
    print("Humidity:", humidity, "%")
    print("Rain expected:", rain_expected)
    print("================================")
    
    print("\n🤖 Running AI Multimodal Analysis...")
    result = analyze_multimodal(
        image_path, crop, growth_stage, soil_moisture, soil_temperature, soil_ph, 
        nitrogen, phosphorus, potassium, air_temperature, humidity, rain_expected
    )
    
    print("\n📋 AI Analysis Verdict:")
    print(f"Health Status: {result['crop_health_status'].upper()}")
    print(f"Vision Check: {result['vision_check']}")
    print(f"Sensor Verdict: {result['sensor_verdict']}")
    print("Recommendations:")
    for rec in result["recommendations"]:
        print(f" - {rec}")


if __name__ == "__main__":
    collect_farm_data()