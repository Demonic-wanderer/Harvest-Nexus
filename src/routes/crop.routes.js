const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const { createCrop, getCropsByFarm, getCropById } = require('../controllers/crop.controller');

router.post('/', authMiddleware, createCrop);
router.get('/farm/:farmId', authMiddleware, getCropsByFarm);
router.get('/:id', authMiddleware, getCropById);

module.exports = router;
