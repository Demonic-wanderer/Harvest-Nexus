const DiseaseHistory = require('../models/DiseaseHistory');
const { success, error } = require('../utils/responseFormatter');

// Called by Oracle (Arpan's AI engine) after inference
async function submitPrediction(req, res) {
  try {
    const { crop_id, image_url, disease_name, confidence, severity } = req.body;

    if (!crop_id || !disease_name) {
      return error(res, 'crop_id and disease_name are required', 400);
    }

    const record = await DiseaseHistory.create({ crop_id, image_url, disease_name, confidence, severity });
    return success(res, { record }, 'Disease prediction stored', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

async function getHistoryByCrop(req, res) {
  try {
    const history = await DiseaseHistory.findByCropId(req.params.cropId);
    return success(res, { history });
  } catch (err) {
    return error(res, err.message);
  }
}

async function getLatestByCrop(req, res) {
  try {
    const latest = await DiseaseHistory.findLatestByCropId(req.params.cropId);
    return success(res, { latest });
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = { submitPrediction, getHistoryByCrop, getLatestByCrop };
