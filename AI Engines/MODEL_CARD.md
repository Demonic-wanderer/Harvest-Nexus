# Oracle leaf-disease model card

## Intended use
Classify tomato leaf images into the PlantVillage-style classes listed in `labels.json`.
The API returns disease name, confidence, severity, and treatment steps from `treatments.json`.

## Training
```bash
python "AI Engines/train.py" --dataset path/to/leaf --epochs 10
```
Checkpoint path: `AI Engines/mobilenetv2_disease.pth` (gitignored; too large for the repo).

A smoke-train on synthetic colour tiles:
```bash
python "AI Engines/train.py" --synthetic --epochs 1
```

## Evaluation
```bash
python "AI Engines/evaluate.py" --dataset path/to/leaf --checkpoint "AI Engines/mobilenetv2_disease.pth"
```
Writes `eval_report.json` and merges metrics into `metrics.json`.

## Fallback
If the checkpoint is missing, `disease_detection.py` uses a documented colour heuristic so the service is not blocked. Predictions then have `"source": "color_heuristic"` and must not be treated as MobileNet output.

## Limitations
- The heuristic is not a substitute for a trained model.
- Severity is derived from class + confidence, not lesion area.
- Treatment text is agronomic guidance, not a pesticide prescription.
