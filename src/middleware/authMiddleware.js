const jwt = require('jsonwebtoken');
const { JWT_SECRET } = require('../config/env');
const { error } = require('../utils/responseFormatter');

function authMiddleware(req, res, next) {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return error(res, 'No token provided', 401);
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded; // { id, role, email }
    next();
  } catch (err) {
    return error(res, 'Invalid or expired token', 401);
  }
}

module.exports = authMiddleware;
