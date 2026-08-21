# 🌐 Harvest Nexus — System Integration Map
### *How All 6 Modules Connect Into One Unified Platform*

---

<p align="center">
  <img src="https://img.shields.io/badge/Modules-6-7C4DFF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI-MobileNetV2%20(PlantVillage)-EE4C2C?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Languages-Hindi%20%2F%20English-FF9800?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Stack-Flutter%20%7C%20FastAPI%20%7C%20Node.js-02569B?style=for-the-badge" />
</p>

---

## 🧩 The 6 Modules at a Glance

| # | Module | Tech Stack | Port | Role |
|:-:|:-------|:-----------|:----:|:-----|
| 1 | **Oracle AI Engine** | Python, PyTorch, FastAPI | 8001 | Disease detection via MobileNetV2 trained on PlantVillage dataset |
| 2 | **Advisory Engine** | Python | — | Rule-based ICAR agronomic advisory with bilingual output |
| 3 | **Forge Backend** | Node.js, Express, PostgreSQL | 5000 | REST API gateway, authentication, data persistence |
| 4 | **Flutter Frontend** | Dart, Flutter | — | Cross-platform mobile/web farmer interface |
| 5 | **Insight Market** | Python, FastAPI, SQLite | 8000 | Mandi price intelligence, demand analytics, forecasting |
| 6 | **Nexus** | Python, Batch Scripts | — | Orchestrator — config, startup, and integration glue |

---

## 🔄 Full Integration Architecture

```
                          ┌─────────────────────────┐
                          │    👨‍🌾 FARMER / USER      │
                          └────────────┬────────────┘
                                       │
                                       ↓
              ┌────────────────────────────────────────────┐
              │         MODULE 4: FLUTTER FRONTEND          │
              │                                            │
              │  📸 Camera Scan    🌐 Hindi/English Toggle  │
              │  🌿 Demo Presets   📊 Market Dashboard      │
              │  ⚠️ Diagnostic     🚚 Logistics Booking     │
              └───────┬────────────────────┬───────────────┘
                      │                    │
          POST /assess-upload         REST /api/*
          (multipart image +          (CRUD operations)
           sensor telemetry)
                      │                    │
                      ↓                    ↓
  ┌───────────────────────────┐   ┌─────────────────────────┐
  │  MODULE 1: ORACLE AI      │   │  MODULE 3: FORGE         │
  │  ENGINE                    │   │  BACKEND                 │
  │                            │   │                          │
  │  🧠 MobileNetV2 Inference  │   │  🔐 JWT Auth             │
  │  📊 Top-3 Predictions      │   │  👨‍🌾 Farmer/Farm/Crop     │
  │  🎯 Confidence Gating      │   │  💾 Disease Records      │
  │  🌡️ Multimodal Fusion      │   │  📋 Advisory Storage     │
  │                            │   │  🤝 Buyer Management     │
  │  Trained on PlantVillage   │   │  🚚 Logistics Tracking   │
  │  10 Tomato Disease Classes │   │  💰 Transactions         │
  │  224×224 RGB / ImageNet    │   │                          │
  │  Checkpoint: 9.19 MB      │   │  PostgreSQL Database     │
  └──────────┬─────────────────┘   └──────────┬──────────────┘
             │                                 ↑
             │  Python import                  │  HTTP persist
             ↓                                 │
  ┌──────────────────────────────┐             │
  │  MODULE 2: ADVISORY ENGINE   │─────────────┘
  │  (Akasha)                    │
  │                              │
  │  Rule 1: 🧪 Chemical Safety │  ← Blocks spray if rain ≥ 60%
  │  Rule 2: 🦠 Disease Advisory│  ← ICAR treatment guidance
  │  Rule 3: 💧 Irrigation      │  ← Soil moisture vs crop stage
  │  Rule 4: 🧬 NPK Nutrition   │  ← Detects N, P, K deficiency
  │  Rule 5: ⚗️ Soil pH         │  ← Lime / Gypsum correction
  │  Rule 6: 🌡️ Weather Stress  │  ← Heat & humidity fungal risk
  │  Rule 7: 📦 Harvest–Mandi   │  ← Links harvest to price peaks ←──┐
  │  Rule 8: 📊 Market Signal   │  ← Current mandi rate & trend  ←──┤
  │                              │                                    │
  │  Output: Bilingual Action    │                                    │
  │  Plan + Farm Health Score    │                                    │
  └──────────────────────────────┘                                    │
                                                                      │
                                        ┌─────────────────────────────┘
                                        │
                            ┌───────────┴───────────────┐
                            │  MODULE 5: INSIGHT MARKET  │
                            │  ENGINE                    │
                            │                            │
                            │  📈 Live Mandi Prices      │
                            │  📉 Historical Trends      │
                            │  🔮 Price Forecasting      │
                            │  🤝 Buyer Demand Matching  │
                            │                            │
                            │  SQLite: insight_module.db │
                            └────────────────────────────┘


                    ┌────────────────────────────────────┐
                    │  MODULE 6: NEXUS (ORCHESTRATOR)     │
                    │                                    │
                    │  Owns: .env, start_all.bat,        │
                    │  main.py, shared/, db/, tests/     │
                    │                                    │
                    │  Binds all 5 modules into one      │
                    │  deployable, launchable system.    │
                    └────────────────────────────────────┘
```

---

## 🔑 Critical Integration Points

### 1. 📸 Flutter → Oracle AI (Disease Detection)

> **Protocol:** HTTP POST (multipart/form-data)  
> **Endpoint:** `POST /assess-upload`  
> **Payload:** `{ file: leaf.jpg, crop: "Tomato", soil_moisture: 25.0, humidity: 65 }`  
> **Response:** Full diagnosis + top-3 candidates + bilingual treatments + advisory plan

