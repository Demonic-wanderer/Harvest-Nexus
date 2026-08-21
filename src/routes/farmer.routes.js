const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const {
  getProfile, createFarm, getFarmsByFarmer, updateFarm,
} = require('../controllers/farmer.controller');

router.get('/:id', authMiddleware, getProfile);
router.post('/farm', authMiddleware, createFarm);
router.get('/:farmerId/farms', authMiddleware, getFarmsByFarmer);
router.put('/farm/:id', authMiddleware, updateFarm);

module.exports = router;
