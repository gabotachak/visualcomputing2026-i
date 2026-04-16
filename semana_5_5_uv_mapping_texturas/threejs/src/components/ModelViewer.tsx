import { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { Text } from '@react-three/drei';

interface ModelViewerProps {
  geometry: THREE.BufferGeometry;
  label: string;
  position: [number, number, number];
  texture: THREE.Texture;
  uvRepeat?: [number, number];
  uvOffset?: [number, number];
  uvRotation?: number;
}

export default function ModelViewer({
  geometry,
  label,
  position,
  texture,
  uvRepeat = [1, 1],
  uvOffset = [0, 0],
  uvRotation = 0,
}: ModelViewerProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  useEffect(() => {
    const mesh = meshRef.current;
    if (!mesh) return;
    const mat = mesh.material as THREE.MeshStandardMaterial;
    if (!mat.map) return;
    mat.map.repeat.set(uvRepeat[0], uvRepeat[1]);
    mat.map.offset.set(uvOffset[0], uvOffset[1]);
    mat.map.rotation = uvRotation;
    mat.map.needsUpdate = true;
  }, [uvRepeat, uvOffset, uvRotation]);

  // Clone texture so each model has independent UV transform state.
  const clonedTexture = texture.clone();
  clonedTexture.needsUpdate = true;

  return (
    <group position={position}>
      <mesh ref={meshRef} geometry={geometry}>
        <meshStandardMaterial map={clonedTexture} />
      </mesh>
      <Text
        position={[0, -1.6, 0]}
        fontSize={0.22}
        color="#222222"
        anchorX="center"
        anchorY="top"
        maxWidth={3}
      >
        {label}
      </Text>
    </group>
  );
}
