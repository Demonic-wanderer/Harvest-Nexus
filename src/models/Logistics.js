const db = require('../config/db');

const Logistics = {
  async create({ transaction_id, transporter_name, contact_phone, pickup_location, drop_location }) {
    const result = await db.query(
      `INSERT INTO logistics (transaction_id, transporter_name, contact_phone, pickup_location, drop_location)
       VALUES ($1,$2,$3,$4,$5) RETURNING *`,
      [transaction_id, transporter_name, contact_phone, pickup_location, drop_location]
    );
    return result.rows[0];
  },

  async findByTransactionId(transaction_id) {
    const result = await db.query(`SELECT * FROM logistics WHERE transaction_id = $1`, [transaction_id]);
    return result.rows[0];
  },

  async updateStatus(id, status) {
    const result = await db.query(
      `UPDATE logistics SET status = $1 WHERE id = $2 RETURNING *`,
      [status, id]
    );
    return result.rows[0];
  },
};

module.exports = Logistics;
