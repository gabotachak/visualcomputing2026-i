import { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Text, Html, Grid } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

function XRScene({ speed }) {
  const groupRef = useRef();
  const timeRef = useRef(0);

  useFrame((_, dt) => {
    timeRef.current += dt;
    // Floating objects in XR scene
  });

  const objects = [
    { pos: [0, 1, -3], color: '#4af', shape: 'box', label: 'Object A' },
    { pos: [3, 0.5, 0], color: '#4e4', shape: 'sphere', label: 'Object B' },
    { pos: [-3, 1, -1], color: '#f84', shape: 'torus', label: 'Object C' },
    { pos: [0, 2, -6], color: '#a4e', shape: 'cylinder', label: 'Object D' },
  ];

  return (
    <group ref={groupRef}>
      {objects.map((obj, i) => (
        <FloatingInteractable key={i} {...obj} index={i} speed={speed} />
      ))}
      {/* Floor grid */}
      <mesh rotation={[-Math.PI/2, 0, 0]} position={[0, 0, 0]}>
        <planeGeometry args={[20, 20]} />
        <meshStandardMaterial color="#0a0a1e" />
      </mesh>
      <Grid args={[20, 20]} position={[0, 0.01, 0]} cellColor="#1a1a3e" sectionColor="#2a2a5e" />
    </group>
  );
}

function FloatingInteractable({ pos, color, shape, label, index, speed }) {
  const ref = useRef();
  const [hovered, setHovered] = useState(false);
  const [clicked, setClicked] = useState(false);
  const phase = index * Math.PI / 2;

  useFrame(({ clock }) => {
    if (ref.current) {
      ref.current.position.y = pos[1] + Math.sin(clock.elapsedTime * speed + phase) * 0.3;
      if (!clicked) ref.current.rotation.y += 0.01;
    }
  });

  return (
    <mesh ref={ref} position={pos}
      onPointerOver={() => setHovered(true)}
      onPointerOut={() => setHovered(false)}
      onClick={() => setClicked(c => !c)}
      scale={hovered ? 1.2 : 1}>
      {shape === 'box' && <boxGeometry args={[0.8, 0.8, 0.8]} />}
      {shape === 'sphere' && <sphereGeometry args={[0.5, 32, 32]} />}
      {shape === 'torus' && <torusGeometry args={[0.4, 0.15, 16, 32]} />}
      {shape === 'cylinder' && <cylinderGeometry args={[0.3, 0.3, 0.8, 32]} />}
      <meshStandardMaterial color={clicked ? 'white' : color} emissive={color}
        emissiveIntensity={hovered ? 0.5 : 0.1} metalness={0.4} roughness={0.3} />
      {hovered && (
        <Html center distanceFactor={6}>
          <div style={{color:'white',background:'rgba(0,0,0,0.8)',padding:'4px 8px',borderRadius:'4px',fontSize:'12px',whiteSpace:'nowrap'}}>
            {label} {clicked ? '✓' : ''}
          </div>
        </Html>
      )}
    </mesh>
  );
}

function FlyCamera() {
  const { camera } = useThree();
  const keysRef = useRef(new Set());
  useEffect(() => {
    const dn = e => keysRef.current.add(e.key.toLowerCase());
    const up = e => keysRef.current.delete(e.key.toLowerCase());
    window.addEventListener('keydown', dn);
    window.addEventListener('keyup', up);
    return () => { window.removeEventListener('keydown', dn); window.removeEventListener('keyup', up); };
  }, []);
  useFrame((_, dt) => {
    const k = keysRef.current;
    const spd = 4 * dt;
    const dir = new THREE.Vector3();
    camera.getWorldDirection(dir);
    if (k.has('w')) camera.position.addScaledVector(dir, spd);
    if (k.has('s')) camera.position.addScaledVector(dir, -spd);
    if (k.has('a')) camera.position.x -= spd;
    if (k.has('d')) camera.position.x += spd;
    if (k.has('q')) camera.position.y -= spd;
    if (k.has('e')) camera.position.y += spd;
  });
  return null;
}

export default function App() {
  const { speed, flyMode } = useControls({
    speed: { value: 0.8, min: 0.1, max: 3, label: 'Float speed' },
    flyMode: { value: false, label: 'FlyCamera (WASD/QE)' },
  });

  return (
    <>
      <div style={{
        position:'fixed', top:10, left:10, color:'white', background:'rgba(0,0,0,0.8)',
        padding:'12px 16px', borderRadius:'8px', fontFamily:'monospace', fontSize:'12px', zIndex:100,
      }}>
        <div style={{color:'#4af',fontWeight:'bold',marginBottom:8}}>XR Immersive Scene</div>
        <div>Orbit: drag | Zoom: scroll</div>
        <div>Click objects to interact</div>
        <div style={{color:'#f84'}}>FlyMode: WASD + Q/E</div>
      </div>
      <Canvas camera={{ position: [0, 3, 8], fov: 70 }}>
        <ambientLight intensity={0.3} />
        <directionalLight position={[5, 10, 5]} intensity={1} />
        <pointLight position={[0, 5, 0]} intensity={0.5} color="#4af" />
        <XRScene speed={speed} />
        {flyMode ? <FlyCamera /> : <OrbitControls makeDefault />}
      </Canvas>
    </>
  );
}
