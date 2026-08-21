const db = require('../config/db');

const Buyer = {
  async create({ name, contact_phone, contact_email, location, crop_interest }) {
    const result = await db.query(
      `INSERT INTO buyers (name, contact_phone, contact_email, location, crop_interest)
       VALUES ($1,$2,$3,$4,$5) RETURNING *`,
      [name, contact_phone, contact_email, location, crop_interest]
    );
    return result.rows[0];
  },

  async findAll() {
    const result = await db.query(`SELECT * FROM buyers ORDER BY created_at DESC`);
    return result.rows;
  },

  async findByCropInterest(crop_name) {
    const result = await db.query(`SELECT * FROM buyers WHERE crop_interest = $1`, [crop_name]);
    return result.rows;
  },

  async findById(id) {
    const result = await db.query(`SELECT * FROM buyers WHERE id = $1`, [id]);
    return result.rows[0];
  },
};

module.exports = Buyer;
