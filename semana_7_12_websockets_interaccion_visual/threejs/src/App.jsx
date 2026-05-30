import { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Html } from '@react-three/drei';
import * as THREE from 'three';

const WS_URL = 'ws://localhost:8765';
const COLORS = { red: '#e44', green: '#4a4', blue: '#44e', white: '#fff', yellow: '#ee4' };

function DataSphere({ pos, color, scale }) {
  const ref = useRef();
  const targetPos = useRef(new THREE.Vector3(...pos));
  const currentPos = useRef(new THREE.Vector3(...pos));

  useEffect(() => { targetPos.current.set(...pos); }, [pos]);

  useFrame((_, dt) => {
    currentPos.current.lerp(targetPos.current, dt * 5);
    if (ref.current) ref.current.position.copy(currentPos.current);
  });

  return (
    <mesh ref={ref} position={pos} scale={scale}>
      <sphereGeometry args={[0.5, 32, 32]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.2} />
    </mesh>
  );
}

function ConnectionStatus({ status }) {
  const colors = { connecting: '#ea4', connected: '#4a4', disconnected: '#e44', demo: '#44e' };
  return (
    <div style={{
      position: 'fixed', top: 20, left: 20, zIndex: 100,
      background: 'rgba(0,0,0,0.85)', padding: '16px', borderRadius: '10px', fontFamily: 'monospace',
    }}>
      <div style={{ color: '#fff', fontWeight: 'bold', marginBottom: 8, fontSize: 14 }}>WebSocket 3D Viewer</div>
      <div style={{ color: colors[status] || '#888', marginBottom: 8 }}>
        ● {status.toUpperCase()} — {status === 'demo' ? 'simulated data' : WS_URL}
      </div>
      <div style={{ color: '#888', fontSize: 11 }}>Start Python server for live data</div>
    </div>
  );
}

export default function App() {
  const [wsData, setWsData] = useState({ x: 0, y: 0, color: 'blue' });
  const [status, setStatus] = useState('connecting');
  const [history, setHistory] = useState([]);
  const demoRef = useRef(null);

  useEffect(() => {
    let ws;
    try {
      ws = new WebSocket(WS_URL);
      ws.onopen = () => { setStatus('connected'); if (demoRef.current) clearInterval(demoRef.current); };
      ws.onmessage = e => {
        const data = JSON.parse(e.data);
        setWsData(data);
        setHistory(h => [...h.slice(-30), data]);
      };
      ws.onerror = () => startDemo();
      ws.onclose = () => { setStatus('disconnected'); startDemo(); };
    } catch {
      startDemo();
    }

    function startDemo() {
      setStatus('demo');
      demoRef.current = setInterval(() => {
        const t = Date.now() / 1000;
        const data = {
          x: Math.sin(t * 1.3) * 4,
          y: Math.cos(t * 0.9) * 3,
          color: ['red', 'green', 'blue', 'yellow', 'white'][Math.floor(t) % 5],
        };
        setWsData(data);
        setHistory(h => [...h.slice(-30), data]);
      }, 500);
    }

    return () => { ws?.close(); if (demoRef.current) clearInterval(demoRef.current); };
  }, []);

  return (
    <>
      <ConnectionStatus status={status} />
      <Canvas camera={{ position: [0, 4, 12], fov: 50 }}>
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 8, 5]} intensity={1} />

        {/* Current data sphere */}
        <DataSphere
          pos={[wsData.x, wsData.y, 0]}
          color={COLORS[wsData.color] || '#fff'}
          scale={1.2}
        />

        {/* History trail */}
        {history.map((d, i) => (
          <mesh key={i} position={[d.x, d.y, -(history.length - i) * 0.15]}
            scale={0.3 + (i / history.length) * 0.4}>
            <sphereGeometry args={[0.3, 8, 8]} />
            <meshStandardMaterial color={COLORS[d.color] || '#fff'}
              opacity={i / history.length * 0.6} transparent />
          </mesh>
        ))}

        <gridHelper args={[14, 14, '#222', '#222']} position={[0, -4, 0]} />
        <OrbitControls makeDefault />
      </Canvas>
    </>
  );
}
