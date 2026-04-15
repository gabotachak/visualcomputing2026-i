import React, { useRef, useMemo, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { createSpiralPositions, gradientColor } from '../utils/geometryHelpers';

export default function SpiralGenerator({
  turns,
  segments,
  radius,
  height,
  scaleVariation,
  animationSpeed,
}) {
  const timeRef = useRef(0);
  const [dynamicRadius, setDynamicRadius] = useState(radius);

  useFrame((_, delta) => {
    timeRef.current += delta * animationSpeed * 60;
    const newRadius = radius + Math.sin(timeRef.current * 0.05) * (radius * 0.4);
    setDynamicRadius(newRadius);
  });

  const items = useMemo(
    () => createSpiralPositions(turns, segments, dynamicRadius, height),
    [turns, segments, dynamicRadius, height]
  );

  return (
    <group>
      {items.map(({ position, t }, i) => {
        const s = 1 + (t - 0.5) * scaleVariation;
        return (
          <mesh key={i} position={position} scale={[s, s, s]}>
            <cylinderGeometry args={[0.1, 0.15, 0.4, 8]} />
            <meshStandardMaterial color={gradientColor(t)} />
          </mesh>
        );
      })}
    </group>
  );
}
