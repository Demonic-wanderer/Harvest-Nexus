# Harvest Nexus — Cloud Backend (SQL)
**Module:** Forge | **Owner:** Moin

Central data layer for the Harvest Nexus platform. Every other module (Oracle/AI, Pulse/Flutter app, Insight/Market, Akasha/Advisory) reads from and writes to this backend.

## Tech Stack
- Node.js + Express
- PostgreSQL (Supabase / Neon recommended)
- JWT auth with role-based access control
- bcrypt for password hashing

## Setup

```bash
npm install
cp .env.example .env   # fill in your DATABASE_URL and JWT_SECRET
npm run migrate        # creates all tables (db/schema.sql)
npm run seed           # optional demo data (db/seed.sql)
npm run dev             # starts server with nodemon
```

## Folder Structure

```
src/
  config/       DB connection + env vars
  models/       Raw SQL query layer per table
  routes/       Express route definitions
  controllers/  Business logic per route
  middleware/   Auth, role-checks, error handling
  utils/        Logger, response formatter
db/
  schema.sql    Table creation
  seed.sql      Demo data
server.js        Entry point
```

## Core API Endpoints

| Endpoint | Method | Used By |
|---|---|---|
| `/api/auth/register`, `/login` | POST | Everyone |
| `/api/farmer/:id` | GET | Pulse (Flutter app) |
| `/api/farmer/farm` | POST | Pulse |
| `/api/crop` | POST | Pulse |
| `/api/disease/predict-result` | POST | Oracle (AI engine) |
| `/api/advisory` | POST | Akasha (Advisory engine) |
| `/api/market` | POST | Insight (Market/Logistics) |
| `/api/buyer` | GET/POST | Insight, Pulse |
| `/api/transaction` | POST | Pulse |

## Focus Order (4-day MVP)
1. Finalize schema (`db/schema.sql`) ✅
2. Set up cloud SQL instance (Supabase/Neon)
3. Core CRUD APIs ✅
4. Auth + role middleware ✅
5. Integrate with AI + Advisory + Market modules
6. Optimize (indexing — already added in schema)
