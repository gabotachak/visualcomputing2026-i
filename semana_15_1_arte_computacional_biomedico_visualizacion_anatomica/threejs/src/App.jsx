import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere, Text, Html } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

// Procedural anatomy visualization: layered spheres representing body systems
function AnatomyModel({ showBones, showMuscles, showNervous, showCirculatory, opacity }) {
  const groupRef = useRef();
  useFrame((_, d) => { if (groupRef.current) groupRef.current.rotation.y += d * 0.15; });

  return (
    <group ref={groupRef}>
      {/* Skin layer */}
      <Sphere args={[1.5, 64, 64]}>
        <meshStandardMaterial color="#f4b880" transparent opacity={opacity * 0.25} side={THREE.DoubleSide} />
      </Sphere>

      {/* Bones */}
      {showBones && (
        <>
          <mesh position={[0, 0, 0]}>
            <cylinderGeometry args={[0.08, 0.08, 2.5, 16]} />
            <meshStandardMaterial color="#e8e0d0" />
          </mesh>
          {[-0.4, 0.4].map((x, i) => (
            <mesh key={i} position={[x, 0.8, 0]} rotation={[0, 0, x * 0.4]}>
              <cylinderGeometry args={[0.05, 0.05, 1.2, 12]} />
              <meshStandardMaterial color="#e8e0d0" />
            </mesh>
          ))}
          {[-0.4, 0.4].map((x, i) => (
            <mesh key={i} position={[x, -0.6, 0]} rotation={[0, 0, 0]}>
              <cylinderGeometry args={[0.06, 0.06, 1.0, 12]} />
              <meshStandardMaterial color="#e8e0d0" />
            </mesh>
          ))}
        </>
      )}

      {/* Muscles */}
      {showMuscles && (
        <>
          {[[-0.3, 0.5, 0.2], [0.3, 0.5, 0.2], [-0.3, -0.2, 0.3], [0.3, -0.2, 0.3]].map((pos, i) => (
            <mesh key={i} position={pos} rotation={[0.2 * (i%2 ? 1:-1), 0, 0.3*(i<2?1:-1)]}>
              <capsuleGeometry args={[0.12, 0.7, 8, 16]} />
              <meshStandardMaterial color="#c44040" transparent opacity={0.7} />
            </mesh>
          ))}
        </>
      )}

      {/* Nervous system */}
      {showNervous && (
        <mesh>
          <cylinderGeometry args={[0.02, 0.02, 2.4, 8]} />
          <meshStandardMaterial color="#ffff50" emissive="#ffff50" emissiveIntensity={0.4} />
        </mesh>
      )}

      {/* Circulatory */}
      {showCirculatory && (
        <group>
          <mesh position={[0, 0.3, 0.3]}>
            <sphereGeometry args={[0.25, 32, 32]} />
            <meshStandardMaterial color="#e44" emissive="#e44" emissiveIntensity={0.3} />
          </mesh>
          {[0, 1, 2, 3].map(i => (
            <mesh key={i} position={[
              Math.sin(i*Math.PI/2)*0.6, Math.cos(i*Math.PI/2)*0.3, 0.2
            ]}>
              <cylinderGeometry args={[0.015, 0.015, 0.8, 8]}
                rotation={[Math.cos(i*Math.PI/2)*0.5, 0, Math.sin(i*Math.PI/2)*0.5]} />
              <meshStandardMaterial color="#e44" />
            </mesh>
          ))}
        </group>
      )}
    </group>
  );
}

export default function App() {
  const { showBones, showMuscles, showNervous, showCirculatory, opacity } = useControls({
    showBones: { value: true, label: 'Sistema óseo' },
    showMuscles: { value: true, label: 'Músculos' },
    showNervous: { value: true, label: 'Sistema nervioso' },
    showCirculatory: { value: true, label: 'Sistema circulatorio' },
    opacity: { value: 0.6, min: 0.1, max: 1, step: 0.05, label: 'Opacidad piel' },
  });

  return (
    <Canvas camera={{ position: [0, 0, 5], fov: 50 }}>
      <ambientLight intensity={0.4} />
      <directionalLight position={[5, 5, 5]} intensity={1} />
      <pointLight position={[-3, 3, 3]} intensity={0.5} color="#4af" />
      <AnatomyModel showBones={showBones} showMuscles={showMuscles}
        showNervous={showNervous} showCirculatory={showCirculatory} opacity={opacity} />
      <OrbitControls makeDefault />
    </Canvas>
  );
}
