const db = require('../config/db');

const Mandi = {
  async create({ name, location, latitude, longitude, contact_info }) {
    const result = await db.query(
      `INSERT INTO mandis (name, location, latitude, longitude, contact_info)
       VALUES ($1, $2, $3, $4, $5) RETURNING *`,
      [name, location, latitude, longitude, contact_info]
    );
    return result.rows[0];
  },

  async findAll() {
    const result = await db.query(`SELECT * FROM mandis ORDER BY name ASC`);
    return result.rows;
  },

  async findById(id) {
    const result = await db.query(`SELECT * FROM mandis WHERE id = $1`, [id]);
    return result.rows[0];
  },

  async delete(id) {
    const result = await db.query(`DELETE FROM mandis WHERE id = $1 RETURNING *`, [id]);
    return result.rows[0];
  }
};

module.exports = Mandi;
