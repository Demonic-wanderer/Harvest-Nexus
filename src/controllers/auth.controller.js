const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const Farmer = require('../models/Farmer');
const { JWT_SECRET, JWT_EXPIRES_IN } = require('../config/env');
const { success, error } = require('../utils/responseFormatter');

async function register(req, res) {
  try {
    const { name, email, phone, password, role } = req.body;

    if (!name || !email || !password || !role) {
      return error(res, 'name, email, password, and role are required', 400);
    }

    const existing = await Farmer.findByEmail(email);
    if (existing) return error(res, 'Email already registered', 409);

    const password_hash = await bcrypt.hash(password, 10);
    const user = await Farmer.create({ name, email, phone, password_hash, role });

    return success(res, { user }, 'User registered successfully', 201);
  } catch (err) {
    return error(res, err.message);
  }
}

async function login(req, res) {
  try {
    const { email, phone, password } = req.body;
    if ((!email && !phone) || !password) {
      return error(res, 'email or phone, and password are required', 400);
    }

    const user = email
      ? await Farmer.findByEmail(email)
      : await Farmer.findByPhone(phone);
    if (!user) return error(res, 'Invalid credentials', 401);

    const match = await bcrypt.compare(password, user.password_hash);
    if (!match) return error(res, 'Invalid credentials', 401);

    const token = jwt.sign(
      { id: user.id, role: user.role, email: user.email },
      JWT_SECRET,
      { expiresIn: JWT_EXPIRES_IN }
    );

    return success(res, {
      token,
      user: { id: user.id, name: user.name, email: user.email, role: user.role },
    }, 'Login successful');
  } catch (err) {
    return error(res, err.message);
  }
}

module.exports = { register, login };
