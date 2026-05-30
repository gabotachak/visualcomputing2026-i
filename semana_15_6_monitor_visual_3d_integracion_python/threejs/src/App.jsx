import { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Html } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

function ZoneBar({ position, activity, name, color }) {
  const meshRef = useRef();
  // Target height proportional to activity
  const targetHeight = Math.max(0.1, activity * 2.5);

  useFrame((_, dt) => {
    if (meshRef.current) {
      // Smooth interpolation (lerp) of height transitions
      meshRef.current.scale.y = THREE.MathUtils.lerp(meshRef.current.scale.y, targetHeight, 5 * dt);
      // Offset position y so the bar stands on the floor
      meshRef.current.position.y = meshRef.current.scale.y / 2;
    }
  });

  return (
    <group position={[position[0], 0, position[2]]}>
      {/* 3D Bar representing activity */}
      <mesh ref={meshRef} scale={[1, 0.1, 1]}>
        <boxGeometry args={[0.8, 1, 0.8]} />
        <meshStandardMaterial color={color} metalness={0.5} roughness={0.3} />
      </mesh>

      {/* Floating zone indicator */}
      <Html position={[0, targetHeight + 0.4, 0]} center distanceFactor={5}>
        <div style={{
          color: 'white', background: 'rgba(0,0,0,0.85)', padding: '4px 8px',
          borderRadius: '4px', border: `1px solid ${color}`, fontSize: '11px',
          whiteSpace: 'nowrap', pointerEvents: 'none', fontFamily: 'monospace'
        }}>
          {name}: {Math.round(activity * 100)}%
        </div>
      </Html>
    </group>
  );
}

export default function App() {
  const [zones, setZones] = useState([]);
  const [activeCount, setActiveCount] = useState(0);
  const { simulateData } = useControls({
    simulateData: { value: false, label: 'Simular Ruido Dinámico' }
  });

  // Fetch from python-generated JSON every second
  useEffect(() => {
    const fetchData = () => {
      fetch('/monitor_data.json')
        .then(res => res.json())
        .then(data => {
          if (simulateData) {
            // Add small dynamic noise for animation demonstration
            const noisyZones = data.zones.map(z => ({
              ...z,
              activity: Math.max(0.05, Math.min(1.0, z.activity + (Math.random() - 0.5) * 0.15))
            }));
            setZones(noisyZones);
            setActiveCount(data.active_count + Math.round((Math.random() - 0.5) * 3));
          } else {
            setZones(data.zones);
            setActiveCount(data.active_count);
          }
        })
        .catch(err => console.error("Error loading monitor data:", err));
    };

    fetchData();
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
  }, [simulateData]);

  const getActivityColor = (activity) => {
    if (activity > 0.8) return '#ff3333'; // Red for high activity
    if (activity > 0.4) return '#ffaa00'; // Orange for medium
    return '#33ff33'; // Green for low
  };

  return (
    <>
      <div style={{
        position: 'fixed', top: 15, left: 15, color: 'white',
        background: 'rgba(10,10,20,0.85)', padding: '15px', borderRadius: '10px',
        fontFamily: 'monospace', border: '1px solid #333', zIndex: 100, minWidth: '220px'
      }}>
        <div style={{ color: '#ffaa00', fontWeight: 'bold', fontSize: '14px', marginBottom: '8px' }}>
          3D ACTIVITY MONITOR
        </div>
        <hr style={{ borderColor: '#333', marginBottom: '10px' }} />
        <div style={{ marginBottom: '6px' }}>Zonas Activas: {zones.length}</div>
        <div style={{ marginBottom: '6px' }}>Total Personas: {activeCount}</div>
        <div style={{ fontSize: '10px', color: '#888', marginTop: '10px' }}>
          Datos: local API polling (/monitor_data.json)
        </div>
      </div>

      <Canvas camera={{ position: [0, 4, 5], fof: 50 }}>
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 10, 5]} intensity={1.2} />
        <pointLight position={[-3, 4, -3]} intensity={0.5} color="#ffa500" />
        
        {/* Render zones as dynamic 3D bars */}
        {zones.map((zone) => (
          <ZoneBar
            key={zone.id}
            position={zone.coordinates}
            activity={zone.activity}
            name={zone.name}
            color={getActivityColor(zone.activity)}
          />
        ))}

        <Grid args={[10, 10]} position={[0, 0.01, 0]} cellColor="#333" sectionColor="#555" />
        <OrbitControls makeDefault />
      </Canvas>
    </>
  );
}
