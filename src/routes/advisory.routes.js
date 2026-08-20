const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const {
  submitAdvisory, getAdvisoryHistory, getLatestAdvisory,
} = require('../controllers/advisory.controller');

// Akasha (advisory engine) pushes recommendations here
router.post('/', submitAdvisory);

router.get('/history/:farmId', authMiddleware, getAdvisoryHistory);
router.get('/latest/:farmId', authMiddleware, getLatestAdvisory);

module.exports = router;
