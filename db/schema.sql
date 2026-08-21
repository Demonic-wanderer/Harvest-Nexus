-- ==========================================================
-- Harvest Nexus - Cloud Backend (SQL) Schema
-- Owner: Moin
-- ==========================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto"; -- for gen_random_uuid()

-- USERS / FARMERS
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('farmer','buyer','admin','advisor')),
    created_at TIMESTAMP DEFAULT NOW()
);

-- FARM PROFILES
CREATE TABLE IF NOT EXISTS farm_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    farm_name VARCHAR(150),
    location VARCHAR(150),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    land_size_acres DECIMAL(6,2),
    soil_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- CROP PROFILES
CREATE TABLE IF NOT EXISTS crop_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farm_id UUID REFERENCES farm_profiles(id) ON DELETE CASCADE,
    crop_name VARCHAR(100) NOT NULL,
    sowing_date DATE,
    expected_harvest_date DATE,
    status VARCHAR(30) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

-- DISEASE HISTORY (from Oracle - Arpan's AI engine)
CREATE TABLE IF NOT EXISTS disease_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    crop_id UUID REFERENCES crop_profiles(id) ON DELETE CASCADE,
    image_url TEXT,
    disease_name VARCHAR(150),
    confidence DECIMAL(5,2),
    severity VARCHAR(20),
    detected_at TIMESTAMP DEFAULT NOW()
);

-- ADVISORY HISTORY (from Akasha - Ojas's advisory engine)
CREATE TABLE IF NOT EXISTS advisory_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farm_id UUID REFERENCES farm_profiles(id) ON DELETE CASCADE,
    crop_id UUID REFERENCES crop_profiles(id) ON DELETE SET NULL,
    disease_id UUID REFERENCES disease_history(id) ON DELETE SET NULL,
    irrigation_advice TEXT,
    fertilizer_advice TEXT,
    treatment_plan TEXT,
    priority_level VARCHAR(20), -- HIGH / MEDIUM / OPPORTUNITY
    farm_health_score INT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- MARKET DATA (from Insight - Bhumika's module)
CREATE TABLE IF NOT EXISTS market_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    crop_name VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    current_price DECIMAL(10,2),
    trend VARCHAR(20), -- Rising / Falling / Stable
    demand_indicator VARCHAR(20),
    forecast_price DECIMAL(10,2),
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- BUYERS
CREATE TABLE IF NOT EXISTS buyers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    contact_phone VARCHAR(20),
    contact_email VARCHAR(150),
    location VARCHAR(150),
    crop_interest VARCHAR(100),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    created_at TIMESTAMP DEFAULT NOW()
);

-- MANDIS (markets)
CREATE TABLE IF NOT EXISTS mandis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    location VARCHAR(150),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    contact_info VARCHAR(150)
);

-- TRANSACTIONS
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id UUID REFERENCES users(id) ON DELETE SET NULL,
    buyer_id UUID REFERENCES buyers(id) ON DELETE SET NULL,
    crop_id UUID REFERENCES crop_profiles(id) ON DELETE SET NULL,
    quantity_quintals DECIMAL(10,2),
    price_per_quintal DECIMAL(10,2),
    status VARCHAR(30) DEFAULT 'pending', -- pending / confirmed / completed
    created_at TIMESTAMP DEFAULT NOW()
);

-- TRANSPORTERS
CREATE TABLE IF NOT EXISTS transporters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    contact_phone VARCHAR(20),
    base_location VARCHAR(150),
    vehicle_type VARCHAR(50),
    capacity_quintals DECIMAL(10,2),
    rate_per_km_quintal DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- LOGISTICS
CREATE TABLE IF NOT EXISTS logistics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id UUID REFERENCES transactions(id) ON DELETE CASCADE,
    transporter_name VARCHAR(150),
    contact_phone VARCHAR(20),
    pickup_location VARCHAR(150),
    drop_location VARCHAR(150),
    status VARCHAR(30) DEFAULT 'not_arranged',
    created_at TIMESTAMP DEFAULT NOW()
);

-- TELEMETRY: durable sensor/rover readings used by the advisory and dashboard.
CREATE TABLE IF NOT EXISTS telemetry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farm_id UUID NOT NULL REFERENCES farm_profiles(id) ON DELETE CASCADE,
    soil_moisture DECIMAL(5,2),
    soil_temperature DECIMAL(5,2),
    soil_ph DECIMAL(4,2),
    nitrogen DECIMAL(7,2),
    phosphorus DECIMAL(7,2),
    potassium DECIMAL(7,2),
    ambient_temp DECIMAL(5,2),
    humidity DECIMAL(5,2),
    rain_probability DECIMAL(5,2),
    anomalies JSONB NOT NULL DEFAULT '[]'::jsonb,
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_farm_profiles_farmer ON farm_profiles(farmer_id);
CREATE INDEX IF NOT EXISTS idx_crop_profiles_farm ON crop_profiles(farm_id);
CREATE INDEX IF NOT EXISTS idx_disease_history_crop ON disease_history(crop_id);
CREATE INDEX IF NOT EXISTS idx_advisory_history_farm ON advisory_history(farm_id);
CREATE INDEX IF NOT EXISTS idx_market_data_crop_region ON market_data(crop_name, region);
CREATE INDEX IF NOT EXISTS idx_transactions_farmer ON transactions(farmer_id);
CREATE INDEX IF NOT EXISTS idx_telemetry_farm_recorded ON telemetry(farm_id, recorded_at DESC);

ALTER TABLE buyers ADD COLUMN IF NOT EXISTS latitude DECIMAL(9,6);
ALTER TABLE buyers ADD COLUMN IF NOT EXISTS longitude DECIMAL(9,6);
ALTER TABLE market_data ADD COLUMN IF NOT EXISTS forecast_price DECIMAL(10,2);
