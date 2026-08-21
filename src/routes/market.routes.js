const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const {
  submitMarketData, getMarketByCropRegion, getAllMarketData,
} = require('../controllers/market.controller');

// Insight (market intelligence module) pushes data here
router.post('/', authMiddleware, submitMarketData);

router.get('/search', authMiddleware, getMarketByCropRegion); // ?crop=Tomato&region=MP
router.get('/all', authMiddleware, getAllMarketData);

module.exports = router;
