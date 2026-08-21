# 📱 Module 4 — Flutter Frontend
### *Cross-Platform Mobile & Web Interface for Farmers*

---

<p align="center">
  <img src="https://img.shields.io/badge/Framework-Flutter-02569B?style=for-the-badge&logo=flutter" />
  <img src="https://img.shields.io/badge/Language-Dart-0175C2?style=for-the-badge&logo=dart" />
  <img src="https://img.shields.io/badge/Bilingual-Hindi%20हिंदी%20%2F%20English-FF9800?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Platforms-Android%20%7C%20iOS%20%7C%20Web-43A047?style=for-the-badge" />
</p>

---

## 📋 What It Does

The **Flutter Frontend** is the farmer-facing mobile and web application — the single interface through which smallholder farmers interact with the entire Harvest Nexus ecosystem. It provides:

- 📸 **Camera-based leaf disease scanning** with live MobileNetV2 inference
- 🌡️ **Real-time farm dashboard** showing crop health, soil readings, and weather
- 🏪 **Market intelligence** with mandi prices, buyer connections, and logistics
- 🌐 **Bilingual support** — instant English ↔ Hindi (हिंदी) toggle across all screens

---

## 🏗️ Screen Architecture

```
┌─────────────────────────────────────────────┐
│              HARVEST NEXUS APP               │
├─────────────────────────────────────────────┤
│                                             │
│  🏠 Home / Dashboard                       │
│  ├── Farm Health Score (0–100 gauge)        │
│  ├── Active Crop Status cards               │
│  ├── Weather Summary banner                 │
│  └── Quick-action buttons                   │
│                                             │
│  🌿 Disease Scanner (Core Screen)           │
│  ├── 1-Tap Demo Presets Toolbar             │
│  │   (🍅 Early Blight, 🍂 Late Blight,     │
│  │    🦠 Bacterial Spot, 🌿 Healthy,       │
│  │    ❓ Blurry/Unknown Test)              │
│  ├── 📸 Camera + 🖼️ Gallery buttons         │
│  ├── Leaf image preview container           │
│  ├── ⚠️ Diagnostic Alert card               │
│  ├── 🌧️ Weather Spray Guardrail banner      │
│  ├── Severity Badge (🔴🟠🟢⚠️)            │
│  ├── Confidence Meter (animated bar)        │
│  ├── Top-3 Candidate Predictions            │
│  └── ICAR Treatment Checklist (EN + HI)     │
│                                             │
│  📊 Market & Logistics                      │
│  ├── Nearby Mandi list with live prices     │
│  ├── Price trend charts                     │
│  ├── Buyer directory & matching             │
│  └── Transport booking                      │
│                                             │
│  👨‍🌾 Profile & Settings                     │
│  ├── Farm & Crop registration               │
│  └── Language preference toggle             │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🌿 Disease Scanner — Feature Deep Dive

The **Disease Scanner** is the hero screen of the app. Here's what happens when a farmer scans a leaf:

### Step-by-Step Flow

```
1. Farmer taps 📸 Camera (or 🖼️ Gallery, or a Demo Preset chip)
                    ↓
2. Image is displayed in the preview container
                    ↓
3. Loading spinner: "Running MobileNetV2 Inference..."
                    ↓
4. Multipart POST → FastAPI Oracle (/assess-upload)
   Payload: { file, crop, soil_moisture, air_temperature, humidity }
                    ↓
5. Oracle returns:
   • disease, display_name, display_name_hi
   • confidence %, is_confident, severity
   • top_predictions[3]
   • treatments[] & treatments_hi[]
   • diagnostic_alert & diagnostic_alert_hi
   • advisory { recommendations[], farm_health_score }
                    ↓
6. UI renders:
   • Severity badge (color-coded)
   • Animated confidence bar
   • Top 3 candidates breakdown
   • ICAR Treatment checklist (bilingual)
   • Diagnostic warning (if confidence < 60%)
   • Rain spray guardrail (if applicable)
```

---

## 🌐 Hindi / English Bilingual System

Every text element in the app supports instant language switching:

| Element | English | Hindi |
| :--- | :--- | :--- |
| Disease name | Early Blight | अर्ली ब्लाइट (अगेती झुलसा) |
| Treatment | "Prune affected lower foliage" | "प्रभावित निचली पत्तियों को काटें" |
| Diagnostic alert | "Confidence below 60%" | "विश्वास स्तर 60% से कम है" |
| Severity | HIGH SEVERITY | उच्च गंभीरता |
| Advisory title | Today's Action Plan | आज की कार्य योजना |

---

## 🛡️ Offline Resilience & Error Handling

| Scenario | App Behavior |
| :--- | :--- |
| **Server unreachable** | Falls back to demo preset display with offline notice |
| **No farm registered** | Uses default demo farmer (`Adarsh Krishi Farm`) so scanning is never blocked |
| **HTTP timeout (>30s)** | Shows friendly retry prompt |
| **400/415/503 errors** | Parses server error detail and displays human-friendly message |

---

## 📂 Key Files

```
frontend/flutter_application_1_ui/lib/
├── main.dart           # App entry, routing, all screens & Disease Scanner UI
├── config.dart         # API URL resolution (localhost / emulator / production)
├── api/
│   └── forge_api.dart  # HTTP client — predictLeaf(), assessLeaf()
└── state/
    └── session.dart    # App state — user, farm, crop, scan results, demo presets
```

---

## 🚀 Running

```bash
cd frontend/flutter_application_1_ui
flutter pub get
flutter run           # Android/iOS
flutter run -d chrome  # Web
```
