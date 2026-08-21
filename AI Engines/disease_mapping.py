import json
import os

_DIR = os.path.dirname(os.path.abspath(__file__))

HINDI_DISEASE_NAMES = {
    "Tomato___Bacterial_spot": "बैक्टीरियल स्पॉट",
    "Tomato___Early_blight": "अर्ली ब्लाइट",
    "Tomato___Late_blight": "लेट ब्लाइट",
    "Tomato___Leaf_Mold": "लीफ मोल्ड",
    "Tomato___Septoria_leaf_spot": "सेप्टोरिया लीफ स्पॉट",
    "Tomato___Spider_mites": "स्पाइडर माइट्स",
    "Tomato___Target_Spot": "टारगेट स्पॉट",
    "Tomato___Yellow_Leaf_Curl_Virus": "पीला पत्ता मोड़ वायरस",
    "Tomato___mosaic_virus": "मोज़ेक वायरस",
    "Tomato___healthy": "स्वस्थ पत्ता",
}

HINDI_TREATMENTS = {
    "Tomato___Bacterial_spot": ["बहुत संक्रमित पत्तियाँ हटाएँ", "लेबल की मात्रा में कॉपर आधारित जीवाणुनाशक लगाएँ", "ऊपरी सिंचाई से बचें"],
    "Tomato___Early_blight": ["प्रभावित निचली पत्तियाँ काटें", "लेबल के अनुसार क्लोरोथालोनिल या मैनकोजेब लगाएँ", "हवा का प्रवाह बढ़ाएँ और मिट्टी पर मल्च करें"],
    "Tomato___Late_blight": ["संक्रमित पौधे हटाकर नष्ट करें", "सिस्टमिक और प्रोटेक्टेंट फफूंदनाशक का बारी-बारी उपयोग करें", "पत्तियाँ सूखी रखें और स्वस्थ फल तोड़ें"],
    "Tomato___Leaf_Mold": ["वेंटिलेशन बढ़ाएँ", "नमी 85% से नीचे रखें", "दबाव जारी रहे तो अनुशंसित फफूंदनाशक लगाएँ"],
    "Tomato___Septoria_leaf_spot": ["संक्रमित पत्तियाँ हटाएँ", "मिट्टी के छींटे रोकने के लिए मल्च करें", "7–10 दिन के अंतराल पर प्रोटेक्टेंट फफूंदनाशक लगाएँ"],
    "Tomato___Spider_mites": ["पत्तियों के नीचे पानी का स्प्रे करें", "उपलब्ध हों तो शिकारी माइट्स छोड़ें", "संक्रमण अधिक हो तो लेबल वाला माइटनाशक लगाएँ"],
    "Tomato___Target_Spot": ["छत्र में हवा का प्रवाह बढ़ाएँ", "रात में पत्तियों को गीला न रहने दें", "लेबल के अनुसार फफूंदनाशक लगाएँ"],
    "Tomato___Yellow_Leaf_Curl_Virus": ["संक्रमित पौधे निकालें", "जाल या कीटनाशक रोटेशन से सफेद मक्खी नियंत्रित करें", "अगले मौसम में प्रतिरोधी किस्म लगाएँ"],
    "Tomato___mosaic_virus": ["संक्रमित पौधे हटाएँ", "हर पौधे के बाद औजार कीटाणुरहित करें", "खेत में काम से पहले तंबाकू न छुएँ"],
    "Tomato___healthy": ["नियमित निरीक्षण जारी रखें", "संतुलित सिंचाई और पोषण बनाए रखें"],
}

# Standard ICAR / Agronomic base yields (Quintals per Acre)
CROP_BASE_YIELDS_Q_PER_ACRE = {
    "tomato": 120.0,
    "wheat": 18.5,
    "potato": 95.0,
    "rice": 21.0,
    "paddy": 21.0,
    "maize": 24.0,
    "corn": 24.0,
    "cotton": 12.0,
    "soybean": 10.0,
    "onion": 110.0,
    "mustard": 8.5,
    "chilli": 45.0,
}


def load_labels():
    path = os.path.join(_DIR, "labels.json")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def load_treatments():
    path = os.path.join(_DIR, "treatments.json")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def display_name(class_name):
    mapping = load_treatments()
    entry = mapping.get(class_name, {})
    return entry.get("display_name", class_name.replace("_", " ").replace("Tomato___", "").replace("Tomato", "").strip())


def display_name_hi(class_name):
    return HINDI_DISEASE_NAMES.get(class_name, display_name(class_name))


def treatments_for(class_name, confidence=100.0):
    if confidence < 60.0:
        return [
            "Confidence is low (<60%). Image may be blurry, shadowed, or occluded.",
            "Retake leaf image in clear natural daylight focusing on the affected lesion.",
            "Consult your nearest Krishi Vigyan Kendra (KVK) or extension officer before spraying chemicals.",
        ]

    mapping = load_treatments()
    entry = mapping.get(class_name)
    if not entry:
        return [
            "Maintain balanced irrigation and soil nutrition.",
            "Scout crop rows daily and consult a local agricultural extension specialist if symptoms spread.",
        ]
    return list(entry.get("treatments", []))


def treatments_for_hi(class_name, confidence=100.0):
    if confidence < 60.0:
        return [
            "पहचान का विश्वास स्तर कम है। तस्वीर धुंधली या छाया वाली हो सकती है।",
            "प्राकृतिक रोशनी में रोग वाले हिस्से की साफ तस्वीर लेकर फिर प्रयास करें।",
            "छिड़काव से पहले नजदीकी कृषि विज्ञान केंद्र या कृषि सलाहकार से परामर्श करें।",
        ]
    return HINDI_TREATMENTS.get(class_name, ["संतुलित सिंचाई और पोषण बनाए रखें", "समस्या बढ़ने पर कृषि सलाहकार से संपर्क करें"])


def severity_from_prediction(class_name, confidence_pct):
    if not class_name or "healthy" in class_name.lower():
        return "none"
    if confidence_pct < 60.0:
        return "uncertain"
    if confidence_pct >= 85:
        return "high"
    if confidence_pct >= 65:
        return "medium"
    return "low"


def get_crop_base_yield(crop_name: str) -> float:
    key = (crop_name or "tomato").strip().lower()
    return CROP_BASE_YIELDS_Q_PER_ACRE.get(key, 30.0)
