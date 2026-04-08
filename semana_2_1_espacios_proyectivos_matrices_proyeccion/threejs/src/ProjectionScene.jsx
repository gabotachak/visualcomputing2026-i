import React from 'react';
import { Text } from '@react-three/drei';

// Three boxes at different depths to visualize the difference
// between perspective and orthographic projection
const OBJECTS = [
  { position: [0, 0, 0],   color: '#ef4444', label: 'Z = 0\n(cercano)',  size: 1.2 },
  { position: [0, 0, -5],  color: '#22c55e', label: 'Z = -5\n(medio)',   size: 1.2 },
  { position: [0, 0, -10], color: '#3b82f6', label: 'Z = -10\n(lejano)', size: 1.2 },
];

function DepthBox({ position, color, label, size }) {
  return (
    <group position={position}>
      <mesh>
        <boxGeometry args={[size, size, size]} />
        <meshStandardMaterial color={color} roughness={0.4} metalness={0.3} />
      </mesh>
      {/* Vertical pole to indicate depth */}
      <mesh position={[0, -size / 2 - 2, 0]}>
        <cylinderGeometry args={[0.03, 0.03, 4, 8]} />
        <meshStandardMaterial color={color} opacity={0.5} transparent />
      </mesh>
      <Text
        position={[0, size / 2 + 0.5, 0]}
        fontSize={0.35}
        color="white"
        anchorX="center"
        anchorY="bottom"
        outlineWidth={0.025}
        outlineColor="#000000"
      >
        {label}
      </Text>
    </group>
  );
}

// Floor grid to enhance depth perception
function Floor() {
  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.5, -5]}>
      <planeGeometry args={[20, 14]} />
      <meshStandardMaterial color="#27272a" roughness={1} />
    </mesh>
  );
}

// Grid lines on the floor for stronger depth cues
function GridLines() {
  return (
    <group position={[0, -1.49, -5]}>
      <gridHelper args={[20, 20, '#3f3f46', '#3f3f46']} rotation={[0, 0, 0]} />
    </group>
  );
}

export default function ProjectionScene() {
  return (
    <>
      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 10, 5]} intensity={1.2} castShadow />
      <directionalLight position={[-5, -5, -5]} intensity={0.3} color="#8b5cf6" />

      <Floor />
      <GridLines />

      {OBJECTS.map((obj) => (
        <DepthBox key={obj.label} {...obj} />
      ))}

      {/* Depth axis: a thin rod along Z to reinforce depth cue */}
      <mesh position={[2.5, -1.4, -5]} rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.04, 0.04, 12, 8]} />
        <meshStandardMaterial color="#facc15" />
      </mesh>
    </>
  );
}
