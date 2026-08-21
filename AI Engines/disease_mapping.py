import json
import os

_DIR = os.path.dirname(os.path.abspath(__file__))

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
