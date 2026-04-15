/**
 * Returns an array of [x, y, z] positions for a grid of items.
 * @param {number} gridSize - Number of items per side
 * @param {number} spacing  - Distance between items
 */
export function createGridPositions(gridSize, spacing) {
  const positions = [];
  for (let x = 0; x < gridSize; x++) {
    for (let z = 0; z < gridSize; z++) {
      positions.push([
        x * spacing - (gridSize / 2) * spacing + spacing / 2,
        0,
        z * spacing - (gridSize / 2) * spacing + spacing / 2,
      ]);
    }
  }
  return positions;
}

/**
 * Returns an array of { position, angle, t } for a helix spiral.
 * @param {number} turns     - Number of full turns
 * @param {number} segments  - Total number of cylinders
 * @param {number} radius    - Helix radius
 * @param {number} height    - Total height
 */
export function createSpiralPositions(turns, segments, radius, height) {
  const items = [];
  for (let i = 0; i < segments; i++) {
    const t = i / segments;
    const angle = t * turns * Math.PI * 2;
    const x = radius * Math.cos(angle);
    const z = radius * Math.sin(angle);
    const y = t * height - height / 2;
    items.push({ position: [x, y, z], angle, t });
  }
  return items;
}

/**
 * Returns a random hex color string.
 */
export function randomColor() {
  return `#${Math.floor(Math.random() * 0xffffff)
    .toString(16)
    .padStart(6, '0')}`;
}

/**
 * Returns an interpolated color between red (0°) and blue (240°) in HSL.
 * @param {number} t - value in [0, 1]
 */
export function gradientColor(t) {
  const hue = t * 240;
  return `hsl(${hue}, 80%, 55%)`;
}
