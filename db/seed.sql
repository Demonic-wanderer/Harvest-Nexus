-- Demo seed data for Harvest Nexus (Default password: password123)

INSERT INTO users (name, email, phone, password_hash, role)
VALUES
('Ramesh Patel', 'ramesh@example.com', '9998887771', '$2a$10$nK43b59V2N9yC7.h2.f8KOFp5oZq8WwJ/4B9x9CqHn1XoJmBfB0eG', 'farmer'),
('Green Traders Co.', 'buyer@example.com', '9998887772', '$2a$10$nK43b59V2N9yC7.h2.f8KOFp5oZq8WwJ/4B9x9CqHn1XoJmBfB0eG', 'buyer'),
('Admin User', 'admin@example.com', '9998887773', '$2a$10$nK43b59V2N9yC7.h2.f8KOFp5oZq8WwJ/4B9x9CqHn1XoJmBfB0eG', 'admin')
ON CONFLICT (email) DO UPDATE
SET name = EXCLUDED.name, phone = EXCLUDED.phone, password_hash = EXCLUDED.password_hash, role = EXCLUDED.role;

-- The farmer account used in the walkthrough must have a connected farm, crop,
-- and a visible advisory before any live scan is performed.
WITH ramesh AS (
  SELECT id FROM users WHERE email = 'ramesh@example.com'
), inserted_farm AS (
  INSERT INTO farm_profiles (farmer_id, farm_name, location, latitude, longitude, land_size_acres, soil_type)
  SELECT id, 'Ramesh Tomato Farm', 'Madhya Pradesh', 22.7196, 75.8577, 2.50, 'Loamy'
  FROM ramesh
  WHERE NOT EXISTS (SELECT 1 FROM farm_profiles fp WHERE fp.farmer_id = ramesh.id)
  RETURNING id
)
INSERT INTO crop_profiles (farm_id, crop_name, sowing_date, expected_harvest_date, status)
SELECT COALESCE((SELECT id FROM inserted_farm), (SELECT fp.id FROM farm_profiles fp JOIN ramesh ON fp.farmer_id = ramesh.id ORDER BY fp.created_at LIMIT 1)),
       'Tomato', CURRENT_DATE - 45, CURRENT_DATE + 45, 'active'
WHERE NOT EXISTS (
  SELECT 1 FROM crop_profiles cp
  JOIN farm_profiles fp ON fp.id = cp.farm_id
  JOIN ramesh ON fp.farmer_id = ramesh.id
  WHERE cp.crop_name = 'Tomato'
);

WITH ramesh_farm AS (
  SELECT fp.id AS farm_id, cp.id AS crop_id
  FROM farm_profiles fp
  JOIN users u ON u.id = fp.farmer_id
  JOIN crop_profiles cp ON cp.farm_id = fp.id
  WHERE u.email = 'ramesh@example.com' AND cp.crop_name = 'Tomato'
  ORDER BY cp.created_at LIMIT 1
)
INSERT INTO advisory_history (farm_id, crop_id, irrigation_advice, fertilizer_advice, treatment_plan, priority_level, farm_health_score)
SELECT farm_id, crop_id,
       'Check soil moisture every morning; irrigate only when it falls below 30%.',
       'Apply a balanced NPK dose after a soil test.',
       'Inspect tomato leaves weekly and upload a leaf scan if spots appear.',
       'MEDIUM', 64
FROM ramesh_farm
WHERE NOT EXISTS (SELECT 1 FROM advisory_history ah WHERE ah.farm_id = ramesh_farm.farm_id);

INSERT INTO market_data (crop_name, region, current_price, trend, demand_indicator)
SELECT 'Tomato', 'Madhya Pradesh', 2300.00, 'Rising', 'High'
WHERE NOT EXISTS (SELECT 1 FROM market_data WHERE crop_name = 'Tomato' AND region = 'Madhya Pradesh')
UNION ALL
SELECT 'Wheat', 'Madhya Pradesh', 2100.00, 'Stable', 'Medium'
WHERE NOT EXISTS (SELECT 1 FROM market_data WHERE crop_name = 'Wheat' AND region = 'Madhya Pradesh');

