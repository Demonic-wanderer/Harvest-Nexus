const db = require('../config/db');

const Buyer = {
  async create({ name, contact_phone, contact_email, location, crop_interest, latitude, longitude }) {
    const result = await db.query(
      `INSERT INTO buyers (name, contact_phone, contact_email, location, crop_interest, latitude, longitude)
       VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING *`,
      [name, contact_phone, contact_email, location, crop_interest, latitude, longitude]
    );
    return result.rows[0];
  },

  async findAll(limit = 20, offset = 0) {
    const result = await db.query(
      `SELECT * FROM buyers ORDER BY created_at DESC LIMIT $1 OFFSET $2`,
      [limit, offset]
    );
    return result.rows;
  },

  async findByCropInterest(crop_name) {
    const result = await db.query(`SELECT * FROM buyers WHERE crop_interest = $1`, [crop_name]);
    return result.rows;
  },

  async search({ crop_name, location, limit = 20 }) {
    const result = await db.query(
      `SELECT * FROM buyers
       WHERE crop_interest ILIKE $1
         AND ($2::text IS NULL OR location ILIKE $2)
       ORDER BY created_at DESC
       LIMIT $3`,
      [`%${crop_name}%`, location ? `%${location}%` : null, limit]
    );
    return result.rows;
  },

  async findById(id) {
    const result = await db.query(`SELECT * FROM buyers WHERE id = $1`, [id]);
    return result.rows[0];
  },
};

module.exports = Buyer;
