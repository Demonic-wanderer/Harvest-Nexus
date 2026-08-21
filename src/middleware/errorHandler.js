const logger = require('../utils/logger');
const { error } = require('../utils/responseFormatter');

function errorHandler(err, req, res, next) {
  logger.error(err.stack || err.message);
  const statusCode = err.statusCode || 500;
  const message = err.expose ? err.message : 'Internal Server Error';
  return error(res, message, statusCode);
}

module.exports = errorHandler;
