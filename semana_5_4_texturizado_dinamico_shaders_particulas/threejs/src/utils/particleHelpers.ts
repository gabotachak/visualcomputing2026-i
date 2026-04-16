import * as THREE from 'three';

export function generateRandomPositions(count: number, radius: number): Float32Array {
  const positions = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const r = Math.random() * radius;
    positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = r * Math.cos(phi);
  }
  return positions;
}

export function generateGradientColor(t: number, colorA: THREE.Color, colorB: THREE.Color): THREE.Color {
  return colorA.clone().lerp(colorB, t);
}

export function createParticleGeometry(count: number, radius: number): THREE.BufferGeometry {
  const geometry = new THREE.BufferGeometry();
  const positions = generateRandomPositions(count, radius);
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  return geometry;
}

export interface ParticleConfig {
  count: number;
  color: THREE.Color;
  speed: number;
  lifespan: number;
  size: number;
  emitRadius: number;
}

export function getEnergyParticleConfig(): ParticleConfig {
  return {
    count: 150,
    color: new THREE.Color(0x00ffff),
    speed: 0.025,
    lifespan: 1,
    size: 0.08,
    emitRadius: 1.5,
  };
}

export function getFluidParticleConfig(): ParticleConfig {
  return {
    count: 100,
    color: new THREE.Color(0x0066ff),
    speed: 0.008,
    lifespan: 3,
    size: 0.15,
    emitRadius: 1.8,
  };
}
