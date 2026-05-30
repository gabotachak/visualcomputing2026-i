import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Line, Html } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

const START = new THREE.Vector3(-4, 0, 0);
const END = new THREE.Vector3(4, 0, 0);
const CTRL1 = new THREE.Vector3(-2, 3, 0);
const CTRL2 = new THREE.Vector3(2, 3, 0);

function bezier(t, p0, p1, p2, p3) {
  const mt = 1 - t;
  return new THREE.Vector3(
    mt * mt * mt * p0.x + 3 * mt * mt * t * p1.x + 3 * mt * t * t * p2.x + t * t * t * p3.x,
    mt * mt * mt * p0.y + 3 * mt * mt * t * p1.y + 3 * mt * t * t * p2.y + t * t * t * p3.y,
    0
  );
}

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}

// Build bezier curve points for visualization
const bezierCurve = Array.from({ length: 50 }, (_, i) => {
  const t = i / 49;
  const p = bezier(t, START, CTRL1, CTRL2, END);
  return [p.x, p.y, p.z];
});

function Ball({ color, offset, label, mode, speed }) {
  const ref = useRef();
  const timeRef = useRef(0);

  useFrame((_, delta) => {
    timeRef.current = (timeRef.current + delta * speed) % 1;
    let t = timeRef.current;
    let pos;

    if (mode === 'lerp') {
      pos = new THREE.Vector3().lerpVectors(START, END, t);
    } else if (mode === 'ease') {
      const et = easeInOut(t);
      pos = new THREE.Vector3().lerpVectors(START, END, et);
    } else if (mode === 'bezier') {
      pos = bezier(t, START, CTRL1, CTRL2, END);
    } else if (mode === 'slerp') {
      // Slerp on rotation mapped to position arc
      const angle = t * Math.PI;
      pos = new THREE.Vector3(
        Math.cos(angle) * 4,
        Math.sin(angle) * 2,
        0
      );
    }

    if (ref.current) {
      ref.current.position.set(pos.x, pos.y + offset, pos.z);
    }
  });

  return (
    <group>
      <mesh ref={ref}>
        <sphereGeometry args={[0.25, 16, 16]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.2} />
        <Html center distanceFactor={10}>
          <div style={{ color, fontSize: '11px', whiteSpace: 'nowrap', pointerEvents: 'none' }}>{label}</div>
        </Html>
      </mesh>
    </group>
  );
}

export default function App() {
  const { speed } = useControls({ speed: { value: 0.3, min: 0.05, max: 1, step: 0.05, label: 'Speed' } });

  return (
    <Canvas camera={{ position: [0, 2, 10], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 8, 5]} intensity={1} />

      {/* Path indicators */}
      <Line points={[START.toArray(), END.toArray()]} color="#333" lineWidth={1} />
      <Line points={bezierCurve} color="#226" lineWidth={1} dashed />

      {/* Start/End markers */}
      {[START, END].map((p, i) => (
        <mesh key={i} position={p.toArray()}>
          <boxGeometry args={[0.2, 0.2, 0.2]} />
          <meshStandardMaterial color="#555" />
        </mesh>
      ))}

      <Ball color="#e44" offset={0} label="LERP" mode="lerp" speed={speed} />
      <Ball color="#4a4" offset={-1} label="Ease In/Out" mode="ease" speed={speed} />
      <Ball color="#44e" offset={-2} label="Bézier" mode="bezier" speed={speed} />
      <Ball color="orange" offset={1} label="SLERP arc" mode="slerp" speed={speed} />

      <gridHelper args={[12, 12, '#222', '#222']} position={[0, -1.5, 0]} />
      <OrbitControls makeDefault />
    </Canvas>
  );
}
