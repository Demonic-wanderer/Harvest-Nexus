const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const serviceOrUserAuth = require('../middleware/serviceOrUserAuth');
const {
  createLogistics, createTransporter, listTransporters,
} = require('../controllers/logistics.controller');

router.get('/transporters', authMiddleware, listTransporters);
router.post('/transporters', authMiddleware, createTransporter);
router.post('/', serviceOrUserAuth('insight'), createLogistics);

module.exports = router;
