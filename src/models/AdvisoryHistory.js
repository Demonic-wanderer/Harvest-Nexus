const db = require('../config/db');

const AdvisoryHistory = {
  async create({
    farm_id,
    crop_id,
    disease_id,
    irrigation_advice,
    fertilizer_advice,
    treatment_plan,
    priority_level,
    farm_health_score,
  }) {
    const result = await db.query(
      `INSERT INTO advisory_history
        (farm_id, crop_id, disease_id, irrigation_advice, fertilizer_advice, treatment_plan, priority_level, farm_health_score)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING *`,
      [farm_id, crop_id, disease_id, irrigation_advice, fertilizer_advice, treatment_plan, priority_level, farm_health_score]
    );
    return result.rows[0];
  },

  async findByFarmId(farm_id) {
    const result = await db.query(
      `SELECT * FROM advisory_history WHERE farm_id = $1 ORDER BY created_at DESC`,
      [farm_id]
    );
    return result.rows;
  },

  async findLatestByFarmId(farm_id) {
    const result = await db.query(
      `SELECT * FROM advisory_history WHERE farm_id = $1 ORDER BY created_at DESC LIMIT 1`,
      [farm_id]
    );
    return result.rows[0];
  },
};

module.exports = AdvisoryHistory;
