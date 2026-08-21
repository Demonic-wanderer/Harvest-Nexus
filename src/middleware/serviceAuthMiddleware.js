const crypto = require('crypto');
const { SERVICE_KEYS } = require('../config/env');
const { error } = require('../utils/responseFormatter');

function secureEquals(left, right) {
  const leftBuffer = Buffer.from(left || '');
  const rightBuffer = Buffer.from(right || '');
  return leftBuffer.length === rightBuffer.length
    && crypto.timingSafeEqual(leftBuffer, rightBuffer);
}

function serviceAuthMiddleware(serviceName) {
  return (req, res, next) => {
    const expectedKey = SERVICE_KEYS[serviceName];
    const suppliedKey = req.get('X-Service-Key');

    if (!expectedKey || !secureEquals(suppliedKey, expectedKey)) {
      return error(res, 'Invalid service credentials', 401);
    }

    req.service = serviceName;
    return next();
  };
}

module.exports = serviceAuthMiddleware;
