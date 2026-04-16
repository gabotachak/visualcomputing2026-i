// Controls are defined inline in App.tsx using leva's useControls hook.
// This file is kept as a reference for the control schema.

export interface UVSettings {
  textureType: 'checkerboard' | 'grid' | 'numbered';
  repeatX: number;
  repeatY: number;
  offsetX: number;
  offsetY: number;
  rotation: number;
  showModelA: boolean;
  showModelB: boolean;
  showModelC: boolean;
}
