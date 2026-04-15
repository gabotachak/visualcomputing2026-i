import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function FractalTerrain({
  width,
  depth,
  segments,
  octaves,
  amplitude,
  frequency,
  speed,
  wireframe,
}) {
  const meshRef = useRef();
  const timeRef = useRef(0);

  // Create geometry once (or when structural params change).
  // We rotate the plane so it lies flat on XZ.
  const geometry = useMemo(() => {
    const geo = new THREE.PlaneGeometry(width, depth, segments, segments);
    geo.rotateX(-Math.PI / 2);
    return geo;
  }, [width, depth, segments]);

  useFrame((_, delta) => {
    if (!meshRef.current) return;
    timeRef.current += delta * speed;

    // Direct access to the position buffer — this is what req #3 asks for.
    const posArray = geometry.attributes.position.array;

    for (let i = 0; i < geometry.attributes.position.count; i++) {
      const x = posArray[i * 3];       // x coordinate
      const z = posArray[i * 3 + 2];   // z coordinate (plane was rotated)

      // Fractal Brownian Motion: sum N octaves, each halving amplitude and doubling frequency.
      let y = 0;
      let amp = amplitude;
      let freq = frequency;
      for (let oct = 0; oct < octaves; oct++) {
        y +=
          Math.sin(x * freq + timeRef.current) *
          Math.cos(z * freq * 0.8 + timeRef.current * 0.7) *
          amp;
        amp *= 0.5;
        freq *= 2.0;
      }

      posArray[i * 3 + 1] = y; // overwrite Y in the buffer
    }

    geometry.attributes.position.needsUpdate = true;
    geometry.computeVertexNormals(); // recompute normals for correct lighting
  });

  return (
    <mesh ref={meshRef} geometry={geometry}>
      <meshStandardMaterial
        color="#44aaff"
        side={THREE.DoubleSide}
        wireframe={wireframe}
      />
    </mesh>
  );
}
