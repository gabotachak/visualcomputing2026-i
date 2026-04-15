import { Suspense } from 'react';
import { OrbitControls, Stats } from '@react-three/drei';
import PBRMaterial from './PBRMaterial.jsx';
import BasicMaterial from './BasicMaterial.jsx';

export default function Scene({ metalness, roughness, showBasic }) {
  return (
    <>
      {/* Lights */}
      <ambientLight intensity={0.5} />
      <directionalLight
        position={[5, 5, 5]}
        intensity={1.0}
        castShadow
      />
      <directionalLight position={[-3, 2, -3]} intensity={0.3} />

      {/* Floor */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.2, 0]} receiveShadow>
        <planeGeometry args={[10, 10]} />
        <meshStandardMaterial color="#444444" roughness={0.9} metalness={0.0} />
      </mesh>

      {/* PBR Sphere */}
      <Suspense fallback={null}>
        <PBRMaterial metalness={metalness} roughness={roughness} />
      </Suspense>

      {/* Basic Sphere */}
      <BasicMaterial visible={showBasic} />

      {/* Camera controls */}
      <OrbitControls target={[0, 0, 0]} />

      {/* Labels via HTML overlay handled in App */}
    </>
  );
}
