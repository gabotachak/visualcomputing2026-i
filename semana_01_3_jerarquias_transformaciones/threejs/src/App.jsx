import React, { useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import HierarchyScene from './HierarchyScene';
import { Camera } from 'lucide-react';

export default function App() {
  const canvasRef = useRef(null);

  const takeScreenshot = () => {
    const canvas = document.querySelector('canvas');
    if (canvas) {
      // Create a temporary link element
      const link = document.createElement('a');
      link.download = `hierarchy-screenshot-${new Date().getTime()}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    }
  };

  return (
    <div className="app-container">
      <div className="ui-container">
        <h1>Árbol del Movimiento</h1>
        <p>
          Taller de Jerarquías y Transformaciones.
          Modifica los parámetros del padre para observar cómo afectan a los nodos hijos y nietos en la jerarquía.
        </p>
      </div>

      <button className="screenshot-btn" onClick={takeScreenshot}>
        <Camera size={18} />
        Capturar Pantalla
      </button>

      <Canvas
        ref={canvasRef}
        camera={{ position: [5, 5, 8], fov: 50 }}
        gl={{ preserveDrawingBuffer: true, antialias: true }}
      >
        <color attach="background" args={['#1a1a1a']} />

        {/* Lights */}
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} castShadow />
        <directionalLight position={[-10, -10, -5]} intensity={0.5} color="#4ade80" />

        {/* Environment for reflections */}
        <Environment preset="city" />

        {/* Scene Content */}
        <HierarchyScene />

        {/* Controls */}
        <OrbitControls makeDefault />
      </Canvas>
    </div>
  );
}
