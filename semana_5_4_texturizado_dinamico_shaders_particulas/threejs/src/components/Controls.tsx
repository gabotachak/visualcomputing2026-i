import { useControls, button, folder } from 'leva';

interface ControlValues {
  // Energy
  intensity: number;
  colorCore: string;
  colorEdge: string;
  energyParticleCount: number;
  // Fluid
  waveStrength: number;
  flowSpeed: number;
  colorA: string;
  colorB: string;
  fluidParticleCount: number;
  // Global
  showParticles: boolean;
}

const DEFAULTS = {
  intensity: 1.2,
  colorCore: '#00ffff',
  colorEdge: '#8800ff',
  energyParticleCount: 150,
  waveStrength: 0.1,
  flowSpeed: 1.5,
  colorA: '#0044ff',
  colorB: '#00ccff',
  fluidParticleCount: 100,
  showParticles: true,
};

export function useSceneControls() {
  const [values, set] = useControls(() => ({
    'Energy Material': folder({
      intensity: { value: DEFAULTS.intensity, min: 0.5, max: 2.0, step: 0.1 },
      colorCore: { value: DEFAULTS.colorCore },
      colorEdge: { value: DEFAULTS.colorEdge },
      energyParticleCount: {
        label: 'Particle Count',
        value: DEFAULTS.energyParticleCount,
        min: 50,
        max: 500,
        step: 50,
      },
    }),
    'Fluid Material': folder({
      waveStrength: { value: DEFAULTS.waveStrength, min: 0.01, max: 0.3, step: 0.01 },
      flowSpeed: { value: DEFAULTS.flowSpeed, min: 0.5, max: 3.0, step: 0.1 },
      colorA: { value: DEFAULTS.colorA },
      colorB: { value: DEFAULTS.colorB },
      fluidParticleCount: {
        label: 'Particle Count',
        value: DEFAULTS.fluidParticleCount,
        min: 30,
        max: 300,
        step: 30,
      },
    }),
    Global: folder({
      showParticles: { value: DEFAULTS.showParticles, label: 'Show Particles' },
      'Reset All': button(() => {
        set({
          intensity: DEFAULTS.intensity,
          colorCore: DEFAULTS.colorCore,
          colorEdge: DEFAULTS.colorEdge,
          energyParticleCount: DEFAULTS.energyParticleCount,
          waveStrength: DEFAULTS.waveStrength,
          flowSpeed: DEFAULTS.flowSpeed,
          colorA: DEFAULTS.colorA,
          colorB: DEFAULTS.colorB,
          fluidParticleCount: DEFAULTS.fluidParticleCount,
          showParticles: DEFAULTS.showParticles,
        });
      }),
    }),
  }));

  return values as ControlValues;
}
