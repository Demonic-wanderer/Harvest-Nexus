const Logistics = require('../models/Logistics');
const Transporter = require('../models/Transporter');
const { success, error } = require('../utils/responseFormatter');
const { optionalNumber, optionalString, requireString, requireUuid } = require('../utils/validation');

async function createLogistics(req, res) {
  try {
    const transaction_id = requireUuid(req.body.transaction_id, 'transaction_id');
    const transporter_name = requireString(req.body.transporter_name, 'transporter_name', { max: 150 });
    const contact_phone = optionalString(req.body.contact_phone, 'contact_phone', { max: 20 });
    const pickup_location = requireString(req.body.pickup_location, 'pickup_location', { max: 150 });
    const drop_location = requireString(req.body.drop_location, 'drop_location', { max: 150 });
    const record = await Logistics.create({
      transaction_id, transporter_name, contact_phone, pickup_location, drop_location,
    });
    return success(res, { logistics: record }, 'Logistics attached', 201);
  } catch (err) {
    return error(res, err.message, err.statusCode || 500);
  }
}

async function listTransporters(req, res) {
  try {
    const transporters = await Transporter.findAll();
    return success(res, { transporters });
  } catch (err) {
    return error(res, err.message);
  }
}

async function createTransporter(req, res) {
  try {
    const transporter = await Transporter.create({
      name: requireString(req.body.name, 'name', { max: 150 }),
      contact_phone: optionalString(req.body.contact_phone, 'contact_phone', { max: 20 }),
      base_location: optionalString(req.body.base_location, 'base_location', { max: 150 }),
      vehicle_type: optionalString(req.body.vehicle_type, 'vehicle_type', { max: 50 }),
      capacity_quintals: optionalNumber(req.body.capacity_quintals, 'capacity_quintals', { min: 0, max: 10000 }),
      rate_per_km_quintal: optionalNumber(req.body.rate_per_km_quintal, 'rate_per_km_quintal', { min: 0, max: 100 }),
    });
    return success(res, { transporter }, 'Transporter added', 201);
  } catch (err) {
    return error(res, err.message, err.statusCode || 500);
  }
}

module.exports = { createLogistics, createTransporter, listTransporters };
