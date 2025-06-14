// Worcester boundary coordinates, same as the geojson file
export const boundaryCoordinates = [
  [42.31125981163397, -71.76826678481181],
  [42.29622129331082, -71.75854175122491],
  [42.25449438759649, -71.75127866978954],
  [42.24383880238205, -71.7460788980993],
  [42.241286202077475, -71.7312370382492],
  [42.23797496257023, -71.73342879746599],
  [42.21003972687307, -71.79714013927976],
  [42.22092640552484, -71.80383446356241],
  [42.22389864397315, -71.80675115985495],
  [42.2312626623544, -71.81003453987614],
  [42.22667559159572, -71.85663223538798],
  [42.281252735690636, -71.88404314157144],
  [42.28654443444086, -71.87538752139702],
  [42.33134547345032, -71.80204214881934],
  [42.33134551930074, -71.8020421733052],
  [42.34118701668068, -71.78589439200991],
  [42.32896221071184, -71.77971954592051],
  [42.31125981163397, -71.76826678481181]
];  

// ray-casting algorithm
export function pointInPolygon(point, polygon) {
  const x = point.lng;
  const y = point.lat;
  let inside = false;

  // Loop through the edges of the polygon
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const xi = polygon[i][1], yi = polygon[i][0];
    const xj = polygon[j][1], yj = polygon[j][0];

    // Check if the point passes through the edge
    if ((yi > y) !== (yj > y) &&
      (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) {

      // If it does, toggle the inside variable, if the total number of crossing is odd, the point is inside
      inside = !inside;
    }
  }

  return inside;
}
