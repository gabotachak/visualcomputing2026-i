import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import ParticleSystem from './ParticleSystem';

// Import shaders as raw strings via Vite's ?raw query
import energyVertex from '../shaders/energy/vertex.glsl?raw';
import energyFragment from '../shaders/energy/fragment.glsl?raw';

interface EnergyMaterialProps {
  position: [number, number, number];
  mouse: React.RefObject<THREE.Vector2>;
  intensity: number;
  colorCore: string;
  colorEdge: string;
  particleCount: number;
  showParticles: boolean;
}

export default function EnergyMaterial({
  position,
  mouse,
  intensity,
  colorCore,
  colorEdge,
  particleCount,
  showParticles,
}: EnergyMaterialProps) {
  const materialRef = useRef<THREE.ShaderMaterial>(null!);

  const uniforms = useMemo(
    () => ({
      uTime: { value: 0 },
      uMousePos: { value: new THREE.Vector2(0.5, 0.5) },
      uIntensity: { value: intensity },
      uColorCore: { value: new THREE.Color(colorCore) },
      uColorEdge: { value: new THREE.Color(colorEdge) },
    }),
    []
  );

  useFrame((state) => {
    if (!materialRef.current) return;
    materialRef.current.uniforms.uTime.value = state.clock.elapsedTime;
    materialRef.current.uniforms.uMousePos.value = new THREE.Vector2(
      mouse.current.x * 0.5 + 0.5,
      mouse.current.y * 0.5 + 0.5
    );
    materialRef.current.uniforms.uIntensity.value = intensity;
    materialRef.current.uniforms.uColorCore.value = new THREE.Color(colorCore);
    materialRef.current.uniforms.uColorEdge.value = new THREE.Color(colorEdge);
  });

  return (
    <group position={position}>
      <mesh>
        <sphereGeometry args={[1.2, 64, 64]} />
        <shaderMaterial
          ref={materialRef}
          vertexShader={energyVertex}
          fragmentShader={energyFragment}
          uniforms={uniforms}
          transparent
          side={THREE.DoubleSide}
        />
      </mesh>
      {showParticles && (
        <ParticleSystem
          position={[0, 0, 0]}
          count={particleCount}
          color={new THREE.Color(colorCore)}
          speed={0.025}
          lifespan={1}
          size={0.08}
          emitRadius={1.5}
        />
      )}
    </group>
  );
}
