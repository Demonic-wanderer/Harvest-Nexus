const AdvisoryHistory = require('../models/AdvisoryHistory');
const { success, error } = require('../utils/responseFormatter');

// Called by Akasha (Ojas's advisory engine) after generating recommendations
async function submitAdvisory(req, res) {
  try {
    const {
      farm_id, crop_id, disease_id,
      irrigation_advice, fertilizer_advice, treatment_plan,
      priority_level, farm_health_score,
    } = req.body;

    if (!farm_id) return error(res, 'farm_id is required', 400);

    const record = await AdvisoryHistory.create({
      farm_id, crop_id, disease_id,
      irrigation_advice, fertilizer_advice, treatment_plan,
      priority_level, farm_health_score,
    });

    return success(res, { record }, 'Advisory stored', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

async function getAdvisoryHistory(req, res) {
  try {
    const history = await AdvisoryHistory.findByFarmId(req.params.farmId);
    return success(res, { history });
  } catch (err) {
    return error(res, err.message);
  }
}

async function getLatestAdvisory(req, res) {
  try {
    const latest = await AdvisoryHistory.findLatestByFarmId(req.params.farmId);
    return success(res, { latest });
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = { submitAdvisory, getAdvisoryHistory, getLatestAdvisory };
