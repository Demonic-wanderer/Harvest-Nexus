# Insight Module — Bhumika's role (Market Intelligence & Buyer Linkage Engine)

## Structure
```
app/
├── main.py                     ✅ WORKING — CLI tool, debugged and tested
├── core/
│   └── config.py                  settings for the API layer (not used by CLI yet)
├── db/
│   └── database.py              ✅ WORKING — sqlite, used by main.py
├── models/
│   ├── db_models.py                SQLAlchemy models for future API layer
│   └── schemas.py                  Pydantic request/response shapes
├── services/
│   ├── market_service.py        ✅ WORKING — used by main.py (sqlite)
│   ├── buyer_service.py            scaffold, not yet wired to CLI
│   └── logistics_service.py        scaffold, not yet wired to CLI
└── api/
    ├── market.py                   scaffold FastAPI endpoint
    ├── buyers.py                   scaffold FastAPI endpoint
    └── logistics.py                scaffold FastAPI endpoint
```

## What's actually running right now
Only three files are wired together and tested:
- `app/main.py` — the terminal menu (add price / view prices / exit)
- `app/db/database.py` — sqlite storage (`insight_module.db`)
- `app/services/market_service.py` — the save/list glue between them

Run it:
```
cd insight_module
python app/main.py
```

## What's scaffold (not connected yet)
`core/`, `models/`, `services/buyer_service.py`, `services/logistics_service.py`,
and everything in `api/` are the original design for the fuller
Market Intelligence + Buyer Linkage Engine (FastAPI + SQLAlchemy), matching the
Harvest Nexus architecture doc. They aren't hooked into the CLI tool yet —
the CLI talks to sqlite directly, the API layer expects a SQLAlchemy session.

When you're ready to combine them (e.g. serve `/market/snapshot` over HTTP
using the same data your CLI collects), the two things to reconcile are:
1. Point `DATABASE_URL` in `core/config.py` at the same sqlite file, or
   migrate the CLI's `market_prices` table into that shared DB.
2. Update `app/api/market.py` to read from your sqlite table shape
   (`market`, `commodity`, `price`, `date`) instead of the SQLAlchemy
   `MarketPrice` model's shape (`crop_type`, `region`, `price_per_quintal`).

Until then, keep using `app/main.py` for the working demo.
