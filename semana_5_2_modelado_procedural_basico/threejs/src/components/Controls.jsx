import { useControls, button } from 'leva';

const GRID_DEFAULTS = {
  gridSize: { value: 5, min: 2, max: 12, step: 1 },
  spacing: { value: 1.5, min: 0.5, max: 4, step: 0.1 },
  gridScale: { value: 0.8, min: 0.1, max: 2, step: 0.05 },
  rotationSpeed: { value: 0.01, min: 0, max: 0.1, step: 0.001 },
};

const SPIRAL_DEFAULTS = {
  turns: { value: 3, min: 1, max: 8, step: 0.5 },
  segments: { value: 30, min: 5, max: 80, step: 1 },
  radius: { value: 2.0, min: 0.5, max: 5, step: 0.1 },
  height: { value: 5.0, min: 1, max: 10, step: 0.1 },
  scaleVariation: { value: 0.5, min: 0, max: 2, step: 0.05 },
  animationSpeed: { value: 0.5, min: 0, max: 1.0, step: 0.01 },
};

const TERRAIN_DEFAULTS = {
  width: { value: 8, min: 2, max: 16, step: 1 },
  depth: { value: 8, min: 2, max: 16, step: 1 },
  segments: { value: 30, min: 5, max: 60, step: 5 },
  octaves: { value: 4, min: 1, max: 6, step: 1 },
  amplitude: { value: 0.8, min: 0.1, max: 3, step: 0.05 },
  frequency: { value: 0.5, min: 0.05, max: 2, step: 0.05 },
  terrainSpeed: { value: 0.5, min: 0, max: 2, step: 0.05 },
  wireframe: { value: false },
};

export function useGridControls(resetKey, setResetKey) {
  return useControls('Grid', {
    ...GRID_DEFAULTS,
    Reset: button(() => setResetKey((k) => k + 1)),
  });
}

export function useSpiralControls() {
  return useControls('Spiral', SPIRAL_DEFAULTS);
}

export function useTerrainControls() {
  return useControls('Terrain', TERRAIN_DEFAULTS);
}
