import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import ParticleSystem from './ParticleSystem';

import fluidVertex from '../shaders/fluid/vertex.glsl?raw';
import fluidFragment from '../shaders/fluid/fragment.glsl?raw';

interface FluidMaterialProps {
  position: [number, number, number];
  waveStrength: number;
  flowSpeed: number;
  colorA: string;
  colorB: string;
  particleCount: number;
  showParticles: boolean;
}

export default function FluidMaterial({
  position,
  waveStrength,
  flowSpeed,
  colorA,
  colorB,
  particleCount,
  showParticles,
}: FluidMaterialProps) {
  const materialRef = useRef<THREE.ShaderMaterial>(null!);

  const uniforms = useMemo(
    () => ({
      uTime: { value: 0 },
      uWaveStrength: { value: waveStrength },
      uFlowSpeed: { value: flowSpeed },
      uColorA: { value: new THREE.Color(colorA) },
      uColorB: { value: new THREE.Color(colorB) },
    }),
    []
  );

  useFrame((state) => {
    if (!materialRef.current) return;
    materialRef.current.uniforms.uTime.value = state.clock.elapsedTime;
    materialRef.current.uniforms.uWaveStrength.value = waveStrength;
    materialRef.current.uniforms.uFlowSpeed.value = flowSpeed;
    materialRef.current.uniforms.uColorA.value = new THREE.Color(colorA);
    materialRef.current.uniforms.uColorB.value = new THREE.Color(colorB);
  });

  return (
    <group position={position}>
      <mesh>
        <sphereGeometry args={[1.2, 64, 64]} />
        <shaderMaterial
          ref={materialRef}
          vertexShader={fluidVertex}
          fragmentShader={fluidFragment}
          uniforms={uniforms}
          transparent
          side={THREE.DoubleSide}
        />
      </mesh>
      {showParticles && (
        <ParticleSystem
          position={[0, 0, 0]}
          count={particleCount}
          color={new THREE.Color(colorA)}
          speed={0.008}
          lifespan={3}
          size={0.15}
          emitRadius={1.8}
        />
      )}
    </group>
  );
}
