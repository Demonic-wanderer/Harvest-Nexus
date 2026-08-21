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
Oracle refuses leaf scans when the checkpoint is missing or malformed (`503 ModelUnavailableError`). This avoids presenting a colour heuristic as a disease diagnosis. The health endpoint reports `"model_ready": false` until a checkpoint is installed.

## Limitations
- Severity is derived from class + confidence, not lesion area.
- Treatment text is agronomic guidance, not a pesticide prescription.
