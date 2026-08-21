const authMiddleware = require('./authMiddleware');
const serviceAuthMiddleware = require('./serviceAuthMiddleware');

function serviceOrUserAuth(serviceName) {
  return (req, res, next) => {
    if (req.get('X-Service-Key')) {
      return serviceAuthMiddleware(serviceName)(req, res, next);
    }
    return authMiddleware(req, res, next);
  };
}

module.exports = serviceOrUserAuth;
