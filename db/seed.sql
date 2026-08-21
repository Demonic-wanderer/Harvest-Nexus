-- Demo seed data for Harvest Nexus (Default password: password123)

INSERT INTO users (name, email, phone, password_hash, role)
VALUES
('Ramesh Patel', 'ramesh@example.com', '9998887771', '$2a$10$nK43b59V2N9yC7.h2.f8KOFp5oZq8WwJ/4B9x9CqHn1XoJmBfB0eG', 'farmer'),
('Green Traders Co.', 'buyer@example.com', '9998887772', '$2a$10$nK43b59V2N9yC7.h2.f8KOFp5oZq8WwJ/4B9x9CqHn1XoJmBfB0eG', 'buyer'),
('Admin User', 'admin@example.com', '9998887773', '$2a$10$nK43b59V2N9yC7.h2.f8KOFp5oZq8WwJ/4B9x9CqHn1XoJmBfB0eG', 'admin')
RETURNING id;

INSERT INTO market_data (crop_name, region, current_price, trend, demand_indicator)
VALUES
('Tomato', 'Madhya Pradesh', 2300.00, 'Rising', 'High'),
('Wheat', 'Madhya Pradesh', 2100.00, 'Stable', 'Medium');

INSERT INTO buyers (name, contact_phone, contact_email, location, crop_interest)
VALUES
('Fresh Mandi Traders', '9876543210', 'freshmandi@example.com', 'Indore', 'Tomato'),
('AgriBulk Buyers', '9876543211', 'agribulk@example.com', 'Bhopal', 'Wheat');
