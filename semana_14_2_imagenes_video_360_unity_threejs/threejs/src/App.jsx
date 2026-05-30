import { useRef } from 'react';
import { Canvas, useFrame, useLoader } from '@react-three/fiber';
import { OrbitControls, Html } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

// Generate procedural equirectangular texture (simulates a panoramic image)
function generatePanoTexture() {
  const w = 1024, h = 512;
  const canvas = document.createElement('canvas');
  canvas.width = w; canvas.height = h;
  const ctx = canvas.getContext('2d');

  // Sky gradient
  const skyGrad = ctx.createLinearGradient(0, 0, 0, h * 0.6);
  skyGrad.addColorStop(0, '#1a2a6c');
  skyGrad.addColorStop(0.5, '#b21f1f');
  skyGrad.addColorStop(1, '#fdbb2d');
  ctx.fillStyle = skyGrad;
  ctx.fillRect(0, 0, w, h);

  // Stars
  for (let i = 0; i < 200; i++) {
    ctx.fillStyle = 'rgba(255,255,255,0.8)';
    ctx.beginPath();
    ctx.arc(Math.random()*w, Math.random()*h*0.4, Math.random()*1.5, 0, Math.PI*2);
    ctx.fill();
  }

  // Horizon ground
  const groundGrad = ctx.createLinearGradient(0, h*0.55, 0, h);
  groundGrad.addColorStop(0, '#2d4a1e');
  groundGrad.addColorStop(1, '#1a2d10');
  ctx.fillStyle = groundGrad;
  ctx.fillRect(0, h*0.55, w, h*0.45);

  // Mountains
  ctx.fillStyle = '#3d5a2e';
  for (let i = 0; i < 8; i++) {
    const mx = i * w/8 + Math.random()*50;
    const mh = h * (0.15 + Math.random()*0.2);
    ctx.beginPath();
    ctx.moveTo(mx - 80, h*0.6);
    ctx.lineTo(mx, h*0.6 - mh);
    ctx.lineTo(mx + 80, h*0.6);
    ctx.fill();
  }

  return new THREE.CanvasTexture(canvas);
}

function Panorama({ rotation }) {
  const texture = generatePanoTexture();
  const ref = useRef();
  useFrame((_, d) => { if (ref.current && rotation) ref.current.rotation.y += d * 0.05; });

  return (
    <mesh ref={ref} scale={[-1, 1, 1]}>
      <sphereGeometry args={[500, 60, 40]} />
      <meshBasicMaterial map={texture} side={THREE.BackSide} />
    </mesh>
  );
}

function FloatingObject() {
  const ref = useRef();
  useFrame(({ clock }) => {
    if (ref.current) {
      ref.current.rotation.y = clock.elapsedTime * 0.5;
      ref.current.position.y = Math.sin(clock.elapsedTime) * 0.3;
    }
  });
  return (
    <mesh ref={ref} position={[0, 0, -2]}>
      <torusKnotGeometry args={[0.5, 0.15, 100, 16]} />
      <meshStandardMaterial color="#4af" emissive="#4af" emissiveIntensity={0.3} metalness={0.8} roughness={0.2} />
    </mesh>
  );
}

export default function App() {
  const { autoRotate } = useControls({ autoRotate: true });

  return (
    <>
      <div style={{
        position: 'fixed', top: 10, left: '50%', transform: 'translateX(-50%)',
        color: 'white', background: 'rgba(0,0,0,0.7)', padding: '8px 16px',
        borderRadius: '8px', fontFamily: 'sans-serif', fontSize: '13px', zIndex: 100,
      }}>
        Vista 360° — Arrastra para orbitar | Scroll para zoom
      </div>
      <Canvas camera={{ position: [0, 0, 0.1], fov: 90 }}>
        <ambientLight intensity={0.3} />
        <pointLight position={[0, 0, 0]} intensity={0.5} color="white" />
        <Panorama rotation={autoRotate} />
        <FloatingObject />
        <OrbitControls makeDefault enableZoom={false} rotateSpeed={-0.5} />
      </Canvas>
    </>
  );
}
