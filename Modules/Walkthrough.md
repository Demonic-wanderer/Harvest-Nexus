# Walkthrough: Rock-Solid Disease Prediction & Advisory Pipeline

We have completed the end-to-end integration and enhancement across all three layers in the exact order requested: **Flutter Frontend → Advisory Engine → Oracle AI FastAPI Engine**.

---

## Key Achievements

### 1. Flutter Frontend (`frontend/flutter_application_1_ui/`)
- **[config.dart](file:///d:/Nexus/Harvest-Nexus/frontend/flutter_application_1_ui/lib/config.dart)**: Added dynamic URL resolution supporting Web, Android Emulator (`10.0.2.2`), and Desktop/Localhost (`127.0.0.1:8001`).
- **[forge_api.dart](file:///d:/Nexus/Harvest-Nexus/frontend/flutter_application_1_ui/lib/api/forge_api.dart)**: Implemented `predictLeaf` and `assessLeaf` multipart endpoints with timeout handling and error parsing for 400/413/415/503 responses.
- **[session.dart](file:///d:/Nexus/Harvest-Nexus/frontend/flutter_application_1_ui/lib/state/session.dart)**:
  - Added default demo state (`Adarsh Krishi Farm`, `Tomato Crop`) so leaf scanning **never blocks on missing registration**.
  - Added 1-tap demo preset loaders (`early_blight`, `late_blight`, `bacterial_spot`, `healthy`, `unclear`).
  - Added offline fallback resilience to ensure smooth, unblocked demo flow.
- **[main.dart](file:///d:/Nexus/Harvest-Nexus/frontend/flutter_application_1_ui/lib/main.dart)**:
  - **1-Tap Demo Presets Bar**: Quick chips to test all scenarios instantly (🍅 Early Blight, 🍂 Late Blight, 🦠 Bacterial Spot, 🌿 Healthy Leaf, ❓ Blurry / Unclear Test).
  - **Camera & Gallery Buttons**: 📸 `Scan Leaf (Camera)` and 🖼️ `Upload Gallery`.
  - **Severity Badges**: 🔴 High / 🟠 Medium / 🟢 Healthy / ⚠️ Unverified.
  - **Top Candidate Predictions**: Breakdown of top 3 probabilities for full transparency.
  - **Diagnostic Alert Card**: High-contrast warning banner when confidence is below 60% with photography tips.
  - **Weather & Chemical Spray Guardrail**: Prominently warns farmers to hold chemical spraying if rainfall probability $\ge 60\%$.
  - **Bilingual Switch**: Instant seamless switching between English and authentic Hindi across all diagnosis and advisory elements.

---

### 2. Advisory Engine (`advisory_engine/`)
- **[rules.py](file:///d:/Nexus/Harvest-Nexus/advisory_engine/rules.py)**:
  - Chemical safety rule (rainfall spray hold to prevent runoff pollution).
  - Disease pathology rule with ICAR guidelines.
  - Precision irrigation rule (soil moisture + rain probability + growth stage).
  - NPK soil nutrition and pH balance rules.
  - All rules now generate bilingual output (`message` & `message_hi`).
- **[formatter.py](file:///d:/Nexus/Harvest-Nexus/advisory_engine/formatter.py)**: Propagates bilingual action text and plan titles.
- **[advisory.py](file:///d:/Nexus/Harvest-Nexus/advisory_engine/advisory.py)**: Computes dynamic farm health score (0–100) and highest priority level (HIGH, MEDIUM, LOW).

---

### 3. Oracle AI & Vision Engine (`AI Engines/`)
- **[disease_mapping.py](file:///d:/Nexus/Harvest-Nexus/AI%20Engines/disease_mapping.py)**: Enriched standardized Hindi pathology names (e.g. *अर्ली ब्लाइट (अगेती झुलसा)*, *लेट ब्लाइट (पछेती झुलसा)*, *बैक्टीरियल स्पॉट (जीवाणु धब्बा)*) and complete ICAR treatments for all 10 PlantVillage tomato classes.
- **[disease_detection.py](file:///d:/Nexus/Harvest-Nexus/AI%20Engines/disease_detection.py)**:
  - Added top-3 candidate prediction calculation via softmax `topk`.
  - Added out-of-distribution & low-confidence detection (< 60% confidence alert).
- **[multimodel.py](file:///d:/Nexus/Harvest-Nexus/AI%20Engines/multimodel.py)**: Guarantees full advisory generation even in standalone demo mode without remote database dependency.
- **[oracle_api.py](file:///d:/Nexus/Harvest-Nexus/AI%20Engines/oracle_api.py)**: Robust error handling with user-friendly error codes (`empty_image`, `unsupported_image_type`, `invalid_image`).

---

### 4. Zero-Setup Instant Web Demo (`web_demo.html`)
- Created [web_demo.html](file:///d:/Nexus/Harvest-Nexus/web_demo.html) in the workspace root.
- Directly communicates with the running FastAPI backend (`http://127.0.0.1:8001/assess-upload`).
- Features live camera feed, file upload, demo presets, Hindi/English switch, and live MobileNetV2 confidence bar.

---

## Verification Results

| Test Scenario | Input / Action | Expected Result | Status |
| :--- | :--- | :--- | :---: |
| **Model Inference** | Sample leaf image | Correct disease class + top-3 candidates + confidence score | ✅ Passed |
| **Advisory Engine** | Early Blight + Low Moisture + Rain Risk | High priority disease advisory + irrigation notice + spray hold | ✅ Passed |
| **Bilingual Generation** | Hindi Language Toggle | Authentic Hindi display names, treatments, and alerts | ✅ Passed |
| **Empty Upload** | 0-byte file | HTTP 400 (`empty_image`) | ✅ Passed |
| **Invalid MIME** | Plain text file | HTTP 415 (`unsupported_image_type`) | ✅ Passed |
| **Corrupted File** | Corrupted image bytes | HTTP 400 (`invalid_image`) | ✅ Passed |
| **Low Confidence** | Blurred/Unclear image | `is_confident: false` with daylight diagnostic alert | ✅ Passed |
