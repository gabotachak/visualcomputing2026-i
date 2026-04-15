import React, { useRef, useMemo } from 'react';
import * as THREE from 'three';
import vertexShader from '../shaders/gradient/vertex.glsl?raw';
import fragmentShader from '../shaders/gradient/fragment.glsl?raw';

interface GradientShaderProps {
  colorTop: string;
  colorBottom: string;
}

export default function GradientShader({ colorTop, colorBottom }: GradientShaderProps) {
  const materialRef = useRef<THREE.ShaderMaterial>(null);

  const uniforms = useMemo(
    () => ({
      colorTop: { value: new THREE.Color(colorTop) },
      colorBottom: { value: new THREE.Color(colorBottom) },
    }),
    []
  );

  if (materialRef.current) {
    materialRef.current.uniforms.colorTop.value.set(colorTop);
    materialRef.current.uniforms.colorBottom.value.set(colorBottom);
  }

  return (
    <mesh position={[-3, 0, 0]}>
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
