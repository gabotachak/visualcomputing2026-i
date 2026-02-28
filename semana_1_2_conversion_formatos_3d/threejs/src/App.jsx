import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, ContactShadows } from '@react-three/drei';
import { Box, FileCode, Cpu, Layers } from 'lucide-react';
import { ModelViewer } from './ModelViewer';

const FORMATS = [
  { id: 'OBJ', name: 'Wavefront OBJ', icon: <Box size={18} />, color: '#4ade80', file: '/models/generic_model.obj' },
  { id: 'STL', name: 'Stereolithography', icon: <Layers size={18} />, color: '#3b82f6', file: '/models/generic_model.stl' },
  { id: 'GLTF', name: 'GL Transmission', icon: <FileCode size={18} />, color: '#a855f7', file: '/models/generic_model.gltf' },
];

function App() {
  const [activeFormat, setActiveFormat] = useState(FORMATS[0]);
  const [stats, setStats] = useState({ vertices: 0, polygons: 0 });

  return (
    <div className="app-container">
      {/* Panel Lateral */}
      <div className="sidebar">
        <div>
          <h1>3D Format Converter</h1>
          <p>Taller 2 - Computación Visual</p>
        </div>

        <div className="format-selector">
          {FORMATS.map((fmt) => (
            <button
              key={fmt.id}
              className={activeFormat.id === fmt.id ? 'active' : ''}
              onClick={() => {
                setActiveFormat(fmt);
                setStats({ vertices: 0, polygons: 0 }); // reset while loading
              }}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                {fmt.icon} {fmt.name}
              </span>
              <span style={{ fontSize: '0.8rem', color: '#ccc' }}>.{fmt.id.toLowerCase()}</span>
            </button>
          ))}
        </div>

        <div className="stats-panel">
          <h3><Cpu size={18} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '6px' }} /> Estadísticas del Modelo</h3>
          <div className="stat-item">
            <span className="label">Formato Activo:</span>
            <span className="value" style={{ color: activeFormat.color }}>{activeFormat.id}</span>
          </div>
          <div className="stat-item">
            <span className="label">Vértices:</span>
            <span className="value">{stats.vertices > 0 ? stats.vertices.toLocaleString() : 'Cargando...'}</span>
          </div>
          <div className="stat-item">
            <span className="label">Caras (Polígonos):</span>
            <span className="value">{stats.polygons > 0 ? stats.polygons.toLocaleString() : 'Cargando...'}</span>
          </div>
        </div>
      </div>

      {/* Visor 3D Principal */}
      <div className="canvas-container">
        <Canvas camera={{ position: [0, 2, 5], fov: 50 }}>
          <ambientLight intensity={0.5} />
          <spotLight position={[10, 10, 10]} angle={0.15} penumbra={1} intensity={1} castShadow />
          <pointLight position={[-10, -10, -10]} intensity={0.5} />

          <React.Suspense fallback={null}>
            <ModelViewer
              key={activeFormat.id} // Forza re-render completo al cambiar
              format={activeFormat.id}
              url={activeFormat.file}
              onLoadedStats={(s) => setStats(s)}
            />
            {/* Sombras y entorno realistas para mejorar la estética */}
            <ContactShadows position={[0, -1.5, 0]} opacity={0.4} scale={10} blur={2} far={4} />
            <Environment preset="city" />
          </React.Suspense>

          <OrbitControls
            autoRotate
            autoRotateSpeed={1.5}
            enablePan={true}
            enableZoom={true}
            minDistance={2}
            maxDistance={10}
          />
        </Canvas>
      </div>
    </div>
  );
}

export default App;
