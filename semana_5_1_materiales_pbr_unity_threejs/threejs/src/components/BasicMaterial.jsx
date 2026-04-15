import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

export default function BasicMaterial({ visible }) {
  const meshRef = useRef();

  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.4;
    }
  });

  return (
    <mesh ref={meshRef} position={[1.5, 0, 0]} visible={visible}>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        color={[200 / 255, 150 / 255, 100 / 255]}
        roughness={0.6}
        metalness={0.0}
      />
    </mesh>
  );
}
