const db = require('../config/db');

const MarketData = {
  async create({ crop_name, region, current_price, trend, demand_indicator }) {
    const result = await db.query(
      `INSERT INTO market_data (crop_name, region, current_price, trend, demand_indicator)
       VALUES ($1,$2,$3,$4,$5) RETURNING *`,
      [crop_name, region, current_price, trend, demand_indicator]
    );
    return result.rows[0];
  },

  async findByCropAndRegion(crop_name, region) {
    const result = await db.query(
      `SELECT * FROM market_data WHERE crop_name = $1 AND region = $2 ORDER BY recorded_at DESC LIMIT 1`,
      [crop_name, region]
    );
    return result.rows[0];
  },

  async findAll() {
    const result = await db.query(`SELECT * FROM market_data ORDER BY recorded_at DESC`);
    return result.rows;
  },
};

module.exports = MarketData;
