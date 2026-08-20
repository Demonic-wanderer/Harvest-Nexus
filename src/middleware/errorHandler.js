const logger = require('../utils/logger');
const { error } = require('../utils/responseFormatter');

function errorHandler(err, req, res, next) {
  logger.error(err.stack || err.message);
  return error(res, err.message || 'Internal Server Error', err.statusCode || 500);
}

module.exports = errorHandler;
