import React, { useRef, useMemo } from 'react';
import * as THREE from 'three';
import { useFrame } from '@react-three/fiber';
import vertexShader from '../shaders/fresnel/vertex.glsl?raw';
import fragmentShader from '../shaders/fresnel/fragment.glsl?raw';

interface FresnelShaderProps {
  fresnelPower: number;
  baseColor: string;
  glowColor: string;
}

export default function FresnelShader({ fresnelPower, baseColor, glowColor }: FresnelShaderProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const materialRef = useRef<THREE.ShaderMaterial>(null);

  const uniforms = useMemo(
    () => ({
      uFresnelPower: { value: fresnelPower },
      uBaseColor: { value: new THREE.Color(baseColor) },
      uGlowColor: { value: new THREE.Color(glowColor) },
    }),
    []
  );

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.y += 0.01;
    }
    if (materialRef.current) {
      materialRef.current.uniforms.uFresnelPower.value = fresnelPower;
      materialRef.current.uniforms.uBaseColor.value.set(baseColor);
      materialRef.current.uniforms.uGlowColor.value.set(glowColor);
    }
  });

  return (
    <mesh ref={meshRef} position={[3, 0, 0]}>
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