The Flutter app sends the camera-captured leaf image directly to the Oracle AI Engine. Oracle runs MobileNetV2 inference, calculates top-3 softmax predictions, determines severity, and invokes the Advisory Engine before returning a comprehensive JSON response.

**Key technical detail:** The disease detection model is a **MobileNetV2 backbone pretrained on ImageNet**, then **fine-tuned on the PlantVillage open-source dataset** (Tomato subset — 10 classes). The trained checkpoint (`mobilenetv2_disease.pth`, 9.19 MB) is stored inside `AI Engines/` and loaded once into GPU/CPU memory on first request.

---

### 2. 🧠 Oracle AI → Advisory Engine (Rule-Based Advisory)

> **Protocol:** Direct Python import (in-process call)  
> **Function:** `generate_advisory(AdvisoryRequest(...))`  
> **Trigger:** Automatically invoked inside `/assess-upload` after vision inference completes

After Oracle AI identifies the disease, it constructs an `AdvisoryRequest` containing:
- Disease name, confidence, and severity from the vision model
- Soil moisture, NPK, and pH from telemetry (sent by Flutter)
- Air temperature, humidity, and rain probability from weather data

The Advisory Engine runs all 8 rules, computes a **Farm Health Score (0–100)**, and returns a **priority-sorted bilingual action plan**.

---

### 3. 🦠 Oracle AI → Forge Backend (Persistence)

> **Protocol:** HTTP POST to Forge API  
> **Data Flow:** Disease scan result → `POST /api/diseases` → PostgreSQL  
> **Optional:** Advisory plan → `POST /api/advisories` → PostgreSQL

When `persist_to_forge: true` is set, Oracle AI forwards the scan result and advisory to the Forge Backend for permanent storage. This creates a historical record of every diagnosis for the farm, enabling:
- Disease progression tracking over time
- Historical advisory audit trail
- Agronomist review of past recommendations

---

### 4. 📊 Advisory Engine ← Insight Market (Price Intelligence)

> **Protocol:** Data passed via Advisory Engine's `market` field in `AdvisoryRequest`  
> **Rules:** Rule 7 (Harvest-to-Mandi Sync) + Rule 8 (Market Signal)

The Insight Market Engine's price data feeds into the Advisory Engine's harvest-to-market optimization rules. When prices are trending upward and the farmer's harvest is imminent, the system generates a `HIGH` priority alert:
> *"MARKET PEAK OPPORTUNITY: Azadpur Mandi Tomato price is rising (₹2,450/q). Harvest in 5 days aligns with high demand."*

---

### 5. 🌐 Bilingual Pipeline (End-to-End Hindi/English)

> **Scope:** Spans ALL modules — Oracle AI → Advisory Engine → Flutter UI

The bilingual system is not a superficial UI translation. It flows through every layer:

| Layer | English Field | Hindi Field |
| :--- | :--- | :--- |
| Oracle AI | `display_name` | `display_name_hi` |
| Oracle AI | `treatments[]` | `treatments_hi[]` |
| Oracle AI | `diagnostic_alert` | `diagnostic_alert_hi` |
| Advisory Engine | `action` | `action_hi` |
| Advisory Engine | `title` | `title_hi` |
| Flutter UI | All labels, buttons, tooltips | Instant toggle via `isHindi` flag |

---

### 6. 🛡️ Graceful Error Handling (Cross-Module)

| Error Source | HTTP Code | User-Facing Message |
| :--- | :--- | :--- |
| Empty image upload | 400 | "The selected image is empty. Choose another leaf photograph." |
| Non-image file | 415 | "Use a JPEG, PNG, or WebP leaf photograph." |
| Corrupted image | 400 | "This is not a readable leaf image. Retake a clear photo." |
| Model checkpoint missing | 503 | "Model unavailable. Contact support." |
| Low confidence (<60%) | 200 | `is_confident: false` + diagnostic alert with retake guidance |
| Server unreachable | — | Flutter falls back to offline demo preset mode |

---

## 🚀 One-Command Full System Launch

```bash
# Windows — launches all services in parallel
start_all.bat
```

| Service | URL | Health Check |
| :--- | :--- | :--- |
| Oracle AI Engine | `http://127.0.0.1:8001` | `GET /health` |
| Forge Backend | `http://127.0.0.1:5000` | `GET /api/health` |
| Insight Market | `http://127.0.0.1:8000` | `GET /health` |
| Flutter App | Runs on device/emulator/browser | — |

---

## 📐 Technology Stack Summary

```
┌──────────────────────────────────────────────────────────┐
│  FRONTEND          │  Flutter (Dart)  — Android/iOS/Web  │
├──────────────────────────────────────────────────────────┤
│  AI / ML           │  PyTorch MobileNetV2 (PlantVillage) │
│                    │  FastAPI (Python 3.10+)              │
├──────────────────────────────────────────────────────────┤
│  BACKEND API       │  Express.js (Node.js)                │
├──────────────────────────────────────────────────────────┤
│  DATABASES         │  PostgreSQL (Forge)                  │
│                    │  SQLite (Insight Market)             │
├──────────────────────────────────────────────────────────┤
│  ADVISORY          │  Pure Python Rule Engine             │
│                    │  8 ICAR-compliant agronomic rules    │
├──────────────────────────────────────────────────────────┤
│  ORCHESTRATION     │  Nexus (.env + start_all.bat)        │
│                    │  Shared utilities (shared/)          │
└──────────────────────────────────────────────────────────┘
```

---

> **Harvest Nexus** — From a single leaf photograph to a prioritized, bilingual, market-linked action plan. Six modules, one mission: **empowering India's smallholder farmers with AI-driven precision agriculture.**
