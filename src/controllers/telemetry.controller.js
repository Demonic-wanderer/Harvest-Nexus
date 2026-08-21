const { success, error } = require('../utils/responseFormatter');
const Telemetry = require('../models/Telemetry');
const FarmProfile = require('../models/FarmProfile');

async function submitTelemetry(req, res) {
  try {
    const {
      farm_id,
      soil_moisture,
      soil_temperature,
      soil_ph,
      nitrogen,
      phosphorus,
      potassium,
      ambient_temp,
      humidity,
      rain_probability,
    } = req.body;

    if (!farm_id) {
      return error(res, 'farm_id is required for telemetry ingestion', 400);
    }
    if (req.user && !(await FarmProfile.findByIdAndFarmerId(farm_id, req.user.id))) {
      return error(res, 'Farm not found', 404);
    }

    const moistureVal = parseFloat(soil_moisture ?? 30);
    const phVal = parseFloat(soil_ph ?? 6.5);
    const nVal = parseFloat(nitrogen ?? 35);
    const pVal = parseFloat(phosphorus ?? 25);
    const kVal = parseFloat(potassium ?? 25);

    // Compute live sensor anomalies
    const anomalies = [];
    if (moistureVal < 25) anomalies.push('CRITICAL_LOW_SOIL_MOISTURE');
    if (moistureVal > 80) anomalies.push('EXCESS_SOIL_WATERLOGGING');
    if (phVal < 5.5 || phVal > 7.8) anomalies.push('SOIL_PH_OUT_OF_RANGE');
    if (nVal < 30) anomalies.push('DEFICIENT_NITROGEN');

    const telemetryRecord = {
      farm_id,
      soil_moisture: moistureVal,
      soil_temperature: parseFloat(soil_temperature ?? 26),
      soil_ph: phVal,
      nitrogen: nVal,
      phosphorus: pVal,
      potassium: kVal,
      ambient_temp: parseFloat(ambient_temp ?? 28),
      humidity: parseFloat(humidity ?? 65),
      rain_probability: parseFloat(rain_probability ?? 10),
      anomalies,
    };
    const storedTelemetry = await Telemetry.create(telemetryRecord);

    return success(
      res,
      {
        telemetry: storedTelemetry,
        status: anomalies.length > 0 ? 'ANOMALY_DETECTED' : 'OPTIMAL',
        anomaly_count: anomalies.length,
      },
      'IoT telemetry stream ingested successfully',
      201
    );
  } catch (err) {
    return error(res, err.message);
  }
}

async function getLatestTelemetry(req, res) {
  try {
    const { farmId } = req.params;
    if (!(await FarmProfile.findByIdAndFarmerId(farmId, req.user.id)) && req.user.role !== 'admin') {
      return error(res, 'Farm not found', 404);
    }
    const telemetry = await Telemetry.findLatestByFarmId(farmId);

    return success(res, { telemetry });
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = { submitTelemetry, getLatestTelemetry };
