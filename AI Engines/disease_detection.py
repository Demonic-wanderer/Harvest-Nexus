import torch
from PIL import Image
from torchvision import transforms, models


MODEL_FILE = "mobilenetv2_disease.pth"

IMAGE_SIZE = 224


device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Using:", device)





transform = transforms.Compose([
    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


checkpoint = torch.load(
    MODEL_FILE,
    map_location=device
)

class_names = checkpoint["class_names"]


model = models.mobilenet_v2(
    weights=None
)



model.classifier[1] = torch.nn.Linear(
    model.last_channel,
    len(class_names)
)



model.load_state_dict(
    checkpoint["model_state"]
)

model = model.to(device)

model.eval()



def detect_disease(image_path):

    
    image = Image.open(
        image_path
    ).convert("RGB")

    
    image = transform(image)

    
    image = image.unsqueeze(0)

   
    image = image.to(device)

  
    with torch.no_grad():

        output = model(image)

    
    probabilities = torch.softmax(
        output,
        dim=1
    )

    
    prediction = torch.argmax(
        probabilities,
        dim=1
    ).item()

 
    disease = class_names[prediction]

   
    confidence = (
        probabilities[0][prediction].item()
        * 100
    )

    return disease, confidence


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