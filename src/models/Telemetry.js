const db = require('../config/db');

const Telemetry = {
  async create(reading) {
    const result = await db.query(
      `INSERT INTO telemetry
        (farm_id, soil_moisture, soil_temperature, soil_ph, nitrogen, phosphorus, potassium,
         ambient_temp, humidity, rain_probability, anomalies)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11::jsonb)
       RETURNING *`,
      [
        reading.farm_id, reading.soil_moisture, reading.soil_temperature, reading.soil_ph,
        reading.nitrogen, reading.phosphorus, reading.potassium, reading.ambient_temp,
        reading.humidity, reading.rain_probability, JSON.stringify(reading.anomalies || []),
      ]
    );
    return result.rows[0];
  },

  async findLatestByFarmId(farm_id) {
    const result = await db.query(
      `SELECT * FROM telemetry WHERE farm_id = $1 ORDER BY recorded_at DESC LIMIT 1`,
      [farm_id]
    );
    return result.rows[0];
  },
};

module.exports = Telemetry;
