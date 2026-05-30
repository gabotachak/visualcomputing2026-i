import { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { useControls, button } from 'leva';

const SHAPES = ['box', 'sphere', 'torus', 'cylinder'];
const COLORS = ['#e44', '#4a4', '#44e', '#ea4', '#a4e', '#4ae'];

function Scene({ shape, color, scale, wireframe, autoRotate, lightColor, lightIntensity }) {
  const ref = useRef();
  useFrame((_, d) => { if (autoRotate && ref.current) ref.current.rotation.y += d; });

  const geo = shape === 'box' ? <boxGeometry args={[2, 2, 2]} />
    : shape === 'sphere' ? <sphereGeometry args={[1.2, 32, 32]} />
    : shape === 'torus' ? <torusGeometry args={[1, 0.4, 16, 32]} />
    : <cylinderGeometry args={[0.8, 0.8, 2, 32]} />;

  return (
    <>
      <ambientLight intensity={0.4} />
      <pointLight position={[4, 4, 4]} intensity={lightIntensity} color={lightColor} />
      <pointLight position={[-4, -4, 4]} intensity={0.4} color="#88f" />
      <mesh ref={ref} scale={scale}>
        {geo}
        <meshStandardMaterial color={color} wireframe={wireframe} metalness={0.3} roughness={0.4} />
      </mesh>
      <gridHelper args={[10, 10, '#222', '#222']} position={[0, -2, 0]} />
    </>
  );
}

export default function App() {
  const [shapeIdx, setShapeIdx] = useState(0);

  const { color, scale, wireframe, autoRotate, lightColor, lightIntensity } = useControls({
    color: { value: '#e44', label: 'Color' },
    scale: { value: 1, min: 0.2, max: 3, step: 0.05, label: 'Scale' },
    wireframe: { value: false, label: 'Wireframe' },
    autoRotate: { value: true, label: 'Auto-rotate' },
    lightColor: { value: '#ffffff', label: 'Light color' },
    lightIntensity: { value: 2, min: 0, max: 8, step: 0.1, label: 'Light intensity' },
    'Next Shape': button(() => setShapeIdx(i => (i + 1) % SHAPES.length)),
    'Random Color': button(() => {}),
  });

  return (
    <Canvas camera={{ position: [0, 1, 6], fov: 50 }}>
      <Scene shape={SHAPES[shapeIdx]} color={color} scale={scale}
        wireframe={wireframe} autoRotate={autoRotate}
        lightColor={lightColor} lightIntensity={lightIntensity} />
      <OrbitControls makeDefault />
    </Canvas>
  );
}
