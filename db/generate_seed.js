const bcrypt = require('bcryptjs');
const fs = require('fs');
const path = require('path');

async function main() {
  const password = 'password123';
  const saltRounds = 10;
  const hash = await bcrypt.hash(password, saltRounds);

  const sqlContent = `-- Demo seed data for Harvest Nexus (Default password: ${password})

INSERT INTO users (name, email, phone, password_hash, role)
VALUES
('Ramesh Patel', 'ramesh@example.com', '9998887771', '${hash}', 'farmer'),
('Green Traders Co.', 'buyer@example.com', '9998887772', '${hash}', 'buyer'),
('Admin User', 'admin@example.com', '9998887773', '${hash}', 'admin')
RETURNING id;

INSERT INTO market_data (crop_name, region, current_price, trend, demand_indicator)
VALUES
('Tomato', 'Madhya Pradesh', 2300.00, 'Rising', 'High'),
('Wheat', 'Madhya Pradesh', 2100.00, 'Stable', 'Medium');

INSERT INTO buyers (name, contact_phone, contact_email, location, crop_interest)
VALUES
('Fresh Mandi Traders', '9876543210', 'freshmandi@example.com', 'Indore', 'Tomato'),
('AgriBulk Buyers', '9876543211', 'agribulk@example.com', 'Bhopal', 'Wheat');
`;

  fs.writeFileSync(path.join(__dirname, 'seed.sql'), sqlContent, 'utf8');
  console.log('✅ Generated seed.sql with valid bcrypt hashes for password:', password);
}

main().catch(console.error);
