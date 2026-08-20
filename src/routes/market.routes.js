const express = require('express');
const router = express.Router();
const {
  submitMarketData, getMarketByCropRegion, getAllMarketData,
} = require('../controllers/market.controller');

// Insight (market intelligence module) pushes data here
router.post('/', submitMarketData);

router.get('/', getMarketByCropRegion); // ?crop=Tomato&region=MP
router.get('/all', getAllMarketData);

module.exports = router;
