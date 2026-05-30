import { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

function ParametricObjects({ count, spread, colorMode, rotate }) {
  const group = useRef();
  useFrame((_, d) => { if (rotate && group.current) group.current.rotation.y += d * 0.2; });

  const objects = useMemo(() => {
    return Array.from({ length: count }, (_, i) => {
      const t = i / count;
      const angle = t * Math.PI * 2 * 3;
      const radius = t * spread;
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      const y = (t - 0.5) * spread * 0.8;
      const size = 0.15 + t * 0.4;
      const shapeType = i % 3;

      let color;
      if (colorMode === 'rainbow') color = new THREE.Color().setHSL(t, 0.9, 0.55);
      else if (colorMode === 'heat') color = new THREE.Color(1, 1 - t, 0);
      else color = new THREE.Color(0.3 + t * 0.5, 0.6, 0.9 - t * 0.4);

      return { pos: [x, y, z], size, color: '#' + color.getHexString(), shapeType };
    });
  }, [count, spread, colorMode]);

  return (
    <group ref={group}>
      {objects.map((o, i) => (
        <mesh key={i} position={o.pos}>
          {o.shapeType === 0 ? <boxGeometry args={[o.size, o.size, o.size]} />
            : o.shapeType === 1 ? <sphereGeometry args={[o.size * 0.6, 12, 12]} />
            : <coneGeometry args={[o.size * 0.5, o.size, 8]} />}
          <meshStandardMaterial color={o.color} />
        </mesh>
      ))}
    </group>
  );
}

export default function App() {
  const { count, spread, colorMode, rotate } = useControls({
    count: { value: 80, min: 10, max: 300, step: 1, label: 'Object count' },
    spread: { value: 5, min: 1, max: 12, step: 0.5, label: 'Spread' },
    colorMode: { value: 'rainbow', options: ['rainbow', 'heat', 'cool'], label: 'Color mode' },
    rotate: { value: true, label: 'Auto-rotate' },
  });

  return (
    <Canvas camera={{ position: [0, 8, 14], fov: 55 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <ParametricObjects count={count} spread={spread} colorMode={colorMode} rotate={rotate} />
      <gridHelper args={[20, 20, '#222', '#222']} position={[0, -3, 0]} />
      <OrbitControls makeDefault />
    </Canvas>
  );
}
