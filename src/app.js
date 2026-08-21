const express = require('express');
const cors = require('cors');
const morgan = require('morgan');

const authRoutes = require('./routes/auth.routes');
const farmerRoutes = require('./routes/farmer.routes');
const cropRoutes = require('./routes/crop.routes');
const diseaseRoutes = require('./routes/disease.routes');
const advisoryRoutes = require('./routes/advisory.routes');
const marketRoutes = require('./routes/market.routes');
const buyerRoutes = require('./routes/buyer.routes');
const transactionRoutes = require('./routes/transaction.routes');

const errorHandler = require('./middleware/errorHandler');

const app = express();

app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Health check
app.get('/', (req, res) => {
  res.json({ status: 'ok', message: 'Harvest Nexus Cloud Backend (Forge) is running 🚀' });
});

// Mounted routes
app.use('/api/auth', authRoutes);
app.use('/api/farmer', farmerRoutes);
app.use('/api/crop', cropRoutes);
app.use('/api/disease', diseaseRoutes);       // consumed by Oracle (AI)
app.use('/api/advisory', advisoryRoutes);     // consumed by Akasha (Advisory)
app.use('/api/market', marketRoutes);         // consumed by Insight (Market/Logistics)
app.use('/api/buyer', buyerRoutes);
app.use('/api/transaction', transactionRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({ status: 'error', message: 'Route not found' });
});

// Global error handler (must be last)
app.use(errorHandler);

module.exports = app;
