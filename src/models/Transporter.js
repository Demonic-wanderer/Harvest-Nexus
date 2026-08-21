const db = require('../config/db');

const Transporter = {
  async create({ name, contact_phone, base_location, vehicle_type, capacity_quintals, rate_per_km_quintal }) {
    const result = await db.query(
      `INSERT INTO transporters
        (name, contact_phone, base_location, vehicle_type, capacity_quintals, rate_per_km_quintal)
       VALUES ($1,$2,$3,$4,$5,$6) RETURNING *`,
      [name, contact_phone, base_location, vehicle_type, capacity_quintals, rate_per_km_quintal]
    );
    return result.rows[0];
  },

  async findAll() {
    const result = await db.query(`SELECT * FROM transporters ORDER BY name ASC`);
    return result.rows;
  },
};

module.exports = Transporter;
