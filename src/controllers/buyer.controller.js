const Buyer = require('../models/Buyer');
const { success, error } = require('../utils/responseFormatter');

async function createBuyer(req, res) {
  try {
    const { name, contact_phone, contact_email, location, crop_interest } = req.body;
    const buyer = await Buyer.create({ name, contact_phone, contact_email, location, crop_interest });
    return success(res, { buyer }, 'Buyer added', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

async function getAllBuyers(req, res) {
  try {
    const buyers = await Buyer.findAll();
    return success(res, { buyers });
  } catch (err) {
    return error(res, err.message);
  }
}

async function getBuyersByCrop(req, res) {
  try {
    const buyers = await Buyer.findByCropInterest(req.params.cropName);
    return success(res, { buyers });
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = { createBuyer, getAllBuyers, getBuyersByCrop };
