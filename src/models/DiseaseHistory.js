const db = require('../config/db');

const DiseaseHistory = {
  async create({ crop_id, image_url, disease_name, confidence, severity }) {
    const result = await db.query(
      `INSERT INTO disease_history (crop_id, image_url, disease_name, confidence, severity)
       VALUES ($1,$2,$3,$4,$5) RETURNING *`,
      [crop_id, image_url, disease_name, confidence, severity]
    );
    return result.rows[0];
  },

  async findByCropId(crop_id) {
    const result = await db.query(
      `SELECT * FROM disease_history WHERE crop_id = $1 ORDER BY detected_at DESC`,
      [crop_id]
    );
    return result.rows;
  },

  async findLatestByCropId(crop_id) {
    const result = await db.query(
      `SELECT * FROM disease_history WHERE crop_id = $1 ORDER BY detected_at DESC LIMIT 1`,
      [crop_id]
    );
    return result.rows[0];
  },
};

module.exports = DiseaseHistory;
