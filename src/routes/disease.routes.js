const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const {
  submitPrediction, getHistoryByCrop, getLatestByCrop,
} = require('../controllers/disease.controller');

// Oracle (AI engine) pushes prediction results here
router.post('/predict-result', submitPrediction);

router.get('/history/:cropId', authMiddleware, getHistoryByCrop);
router.get('/latest/:cropId', authMiddleware, getLatestByCrop);

module.exports = router;
