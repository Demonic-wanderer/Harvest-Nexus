const MarketData = require('../models/MarketData');
const { success, error } = require('../utils/responseFormatter');

// Called by Insight (Bhumika's module) to push new price/trend data
async function submitMarketData(req, res) {
  try {
    const { crop_name, region, current_price, trend, demand_indicator, forecast_price } = req.body;

    if (!crop_name || !region) return error(res, 'crop_name and region are required', 400);

    const record = await MarketData.create({
      crop_name, region, current_price, trend, demand_indicator, forecast_price,
    });
    return success(res, { record }, 'Market data stored', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

async function getMarketByCropRegion(req, res) {
  try {
    const { crop, region } = req.query;
    if (!crop || !region) return error(res, 'crop and region query params are required', 400);

    const data = await MarketData.findByCropAndRegion(crop, region);
    return success(res, { data });
  } catch (err) {
    return error(res, err.message);
  }
}

async function getAllMarketData(req, res) {
  try {
    const limit = parseInt(req.query.limit, 10) || 20;
    const page = parseInt(req.query.page, 10) || 1;
    const offset = (page - 1) * limit;

    const data = await MarketData.findAll(limit, offset);
    return success(res, { data, page, limit });
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = { submitMarketData, getMarketByCropRegion, getAllMarketData };
