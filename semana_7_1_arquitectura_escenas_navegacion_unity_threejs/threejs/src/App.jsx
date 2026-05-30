import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Html } from '@react-three/drei';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';

function RotatingBox({ color }) {
  const ref = useRef();
  useFrame((_, d) => { ref.current.rotation.y += d * 0.8; ref.current.rotation.x += d * 0.3; });
  return (
    <mesh ref={ref}>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color={color} />
    </mesh>
  );
}

function MenuScene() {
  return (
    <>
      <Canvas camera={{ position: [0, 0, 6], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 5, 5]} intensity={1} />
        <RotatingBox color="#e44" />
        <OrbitControls makeDefault />
      </Canvas>
      <nav style={navStyle}>
        <h1 style={{ color: '#fff', marginBottom: 16, fontSize: 20 }}>Visual Computing — Menu</h1>
        <Link to="/juego" style={btnStyle('#e44')}>Juego 3D</Link>
        <Link to="/creditos" style={btnStyle('#44e')}>Créditos</Link>
      </nav>
    </>
  );
}

function GameScene() {
  const ref = useRef();
  useFrame = undefined; // suppress linting — used in inner component
  return (
    <>
      <Canvas camera={{ position: [0, 2, 8], fov: 50 }}>
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 10, 5]} intensity={1.2} />
        <Particles />
        <gridHelper args={[10, 10, '#333', '#333']} position={[0, -1, 0]} />
        <OrbitControls makeDefault />
      </Canvas>
      <nav style={navStyle}>
        <h1 style={{ color: '#4af', marginBottom: 16, fontSize: 20 }}>Escena de Juego</h1>
        <Link to="/" style={btnStyle('#555')}>← Menu</Link>
        <Link to="/creditos" style={btnStyle('#44e')}>Créditos</Link>
      </nav>
    </>
  );
}

function Particles() {
  const positions = Array.from({ length: 30 }, (_, i) => ({
    pos: [(Math.random() - 0.5) * 8, (Math.random() - 0.5) * 4, (Math.random() - 0.5) * 4],
    color: ['#e44', '#4a4', '#44e', '#ea4', '#4ae'][i % 5],
    speed: 0.3 + Math.random() * 0.7,
    phase: Math.random() * Math.PI * 2,
  }));

  return (
    <>
      {positions.map((p, i) => (
        <AnimSphere key={i} basePos={p.pos} color={p.color} speed={p.speed} phase={p.phase} />
      ))}
    </>
  );
}

function AnimSphere({ basePos, color, speed, phase }) {
  const ref = useRef();
  useFrame(({ clock }) => {
    const t = clock.elapsedTime * speed + phase;
    ref.current.position.set(basePos[0] + Math.sin(t) * 0.5, basePos[1] + Math.cos(t * 0.7) * 0.5, basePos[2]);
  });
  return (
    <mesh ref={ref} position={basePos}>
      <sphereGeometry args={[0.2, 12, 12]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.3} />
    </mesh>
  );
}

function CreditsScene() {
  return (
    <>
      <Canvas camera={{ position: [0, 0, 8], fov: 50 }}>
        <ambientLight intensity={0.3} />
        <pointLight position={[0, 3, 3]} intensity={2} color="white" />
        <StarField />
        <OrbitControls makeDefault />
      </Canvas>
      <nav style={navStyle}>
        <h1 style={{ color: '#fa4', marginBottom: 12, fontSize: 20 }}>Créditos</h1>
        <p style={{ color: '#ccc', marginBottom: 8, fontSize: 14 }}>Gabriel Andrés Anzola Tachak</p>
        <p style={{ color: '#888', marginBottom: 16, fontSize: 12 }}>Computación Visual — 2026-I</p>
        <Link to="/" style={btnStyle('#555')}>← Menu</Link>
      </nav>
    </>
  );
}

function StarField() {
  const stars = Array.from({ length: 100 }, () => ({
    pos: [(Math.random() - 0.5) * 20, (Math.random() - 0.5) * 20, (Math.random() - 0.5) * 10 - 5],
  }));
  return (
    <>
      {stars.map((s, i) => (
        <mesh key={i} position={s.pos}>
          <sphereGeometry args={[0.05, 6, 6]} />
          <meshStandardMaterial color="white" emissive="white" emissiveIntensity={1} />
        </mesh>
      ))}
    </>
  );
}

const navStyle = {
  position: 'fixed', top: 20, left: 20, zIndex: 100,
  background: 'rgba(0,0,0,0.8)', padding: '20px', borderRadius: '10px',
  display: 'flex', flexDirection: 'column', gap: '10px', minWidth: '180px',
};

const btnStyle = (color) => ({
  padding: '10px 20px', background: color, color: '#fff',
  textDecoration: 'none', borderRadius: '6px', textAlign: 'center',
  fontSize: '14px', fontFamily: 'sans-serif', cursor: 'pointer',
});

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ width: '100vw', height: '100vh' }}>
        <Routes>
          <Route path="/" element={<MenuScene />} />
          <Route path="/juego" element={<GameScene />} />
          <Route path="/creditos" element={<CreditsScene />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
