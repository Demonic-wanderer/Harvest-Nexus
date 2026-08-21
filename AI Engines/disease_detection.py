import os
import sys

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from disease_mapping import (
    display_name,
    display_name_hi,
    load_labels,
    severity_from_prediction,
    treatments_for,
    treatments_for_hi,
)

MODEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mobilenetv2_disease.pth")
IMAGE_SIZE = 224

_model = None
_class_names = None


class ModelUnavailableError(RuntimeError):
    """Raised when Oracle has no validated trained disease checkpoint."""


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
        raise ModelUnavailableError(
            f"Disease-model checkpoint is missing: {MODEL_FILE}. "
            "Train or install a PlantVillage-trained checkpoint before accepting leaf scans."
        )

    torch, models, transforms = _torch_stack()
    device = _device(torch)
    try:
        checkpoint = torch.load(MODEL_FILE, map_location=device, weights_only=True)
    except TypeError:  # PyTorch before the weights_only option
        checkpoint = torch.load(MODEL_FILE, map_location=device)
    except Exception as exc:
        raise ModelUnavailableError(f"Unable to read disease-model checkpoint: {exc}") from exc
    _class_names = checkpoint.get("class_names")
    if not isinstance(_class_names, list) or not _class_names:
        raise ModelUnavailableError("Disease-model checkpoint has no valid class_names metadata.")
    if "model_state" not in checkpoint:
        raise ModelUnavailableError("Disease-model checkpoint has no model_state weights.")
    expected_classes = load_labels()
    if _class_names != expected_classes:
        raise ModelUnavailableError(
            "Disease-model classes do not match this application's supported tomato disease labels."
        )

    model_loaded = models.mobilenet_v2(weights=None)
    model_loaded.classifier[1] = torch.nn.Linear(model_loaded.last_channel, len(_class_names))
    try:
        model_loaded.load_state_dict(checkpoint["model_state"])
    except RuntimeError as exc:
        raise ModelUnavailableError(f"Disease-model weights are incompatible with MobileNetV2: {exc}") from exc
    model_loaded = model_loaded.to(device)
    model_loaded.eval()

    _model = (model_loaded, device, transforms)
    return _model, _class_names


def _pack_result(class_name, confidence, source, top_predictions=None):
    conf_val = round(float(confidence), 2)
    severity = severity_from_prediction(class_name, conf_val)
    is_confident = conf_val >= 60.0

    diagnostic_alert = None
    if not is_confident:
        diagnostic_alert = (
            "Confidence is below 60%. The image may be blurry, occluded, or outside training distribution. "
            "Please retake a clear close-up leaf photograph in natural daylight or consult an agronomist."
        )

    return {
        "disease": class_name,
        "display_name": display_name(class_name),
        "display_name_hi": display_name_hi(class_name),
        "confidence": conf_val,
        "is_confident": is_confident,
        "severity": severity,
        "treatments": treatments_for(class_name, conf_val),
        "treatments_hi": treatments_for_hi(class_name, conf_val),
        "top_predictions": top_predictions or [
            {
                "disease": class_name,
                "display_name": display_name(class_name),
                "display_name_hi": display_name_hi(class_name),
                "confidence": conf_val,
            }
        ],
        "diagnostic_alert": diagnostic_alert,
        "diagnostic_alert_hi": (
            "विश्वास स्तर 60% से कम है। साफ प्राकृतिक रोशनी में पत्ती की तस्वीर लेकर फिर प्रयास करें या कृषि सलाहकार से संपर्क करें।"
            if diagnostic_alert else None
        ),
        "source": source,
    }


def predict_disease(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image '{image_path}' not found.")

    try:
        from PIL import Image
        with Image.open(image_path) as img:
            img.verify()
    except Exception as exc:
        raise ValueError(f"Invalid or corrupted image file: {exc}") from exc

    bundle, class_names_loaded = load_model()

    from PIL import Image

    torch, _models, transforms = _torch_stack()
    model_loaded, device, _ = bundle
    image = Image.open(image_path).convert("RGB")
    tensor = _transform(transforms)(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model_loaded(tensor)

    probabilities = torch.softmax(output, dim=1)[0]
    
    # Calculate top-k predictions for transparent candidate breakdown
    top_k_indices = torch.topk(probabilities, k=min(3, len(class_names_loaded))).indices.tolist()
    top_predictions = [
        {
            "disease": class_names_loaded[idx],
            "display_name": display_name(class_names_loaded[idx]),
            "display_name_hi": display_name_hi(class_names_loaded[idx]),
            "confidence": round(probabilities[idx].item() * 100, 2),
        }
        for idx in top_k_indices
    ]

    prediction = top_k_indices[0]
    disease = class_names_loaded[prediction]
    confidence = probabilities[prediction].item() * 100
    return _pack_result(disease, confidence, "mobilenetv2_plantvillage", top_predictions=top_predictions)


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
        print("Top Candidates:")
        for cand in result.get("top_predictions", []):
            print(f" - {cand['display_name']} ({cand['confidence']}%)")
        print("Treatments:")
        for item in result["treatments"]:
            print(" -", item)
    except Exception as error:
        print("Error:", error)
