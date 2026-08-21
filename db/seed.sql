-- Demo seed data for Harvest Nexus

INSERT INTO users (name, email, phone, password_hash, role)
VALUES
('Ramesh Patel', 'ramesh@example.com', '9998887771', '$2a$10$examplehashvalue', 'farmer'),
('Green Traders Co.', 'buyer@example.com', '9998887772', '$2a$10$examplehashvalue', 'buyer'),
('Admin User', 'admin@example.com', '9998887773', '$2a$10$examplehashvalue', 'admin')
RETURNING id;

INSERT INTO market_data (crop_name, region, current_price, trend, demand_indicator)
VALUES
('Tomato', 'Madhya Pradesh', 2300.00, 'Rising', 'High'),
('Wheat', 'Madhya Pradesh', 2100.00, 'Stable', 'Medium');

INSERT INTO buyers (name, contact_phone, contact_email, location, crop_interest)
VALUES
('Fresh Mandi Traders', '9876543210', 'freshmandi@example.com', 'Indore', 'Tomato'),
('AgriBulk Buyers', '9876543211', 'agribulk@example.com', 'Bhopal', 'Wheat');
