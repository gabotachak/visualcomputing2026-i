import { useRef } from 'react';
import { useFrame, useLoader } from '@react-three/fiber';
import * as THREE from 'three';

export default function PBRMaterial({ metalness, roughness }) {
  const meshRef = useRef();

  const [albedo, roughnessMap, metalnessMap, normalMap] = useLoader(THREE.TextureLoader, [
    '/textures/Metal007_1K-JPG_Color.jpg',
    '/textures/Metal007_1K-JPG_Roughness.jpg',
    '/textures/Metal007_1K-JPG_Metalness.jpg',
    '/textures/Metal007_1K-JPG_NormalGL.jpg',
  ]);

  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.4;
    }
  });

  return (
    <mesh ref={meshRef} position={[-1.5, 0, 0]}>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        map={albedo}
        roughnessMap={roughnessMap}
        metalnessMap={metalnessMap}
        normalMap={normalMap}
        roughness={roughness}
        metalness={metalness}
      />
    </mesh>
  );
}
