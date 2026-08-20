const app = require('./src/app');
const { PORT } = require('./src/config/env');

app.listen(PORT, () => {
  console.log(`🌱 Harvest Nexus Backend (Forge) running on http://localhost:${PORT}`);
});
