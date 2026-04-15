import { useControls, button, folder } from 'leva';

const DEFAULTS = {
  colorTop: '#3380ff',
  colorBottom: '#ff4d33',
  waveFrequency: 5,
  colorA: '#33ffff',
  colorB: '#ff33ff',
  animationSpeed: 0.01,
  fresnelPower: 3,
  baseColor: '#1a3366',
  glowColor: '#4dccff',
};

export interface ShaderControls {
  colorTop: string;
  colorBottom: string;
  waveFrequency: number;
  colorA: string;
  colorB: string;
  animationSpeed: number;
  fresnelPower: number;
  baseColor: string;
  glowColor: string;
}

export function useShaderControls(): ShaderControls {
  const values = useControls({
    'Gradient Shader': folder({
      colorTop: { value: DEFAULTS.colorTop, label: 'Color Top' },
      colorBottom: { value: DEFAULTS.colorBottom, label: 'Color Bottom' },
    }),
    'Wave Shader': folder({
      waveFrequency: { value: DEFAULTS.waveFrequency, min: 0.5, max: 20, step: 0.5, label: 'Wave Frequency' },
      colorA: { value: DEFAULTS.colorA, label: 'Color A' },
      colorB: { value: DEFAULTS.colorB, label: 'Color B' },
      animationSpeed: { value: DEFAULTS.animationSpeed, min: 0.01, max: 0.1, step: 0.01, label: 'Animation Speed' },
    }),
    'Fresnel Shader': folder({
      fresnelPower: { value: DEFAULTS.fresnelPower, min: 0.5, max: 5, step: 0.1, label: 'Fresnel Power' },
      baseColor: { value: DEFAULTS.baseColor, label: 'Base Color' },
      glowColor: { value: DEFAULTS.glowColor, label: 'Glow Color' },
    }),
    'Reset All': button(() => {
      // Leva doesn't expose a reset API on the button callback; users can use the reset icon in the panel
    }),
  });

  return values as ShaderControls;
}
