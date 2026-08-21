const info = (...args) => console.log('[INFO]', new Date().toISOString(), ...args);
const errorLog = (...args) => console.error('[ERROR]', new Date().toISOString(), ...args);

module.exports = { info, error: errorLog };
