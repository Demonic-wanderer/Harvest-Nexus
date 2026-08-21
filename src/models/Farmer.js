const db = require('../config/db');

const Farmer = {
  async create({ name, email, phone, password_hash, role }) {
    const result = await db.query(
      `INSERT INTO users (name, email, phone, password_hash, role)
       VALUES ($1, $2, $3, $4, $5) RETURNING id, name, email, phone, role, created_at`,
      [name, email, phone, password_hash, role]
    );
    return result.rows[0];
  },

  async findByEmail(email) {
    const result = await db.query(`SELECT * FROM users WHERE email = $1`, [email]);
    return result.rows[0];
  },

  async findByPhone(phone) {
    const result = await db.query(`SELECT * FROM users WHERE phone = $1`, [phone]);
    return result.rows[0];
  },

  async findById(id) {
    const result = await db.query(
      `SELECT id, name, email, phone, role, created_at FROM users WHERE id = $1`,
      [id]
    );
    return result.rows[0];
  },

  async findAll(role = null) {
    if (role) {
      const result = await db.query(`SELECT id, name, email, phone, role FROM users WHERE role = $1`, [role]);
      return result.rows;
    }
    const result = await db.query(`SELECT id, name, email, phone, role FROM users`);
    return result.rows;
  },
};

module.exports = Farmer;
