const rateLimitWindowMs = 60 * 1000; // 1 minute
const maxRequestsPerWindow = 100; // 100 requests per minute

const clients = new Map();

function pruneExpiredClients(now) {
  for (const [ip, client] of clients) {
    if (now - client.startTime > rateLimitWindowMs) clients.delete(ip);
  }
}

function rateLimiter(req, res, next) {
  const ip = req.ip || req.socket.remoteAddress;
  const now = Date.now();
  if (clients.size > 1000) pruneExpiredClients(now);

  if (!clients.has(ip)) {
    clients.set(ip, {
      startTime: now,
      count: 1
    });
    return next();
  }

  const client = clients.get(ip);

  if (now - client.startTime > rateLimitWindowMs) {
    client.startTime = now;
    client.count = 1;
    return next();
  }

  client.count++;
  if (client.count > maxRequestsPerWindow) {
    return res.status(429).json({
      status: 'error',
      message: 'Too many requests. Please try again later.'
    });
  }

  next();
}

module.exports = rateLimiter;
