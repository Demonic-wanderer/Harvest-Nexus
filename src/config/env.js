require('dotenv').config();

const isProduction = process.env.NODE_ENV === 'production';

if (!process.env.JWT_SECRET) {
  throw new Error('FATAL: JWT_SECRET environment variable is required');
}

module.exports = {
  CORS_ORIGINS: (process.env.CORS_ORIGINS || '')
    .split(',')
    .map((origin) => origin.trim())
    .filter(Boolean),
  DB_SSL: process.env.DB_SSL === 'true' || isProduction,
  DB_SSL_REJECT_UNAUTHORIZED: process.env.DB_SSL_REJECT_UNAUTHORIZED !== 'false',
  IS_PRODUCTION: isProduction,
  PORT: process.env.PORT || 5000,
  DATABASE_URL: process.env.DATABASE_URL,
  JWT_SECRET: process.env.JWT_SECRET,
  JWT_EXPIRES_IN: process.env.JWT_EXPIRES_IN || '1d',
  SERVICE_KEYS: {
    advisory: process.env.ADVISORY_SERVICE_KEY,
    insight: process.env.INSIGHT_SERVICE_KEY,
    iot_rover: process.env.IOT_ROVER_SERVICE_KEY,
    oracle: process.env.ORACLE_SERVICE_KEY,
  },
};
