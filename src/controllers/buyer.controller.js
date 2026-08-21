const Buyer = require('../models/Buyer');
const { success, error } = require('../utils/responseFormatter');
const { geocodeLocation, withDistance } = require('../utils/geo');

async function createBuyer(req, res) {
  try {
    const { name, contact_phone, contact_email, location, crop_interest, latitude, longitude } = req.body;
    const coords = (latitude != null && longitude != null)
      ? [latitude, longitude]
      : geocodeLocation(location) || [null, null];
    const buyer = await Buyer.create({
      name,
      contact_phone,
      contact_email,
      location,
      crop_interest,
      latitude: latitude ?? coords[0],
      longitude: longitude ?? coords[1],
    });
    return success(res, { buyer }, 'Buyer added', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

async function getAllBuyers(req, res) {
  try {
    const limit = parseInt(req.query.limit, 10) || 20;
    const page = parseInt(req.query.page, 10) || 1;
    const offset = (page - 1) * limit;

    const buyers = await Buyer.findAll(limit, offset);
    return success(res, { buyers, page, limit });
  } catch (err) {
    return error(res, err.message);
  }
}

async function getBuyersByCrop(req, res) {
  try {
    const buyers = await Buyer.findByCropInterest(req.params.cropName);
    const origin = req.query.lat != null && req.query.lon != null
      ? [Number(req.query.lat), Number(req.query.lon)]
      : geocodeLocation(req.query.location);
    const ranked = origin ? withDistance(buyers, origin[0], origin[1]) : buyers;
    return success(res, { buyers: ranked });
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = { createBuyer, getAllBuyers, getBuyersByCrop };