INSERT INTO buyers (name, contact_phone, contact_email, location, crop_interest, latitude, longitude)
SELECT 'Fresh Mandi Traders', '9876543210', 'freshmandi@example.com', 'Indore', 'Tomato', 22.7196, 75.8577
WHERE NOT EXISTS (SELECT 1 FROM buyers WHERE contact_email = 'freshmandi@example.com')
UNION ALL
SELECT 'AgriBulk Buyers', '9876543211', 'agribulk@example.com', 'Bhopal', 'Wheat', 23.2599, 77.4126
WHERE NOT EXISTS (SELECT 1 FROM buyers WHERE contact_email = 'agribulk@example.com');

INSERT INTO transporters (name, contact_phone, base_location, vehicle_type, capacity_quintals, rate_per_km_quintal)
SELECT 'Malwa Agri Transport', '9826011111', 'Indore', 'mini_truck', 80, 1.8
WHERE NOT EXISTS (SELECT 1 FROM transporters WHERE name = 'Malwa Agri Transport')
UNION ALL
SELECT 'Narmada Freight Co.', '9826022222', 'Bhopal', 'truck', 200, 1.4
WHERE NOT EXISTS (SELECT 1 FROM transporters WHERE name = 'Narmada Freight Co.');

INSERT INTO mandis (name, location, latitude, longitude, contact_info)
SELECT 'Indore Mandi', 'Madhya Pradesh', 22.7196, 75.8577, '0731-245-8171'
WHERE NOT EXISTS (SELECT 1 FROM mandis WHERE name = 'Indore Mandi')
UNION ALL
SELECT 'Bhopal Krishi Mandi', 'Madhya Pradesh', 23.2599, 77.4126, '0755-255-0940'
WHERE NOT EXISTS (SELECT 1 FROM mandis WHERE name = 'Bhopal Krishi Mandi');

-- A complete linked sale exercises transactions, buyers, crops, logistics,
-- transporters, and durable telemetry in the live dashboard.
WITH demo_ids AS (
  SELECT u.id AS farmer_id, cp.id AS crop_id, b.id AS buyer_id
  FROM users u
  JOIN farm_profiles fp ON fp.farmer_id = u.id
  JOIN crop_profiles cp ON cp.farm_id = fp.id AND cp.crop_name = 'Tomato'
  JOIN buyers b ON b.contact_email = 'freshmandi@example.com'
  WHERE u.email = 'ramesh@example.com'
  LIMIT 1
), inserted_transaction AS (
  INSERT INTO transactions (farmer_id, buyer_id, crop_id, quantity_quintals, price_per_quintal, status)
  SELECT farmer_id, buyer_id, crop_id, 12.00, 2300.00, 'confirmed'
  FROM demo_ids
  WHERE NOT EXISTS (
    SELECT 1 FROM transactions t WHERE t.farmer_id = demo_ids.farmer_id AND t.buyer_id = demo_ids.buyer_id AND t.crop_id = demo_ids.crop_id
  )
  RETURNING id
), demo_transaction AS (
  SELECT id FROM inserted_transaction
  UNION ALL
  SELECT t.id FROM transactions t JOIN demo_ids d ON t.farmer_id = d.farmer_id AND t.buyer_id = d.buyer_id AND t.crop_id = d.crop_id
  LIMIT 1
)
INSERT INTO logistics (transaction_id, transporter_name, contact_phone, pickup_location, drop_location, status)
SELECT id, 'Malwa Agri Transport', '9826011111', 'Ramesh Tomato Farm', 'Indore Mandi', 'arranged'
FROM demo_transaction
WHERE NOT EXISTS (SELECT 1 FROM logistics l WHERE l.transaction_id = demo_transaction.id);

INSERT INTO telemetry (farm_id, soil_moisture, soil_temperature, soil_ph, nitrogen, phosphorus, potassium, ambient_temp, humidity, rain_probability, anomalies)
SELECT fp.id, 32.00, 25.00, 6.50, 35.00, 28.00, 30.00, 28.00, 65.00, 10.00, '[]'::jsonb
FROM farm_profiles fp
JOIN users u ON u.id = fp.farmer_id
WHERE u.email = 'ramesh@example.com'
  AND NOT EXISTS (SELECT 1 FROM telemetry t WHERE t.farm_id = fp.id);
