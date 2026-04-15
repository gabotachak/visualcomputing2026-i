import { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import Scene from './components/Scene.jsx';

export default function App() {
  const [metalness, setMetalness] = useState(0.0);
  const [roughness, setRoughness] = useState(0.5);
  const [showBasic, setShowBasic] = useState(true);

  return (
    <div className="app-layout">
      {/* Control panel */}
      <div className="controller-panel">
        <div className="panel-title">PBR Controls</div>

        {/* Metalness slider */}
        <div className="control-group">
          <div className="control-row">
            <span className="control-label">Metalness</span>
            <span className="control-value">{metalness.toFixed(2)}</span>
          </div>
          <div className="slider-container">
            <input
              type="range"
              className="slider"
              min={0}
              max={1}
              step={0.01}
              value={metalness}
              onChange={(e) => setMetalness(parseFloat(e.target.value))}
            />
          </div>
          <span className="desc-text">
            Controls mirror-like reflectance. 0 = dielectric, 1 = fully metallic.
          </span>
        </div>

        {/* Roughness slider */}
        <div className="control-group">
          <div className="control-row">
            <span className="control-label">Roughness</span>
            <span className="control-value">{roughness.toFixed(2)}</span>
          </div>
          <div className="slider-container">
            <input
              type="range"
              className="slider"
              min={0}
              max={1}
              step={0.01}
              value={roughness}
              onChange={(e) => setRoughness(parseFloat(e.target.value))}
            />
          </div>
          <span className="desc-text">
            Controls surface micro-roughness. 0 = mirror-smooth, 1 = fully diffuse.
          </span>
        </div>

        {/* Show basic toggle */}
        <div className="control-group">
          <div className="toggle-row">
            <span className="toggle-label">Show Basic Sphere</span>
            <label className="toggle">
              <input
                type="checkbox"
                checked={showBasic}
                onChange={(e) => setShowBasic(e.target.checked)}
              />
              <span className="toggle-slider" />
            </label>
          </div>
          <span className="desc-text">
            Toggle the right sphere to compare PBR vs basic material.
          </span>
        </div>

        {/* Legend */}
        <div className="control-group">
          <div className="control-label">Legend</div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <span className="badge badge-pbr">PBR (left)</span>
            <span className="badge badge-basic">Basic (right)</span>
          </div>
          <span className="desc-text">
            Left sphere uses albedo, roughness, metalness and normal maps.<br />
            Right sphere uses a flat color with no textures.
          </span>
        </div>

        <div className="status-bar">
          metalness: {metalness.toFixed(2)} &nbsp;|&nbsp; roughness: {roughness.toFixed(2)}
        </div>
      </div>

      {/* 3D Canvas */}
      <div className="canvas-container">
        <Canvas
          camera={{ position: [0, 2, 5], fov: 50 }}
          shadows
          style={{ background: '#cccccc' }}
        >
          <Scene metalness={metalness} roughness={roughness} showBasic={showBasic} />
        </Canvas>
      </div>
    </div>
  );
}
