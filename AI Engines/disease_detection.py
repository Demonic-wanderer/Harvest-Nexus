import os

import torch
from PIL import Image
from torchvision import models, transforms

MODEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mobilenetv2_disease.pth")

IMAGE_SIZE = 224


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

transform = transforms.Compose([
    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


_model = None
_class_names = None


def load_model():
    global _model, _class_names
    if _model is not None:
        return _model, _class_names

    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(
            f"Model file '{MODEL_FILE}' not found. Please ensure it is present in the working directory before running inference."
        )

    print("Loading model onto:", device)
    checkpoint = torch.load(
        MODEL_FILE,
        map_location=device
    )

    _class_names = checkpoint["class_names"]

    model_loaded = models.mobilenet_v2(
        weights=None
    )

    model_loaded.classifier[1] = torch.nn.Linear(
        model_loaded.last_channel,
        len(_class_names)
    )

    model_loaded.load_state_dict(
        checkpoint["model_state"]
    )

    model_loaded = model_loaded.to(device)
    model_loaded.eval()

    _model = model_loaded
    return _model, _class_names


def detect_disease(image_path):
    model_loaded, class_names_loaded = load_model()
    
    image = Image.open(
        image_path
    ).convert("RGB")

    image = transform(image)
    image = image.unsqueeze(0)
    image = image.to(device)

    with torch.no_grad():
        output = model_loaded(image)

    probabilities = torch.softmax(
        output,
        dim=1
    )

    prediction = torch.argmax(
        probabilities,
        dim=1
    ).item()

    disease = class_names_loaded[prediction]

    confidence = (
        probabilities[0][prediction].item()
        * 100
    )

    return disease, confidence


if __name__ == "__main__":
    print()
    print("==============================")
    print("      🌾 KISAN AI")
    print("==============================")

    image_path = input(
        "Enter leaf image path: "
    )

    try:
        disease, confidence = detect_disease(
            image_path
        )

        print()
        print("==============================")
        print("       DISEASE RESULT")
        print("==============================")

        print()
        print("🌱 Disease:")
        print(disease)

        print()
        print("📊 Confidence:")
        print(round(confidence, 2), "%")

        print()
        print("==============================")

    except Exception as error:
        print()
        print("❌ Error:")
        print(error)