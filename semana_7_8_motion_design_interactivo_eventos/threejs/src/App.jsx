import { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Html } from '@react-three/drei';
import * as THREE from 'three';

// Procedural humanoid figure made from primitives
function HumanoidFigure({ action }) {
  const bodyRef = useRef();
  const lArmRef = useRef();
  const rArmRef = useRef();
  const lLegRef = useRef();
  const rLegRef = useRef();
  const headRef = useRef();
  const timeRef = useRef(0);
  const [jumpY, setJumpY] = useState(0);
  const jumpVelRef = useRef(0);
  const onGround = useRef(true);

  useFrame((_, dt) => {
    timeRef.current += dt;
    const t = timeRef.current;

    // Jump physics
    if (!onGround.current) {
      jumpVelRef.current -= 15 * dt;
      setJumpY(y => {
        const ny = Math.max(0, y + jumpVelRef.current * dt);
        if (ny <= 0) { onGround.current = true; jumpVelRef.current = 0; }
        return ny;
      });
    }

    let lArmZ = 0, rArmZ = 0, lLegZ = 0, rLegZ = 0, bodyY = 0, headTilt = 0;

    if (action === 'idle') {
      lArmZ = Math.sin(t * 1.5) * 0.1;
      rArmZ = -Math.sin(t * 1.5) * 0.1;
      bodyY = Math.sin(t * 2) * 0.04;
    } else if (action === 'wave') {
      rArmZ = -Math.PI / 2 + Math.sin(t * 6) * 0.4;
      lArmZ = 0;
    } else if (action === 'run') {
      lArmZ = Math.sin(t * 8) * 0.6;
      rArmZ = -Math.sin(t * 8) * 0.6;
      lLegZ = Math.sin(t * 8 + Math.PI) * 0.8;
      rLegZ = Math.sin(t * 8) * 0.8;
      bodyY = Math.abs(Math.sin(t * 8)) * 0.1;
    } else if (action === 'dance') {
      lArmZ = Math.sin(t * 4) * 0.8 - 0.3;
      rArmZ = -(Math.cos(t * 4) * 0.8 - 0.3);
      lLegZ = Math.sin(t * 3) * 0.4;
      rLegZ = Math.cos(t * 3) * 0.4;
      headTilt = Math.sin(t * 5) * 0.3;
      bodyY = Math.sin(t * 6) * 0.1;
    }

    if (lArmRef.current) lArmRef.current.rotation.z = lArmZ;
    if (rArmRef.current) rArmRef.current.rotation.z = rArmZ;
    if (lLegRef.current) lLegRef.current.rotation.z = lLegZ;
    if (rLegRef.current) rLegRef.current.rotation.z = rLegZ;
    if (bodyRef.current) bodyRef.current.position.y = bodyY;
    if (headRef.current) headRef.current.rotation.z = headTilt;
  });

  const limbMat = <meshStandardMaterial color="#4a8" />;
  const bodyMat = <meshStandardMaterial color="#48c" />;

  return (
    <group position={[0, jumpY, 0]}>
      {/* Body */}
      <group ref={bodyRef}>
        {/* Torso */}
        <mesh position={[0, 1, 0]}><boxGeometry args={[0.8, 1, 0.4]} />{bodyMat}</mesh>
        {/* Head */}
        <group ref={headRef} position={[0, 1.8, 0]}>
          <mesh><sphereGeometry args={[0.35, 16, 16]} /><meshStandardMaterial color="#f4c" /></mesh>
          {/* Eyes */}
          <mesh position={[0.12, 0.05, 0.3]}><sphereGeometry args={[0.06, 8, 8]} /><meshStandardMaterial color="#222" /></mesh>
          <mesh position={[-0.12, 0.05, 0.3]}><sphereGeometry args={[0.06, 8, 8]} /><meshStandardMaterial color="#222" /></mesh>
        </group>
        {/* Left arm */}
        <group ref={lArmRef} position={[0.55, 1.3, 0]}>
          <mesh position={[0, -0.35, 0]}><boxGeometry args={[0.22, 0.7, 0.22]} />{limbMat}</mesh>
        </group>
        {/* Right arm */}
        <group ref={rArmRef} position={[-0.55, 1.3, 0]}>
          <mesh position={[0, -0.35, 0]}><boxGeometry args={[0.22, 0.7, 0.22]} />{limbMat}</mesh>
        </group>
        {/* Left leg */}
        <group ref={lLegRef} position={[0.25, 0.5, 0]}>
          <mesh position={[0, -0.45, 0]}><boxGeometry args={[0.25, 0.9, 0.25]} />{limbMat}</mesh>
        </group>
        {/* Right leg */}
        <group ref={rLegRef} position={[-0.25, 0.5, 0]}>
          <mesh position={[0, -0.45, 0]}><boxGeometry args={[0.25, 0.9, 0.25]} />{limbMat}</mesh>
        </group>
      </group>
    </group>
  );
}

const ACTIONS = ['idle', 'wave', 'run', 'dance', 'jump'];
const ACTION_LABELS = { idle: 'Idle (I)', wave: 'Wave (W)', run: 'Run (R)', dance: 'Dance (D)', jump: 'Jump (Space)' };

export default function App() {
  const [action, setAction] = useState('idle');
  const [jumpY, setJumpY] = useState(0);
  const jumpActive = useRef(false);

  useEffect(() => {
    const handleKey = e => {
      const k = e.key.toLowerCase();
      if (k === 'i') setAction('idle');
      else if (k === 'w') setAction('wave');
      else if (k === 'r') setAction('run');
      else if (k === 'd') setAction('dance');
      else if (k === ' ') { setAction('jump'); }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, []);

  return (
    <>
      <div style={{
        position: 'fixed', top: 20, left: 20, zIndex: 100,
        background: 'rgba(0,0,0,0.85)', padding: '16px', borderRadius: '10px',
        display: 'flex', flexDirection: 'column', gap: '8px',
      }}>
        <div style={{ color: '#fff', fontWeight: 'bold', marginBottom: 4, fontFamily: 'sans-serif' }}>
          Motion Design — {action.toUpperCase()}
        </div>
        {ACTIONS.map(a => (
          <button key={a} onClick={() => setAction(a)} style={{
            padding: '8px 14px', background: action === a ? '#4af' : '#333',
            color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer',
            fontFamily: 'sans-serif', fontSize: '13px',
          }}>{ACTION_LABELS[a]}</button>
        ))}
        <div style={{ color: '#888', fontSize: '11px', marginTop: 4, fontFamily: 'monospace' }}>
          Keys: I W R D Space
        </div>
      </div>
      <Canvas camera={{ position: [0, 2, 7], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 8, 5]} intensity={1} />
        <HumanoidFigure action={action} />
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
          <planeGeometry args={[12, 12]} />
          <meshStandardMaterial color="#1a1a2e" />
        </mesh>
        <gridHelper args={[12, 12, '#222', '#222']} />
        <OrbitControls makeDefault />
      </Canvas>
    </>
  );
}
