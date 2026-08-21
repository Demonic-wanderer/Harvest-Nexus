const express = require('express');
const router = express.Router();
const authMiddleware = require('../middleware/authMiddleware');
const {
  createMandi,
  getAllMandis,
  getMandiById,
  deleteMandi
} = require('../controllers/mandi.controller');

router.post('/', authMiddleware, createMandi);
router.get('/', authMiddleware, getAllMandis);
router.get('/:id', authMiddleware, getMandiById);
router.delete('/:id', authMiddleware, deleteMandi);

module.exports = router;
