# 📊 Module 5 — Insight Market Engine
### *Agricultural Market Intelligence, Mandi Prices & Demand Analytics*

---

<p align="center">
  <img src="https://img.shields.io/badge/Framework-FastAPI-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite" />
  <img src="https://img.shields.io/badge/Data-Mandi%20Prices-43A047?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Analytics-Trends%20%26%20Forecasts-FF9800?style=for-the-badge" />
</p>

---

## 📋 What It Does

The **Insight Market Engine** is the market intelligence backbone of Harvest Nexus. It aggregates, stores, and serves **real-time agricultural commodity prices** from mandis (wholesale markets) across India, providing farmers with:

- 📈 **Live price tracking** for crops at nearby mandis
- 📉 **Historical trend analysis** to identify optimal selling windows
- 🔮 **Price forecasting** to help plan harvest timing
- 🤝 **Buyer demand matching** — connect surplus crops to active buyers
- 🚚 **Logistics cost estimation** for farm-to-mandi transport

It answers the farmer's post-harvest question:
> *"Where should I sell my tomatoes today for the best price, and is the market going up or down?"*

---

## 🏗️ Architecture

```
  Mandi Data Sources (Gov APIs, Scraped Data)
              ↓
  ┌──────────────────────────────────┐
  │      INSIGHT MARKET ENGINE        │
  │        (FastAPI – Port 8000)      │
  ├──────────────────────────────────┤
  │                                  │
  │   📥 Data Ingestion Layer        │  ← Fetches/imports mandi price feeds
  │   💾 SQLite Persistence          │  ← insight_module.db (local store)
  │   📊 Analytics Services          │  ← Trend calculation & forecasting
  │   🔍 Query API                   │  ← Search by crop, region, date
  │                                  │
  └──────────┬───────────────────────┘
             ↓
  ┌──────────────────────────────────┐
  │   Consumers:                      │
  │   • Flutter App (Market Screen)   │
  │   • Advisory Engine (Rule 7 & 8)  │
  │   • Forge Backend (Market Routes) │
  └──────────────────────────────────┘
```

---

## 📦 Data Model

| Entity | Key Fields | Purpose |
| :--- | :--- | :--- |
| **Commodity** | name, category, season | Crop master data |
| **Mandi** | name, state, district, location | Market directory |
| **PriceRecord** | commodity, mandi, date, min_price, max_price, modal_price | Daily price log |
| **Buyer** | name, contact, crops_needed, location | Demand-side profiles |
| **Forecast** | commodity, mandi, forecast_date, predicted_price, confidence | ML price projection |

---

## 🔗 How the Advisory Engine Uses It

The Insight Market Engine feeds data directly into the Advisory Engine's **Rule 7 (Harvest-to-Mandi Sync)** and **Rule 8 (Market Price Signal)**:

```
Insight Market Engine
   ├── current_price: ₹2,450/quintal
   ├── trend: "Rising"
   ├── forecast_price: ₹2,680/quintal
   └── region: "Azadpur Mandi, Delhi"
          ↓
Advisory Engine Rule 7:
   "MARKET PEAK OPPORTUNITY: Azadpur Mandi Tomato price is rising
    (₹2,450/q). Harvest in 5 days aligns with high demand.
    Book transport early to lock in peak margins."
```

---

## 📂 Key Files

```
insight_module_final/
├── app/
│   ├── main.py           # FastAPI application entry point
│   ├── api/              # REST endpoint definitions
│   ├── core/             # Configuration and startup logic
│   ├── data/             # Seed data and import scripts
│   ├── db/               # Database connection and session management
│   ├── models/           # SQLAlchemy ORM models
│   └── services/         # Business logic (price analytics, forecasting)
├── insight_module.db      # SQLite database file
└── requirements.txt       # Python dependencies
```

---

## 🚀 Running

```bash
cd insight_module_final
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Health Check:** `GET http://127.0.0.1:8000/health`
