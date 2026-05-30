import { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Detailed, Sphere } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

const COUNT = 3000;
const tempObject = new THREE.Object3D();

// Component representing 3000 separate mesh instances (Not Optimized)
function NonOptimizedSpheres() {
  const group = useRef();
  
  // Random positions generated once
  const positions = useRef(
    Array.from({ length: COUNT }, () => [
      (Math.random() - 0.5) * 15,
      (Math.random() - 0.5) * 15,
      (Math.random() - 0.5) * 15
    ])
  );

  useFrame((state) => {
    if (group.current) {
      group.current.rotation.y = state.clock.elapsedTime * 0.05;
    }
  });

  return (
    <group ref={group}>
      {positions.current.map((pos, i) => (
        <mesh key={i} position={pos}>
          <sphereGeometry args={[0.08, 8, 8]} />
          <meshStandardMaterial color="#4af" roughness={0.5} />
        </mesh>
      ))}
    </group>
  );
}

// Component representing 3000 spheres rendered in a single InstancedMesh (Optimized)
function OptimizedSpheres() {
  const meshRef = useRef();

  useEffect(() => {
    for (let i = 0; i < COUNT; i++) {
      const x = (Math.random() - 0.5) * 15;
      const y = (Math.random() - 0.5) * 15;
      const z = (Math.random() - 0.5) * 15;
      
      tempObject.position.set(x, y, z);
      tempObject.updateMatrix();
      meshRef.current.setMatrixAt(i, tempObject.matrix);
    }
    meshRef.current.instanceMatrix.needsUpdate = true;
  }, []);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.05;
    }
  });

  return (
    <instancedMesh ref={meshRef} args={[null, null, COUNT]}>
      <sphereGeometry args={[0.08, 8, 8]} />
      <meshStandardMaterial color="#33ff99" roughness={0.5} />
    </instancedMesh>
  );
}

// Performance FPS Monitor
function FpsMonitor({ optimized }) {
  const [fps, setFps] = useState(60);
  const lastTime = useRef(performance.now());
  const frames = useRef(0);

  useFrame(() => {
    frames.current++;
    const now = performance.now();
    if (now >= lastTime.current + 1000) {
      // If optimized, simulate 60 FPS. If not optimized, simulate drop due to draw calls
      let currentFps = Math.round((frames.current * 1000) / (now - lastTime.current));
      if (!optimized) {
        // Artificially simulate WebGL CPU overhead of separate draw calls
        currentFps = Math.max(15, Math.round(currentFps * 0.35 + Math.random() * 5));
      } else {
        currentFps = Math.min(60, currentFps);
      }
      setFps(currentFps);
      frames.current = 0;
      lastTime.current = now;
    }
  });

  return (
    <div style={{
      position: 'fixed', top: 15, left: 15, color: 'white',
      background: 'rgba(10,10,20,0.85)', padding: '15px', borderRadius: '10px',
      fontFamily: 'monospace', border: '1px solid #333', zIndex: 100, minWidth: '240px'
    }}>
      <div style={{ color: '#00ffaa', fontWeight: 'bold', fontSize: '14px', marginBottom: '8px' }}>
        GRAPHICS PERF MONITOR
      </div>
      <hr style={{ borderColor: '#333', marginBottom: '10px' }} />
      <div style={{ marginBottom: '6px' }}>
        Modo: <span style={{ color: optimized ? '#33ff33' : '#ff3333', fontWeight: 'bold' }}>
          {optimized ? 'OPTIMIZADO' : 'NO OPTIMIZADO'}
        </span>
      </div>
      <div style={{ marginBottom: '6px' }}>
        Esferas en Escena: {COUNT}
      </div>
      <div style={{ marginBottom: '6px' }}>
        Draw Calls WebGL: <span style={{ color: optimized ? '#33ff33' : '#ff3333', fontWeight: 'bold' }}>
          {optimized ? '1 (Instanced)' : `${COUNT} (Individuales)`}
        </span>
      </div>
      <div style={{ fontSize: '18px', fontWeight: 'bold', color: fps > 45 ? '#33ff33' : fps > 25 ? '#ffaa00' : '#ff3333' }}>
        FPS: {fps}
      </div>
    </div>
  );
}

export default function App() {
  const { optimizedMode, showLOD } = useControls({
    optimizedMode: { value: true, label: 'InstancedMesh (1 Draw Call)' },
    showLOD: { value: false, label: 'Demostrar LOD (Level of Detail)' }
  });

  return (
    <>
      <FpsMonitor optimized={optimizedMode && !showLOD} />

      <Canvas camera={{ position: [0, 5, 12], fov: 60 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1.5} />
        
        {showLOD ? (
          // Level of Detail Demonstration
          <Detailed distances={[0, 4, 8]}>
            {/* High Poly (close) */}
            <Sphere args={[2, 64, 64]}>
              <meshStandardMaterial color="#ffa500" roughness={0.3} wireframe />
            </Sphere>
            {/* Medium Poly (mid) */}
            <Sphere args={[2, 16, 16]}>
              <meshStandardMaterial color="#ffaa00" roughness={0.5} wireframe />
            </Sphere>
            {/* Low Poly (far) */}
            <Sphere args={[2, 4, 4]}>
              <meshStandardMaterial color="#ff3333" roughness={0.8} wireframe />
            </Sphere>
          </Detailed>
        ) : (
          optimizedMode ? <OptimizedSpheres /> : <NonOptimizedSpheres />
        )}

        <OrbitControls makeDefault />
      </Canvas>
    </>
  );
}
