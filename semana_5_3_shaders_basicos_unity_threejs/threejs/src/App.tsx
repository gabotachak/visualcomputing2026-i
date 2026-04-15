import React from 'react';
import { Canvas } from '@react-three/fiber';
import Scene from './components/Scene';

export default function App() {
  return (
    <div className="app-layout">
      <div className="canvas-container">
        <Canvas camera={{ position: [0, 0, 8], fov: 50 }}>
          <Scene />
        </Canvas>
      </div>
    </div>
  );
}
