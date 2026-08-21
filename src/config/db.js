const { Pool } = require('pg');
const { DATABASE_URL, DB_SSL, DB_SSL_REJECT_UNAUTHORIZED } = require('./env');

if (!DATABASE_URL) {
  throw new Error('FATAL: DATABASE_URL environment variable is required');
}

const pool = new Pool({
  connectionString: DATABASE_URL,
  ssl: DB_SSL ? { rejectUnauthorized: DB_SSL_REJECT_UNAUTHORIZED } : false,
});

pool.on('connect', () => {
  console.log('✅ Connected to PostgreSQL');
});

pool.on('error', (err) => {
  console.error('❌ Unexpected DB error', err);
});

module.exports = {
  query: (text, params) => pool.query(text, params),
  pool,
};
