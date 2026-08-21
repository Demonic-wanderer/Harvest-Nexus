# Harvest Nexus — SIH Qualifier Master Transcript & Engineering Guide
**Problem Statement:** Cloud-Native Agri-Advisory & Market Linkage Ecosystem with Multi-Modal AI and Mobile Telemetry  
**Domain:** Smart Agriculture & Rural Logistics  
**Competition:** Smart India Hackathon (SIH) Internal Qualifier (Software Edition)  
**Team Composition:** 6 Members (Ram, Arpan, Mananya, Bhumika, Moin, Ojas)  
**Target Date:** 22 Aug 2026

---

## Table of Contents
1. [SIH Problem Statement & Key Deliverables](#1-sih-problem-statement--key-deliverables)
2. [Team Allocation & 6-Module Architecture](#2-team-allocation--6-module-architecture)
3. [Comprehensive Security Flaws & Real-World Agronomic Backlashes](#3-comprehensive-security-flaws--real-world-agronomic-backlashes)
4. [Prototype Gap Analysis (What Your Submission Currently Lacks)](#4-prototype-gap-analysis-what-your-submission-currently-lacks)
5. [3-Day Team Sprint Checklist](#5-3-day-team-sprint-checklist)
6. [Winning SIH Presentation Structure (Slide-by-Slide Script)](#6-winning-sih-presentation-structure-slide-by-slide-script)
7. [The 3-Minute Live Jury Demo Script](#7-the-3-minute-live-jury-demo-script)
8. [Jury Q&A & Viva Defense Sheet](#8-jury-qa--viva-defense-sheet)
9. [Single-Command Startup Script (`start_all.bat`)](#9-single-command-startup-script-start_allbat)

---

## 1. SIH Problem Statement & Key Deliverables

### Background
Smallholder farmers encounter fragmented solutions that tackle either field-level agronomy (pest/disease detection, soil management) or post-harvest operations (mandi pricing, market linkage). The absence of a unified platform leads to sub-optimal yields, delayed disease interventions, and distress selling due to lack of market intelligence.

### Core Software Deliverables
1. **Agro-Cloud Backend & Pipelines:** Scalable REST/GraphQL APIs managing telemetry streams, database persistence, and automated AI model serving.
2. **Multi-Modal AI Engine:** Cloud-hosted deep learning model for plant disease identification from leaf imagery, paired with time-series forecasting for harvest volume and mandi price trends.
3. **Multilingual Mobile Interface:** Farmer dashboard featuring offline-first data caching, leaf photo upload, localized advisory push notifications, and market price tracking.
4. **Intelligent Advisory & Farm-to-Market Module:** Automated advisory generator for soil health and irrigation, plus a trade/logistics module linking harvest schedules with local mandi demand.

---

## 2. Team Allocation & 6-Module Architecture

```
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                                       HARVEST NEXUS ECOSYSTEM                                          │
 └────────────────────────────────────────────────────────────────────────────────────────────────────────┘
            │                                     │                                      │
            ▼                                     ▼                                      ▼
 ┌──────────────────────┐              ┌──────────────────────┐              ┌──────────────────────┐
 │    ORACLE (AI)       │              │    AKASHA (ADVISORY) │              │   INSIGHT (MARKET)   │
 │ • Lead: Arpan        │              │ • Lead: Ojas         │              │ • Lead: Bhumika      │
 │ • MobileNetV2 Vision │              │ • Rule Engine        │              │ • Mandi Price Trends │
 │ • Disease Diagnosis  │              │ • Health Scoring     │              │ • Buyer Linkage      │
 │ • Yield Forecasting  │              │ • Dosage Rails       │              │ • Logistics Quotes   │
 └──────────┬───────────┘              └──────────┬───────────┘              └──────────┬───────────┘
            │                                     │                                      │
            └──────────────────────────┬──────────┴──────────────────────────────────────┘
                                       │
                                       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                               FORGE BACKEND (PostgreSQL / Supabase / Neon)                             │
 │ • Lead: Moin                                                                                           │
 │ • REST APIs & JWT Auth (Farmer, Buyer, Admin, Advisor)    • Farm, Crop & Disease History               │
 │ • Telemetry Ingestion Pipeline                            • Transactions & Logistics State             │
 └─────────────────────────────────────┬──────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                                    PULSE (Flutter Mobile Client)                                       │
 │ • Lead: Mananya                                                                                        │
 │ • Multilingual Farmer Dashboard (Hindi/English)           • Leaf Photo Upload & Camera Pipeline        │
 │ • Offline-First Storage / Caching                         • Push Alerts & Emergency Banners            │
 └────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                                   OVERALL SYSTEM LEAD & PITCH                                          │
 │ • Lead: Ram                                                                                            │
 │ • System Integration, SIH PPT Template, Live Demo Orchestration & Q&A Coordination                    │
 └────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Comprehensive Security Flaws & Real-World Agronomic Backlashes

Judges frequently test whether teams understand that in agricultural cyber-physical systems, software security flaws result directly in **crop failure, chemical over-application, and financial loss**.

| Component / Feature | Security Vulnerability | Threat Actor & Exploit Scenario | Real-World Backlash & Agronomic Impact |
|---|---|---|---|
| **Disease Diagnosis (Oracle)** | Adversarial noise / OOD misclassification | Attacker adds subtle camera glare/noise to leaf image | Blight misdiagnosed as healthy; pathogen wipes out entire field in 72 hours. |
| **Image Upload Pipeline** | Image decompression bomb / unvalidated buffer | Malicious file upload on `/predict-upload` | AI worker node memory exhaustion (DoS), halting service during peak harvest. |
| **Priority & Rule Engine (Akasha)** | Unauthenticated IoT telemetry injection | Attacker injects spoofed 0% soil moisture readings | Automated flood irrigation triggered, rotting roots and causing mold outbreaks. |
| **Chemical Dosage Logic (Akasha)** | Boundary condition failure on extreme inputs | Negative or NaN input passes threshold checks | Over-fertilization advisory issued; crops burned and soil salinized. |
| **Mandi Price Forecast (Insight)** | Unfiltered price data injection | Cartels inject low-rate historical transactions | Artificially depressed trend forces farmers into panic distress selling. |
| **Buyer Linkage (Insight)** | Unverified buyer self-registration | Phantom buyer lists inflated price quotes | Harvest collected on credit; buyer absconds with hundreds of tons of grain. |
| **Logistics Quoting (Insight)** | IDOR on transport route/status updates | Rogue user modifies `drop_location` parameter | High-value agricultural cargo intercepted and redirected to illegal warehouse. |
| **Cloud Authentication (Forge)** | Privilege escalation on registration | Public signup payload includes `"role": "admin"` | Full database takeover, exfiltration of farmer PII and transaction records. |
| **Inter-Service Security (Forge)** | Static shared `X-Service-Key` | Intercepted key from one microservice | Unauthorized read/write across all backend database tables. |
| **Mobile App (Pulse)** | Lack of offline-first local encryption | Rooted device alters local database cache | Inaccurate advisory shown to farmer; wrong treatment applied in field. |
| **Multilingual Engine (Pulse)** | Localization translation poisoning | Unsanitized translation table inverts safety terms | *"Do NOT spray before rain"* translated as *"Spray before rain"*, poisoning water runoff. |

---

## 4. Prototype Gap Analysis (What Your Submission Currently Lacks)

*Note: Excludes non-essential auxiliary items (e.g. ChatBot) to focus strictly on core SIH Problem Statement deliverables.*

```
 ┌────────────────────────────────────────────────────────┬────────────┬────────────────────────────────────────────────────────┐
 │ Official SIH Software Deliverable                     │ Status     │ Exact Gaps in Current Codebase                         │
 ├────────────────────────────────────────────────────────┼────────────┼────────────────────────────────────────────────────────┤
 │ 1. Multi-Modal AI Engine (Oracle & Insight)            │ 🟡 Partial  │ • Missing Harvest Volume / Yield Forecasting.          │
 │    • Leaf disease vision model (MobileNetV2)           │            │ • Linear price slope used instead of time-series model.│
 │    • Time-series price & volume forecasting            │            │ • Multi-modal scoring not auto-triggered on upload.   │
 ├────────────────────────────────────────────────────────┼────────────┼────────────────────────────────────────────────────────┤
 │ 2. Agro-Cloud Backend & Telemetry Pipelines (Forge)   │ 🟡 Partial  │ • No dedicated `/api/telemetry` streaming endpoint.    │
 │    • Scalable REST APIs & PostgreSQL persistence       │            │ • Missing automated webhook/pipeline orchestration.   │
 │    • Automated model serving orchestration             │            │ • BOLA / authorization holes in farmer routes.         │
 ├────────────────────────────────────────────────────────┼────────────┼────────────────────────────────────────────────────────┤
 │ 3. Intelligent Advisory & Farm-to-Market (Akasha)      │ 🟡 Partial  │ • Harvest schedule NOT linked to Mandi demand peaks.   │
 │    • Automated soil, NPK & irrigation advisory         │            │ • Transporter booking not fully wired to DB state.     │
 │    • Logistics & mandi trade linkage                   │            │ • Lack of ICAR chemical dosage safety clamps.          │
 ├────────────────────────────────────────────────────────┼────────────┼────────────────────────────────────────────────────────┤
 │ 4. Multilingual Mobile Interface (Pulse)               │ 🟡 Partial  │ • Missing true offline-first cache (fails on no-net).  │
 │    • Multilingual farmer dashboard (Hindi/English)     │            │ • No dynamic emergency alert / push notification bar.  │
 │    • Offline-first caching & market tracking           │            │ • Incomplete Hindi translation on dynamic strings.     │
 ├────────────────────────────────────────────────────────┼────────────┼────────────────────────────────────────────────────────┤
 │ 5. System Orchestration & Startup                      │ 🔴 Missing  │ • No single-command startup (`start_all.bat` / Docker) │
 │    • Unified service launcher for live jury demo       │            │   to run Forge, Oracle, Insight & Weather together.    │
 └────────────────────────────────────────────────────────┴────────────┴────────────────────────────────────────────────────────┘
```

---

## 5. 3-Day Team Sprint Checklist

Assign these exact tasks across your 6 team members for the qualifier round on **22 Aug 2026**:

| Team Member | Module | Immediate Action Items (Next 48 Hours) |
|---|---|---|
| **1. Ram (Lead)** | Orchestration & Pitch | • Create `start_all.bat` to launch Forge, Oracle, and Insight concurrently.<br>• Build the 6-slide SIH official PPT template.<br>• Coordinate 3 golden test leaf image files. |
| **2. Arpan (AI)** | Oracle (AI Engine) | • Implement yield estimation formula in `multimodel.py`.<br>• Add confidence score guardrail ($<60\%$ = uncertain).<br>• Verify MobileNetV2 on Tomato, Wheat, and Potato samples. |
| **3. Moin (Cloud)** | Forge (Backend SQL) | • Add `POST /api/telemetry` for live IoT sensor streams.<br>• Deploy PostgreSQL schema to Supabase/Neon.<br>• Seed database with 5 Mandis, 3 Buyers, and 3 Transporters. |
| **4. Ojas (Advisory)** | Akasha (Advisory Engine) | • Implement `harvest_market_sync_rule` linking harvest dates to price peaks.<br>• Enforce ICAR chemical dosage safety limits in `rules.py`. |
| **5. Bhumika (Market)** | Insight (Market & Logistics) | • Wire 7-day price moving average calculation into `market_analytics.py`.<br>• Verify distance-based transport quote calculation with per-km rates. |
| **6. Mananya (Mobile)** | Pulse (Flutter App) | • Implement offline fallback caching in `session.dart` using local storage.<br>• Add the Emergency Alert Banner on the Flutter home dashboard.<br>• Record a 60-second backup video of the working app on a physical device. |

---

## 6. Winning SIH Presentation Structure (Slide-by-Slide Script)

```
 ┌─────────┬──────────────────────────────────────────┬─────────────────────────────────────────┐
 │ Slide # │ Official SIH Section                     │ Team Presenter & Key Content            │
 ├─────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
 │ Slide 1 │ Problem Statement ID & Title             │ Ram (Lead)                              │
 │         │ • Domain: Smart Agriculture              │ • Highlights the pre/post-harvest gap   │
 ├─────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
 │ Slide 2 │ Proposed Solution & Core Innovation      │ Ram & Ojas                              │
 │         │ • Unified Pre- & Post-Harvest Loop       │ • Multi-modal assessment (0-100 score)  │
 ├─────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
 │ Slide 3 │ Technical Architecture & Data Flow       │ Moin (Cloud) & Arpan (AI)               │
 │         │ • Cloud Backend + AI + Advisory Pipeline │ • Clean block diagram showing all 6     │
 ├─────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
 │ Slide 4 │ AI Models & Telemetry Processing         │ Arpan & Bhumika                         │
 │         │ • MobileNetV2 + Rule-based Advisory      │ • Time-series mandi price forecasting   │
 ├─────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
 │ Slide 5 │ Live Prototype Demonstration             │ Mananya (Pulse) & Ram                   │
 │         │ • Working Flutter App + Live Cloud APIs  │ • End-to-end 90-second user journey     │
 ├─────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
 │ Slide 6 │ Security, Agronomic Safety & Feasibility │ Ojas & Moin                             │
 │         │ • Dosage caps, KYC, RBAC, offline cache  │ • Directly addresses jury's edge cases  │
 ├─────────┼──────────────────────────────────────────┼─────────────────────────────────────────┤
 │ Slide 7 │ Business Potential & Future Scope        │ Bhumika & Ram                           │
 │         │ • Mandi commission, FPO subscriptions    │ • Hardware rover / edge-AI extension    │
 └─────────┴──────────────────────────────────────────┴─────────────────────────────────────────┘
```

---

## 7. The 3-Minute Live Jury Demo Script

1. **Step 1: Ingestion & AI Diagnosis (0:00 - 0:45) — *Mananya & Arpan***
   * Open Pulse App (toggle Hindi $\leftrightarrow$ English).
   * Pick sample `Tomato Early Blight` leaf photo.
   * Oracle returns: *"Tomato Early Blight (92% Confidence)"*.
2. **Step 2: Multi-Modal Advisory & Yield Forecast (0:45 - 1:30) — *Ojas & Moin***
   * Ingest live soil telemetry (Moisture 18%, NPK, Temp 31°C).
   * Akasha calculates **Farm Health Score: 64/100** and **Estimated Yield: 42 quintals/acre**.
   * Urgent priority actions: *"1. Apply Copper Fungicide | 2. Irrigate within 24h"*.
3. **Step 3: Market Intelligence & Buyer Linkage (1:30 - 2:15) — *Bhumika***
   * Open Market tab $\rightarrow$ System aligns expected harvest date with Mandi Indore's rising price trend ($₹2,300/\text{q}$).
   * Matches 2 nearby verified buyers and outputs an instant transport quote with per-km freight calculation.
4. **Step 4: Safety & Robustness Defense Summary (2:15 - 3:00) — *Ram***
   * Summarize offline-first caching for rural connectivity, ICAR chemical safety caps, and cloud scalability.

---

## 8. Jury Q&A & Viva Defense Sheet

```
 ┌─────────────────────────────────────────────────────────────────────────────────────────────┐
 │                         HOW TO ANSWER SIH JUDGES ON SECURITY & SAFETY                       │
 ├───────────────────────────────┬─────────────────────────────────────────────────────────────┤
 │ Judge's Trap Question         │ Your Winning 15-Second Answer                               │
 ├───────────────────────────────┼─────────────────────────────────────────────────────────────┤
 │ 1. "What if your AI detects   │ "We implement a Multi-Modal Fallback with Confidence        │
 │     the wrong disease and     │  Gating (<70% triggers manual review) and hardcoded ICAR    │
 │     recommends toxic spray?"  │  dosage ceilings in Akasha that prevent chemical overdosing."│
 ├───────────────────────────────┼─────────────────────────────────────────────────────────────┤
 │ 2. "What if someone submits   │ "Sensor readings pass through physical range plausibility    │
 │     fake/broken IoT sensor    │  filters; anomalies are flagged as 'Sensor Fault' rather    │
 │     data (e.g. 0% moisture)?" │  than triggering emergency irrigation."                     │
 ├───────────────────────────────┼─────────────────────────────────────────────────────────────┤
 │ 3. "How do you stop fake      │ "We apply rolling median outlier filtering to discard fake   │
 │     buyers from scamming      │  price spikes, and buyer contact discovery requires OTP/    │
 │     farmers or price fixing?" │  verified credentials before unlocking direct linkage."      │
 ├───────────────────────────────┼─────────────────────────────────────────────────────────────┤
 │ 4. "What stops someone from   │ "Forge uses role-based JWT auth (Farmer, Buyer, Advisor,    │
 │     scraping private farmer   │  Admin) and UUID-based object authorization to prevent      │
 │     locations and land data?" │  unauthorized farm profile enumeration."                    │
 ├───────────────────────────────┼─────────────────────────────────────────────────────────────┤
 │ 5. "How does the mobile app   │ "The Flutter app implements local storage caching for all   │
 │     function in remote areas  │  advisories and price tables, syncing back to Forge once    │
 │     with zero connectivity?"  │  cellular connection is restored."                          │
 └───────────────────────────────┴─────────────────────────────────────────────────────────────┘
```

---

## 9. Single-Command Startup Script (`start_all.bat`)

Place this file in the workspace root (`c:\Users\amans\Nexus\Harvest-Nexus\start_all.bat`) to launch all microservices and the Flutter frontend with one click:

```bat
@echo off
echo ===================================================
echo     STARTING HARVEST NEXUS CLOUD PLATFORM
echo ===================================================

:: 1. Start Cloud Backend (Forge)
start "Forge Backend (Port 5000)" cmd /k "npm run dev"

:: 2. Start Oracle AI Engine
start "Oracle AI (Port 8001)" cmd /k "uvicorn AI Engines.oracle_api:app --port 8001 --reload"

:: 3. Start Insight Market Module
start "Insight Market (Port 8000)" cmd /k "cd insight_module_final && uvicorn app.main:app --port 8000 --reload"

echo All backend microservices launched successfully!
echo Launching Flutter App...
cd frontend/flutter_application_1_ui
flutter run -d chrome
```
