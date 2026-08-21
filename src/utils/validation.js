const { httpError } = require('./httpError');

const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function requireString(value, field, { min = 1, max = 500 } = {}) {
  if (typeof value !== 'string') throw httpError(400, `${field} must be a string`);
  const normalized = value.trim();
  if (normalized.length < min || normalized.length > max) {
    throw httpError(400, `${field} must be between ${min} and ${max} characters`);
  }
  return normalized;
}

function optionalString(value, field, options) {
  if (value === undefined || value === null || value === '') return null;
  return requireString(value, field, options);
}

function requireUuid(value, field) {
  const normalized = requireString(value, field, { min: 36, max: 36 });
  if (!UUID_PATTERN.test(normalized)) throw httpError(400, `${field} must be a UUID`);
  return normalized;
}

function optionalUuid(value, field) {
  if (value === undefined || value === null || value === '') return null;
  return requireUuid(value, field);
}

function requireNumber(value, field, { min = 0, max = Number.MAX_SAFE_INTEGER } = {}) {
  const numeric = typeof value === 'number' ? value : Number(value);
  if (!Number.isFinite(numeric) || numeric < min || numeric > max) {
    throw httpError(400, `${field} must be a number between ${min} and ${max}`);
  }
  return numeric;
}

function optionalNumber(value, field, options) {
  if (value === undefined || value === null || value === '') return null;
  return requireNumber(value, field, options);
}

function requireEnum(value, field, allowed) {
  const normalized = requireString(value, field, { max: 50 }).toLowerCase();
  if (!allowed.includes(normalized)) {
    throw httpError(400, `${field} must be one of: ${allowed.join(', ')}`);
  }
  return normalized;
}

function requireEmail(value) {
  const email = requireString(value, 'email', { max: 150 }).toLowerCase();
  if (!EMAIL_PATTERN.test(email)) throw httpError(400, 'email must be valid');
  return email;
}

function requirePassword(value) {
  if (typeof value !== 'string' || value.length < 12 || value.length > 128) {
    throw httpError(400, 'password must be between 12 and 128 characters');
  }
  return value;
}

module.exports = {
  optionalNumber,
  optionalString,
  optionalUuid,
  requireEmail,
  requireEnum,
  requireNumber,
  requirePassword,
  requireString,
  requireUuid,
};
