import { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Html } from '@react-three/drei';
import * as THREE from 'three';

function InfoPanel({ pos, vel, keys, clicks }) {
  return (
    <div style={{
      position: 'fixed', top: 20, left: 20, background: 'rgba(0,0,0,0.8)',
      color: '#4af', padding: '16px', borderRadius: '8px', fontFamily: 'monospace', fontSize: '13px',
      zIndex: 100, minWidth: '200px',
    }}>
      <div style={{ color: '#fff', marginBottom: 8, fontSize: 14, fontWeight: 'bold' }}>3D Input & UI</div>
      <div>Position: ({pos.map(v => v.toFixed(2)).join(', ')})</div>
      <div>Velocity: ({vel.map(v => v.toFixed(2)).join(', ')})</div>
      <div>Keys: {keys.join(' ') || 'none'}</div>
      <div>Clicks: {clicks}</div>
      <div style={{ marginTop: 12, color: '#888', fontSize: 11 }}>
        WASD: move | Arrow: rotate | Space: jump | R: reset
      </div>
    </div>
  );
}

function Cube({ keysRef, onClick, onPosChange }) {
  const ref = useRef();
  const vel = useRef(new THREE.Vector3());
  const angVel = useRef(new THREE.Vector3());
  const jumpRef = useRef(false);

  useFrame((_, dt) => {
    const k = keysRef.current;
    const speed = 5, rSpeed = 2;
    const acc = new THREE.Vector3(
      (k.has('d') || k.has('arrowright') ? 1 : 0) - (k.has('a') || k.has('arrowleft') ? 1 : 0),
      0,
      (k.has('s') || k.has('arrowdown') ? 1 : 0) - (k.has('w') || k.has('arrowup') ? 1 : 0)
    ).multiplyScalar(speed);

    vel.current.add(acc.multiplyScalar(dt));
    vel.current.multiplyScalar(0.85); // friction

    ref.current.position.add(vel.current.clone().multiplyScalar(dt));
    ref.current.position.x = Math.max(-4, Math.min(4, ref.current.position.x));
    ref.current.position.z = Math.max(-4, Math.min(4, ref.current.position.z));

    if (k.has(' ') && !jumpRef.current) {
      vel.current.y = 6;
      jumpRef.current = true;
    }
    vel.current.y -= 12 * dt; // gravity
    ref.current.position.y = Math.max(0, ref.current.position.y + vel.current.y * dt);
    if (ref.current.position.y <= 0) { vel.current.y = 0; jumpRef.current = false; }

    ref.current.rotation.y += (k.has('e') ? 1 : k.has('q') ? -1 : 0) * rSpeed * dt;

    onPosChange(
      [ref.current.position.x, ref.current.position.y, ref.current.position.z],
      [vel.current.x, vel.current.y, vel.current.z]
    );
  });

  return (
    <mesh ref={ref} position={[0, 0, 0]} onClick={onClick} castShadow>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#e44" metalness={0.3} roughness={0.4} />
    </mesh>
  );
}

export default function App() {
  const keysRef = useRef(new Set());
  const [activeKeys, setActiveKeys] = useState([]);
  const [pos, setPos] = useState([0, 0, 0]);
  const [vel, setVel] = useState([0, 0, 0]);
  const [clicks, setClicks] = useState(0);
  const [orbitEnabled, setOrbitEnabled] = useState(true);

  useEffect(() => {
    const dn = e => {
      keysRef.current.add(e.key.toLowerCase());
      if (e.key.toLowerCase() === 'r') keysRef.current.add('reset');
      setActiveKeys([...keysRef.current]);
      if ([' ', 'arrowup', 'arrowdown'].includes(e.key.toLowerCase())) e.preventDefault();
    };
    const up = e => { keysRef.current.delete(e.key.toLowerCase()); setActiveKeys([...keysRef.current]); };
    window.addEventListener('keydown', dn);
    window.addEventListener('keyup', up);
    return () => { window.removeEventListener('keydown', dn); window.removeEventListener('keyup', up); };
  }, []);

  return (
    <>
      <InfoPanel pos={pos} vel={vel} keys={activeKeys.filter(k => ['w','a','s','d',' ','q','e'].includes(k))} clicks={clicks} />
      <Canvas camera={{ position: [0, 4, 8], fov: 50 }} shadows>
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 10, 5]} intensity={1} castShadow />
        <Cube keysRef={keysRef}
          onClick={() => setClicks(c => c + 1)}
          onPosChange={(p, v) => { setPos(p); setVel(v); }} />
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]} receiveShadow>
          <planeGeometry args={[10, 10]} />
          <meshStandardMaterial color="#1a1a2e" />
        </mesh>
        <gridHelper args={[10, 10, '#333', '#222']} />
        <OrbitControls makeDefault enablePan={false} />
      </Canvas>
    </>
  );
}
