const Farmer = require('../models/Farmer');
const FarmProfile = require('../models/FarmProfile');
const { success, error } = require('../utils/responseFormatter');

async function getProfile(req, res) {
  try {
    const user = await Farmer.findById(req.params.id);
    if (!user) return error(res, 'User not found', 404);
    return success(res, { user });
  } catch (err) {
    return error(res, err.message);
  }
}

async function createFarm(req, res) {
  try {
    const { farmer_id, farm_name, location, latitude, longitude, land_size_acres, soil_type } = req.body;
    const farm = await FarmProfile.create({
      farmer_id, farm_name, location, latitude, longitude, land_size_acres, soil_type,
    });
    return success(res, { farm }, 'Farm profile created', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

async function getFarmsByFarmer(req, res) {
  try {
    const farms = await FarmProfile.findByFarmerId(req.params.farmerId);
    return success(res, { farms });
  } catch (err) {
    return error(res, err.message);
  }
}

async function updateFarm(req, res) {
  try {
    const farm = await FarmProfile.update(req.params.id, req.body);
    if (!farm) return error(res, 'Farm not found', 404);
    return success(res, { farm }, 'Farm updated');
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = { getProfile, createFarm, getFarmsByFarmer, updateFarm };
