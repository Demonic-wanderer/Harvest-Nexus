# 🔗 Module 6 — Nexus (The Orchestrator)
### *Central Coordination Layer — The Leader That Binds Every Module*

---

<p align="center">
  <img src="https://img.shields.io/badge/Role-Orchestrator-7C4DFF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Entry-main.py-3776AB?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Launcher-start__all.bat-0078D6?style=for-the-badge&logo=windows" />
  <img src="https://img.shields.io/badge/Config-.env-ECD53F?style=for-the-badge" />
</p>

---

## 📋 What It Does

**Nexus** is the orchestrator — the central nervous system that binds all five modules into one cohesive, deployable ecosystem. It is not a standalone service; it is the **coordination logic, shared configuration, startup scripts, and integration glue** that ensures:

- Every module discovers every other module's URL and port
- All services start in the correct order with a single command
- Shared environment variables (API keys, database URLs, ports) are centralized
- Cross-module communication contracts are enforced
- The entire system behaves as **one product**, not five disconnected tools

It answers the developer/deployment question:
> *"How do I start the entire Harvest Nexus platform with one command, and how do the modules know where to find each other?"*

---

## 🏗️ What Nexus Controls

```
┌─────────────────────────────────────────────────────────┐
│                    NEXUS ORCHESTRATOR                     │
│                                                          │
│   📄 .env                                                │
│   ├── ORACLE_PORT=8001                                   │
│   ├── FORGE_PORT=5000                                    │
│   ├── INSIGHT_PORT=8000                                  │
│   ├── DATABASE_URL=postgresql://...                      │
│   └── JWT_SECRET=...                                     │
│                                                          │
│   🚀 start_all.bat          (One-click full launch)      │
│   ├── 1. Oracle AI Engine   → uvicorn :8001              │
│   ├── 2. Forge Backend      → node :5000                 │
│   ├── 3. Insight Market     → uvicorn :8000              │
│   └── 4. Flutter / Web Demo → flutter run / browser      │
│                                                          │
│   🐍 main.py                (Python entrypoint)          │
│   ├── Validates all service dependencies                 │
│   ├── Runs health checks on startup                      │
│   └── Exposes unified status endpoint                    │
│                                                          │
│   📁 shared/                 (Cross-module utilities)    │
│   ├── forge_client.py       → HTTP client to Forge API   │
│   ├── weather/              → Shared weather API access   │
│   └── Common data schemas                                │
│                                                          │
│   📁 db/                     (Database migrations)       │
│   ├── Schema definitions                                 │
│   └── Seed data scripts                                  │
│                                                          │
│   📁 tests/                  (Integration test suite)    │
│   └── End-to-end pipeline verification                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 Service Discovery & Communication Map

Nexus ensures every module can talk to every other module through a shared `.env` configuration:

```
 ┌──────────┐      POST /assess-upload       ┌──────────────┐
 │ Flutter  │ ──────────────────────────────→ │  Oracle AI   │
 │ Frontend │                                 │  (Port 8001) │
 │          │ ◄────── JSON response ───────── │              │
 └────┬─────┘                                 └──────┬───────┘
      │                                              │
      │  REST /api/*                                 │ Python import
      ↓                                              ↓
 ┌──────────┐                                 ┌──────────────┐
 │  Forge   │ ◄─── persist advisory ───────── │  Advisory    │
 │ Backend  │                                 │  Engine      │
 │ (Port    │                                 │              │
 │  5000)   │                                 └──────────────┘
 └────┬─────┘
      │  HTTP
      ↓
 ┌──────────────┐
 │  Insight     │
 │  Market      │
 │  (Port 8000) │
 └──────────────┘
```

---

## 🚀 One-Command Launch

### Windows
```bash
start_all.bat
```

### Manual (Individual Services)
```bash
# Terminal 1 — Oracle AI Engine
cd "AI Engines"
uvicorn oracle_api:app --port 8001

# Terminal 2 — Forge Backend
npm run dev

# Terminal 3 — Insight Market
cd insight_module_final
uvicorn app.main:app --port 8000

# Terminal 4 — Flutter App
cd frontend/flutter_application_1_ui
flutter run -d chrome
```

---

## 📂 Key Files at Repository Root

| File / Directory | Purpose |
| :--- | :--- |
| `main.py` | Python orchestrator entry — service validation & health checks |
| `start_all.bat` | One-click Windows launcher for all services |
| `.env` | Centralized environment config (ports, secrets, DB URLs) |
| `shared/` | Cross-module utilities (Forge HTTP client, weather API) |
| `db/` | Database schema definitions and seed data |
| `tests/` | Integration tests spanning multiple modules |
| `requirements.txt` | Python dependencies for Oracle AI + Advisory + Insight |
| `package.json` | Node.js dependencies for Forge Backend |
| `web_demo.html` | Zero-setup browser demo connected to live Oracle AI |

---

## 💡 Why Nexus Matters

Without Nexus, you have five isolated tools. **With Nexus**, you have:

> ✅ A farmer scans a leaf → Oracle AI diagnoses it → Advisory Engine generates treatment plans → Forge persists the record → Insight Market links harvest to the best mandi price → Flutter displays it all — **in one seamless flow, in two languages, from a single app.**

Nexus is the difference between a **collection of scripts** and a **production-grade agri-tech platform**.
