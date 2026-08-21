function haversineKm(lat1, lon1, lat2, lon2) {
  const toRad = (value) => (value * Math.PI) / 180;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) ** 2
    + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;
  return Number((6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))).toFixed(2));
}

const CITY_COORDINATES = {
  indore: [22.7196, 75.8577],
  bhopal: [23.2599, 77.4126],
  ujjain: [23.1765, 75.7885],
  gwalior: [26.2183, 78.1828],
  jabalpur: [23.1815, 79.9864],
};

function geocodeLocation(location) {
  if (!location) return null;
  const key = String(location).trim().toLowerCase();
  if (CITY_COORDINATES[key]) return CITY_COORDINATES[key];
  const match = Object.keys(CITY_COORDINATES).find((city) => key.includes(city));
  return match ? CITY_COORDINATES[match] : null;
}

function withDistance(rows, originLat, originLon) {
  return rows.map((row) => {
    const lat = row.latitude != null ? Number(row.latitude) : geocodeLocation(row.location)?.[0];
    const lon = row.longitude != null ? Number(row.longitude) : geocodeLocation(row.location)?.[1];
    const distance_km = (lat != null && lon != null && originLat != null && originLon != null)
      ? haversineKm(originLat, originLon, lat, lon)
      : null;
    return { ...row, distance_km };
  }).sort((a, b) => (a.distance_km ?? 10000) - (b.distance_km ?? 10000));
}

module.exports = { geocodeLocation, haversineKm, withDistance };
