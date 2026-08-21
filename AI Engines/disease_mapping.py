import json
import os

_DIR = os.path.dirname(os.path.abspath(__file__))


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
    return entry.get("display_name", class_name.replace("_", " ").replace("Tomato   ", "").strip())


def treatments_for(class_name):
    mapping = load_treatments()
    entry = mapping.get(class_name)
    if not entry:
        return ["Scout the field and consult a local agronomist."]
    return list(entry.get("treatments", []))


def severity_from_prediction(class_name, confidence_pct):
    if not class_name or "healthy" in class_name.lower():
        return "none"
    if confidence_pct >= 85:
        return "high"
    if confidence_pct >= 65:
        return "medium"
    return "low"
