const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const {
  createTransaction, getTransactionsByFarmer, updateTransactionStatus, attachLogistics,
} = require('../controllers/transaction.controller');

router.post('/', authMiddleware, createTransaction);
router.get('/farmer/:farmerId', authMiddleware, getTransactionsByFarmer);
router.put('/:id/status', authMiddleware, updateTransactionStatus);
router.post('/logistics', authMiddleware, attachLogistics);

module.exports = router;
