from PIL import Image

print("🌾 KISAN AI")
print()

image_path = input("Enter crop image name: ")


image = Image.open(image_path)

print("✅ Image received!")
print()



crop = input("Enter crop name: ")

growth_stage = input("Enter growth stage: ")

soil_moisture = input("Enter soil moisture (%): ")

soil_temperature = input("Enter soil temperature (°C): ")

soil_ph = input("Enter soil pH: ")

nitrogen = input("Enter nitrogen (mg/kg): ")

phosphorus = input("Enter phosphorus (mg/kg): ")

potassium = input("Enter potassium (mg/kg): ")

air_temperature = input("Enter air temperature (°C): ")

humidity = input("Enter humidity (%): ")

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
print("Nitrogen:", nitrogen)
print("Phosphorus:", phosphorus)
print("Potassium:", potassium)
print("Air temperature:", air_temperature, "°C")
print("Humidity:", humidity, "%")
print("Rain expected:", rain_expected)

print()
print("📷 Image + 🌱 Farm data received!")
print("🤖 Ready for AI analysis...")