import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, OrthographicCamera } from '@react-three/drei';
import { Camera } from 'lucide-react';
import ProjectionScene from './ProjectionScene';

export default function App() {
  const [cameraMode, setCameraMode] = useState('perspective');

  const takeScreenshot = () => {
    const canvas = document.querySelector('canvas');
    if (canvas) {
      const link = document.createElement('a');
      link.download = `proyeccion-${cameraMode}-${Date.now()}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
    }
  };

  return (
    <div className="app-container">
      {/* Info panel */}
      <div className="ui-container">
        <h1>Espacios Proyectivos</h1>
        <p>
          Tres cubos ubicados a distintas profundidades (Z = 0, -5, -10).
          Cambia entre cámara perspectiva y ortográfica para observar cómo
          varía la percepción de profundidad.
        </p>
        <span className={`camera-badge ${cameraMode}`}>
          {cameraMode === 'perspective' ? 'Perspectiva (FOV 60°)' : 'Ortográfica'}
        </span>
      </div>

      {/* Camera toggle buttons */}
      <div className="controls-panel">
        <button
          className={`camera-btn ${cameraMode === 'perspective' ? 'active perspective' : ''}`}
          onClick={() => setCameraMode('perspective')}
        >
          Perspectiva
        </button>
        <button
          className={`camera-btn ${cameraMode === 'orthographic' ? 'active orthographic' : ''}`}
          onClick={() => setCameraMode('orthographic')}
        >
          Ortográfica
        </button>
      </div>

      {/* Screenshot button */}
      <button className="screenshot-btn" onClick={takeScreenshot}>
        <Camera size={18} />
        Capturar
      </button>

      <Canvas gl={{ preserveDrawingBuffer: true, antialias: true }}>
        <color attach="background" args={['#1a1a1a']} />

        {/* Perspective camera */}
        {cameraMode === 'perspective' && (
          <PerspectiveCamera
            makeDefault
            position={[0, 3, 8]}
            fov={60}
            near={0.1}
            far={100}
          />
        )}

        {/* Orthographic camera — zoom chosen so objects appear similar in screen size */}
        {cameraMode === 'orthographic' && (
          <OrthographicCamera
            makeDefault
            position={[0, 3, 8]}
            zoom={55}
            near={0.1}
            far={100}
          />
        )}

        <ProjectionScene />

        <OrbitControls makeDefault />
      </Canvas>
    </div>
  );
}
