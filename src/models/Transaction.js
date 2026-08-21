const db = require('../config/db');

const Transaction = {
  async create({ farmer_id, buyer_id, crop_id, quantity_quintals, price_per_quintal, status }) {
    const result = await db.query(
      `INSERT INTO transactions (farmer_id, buyer_id, crop_id, quantity_quintals, price_per_quintal, status)
       VALUES ($1,$2,$3,$4,$5,$6) RETURNING *`,
      [farmer_id, buyer_id, crop_id, quantity_quintals, price_per_quintal, status || 'pending']
    );
    return result.rows[0];
  },

  async findByFarmerId(farmer_id) {
    const result = await db.query(
      `SELECT * FROM transactions WHERE farmer_id = $1 ORDER BY created_at DESC`,
      [farmer_id]
    );
    return result.rows;
  },

  async findByIdAndFarmerId(id, farmer_id) {
    const result = await db.query(
      `SELECT * FROM transactions WHERE id = $1 AND farmer_id = $2`,
      [id, farmer_id]
    );
    return result.rows[0];
  },

  async updateStatusOwned(id, farmer_id, status) {
    const result = await db.query(
      `UPDATE transactions SET status = $1 WHERE id = $2 AND farmer_id = $3 RETURNING *`,
      [status, id, farmer_id]
    );
    return result.rows[0];
  },
};

module.exports = Transaction;
