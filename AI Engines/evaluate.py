"""Evaluate a saved MobileNet checkpoint on a labelled folder dataset."""

from __future__ import annotations

import argparse
import json
import os

import torch
from torch.utils.data import DataLoader

from disease_mapping import load_labels
from train import DEFAULT_CHECKPOINT, FolderImageDataset, METRICS_FILE, _make_transform, evaluate_loader
from torchvision import models

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))


def evaluate(dataset_dir, checkpoint_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(checkpoint_path, map_location=device)
    class_names = checkpoint.get("class_names") or load_labels()

    model = models.mobilenet_v2(weights=None)
    model.classifier[1] = torch.nn.Linear(model.last_channel, len(class_names))
    model.load_state_dict(checkpoint["model_state"])
    model = model.to(device)

    dataset = FolderImageDataset(dataset_dir, class_names, _make_transform(train=False))
    loader = DataLoader(dataset, batch_size=8, shuffle=False)
    accuracy = evaluate_loader(model, loader, device)

    per_class = {name: {"correct": 0, "total": 0} for name in class_names}
    model.eval()
    with torch.no_grad():
        for images, labels in loader:
            predicted = model(images.to(device)).argmax(dim=1).cpu()
            for truth, pred in zip(labels, predicted):
                name = class_names[int(truth)]
                per_class[name]["total"] += 1
                if int(truth) == int(pred):
                    per_class[name]["correct"] += 1

    report = {
        "checkpoint": checkpoint_path,
        "dataset": dataset_dir,
        "accuracy": accuracy,
        "per_class": {
            name: {
                "support": stats["total"],
                "accuracy": round(100.0 * stats["correct"] / stats["total"], 2) if stats["total"] else None,
            }
            for name, stats in per_class.items()
        },
    }
    eval_path = os.path.join(ENGINE_DIR, "eval_report.json")
    with open(eval_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, encoding="utf-8") as handle:
            metrics = json.load(handle)
        metrics["evaluation"] = report
        with open(METRICS_FILE, "w", encoding="utf-8") as handle:
            json.dump(metrics, handle, indent=2)
    print(json.dumps(report, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description="Evaluate leaf-disease MobileNetV2")
    parser.add_argument("--dataset", default=os.path.join(ENGINE_DIR, "datasets", "leaf"))
    parser.add_argument("--checkpoint", default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()
    evaluate(args.dataset, args.checkpoint)


if __name__ == "__main__":
    main()
