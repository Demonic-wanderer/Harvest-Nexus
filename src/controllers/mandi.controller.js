const Mandi = require('../models/Mandi');
const { success, error } = require('../utils/responseFormatter');

async function createMandi(req, res) {
  try {
    const { name, location, latitude, longitude, contact_info } = req.body;
    if (!name) return error(res, 'name is required', 400);

    const mandi = await Mandi.create({ name, location, latitude, longitude, contact_info });
    return success(res, { mandi }, 'Mandi created successfully', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

async function getAllMandis(req, res) {
  try {
    const mandis = await Mandi.findAll();
    return success(res, { mandis });
  } catch (err) {
    return error(res, err.message);
  }
}

async function getMandiById(req, res) {
  try {
    const mandi = await Mandi.findById(req.params.id);
    if (!mandi) return error(res, 'Mandi not found', 404);
    return success(res, { mandi });
  } catch (err) {
    return error(res, err.message);
  }
}

async function deleteMandi(req, res) {
  try {
    const mandi = await Mandi.delete(req.params.id);
    if (!mandi) return error(res, 'Mandi not found', 404);
    return success(res, { mandi }, 'Mandi deleted successfully');
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = {
  createMandi,
  getAllMandis,
  getMandiById,
  deleteMandi
};
