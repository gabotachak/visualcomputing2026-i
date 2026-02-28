import React, { Suspense, useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Html } from '@react-three/drei'
import ModelViewer from './ModelViewer'

export default function App() {
  const [mode, setMode] = useState('solid')
  const [stats, setStats] = useState(null)

  return (
    <div className="app-root">
      <aside className="panel">
        <h2>Three.js - Visualizador</h2>
        <div className="buttons">
          <button onClick={() => setMode('solid')} className={mode==='solid'? 'active':''}>Sólido</button>
          <button onClick={() => setMode('wireframe')} className={mode==='wireframe'? 'active':''}>Wireframe</button>
          <button onClick={() => setMode('edges')} className={mode==='edges'? 'active':''}>Edges</button>
          <button onClick={() => setMode('points')} className={mode==='points'? 'active':''}>Points</button>
        </div>
        <div className="stats">
          <h3>Estadísticas</h3>
          {stats ? (
            <ul>
              <li>Vértices: {stats.vertices}</li>
              <li>Caras (triángulos): {stats.faces}</li>
              <li>Mallas: {stats.meshes}</li>
            </ul>
          ) : (
            <p>No cargado</p>
          )}
        </div>
        <div className="notes">
          <p>Coloca tu modelo en <code>public/models/scene.obj</code> (o cambia la ruta en <code>App.jsx</code>).</p>
        </div>
      </aside>

      <main className="viewer">
        <Canvas shadows camera={{ position: [0, 0, 3], fov: 50 }}>
          <ambientLight intensity={0.6} />
          <directionalLight position={[5, 5, 5]} intensity={1} />
          <Suspense fallback={<Html center>Cargando modelo...</Html>}>
            <ModelViewer src="/models/scene.obj" mode={mode} onLoaded={setStats} />
          </Suspense>
          <OrbitControls />
        </Canvas>
      </main>
    </div>
  )
}
