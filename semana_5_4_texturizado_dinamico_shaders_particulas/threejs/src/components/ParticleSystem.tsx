import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { generateRandomPositions } from '../utils/particleHelpers';

interface ParticleSystemProps {
  position: [number, number, number];
  count: number;
  color: THREE.Color;
  speed: number;
  lifespan: number;
  size: number;
  emitRadius: number;
}

export default function ParticleSystem({
  position,
  count,
  color,
  speed,
  lifespan,
  size,
  emitRadius,
}: ParticleSystemProps) {
  const geometryRef = useRef<THREE.BufferGeometry>(null!);
  const agesRef = useRef<Float32Array>(new Float32Array(count));

  const initialPositions = useMemo(() => generateRandomPositions(count, emitRadius), [count, emitRadius]);

  useMemo(() => {
    const now = Date.now();
    // Stagger initial ages so particles don't all die at once
    for (let i = 0; i < count; i++) {
      agesRef.current[i] = now - Math.random() * lifespan * 1000;
    }
  }, [count, lifespan]);

  useFrame(() => {
    if (!geometryRef.current) return;
    const positions = geometryRef.current.attributes.position.array as Float32Array;
    const ages = agesRef.current;

    for (let i = 0; i < count; i++) {
      const idx = i * 3;
      const age = (Date.now() - ages[i]) / (lifespan * 1000);

      if (age > 1.0) {
        // Regenerate particle at random position within emit radius
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        const r = Math.random() * emitRadius * 0.5;
        positions[idx] = r * Math.sin(phi) * Math.cos(theta);
        positions[idx + 1] = r * Math.sin(phi) * Math.sin(theta);
        positions[idx + 2] = r * Math.cos(phi);
        ages[i] = Date.now();
      } else {
        // Move particle outward
        const dx = positions[idx];
        const dy = positions[idx + 1];
        const dz = positions[idx + 2];
        const length = Math.sqrt(dx * dx + dy * dy + dz * dz) || 0.001;

        positions[idx] += (dx / length) * speed;
        positions[idx + 1] += (dy / length) * speed;
        positions[idx + 2] += (dz / length) * speed;
      }
    }

    geometryRef.current.attributes.position.needsUpdate = true;
  });

  return (
    <points position={position}>
      <bufferGeometry ref={geometryRef}>
        <bufferAttribute
          attach="attributes-position"
          args={[initialPositions, 3]}
        />
      </bufferGeometry>
      <pointsMaterial
        color={color}
        size={size}
        sizeAttenuation
        transparent
        opacity={0.7}
        depthWrite={false}
      />
    </points>
  );
}
