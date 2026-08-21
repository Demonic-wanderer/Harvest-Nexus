import json
import os

_DIR = os.path.dirname(os.path.abspath(__file__))

HINDI_DISEASE_NAMES = {
    "Tomato___Bacterial_spot": "बैक्टीरियल स्पॉट (जीवाणु धब्बा)",
    "Tomato___Early_blight": "अर्ली ब्लाइट (अगेती झुलसा)",
    "Tomato___Late_blight": "लेट ब्लाइट (पछेती झुलसा)",
    "Tomato___Leaf_Mold": "लीफ मोल्ड (पत्ती फफूंद)",
    "Tomato___Septoria_leaf_spot": "सेप्टोरिया लीफ स्पॉट (पत्ती धब्बा)",
    "Tomato___Spider_mites": "स्पाइडर माइट्स (लाल मकड़ी)",
    "Tomato___Target_Spot": "टारगेट स्पॉट (लक्ष्य धब्बा)",
    "Tomato___Yellow_Leaf_Curl_Virus": "येलो लीफ कर्ल वायरस (पत्ती मुड़न विषाणु)",
    "Tomato___mosaic_virus": "मोज़ेक वायरस (चित्तीदार विषाणु)",
    "Tomato___healthy": "स्वस्थ पत्ती (रोगमुक्त)",
}

HINDI_TREATMENTS = {
    "Tomato___Bacterial_spot": [
        "प्रभावित पत्तियों को काटकर नष्ट करें ताकि जीवाणु आगे न फैले",
        "कॉपर ऑक्सीक्लोराइड (3g/L) + प्लांटोमाइसिन (1g/10L) का घोल बनाकर छिड़कें",
        "ऊपरी फव्वारा सिंचाई से बचें और पौधों के बीच हवा का संचार बनाए रखें",
    ],
    "Tomato___Early_blight": [
        "रोग ग्रस्त निचली पत्तियों को तुरंत काटकर खेत से दूर नष्ट करें",
        "क्लोरोथालोनिल या मैनकोजेब (2g प्रति लीटर पानी) का लेबल अनुसार स्प्रे करें",
        "हवा का प्रवाह बढ़ाएँ और मिट्टी पर पुआल की मल्चिंग करें ताकि मिट्टी के छींटे न लगें",
    ],
    "Tomato___Late_blight": [
        "संक्रमित पौधों को तुरंत उखाड़कर गहरे गड्ढे में दबाएँ",
        "सिस्टमिक फफूंदनाशक (मेटालेक्सिल + मैनकोजेब @ 2.5g/लीटर) का तुरंत छिड़काव करें",
        "पत्तियों को सूखा रखें और स्वस्थ फलों की तुरंत तुड़ाई कर लें",
    ],
    "Tomato___Leaf_Mold": [
        "पॉलीहाउस/खेत में वेंटिलेशन बढ़ाएँ और पौधों में उचित दूरी रखें",
        "आर्द्रता (नमी) को 85% से नीचे बनाए रखने का प्रयास करें",
        "दबाव अधिक होने पर कॉपर हाइड्रोक्साइड या अनुशंसित फफूंदनाशक लगाएँ",
    ],
    "Tomato___Septoria_leaf_spot": [
        "संक्रमित निचली पत्तियाँ हटाएँ और खेत साफ रखें",
        "मिट्टी के पानी के छींटे रोकने के लिए जैविक मल्चिंग का उपयोग करें",
        "7–10 दिन के अंतराल पर प्रोटेक्टेंट फफूंदनाशक (मैनकोजेब) का छिड़काव करें",
    ],
    "Tomato___Spider_mites": [
        "पत्तियों के निचले हिस्से पर तेज धार से पानी का स्प्रे करें",
        "उपलब्ध होने पर शिकारी माइट्स (Phytoseiulus) छोड़ें",
        "संक्रमण गंभीर होने पर अनुशंसित एसारिसाइड/माइटनाशक (प्रोपारगाइट) का प्रयोग करें",
    ],
    "Tomato___Target_Spot": [
        "पौधों के घेरे में हवा का प्रवाह सुधारें और अतिरिक्त शाखाएं काटें",
        "रात के समय पत्तियों पर पानी जमा न रहने दें",
        "स्ट्रोबिल्यूरिन या SDHI वर्ग का फफूंदनाशक लेबल अनुसार स्प्रे करें",
    ],
    "Tomato___Yellow_Leaf_Curl_Virus": [
        "संक्रमित पौधों को तुरंत उखाड़कर नष्ट करें (रोकथाम ही उपाय है)",
        "पीले चिपचिपे कार्ड (Yellow Sticky Traps) से सफेद मक्खी नियंत्रित करें",
        "अगले मौसम में रोग प्रतिरोधी हाइब्रिड किस्मों का चयन करें",
    ],
    "Tomato___mosaic_virus": [
        "विषाणु से संक्रमित पौधों को तुरंत उखाड़कर नष्ट करें",
        "हर पौधे के बाद औजारों को ट्राइसोडियम फॉस्फेट या साबुन पानी से कीटाणुरहित करें",
        "खेत में काम करते समय तंबाकू या बीड़ी का उपयोग बिल्कुल न करें",
    ],
    "Tomato___healthy": [
        "फसल पूरी तरह रोगमुक्त है। 3-4 दिन में नियमित निगरानी जारी रखें",
        "संतुलित सिंचाई और NPK पोषक तत्वों का समय पर प्रबंधन करें",
    ],
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
            "पहचान का विश्वास स्तर कम है (<60%)। तस्वीर धुंधली या छाया वाली हो सकती है।",
            "प्राकृतिक रोशनी में रोग वाले हिस्से की साफ तस्वीर लेकर फिर प्रयास करें।",
            "छिड़काव से पहले नजदीकी कृषि विज्ञान केंद्र या कृषि सलाहकार से परामर्श करें।",
        ]
    return HINDI_TREATMENTS.get(class_name, [
        "संतुलित सिंचाई और पोषण बनाए रखें",
        "समस्या बढ़ने पर कृषि सलाहकार से संपर्क करें",
    ])


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
