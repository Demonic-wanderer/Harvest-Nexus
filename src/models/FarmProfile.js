const db = require('../config/db');

const FarmProfile = {
  async create({ farmer_id, farm_name, location, latitude, longitude, land_size_acres, soil_type }) {
    const result = await db.query(
      `INSERT INTO farm_profiles (farmer_id, farm_name, location, latitude, longitude, land_size_acres, soil_type)
       VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING *`,
      [farmer_id, farm_name, location, latitude, longitude, land_size_acres, soil_type]
    );
    return result.rows[0];
  },

  async findByFarmerId(farmer_id) {
    const result = await db.query(`SELECT * FROM farm_profiles WHERE farmer_id = $1`, [farmer_id]);
    return result.rows;
  },

  async findById(id) {
    const result = await db.query(`SELECT * FROM farm_profiles WHERE id = $1`, [id]);
    return result.rows[0];
  },

  async update(id, fields) {
    const keys = Object.keys(fields);
    const values = Object.values(fields);
    const setClause = keys.map((k, i) => `${k} = $${i + 1}`).join(', ');
    const result = await db.query(
      `UPDATE farm_profiles SET ${setClause} WHERE id = $${keys.length + 1} RETURNING *`,
      [...values, id]
    );
    return result.rows[0];
  },
};

module.exports = FarmProfile;
