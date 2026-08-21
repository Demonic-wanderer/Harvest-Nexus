const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const { createBuyer, getAllBuyers, getBuyersByCrop } = require('../controllers/buyer.controller');

router.post('/', authMiddleware, createBuyer);
router.get('/', authMiddleware, getAllBuyers);
router.get('/crop/:cropName', authMiddleware, getBuyersByCrop);

module.exports = router;
