# ⚒️ Module 3 — Forge Backend
### *Node.js REST API Gateway & Data Persistence Layer*

---

<p align="center">
  <img src="https://img.shields.io/badge/Runtime-Node.js-339933?style=for-the-badge&logo=nodedotjs" />
  <img src="https://img.shields.io/badge/Framework-Express-000000?style=for-the-badge&logo=express" />
  <img src="https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql" />
  <img src="https://img.shields.io/badge/Auth-JWT-FB015B?style=for-the-badge" />
</p>

---

## 📋 What It Does

**Forge** is the central backend REST API that serves as the **data backbone** of Harvest Nexus. It handles user authentication, farm/crop registration, disease record persistence, advisory storage, market transactions, buyer management, and logistics coordination.

It answers the system-level question:
> *"Where do all farms, crops, scan results, advisories, transactions, and logistics records live and get managed?"*

---

## 🏗️ Architecture

```
  Flutter App / Web Demo
         ↓ HTTP
  ┌──────────────────────────────────┐
  │         EXPRESS.JS SERVER         │
  │          (Port 5000)              │
  ├──────────────────────────────────┤
  │                                  │
  │   🔐 Auth Routes                │  ← Farmer registration & JWT login
  │   👨‍🌾 Farmer Routes             │  ← Profile CRUD
  │   🌱 Crop Routes                │  ← Crop registration per farm
  │   🦠 Disease Routes             │  ← Persist AI scan results
  │   📋 Advisory Routes            │  ← Store & retrieve action plans
  │   📡 Telemetry Routes           │  ← IoT sensor data ingestion
  │   🏪 Mandi Routes               │  ← Nearby mandi discovery
  │   📊 Market Routes              │  ← Price trends & forecasts
  │   🤝 Buyer Routes               │  ← Buyer profiles & matching
  │   🚚 Logistics Routes           │  ← Transport booking & tracking
  │   💰 Transaction Routes         │  ← Purchase orders & settlements
  │                                  │
  ├──────────────────────────────────┤
  │   Middleware: CORS, JWT Guard,   │
  │   Error Handler, Rate Limiter    │
  └──────────┬───────────────────────┘
             ↓
  ┌──────────────────────────────────┐
  │        PostgreSQL Database        │
  │   Tables: farmers, farms, crops, │
  │   diseases, advisories, mandis,  │
  │   buyers, logistics, telemetry,  │
  │   transactions                   │
  └──────────────────────────────────┘
```

---

## 🗂️ API Routes Overview

| Route File | Base Path | Purpose |
| :--- | :--- | :--- |
| `auth.routes.js` | `/api/auth` | Farmer signup, login, JWT token issuance |
| `farmer.routes.js` | `/api/farmers` | Farmer profile CRUD operations |
| `crop.routes.js` | `/api/crops` | Register and manage crops per farm |
| `disease.routes.js` | `/api/diseases` | Persist Oracle AI disease scan results |
| `advisory.routes.js` | `/api/advisories` | Store and retrieve advisory action plans |
| `telemetry.routes.js` | `/api/telemetry` | Ingest soil & weather sensor readings |
| `mandi.routes.js` | `/api/mandis` | Discover nearby agricultural markets |
| `market.routes.js` | `/api/market` | Live price data, trends, and forecasts |
| `buyer.routes.js` | `/api/buyers` | Buyer profiles and crop demand matching |
| `logistics.routes.js` | `/api/logistics` | Transport booking and shipment tracking |
| `transaction.routes.js` | `/api/transactions` | Purchase orders and payment settlements |

---

## 🔐 Security

| Feature | Implementation |
| :--- | :--- |
| **Authentication** | JWT-based token issuance on login |
| **Route Protection** | Middleware guard on all protected endpoints |
| **CORS** | Configured for Flutter app and web demo origins |
| **Input Validation** | Request body validation on all write endpoints |

---

## 📂 Key Files

```
src/
├── app.js                  # Express app setup, middleware, route mounting
├── config/                 # Database connection & environment config
├── controllers/            # Business logic per domain entity
├── middleware/              # JWT auth guard, error handler, CORS
├── models/                 # Database models / ORM definitions
├── routes/                 # 11 route files (listed above)
└── utils/                  # Shared helpers and response formatters
```

---

## 🚀 Running

```bash
npm install
npm run dev    # Starts Express on port 5000
```

**Health Check:** `GET http://127.0.0.1:5000/api/health`
