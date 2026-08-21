import os

from disease_mapping import (
    display_name,
    load_labels,
    severity_from_prediction,
    treatments_for,
)

MODEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mobilenetv2_disease.pth")
IMAGE_SIZE = 224

_model = None
_class_names = None


def _torch_stack():
    import torch
    from torchvision import models, transforms
    return torch, models, transforms


def _device(torch):
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _transform(transforms):
    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])


def load_model():
    global _model, _class_names
    if _model is not None:
        return _model, _class_names

    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(MODEL_FILE)

    torch, models, transforms = _torch_stack()
    device = _device(torch)
    checkpoint = torch.load(MODEL_FILE, map_location=device)
    _class_names = checkpoint["class_names"]

    model_loaded = models.mobilenet_v2(weights=None)
    model_loaded.classifier[1] = torch.nn.Linear(model_loaded.last_channel, len(_class_names))
    model_loaded.load_state_dict(checkpoint["model_state"])
    model_loaded = model_loaded.to(device)
    model_loaded.eval()

    _model = (model_loaded, device, transforms)
    return _model, _class_names


def _heuristic_predict(image_path):
    """Used only when the trained checkpoint is absent so the API is not blocked."""
    from PIL import Image, ImageStat

    image = Image.open(image_path).convert("RGB")
    stats = ImageStat.Stat(image)
    r, g, b = stats.mean
    labels = load_labels()

    if g > r + 20 and g > b + 10:
        class_name = "Tomato___healthy"
        confidence = min(92.0, 55 + (g - r) / 2)
    elif r > g + 15 and r > b:
        class_name = "Tomato___Early_blight"
        confidence = min(88.0, 50 + (r - g) / 2)
    elif b > g and r < 90:
        class_name = "Tomato___Late_blight"
        confidence = 62.0
    elif r > 140 and g > 140 and b < 90:
        class_name = "Tomato___Yellow_Leaf_Curl_Virus"
        confidence = 70.0
    else:
        class_name = labels[0]
        confidence = 54.0

    return class_name, confidence, "color_heuristic"


def _pack_result(class_name, confidence, source):
    return {
        "disease": class_name,
        "display_name": display_name(class_name),
        "confidence": round(float(confidence), 2),
        "severity": severity_from_prediction(class_name, confidence),
        "treatments": treatments_for(class_name),
        "source": source,
    }


def predict_disease(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image '{image_path}' not found.")

    try:
        bundle, class_names_loaded = load_model()
    except FileNotFoundError:
        class_name, confidence, source = _heuristic_predict(image_path)
        return _pack_result(class_name, confidence, source)

    from PIL import Image

    torch, _models, transforms = _torch_stack()
    model_loaded, device, _ = bundle
    image = Image.open(image_path).convert("RGB")
    tensor = _transform(transforms)(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model_loaded(tensor)

    probabilities = torch.softmax(output, dim=1)
    prediction = torch.argmax(probabilities, dim=1).item()
    disease = class_names_loaded[prediction]
    confidence = probabilities[0][prediction].item() * 100
    return _pack_result(disease, confidence, "mobilenetv2")


def detect_disease(image_path):
    result = predict_disease(image_path)
    return result["disease"], result["confidence"]


if __name__ == "__main__":
    print("==============================")
    print("      Harvest Nexus Oracle")
    print("==============================")
    image_path = input("Enter leaf image path: ")
    try:
        result = predict_disease(image_path)
        print()
        print("Disease:", result["display_name"])
        print("Class:", result["disease"])
        print("Confidence:", result["confidence"], "%")
        print("Severity:", result["severity"])
        print("Source:", result["source"])
        print("Treatments:")
        for item in result["treatments"]:
            print(" -", item)
    except Exception as error:
        print("Error:", error)
