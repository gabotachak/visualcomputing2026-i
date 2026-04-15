import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { createGridPositions, gradientColor } from '../utils/geometryHelpers';

export default function GridGenerator({ gridSize, spacing, scale, rotationSpeed }) {
  const groupRef = useRef();

  const positions = useMemo(
    () => createGridPositions(gridSize, spacing),
    [gridSize, spacing]
  );

  useFrame(() => {
    if (groupRef.current) {
      groupRef.current.rotation.y += rotationSpeed;
    }
  });

  return (
    <group ref={groupRef}>
      {positions.map(([x, y, z], i) => {
        const t = i / positions.length;
        return (
          <mesh key={i} position={[x, y, z]} scale={[scale, scale, scale]}>
            <boxGeometry args={[1, 1, 1]} />
            <meshStandardMaterial color={gradientColor(t)} />
          </mesh>
        );
      })}
    </group>
  );
}
