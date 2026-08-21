const db = require('../config/db');

const CropProfile = {
  async create({ farm_id, crop_name, sowing_date, expected_harvest_date }) {
    const result = await db.query(
      `INSERT INTO crop_profiles (farm_id, crop_name, sowing_date, expected_harvest_date)
       VALUES ($1,$2,$3,$4) RETURNING *`,
      [farm_id, crop_name, sowing_date, expected_harvest_date]
    );
    return result.rows[0];
  },

  async findByFarmId(farm_id) {
    const result = await db.query(`SELECT * FROM crop_profiles WHERE farm_id = $1`, [farm_id]);
    return result.rows;
  },

  async findById(id) {
    const result = await db.query(`SELECT * FROM crop_profiles WHERE id = $1`, [id]);
    return result.rows[0];
  },
};

module.exports = CropProfile;
