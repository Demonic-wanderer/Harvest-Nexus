# 🧠 Module 1 — Oracle AI Engine
### *Deep Learning Disease Vision & Multimodal Intelligence*

---

<p align="center">
  <img src="https://img.shields.io/badge/Framework-PyTorch-EE4C2C?style=for-the-badge&logo=pytorch" />
  <img src="https://img.shields.io/badge/Model-MobileNetV2-4285F4?style=for-the-badge&logo=google" />
  <img src="https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Dataset-PlantVillage-43A047?style=for-the-badge" />
</p>

---

## 📋 What It Does

The **Oracle AI Engine** is the brain of Harvest Nexus — a real-time computer vision microservice that diagnoses crop leaf diseases from a single photograph using a fine-tuned **MobileNetV2** convolutional neural network.

It answers the farmer's core question:
> *"My leaf looks unhealthy — what disease is this, how confident are you, and what should I spray?"*

---

## 🏗️ Architecture

```
📸 Leaf Image Upload
        ↓
   ┌─────────────┐
   │  FastAPI     │  ← /predict-upload  (pure vision)
   │  Gateway     │  ← /assess-upload   (vision + soil + weather + advisory)
   │  (Port 8001) │  ← /forecast-yield  (harvest volume forecaster)
   └──────┬───────┘
          ↓
   ┌─────────────────────────┐
   │   MobileNetV2 Backbone  │  ← Pretrained on ImageNet
   │   + Custom Classifier   │  ← Fine-tuned on PlantVillage (10 classes)
   │   (224×224 RGB Input)   │
   └──────┬──────────────────┘
          ↓
   ┌─────────────────────┐
   │  Softmax → Top-3    │  ← Probability distribution over all 10 classes
   │  Confidence Gating  │  ← If confidence < 60% → flag as "uncertain"
   │  Severity Mapping   │  ← High (≥85%) / Medium (≥65%) / Low / Uncertain
   └──────┬──────────────┘
          ↓
   ┌──────────────────────────────┐
   │  Bilingual Response Packing  │
   │  • display_name (English)    │
   │  • display_name_hi (Hindi)   │
   │  • treatments[] (ICAR)       │
   │  • treatments_hi[]           │
   │  • diagnostic_alert          │
   │  • top_predictions[3]        │
   └──────────────────────────────┘
```

---

## 🧬 Model Training Details

| Parameter | Value |
| :--- | :--- |
| **Base Architecture** | MobileNetV2 (torchvision) |
| **Pretrained Weights** | ImageNet-1K |
| **Training Dataset** | [PlantVillage](https://github.com/spMohanty/PlantVillage-Dataset) (Tomato subset) |
| **Number of Classes** | 10 |
| **Input Resolution** | 224 × 224 × 3 (RGB) |
| **Normalization** | ImageNet mean `[0.485, 0.456, 0.406]` / std `[0.229, 0.224, 0.225]` |
| **Checkpoint File** | `mobilenetv2_disease.pth` (9.19 MB) |
| **Training Script** | `train.py` |

### Supported Disease Classes

| # | Class Name | Hindi Name |
|:--|:-----------|:-----------|
| 1 | Bacterial Spot | बैक्टीरियल स्पॉट (जीवाणु धब्बा) |
| 2 | Early Blight | अर्ली ब्लाइट (अगेती झुलसा) |
| 3 | Late Blight | लेट ब्लाइट (पछेती झुलसा) |
| 4 | Leaf Mold | लीफ मोल्ड (पत्ती फफूंद) |
| 5 | Septoria Leaf Spot | सेप्टोरिया लीफ स्पॉट (पत्ती धब्बा) |
| 6 | Spider Mites | स्पाइडर माइट्स (लाल मकड़ी) |
| 7 | Target Spot | टारगेट स्पॉट (लक्ष्य धब्बा) |
| 8 | Yellow Leaf Curl Virus | येलो लीफ कर्ल वायरस (पत्ती मुड़न विषाणु) |
| 9 | Mosaic Virus | मोज़ेक वायरस (चित्तीदार विषाणु) |
| 10 | Healthy | स्वस्थ पत्ती (रोगमुक्त) |

---

## 🛡️ Edge Case Handling

| Scenario | Behavior |
| :--- | :--- |
| **Empty file upload** | HTTP 400 — `"The selected image is empty."` |
| **Non-image MIME** | HTTP 415 — `"Use a JPEG, PNG, or WebP leaf photograph."` |
| **Corrupted image** | HTTP 400 — `"Not a readable leaf image."` |
| **Blurry / OOD image** | Returns `is_confident: false` + `diagnostic_alert` with retake guidance |
| **Model checkpoint missing** | HTTP 503 — `"Model unavailable."` |

---

## 📂 Key Files

| File | Purpose |
| :--- | :--- |
| `oracle_api.py` | FastAPI application — all REST endpoints |
| `disease_detection.py` | Model loading, preprocessing, inference, top-3 extraction |
| `disease_mapping.py` | Bilingual disease names, ICAR treatments, severity logic |
| `multimodel.py` | Multimodal fusion (vision + soil + weather + advisory) |
| `train.py` | Training script for MobileNetV2 on PlantVillage |
| `treatments.json` | Structured treatment data per disease class |
| `labels.json` | Ordered class name list matching checkpoint metadata |
| `mobilenetv2_disease.pth` | Trained model checkpoint (PyTorch) |

---

## 🚀 Running

```bash
cd "AI Engines"
uvicorn oracle_api:app --host 0.0.0.0 --port 8001 --reload
```

**Health Check:** `GET http://127.0.0.1:8001/health`
