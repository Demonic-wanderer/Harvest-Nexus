# 🌾 Module 2 — Advisory Engine (Akasha)
### *Rule-Based Agronomic Intelligence & Farm Health Scoring*

---

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Rules-ICAR%20Compliant-43A047?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Output-Bilingual%20हिंदी%20%2F%20English-FF9800?style=for-the-badge" />
</p>

---

## 📋 What It Does

The **Advisory Engine** (codenamed **Akasha**) transforms raw sensor data, AI predictions, and weather telemetry into **prioritized, farmer-friendly action plans** — in both English and Hindi.

It answers the farmer's real-world question:
> *"I know my crop has Early Blight and soil moisture is low — but what exactly should I do TODAY, and in what order?"*

---

## 🏗️ How It Works

```
  Disease Prediction (from Oracle AI)
  Soil Sensors (Moisture, NPK, pH)
  Weather Data (Temp, Humidity, Rain %)
  Crop Stage (Vegetative / Flowering / Fruiting)
           ↓
   ┌──────────────────────────────────┐
   │       RULE ENGINE PIPELINE       │
   │                                  │
   │  1. 🧪 Chemical Safety Rule     │  ← Blocks spray if rain ≥ 60%
   │  2. 🦠 Disease Pathology Rule   │  ← Confidence-gated ICAR advisory
   │  3. 💧 Precision Irrigation     │  ← Soil moisture vs crop stage need
   │  4. 🧬 NPK Nutrition Rule      │  ← Detects N, P, K deficiencies
   │  5. ⚗️  Soil pH Balance Rule    │  ← Lime vs Gypsum correction
   │  6. 🌡️ Weather Stress Rule     │  ← Heat stress & humidity fungal risk
   │  7. 📦 Harvest–Mandi Sync      │  ← Links harvest date to price peaks
   │  8. 📊 Market Price Signal      │  ← Current mandi rate & trend
   └──────────┬───────────────────────┘
              ↓
   ┌──────────────────────────────────┐
   │        PRIORITY SORTER           │
   │  HIGH → MEDIUM → LOW ordering    │
   └──────────┬───────────────────────┘
              ↓
   ┌──────────────────────────────────┐
   │     FARM HEALTH SCORE (0–100)    │
   │  Deductions for:                 │
   │   • Active disease (−20 to −40)  │
   │   • Low soil moisture (−10)      │
   │   • NPK deficiency (−10)        │
   │   • Extreme pH (−5 to −10)      │
   └──────────┬───────────────────────┘
              ↓
   ┌──────────────────────────────────┐
   │     BILINGUAL ACTION PLAN        │
   │  {                               │
   │    "title": "Today's Action Plan"│
   │    "title_hi": "आज की कार्य योजना"│
   │    "recommendations": [...]      │
   │    "farm_health_score": 40       │
   │    "priority_level": "HIGH"      │
   │  }                               │
   └──────────────────────────────────┘
```

---

## 🧪 Rule Breakdown

### Rule 1 — Chemical Safety Guardrail 🌧️
> **Input:** Disease name + Rain probability  
> **Logic:** If rain probability ≥ 60%, **blocks** all foliar chemical spraying to prevent pesticide runoff and environmental contamination.  
> **Priority:** `HIGH`

### Rule 2 — Disease Pathology Advisory 🦠
> **Input:** Disease name + Model confidence + Crop name + Severity  
> **Logic:**
> - Confidence ≥ 80% → `HIGH` — *"Prune infected foliage and apply ICAR fungicide rotation"*
> - Confidence 60–80% → `MEDIUM` — *"Inspect leaves, implement preventative biocontrol"*
> - Confidence < 60% → `LOW` — *"Retake photo or consult KVK agronomist"*
> - Healthy → `LOW` — *"No pathogen detected"*

### Rule 3 — Precision Irrigation 💧
> **Input:** Soil moisture % + Rain probability + Crop growth stage  
> **Logic:** Adjusts irrigation threshold based on crop stage (flowering/fruiting need 40%+). Cross-references rain forecast to prevent waterlogging.

### Rule 4 — NPK Soil Nutrition 🧬
> **Input:** Nitrogen, Phosphorus, Potassium readings  
> **Logic:** Flags deficiencies below ICAR thresholds with specific fertilizer recommendations (Neem-coated Urea, SSP/DAP, MOP).

### Rule 5 — Soil pH Balance ⚗️
> **Input:** Soil pH value  
> **Logic:** Acidic (< 5.5) → Lime/Dolomite correction. Alkaline (> 7.8) → Gypsum/organic matter.

### Rule 6 — Weather & Microclimate 🌡️
> **Input:** Air temperature + Relative humidity  
> **Logic:** High temp (≥ 35°C) → Mulching & heat-stress monitoring. High humidity (≥ 80%) → Fungal spore risk alert.

### Rule 7 — Harvest-to-Mandi Sync 📦
> **Input:** Crop + Expected harvest date + Market price data  
> **Logic:** If mandi prices are rising and harvest is ≤ 7 days away → `HIGH` priority market opportunity alert.

### Rule 8 — General Market Signal 📊
> **Input:** Current mandi price + Trend  
> **Logic:** Provides baseline price awareness for transport and dispatch planning.

---

## 🌐 Bilingual Output

Every single rule generates **dual outputs**:

```json
{
  "priority": "HIGH",
  "category": "disease",
  "action": "Tomato___Early_blight detected with high confidence (92%). Prune infected foliage...",
  "action_hi": "उच्च विश्वास स्तर (92%) के साथ अर्ली ब्लाइट के लक्षण मिले। संक्रमित पत्तियों को काटें..."
}
```

---

## 📂 Key Files

| File | Purpose |
| :--- | :--- |
| `rules.py` | All 8 rule functions with bilingual message generation |
| `advisory.py` | Orchestrator — runs all rules, computes farm health score |
| `formatter.py` | Converts raw recommendations into farmer-friendly action plan |
| `priority.py` | Priority sorting logic (HIGH → MEDIUM → LOW) |
| `schemas.py` | Pydantic data models for structured input validation |

---

## 🚀 Usage

```python
from advisory_engine.advisory import generate_advisory
from advisory_engine.schemas import AdvisoryRequest

plan = generate_advisory(AdvisoryRequest(
    crop="Tomato",
    disease={"name": "Tomato___Early_blight", "confidence": 92, "severity": "high"},
    soil={"moisture": 22.0},
    weather={"temperature": 31, "humidity": 65, "rain_probability": 10}
))
# → Returns prioritized bilingual action plan with farm_health_score
```
