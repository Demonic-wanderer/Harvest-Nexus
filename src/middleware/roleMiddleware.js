const { error } = require('../utils/responseFormatter');

/**
 * Usage: roleMiddleware(['admin', 'advisor'])
 */
function roleMiddleware(allowedRoles = []) {
  return (req, res, next) => {
    if (!req.user) {
      return error(res, 'Unauthorized', 401);
    }

    if (!allowedRoles.includes(req.user.role)) {
      return error(res, 'Forbidden: insufficient role permissions', 403);
    }

    next();
  };
}

module.exports = roleMiddleware;
