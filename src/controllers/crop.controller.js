const CropProfile = require('../models/CropProfile');
const { success, error } = require('../utils/responseFormatter');

async function createCrop(req, res) {
  try {
    const { farm_id, crop_name, sowing_date, expected_harvest_date } = req.body;
    const crop = await CropProfile.create({ farm_id, crop_name, sowing_date, expected_harvest_date });
    return success(res, { crop }, 'Crop profile created', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

async function getCropsByFarm(req, res) {
  try {
    const crops = await CropProfile.findByFarmId(req.params.farmId);
    return success(res, { crops });
  } catch (err) {
    return error(res, err.message);
  }
}

async function getCropById(req, res) {
  try {
    const crop = await CropProfile.findById(req.params.id);
    if (!crop) return error(res, 'Crop not found', 404);
    return success(res, { crop });
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = { createCrop, getCropsByFarm, getCropById };
