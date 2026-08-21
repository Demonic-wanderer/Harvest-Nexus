const express = require('express');
const router = express.Router();
const { createBuyer, getAllBuyers, getBuyersByCrop } = require('../controllers/buyer.controller');

router.post('/', createBuyer);
router.get('/', getAllBuyers);
router.get('/crop/:cropName', getBuyersByCrop);

module.exports = router;
