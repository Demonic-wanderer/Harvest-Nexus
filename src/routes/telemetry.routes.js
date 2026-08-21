const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const serviceOrUserAuth = require('../middleware/serviceOrUserAuth');
const {
  submitTelemetry,
  getLatestTelemetry,
} = require('../controllers/telemetry.controller');

// IoT edge devices, hardware rovers, and Flutter clients push live telemetry streams here
router.post('/stream', serviceOrUserAuth('iot_rover'), submitTelemetry);
router.get('/latest/:farmId', authMiddleware, getLatestTelemetry);

module.exports = router;
