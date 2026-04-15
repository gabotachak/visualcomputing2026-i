import React, { useRef, useMemo } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import vertexShader from '../shaders/waves/vertex.glsl?raw';
import fragmentShader from '../shaders/waves/fragment.glsl?raw';

interface WaveShaderProps {
  waveFrequency: number;
  colorA: string;
  colorB: string;
  animationSpeed: number;
}

export default function WaveShader({ waveFrequency, colorA, colorB, animationSpeed }: WaveShaderProps) {
  const materialRef = useRef<THREE.ShaderMaterial>(null);

  const uniforms = useMemo(
    () => ({
      uTime: { value: 0 },
      uWaveFrequency: { value: waveFrequency },
      uColorA: { value: new THREE.Color(colorA) },
      uColorB: { value: new THREE.Color(colorB) },
    }),
    []
  );

  useFrame(() => {
    if (!materialRef.current) return;
    materialRef.current.uniforms.uTime.value += animationSpeed;
    materialRef.current.uniforms.uWaveFrequency.value = waveFrequency;
    materialRef.current.uniforms.uColorA.value.set(colorA);
    materialRef.current.uniforms.uColorB.value.set(colorB);
  });

  return (
    <mesh position={[0, 0, 0]}>
      <sphereGeometry args={[1.2, 32, 32]} />
      <shaderMaterial
        ref={materialRef}
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
      />
    </mesh>
  );
}
