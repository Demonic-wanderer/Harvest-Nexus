"""Train MobileNetV2 on a folder of labelled leaf images.

Expected layout:
    dataset/
        Tomato___Early_blight/*.jpg
        Tomato___healthy/*.jpg
"""

from __future__ import annotations

import argparse
import json
import os
import random
from datetime import datetime, timezone

import torch
from PIL import Image
from torch import nn
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms

from disease_mapping import load_labels

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CHECKPOINT = os.path.join(ENGINE_DIR, "mobilenetv2_disease.pth")
METRICS_FILE = os.path.join(ENGINE_DIR, "metrics.json")
IMAGE_SIZE = 224


class FolderImageDataset(Dataset):
    def __init__(self, root, class_names, image_transform):
        self.samples = []
        self.transform = image_transform
        self.class_names = class_names
        index = {name: i for i, name in enumerate(class_names)}
        for class_name in class_names:
            class_dir = os.path.join(root, class_name)
            if not os.path.isdir(class_dir):
                continue
            for filename in os.listdir(class_dir):
                if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    self.samples.append((os.path.join(class_dir, filename), index[class_name]))
        if not self.samples:
            raise FileNotFoundError(f"No images found under {root}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        image = Image.open(path).convert("RGB")
        return self.transform(image), label


def _make_transform(train=False):
    ops = [transforms.Resize((IMAGE_SIZE, IMAGE_SIZE))]
    if train:
        ops.append(transforms.RandomHorizontalFlip())
    ops.extend([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transforms.Compose(ops)


def write_synthetic_dataset(root, images_per_class=4):
    os.makedirs(root, exist_ok=True)
    labels = load_labels()
    color_for = {
        "Tomato___healthy": (40, 160, 50),
        "Tomato___Early_blight": (140, 70, 30),
        "Tomato___Late_blight": (40, 50, 90),
        "Tomato___Yellow_Leaf_Curl_Virus": (180, 180, 40),
    }
    for class_name in labels:
        class_dir = os.path.join(root, class_name)
        os.makedirs(class_dir, exist_ok=True)
        color = color_for.get(class_name, (
            random.randint(20, 200),
            random.randint(20, 200),
            random.randint(20, 200),
        ))
        for i in range(images_per_class):
            image = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), color)
            image.save(os.path.join(class_dir, f"sample_{i}.png"))
    return labels


def evaluate_loader(model, loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            predicted = model(images).argmax(dim=1)
            correct += (predicted == labels).sum().item()
            total += labels.size(0)
    return round(100.0 * correct / max(total, 1), 2)


def train(dataset_dir, epochs, batch_size, output_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    class_names = load_labels()
    dataset = FolderImageDataset(dataset_dir, class_names, _make_transform(train=True))
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = nn.Linear(model.last_channel, len(class_names))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    history = []
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * images.size(0)
        accuracy = evaluate_loader(model, loader, device)
        epoch_loss = running_loss / len(dataset)
        history.append({"epoch": epoch, "loss": round(epoch_loss, 4), "accuracy": accuracy})
        print(f"epoch {epoch}/{epochs} loss={epoch_loss:.4f} acc={accuracy:.2f}%")

    torch.save({"class_names": class_names, "model_state": model.state_dict()}, output_path)
    metrics = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dataset": dataset_dir,
        "epochs": epochs,
        "samples": len(dataset),
        "classes": class_names,
        "history": history,
        "checkpoint": output_path,
    }
    with open(METRICS_FILE, "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
    print("saved", output_path)
    return metrics


def main():
    parser = argparse.ArgumentParser(description="Train leaf-disease MobileNetV2")
    parser.add_argument("--dataset", default=os.path.join(ENGINE_DIR, "datasets", "leaf"))
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--output", default=DEFAULT_CHECKPOINT)
    parser.add_argument("--synthetic", action="store_true", help="Generate a tiny colour dataset for a smoke train")
    args = parser.parse_args()

    if args.synthetic:
        write_synthetic_dataset(args.dataset)

    train(args.dataset, args.epochs, args.batch_size, args.output)


if __name__ == "__main__":
    main()
