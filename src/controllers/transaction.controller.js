const Transaction = require('../models/Transaction');
const Logistics = require('../models/Logistics');
const { success, error } = require('../utils/responseFormatter');

async function createTransaction(req, res) {
  try {
    const { farmer_id, buyer_id, crop_id, quantity_quintals, price_per_quintal, status } = req.body;
    const txn = await Transaction.create({ farmer_id, buyer_id, crop_id, quantity_quintals, price_per_quintal, status });
    return success(res, { transaction: txn }, 'Transaction created', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

async function getTransactionsByFarmer(req, res) {
  try {
    const transactions = await Transaction.findByFarmerId(req.params.farmerId);
    return success(res, { transactions });
  } catch (err) {
    return error(res, err.message);
  }
}

async function updateTransactionStatus(req, res) {
  try {
    const { status } = req.body;
    const txn = await Transaction.updateStatus(req.params.id, status);
    if (!txn) return error(res, 'Transaction not found', 404);
    return success(res, { transaction: txn }, 'Status updated');
  } catch (err) {
    return error(res, err.message);
  }
}

async function attachLogistics(req, res) {
  try {
    const { transaction_id, transporter_name, contact_phone, pickup_location, drop_location } = req.body;
    const record = await Logistics.create({
      transaction_id, transporter_name, contact_phone, pickup_location, drop_location,
    });
    return success(res, { logistics: record }, 'Logistics attached', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = {
  createTransaction,
  getTransactionsByFarmer,
  updateTransactionStatus,
  attachLogistics,
};
