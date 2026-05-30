import { useRef, useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Html, Image } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

function DetectionBox({ position, scale, label, confidence, color }) {
  const [hovered, setHovered] = useState(false);

  return (
    <group position={position}>
      {/* 3D Wireframe box around detection */}
      <mesh onPointerOver={() => setHovered(true)} onPointerOut={() => setHovered(false)}>
        <boxGeometry args={scale} />
        <meshBasicMaterial color={color} wireframe transparent opacity={0.6} />
      </mesh>
      
      {/* Solid semitransparent fill on hover */}
      {hovered && (
        <mesh>
          <boxGeometry args={scale} />
          <meshBasicMaterial color={color} transparent opacity={0.15} />
        </mesh>
      )}

      {/* Floating text label */}
      <Html distanceFactor={4} center>
        <div style={{
          color: 'white', background: 'rgba(0,0,0,0.85)', padding: '4px 8px',
          borderRadius: '4px', border: `1px solid ${color}`, fontSize: '11px',
          whiteSpace: 'nowrap', pointerEvents: 'none', fontFamily: 'monospace'
        }}>
          {label} ({Math.round(confidence * 100)}%)
        </div>
      </Html>
    </group>
  );
}

export default function App() {
  const [data, setData] = useState(null);
  const { bgOpacity } = useControls({
    bgOpacity: { value: 0.5, min: 0, max: 1, step: 0.05, label: 'Opacidad Imagen' }
  });

  useEffect(() => {
    fetch('/detections.json')
      .then(res => res.json())
      .then(data => setData(data))
      .catch(err => console.error("Error loading detections:", err));
  }, []);

  const classColors = {
    laptop: '#00ffcc',
    cup: '#f84',
    person: '#a4e'
  };

  return (
    <>
      <div style={{
        position: 'fixed', top: 15, left: 15, color: 'white',
        background: 'rgba(10,10,20,0.85)', padding: '15px', borderRadius: '10px',
        fontFamily: 'monospace', border: '1px solid #333', zIndex: 100, minWidth: '220px'
      }}>
        <div style={{ color: '#a4e', fontWeight: 'bold', fontSize: '14px', marginBottom: '8px' }}>
          COLLABORATIVE AI VISUALIZER
        </div>
        <hr style={{ borderColor: '#333', marginBottom: '10px' }} />
        {data ? (
          <>
            <div style={{ marginBottom: '6px' }}>Objetos Detectados: {data.detections.length}</div>
            <div style={{ marginBottom: '10px' }}>Timestamp: {new Date(data.timestamp).toLocaleTimeString()}</div>
            <ul style={{ paddingLeft: '15px', margin: 0 }}>
              {data.detections.map((det, i) => (
                <li key={i} style={{ color: classColors[det.class] || '#fff', marginBottom: '4px' }}>
                  {det.class}: {Math.round(det.confidence * 100)}%
                </li>
              ))}
            </ul>
          </>
        ) : (
          <div>Cargando detecciones...</div>
        )}
      </div>

      <Canvas camera={{ position: [0, 0, 3], fov: 70 }}>
        <ambientLight intensity={0.5} />
        
        {/* Background Image Plane in 3D */}
        <Image url="/detection.png" scale={[4, 3]} position={[0, 0, -2.01]} transparent opacity={bgOpacity} />
        
        {/* Render bounding boxes in 3D */}
        {data && data.detections.map((det, i) => (
          <DetectionBox
            key={i}
            position={det.position}
            scale={det.scale}
            label={det.class}
            confidence={det.confidence}
            color={classColors[det.class] || '#fff'}
          />
        ))}

        <OrbitControls makeDefault />
      </Canvas>
    </>
  );
}
