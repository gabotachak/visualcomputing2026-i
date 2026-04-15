import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import GridGenerator from './GridGenerator';
import SpiralGenerator from './SpiralGenerator';
import FractalTerrain from './FractalTerrain';
import { useGridControls, useSpiralControls, useTerrainControls } from './Controls';

function SceneContent() {
  const [resetKey, setResetKey] = useState(0);

  const { gridSize, spacing, gridScale, rotationSpeed } = useGridControls(resetKey, setResetKey);
  const { turns, segments, radius, height, scaleVariation, animationSpeed } = useSpiralControls();
  const {
    width, depth, segments: terrainSegments, octaves,
    amplitude, frequency, terrainSpeed, wireframe,
  } = useTerrainControls();

  return (
    <>
      <color attach="background" args={['#888888']} />
      <ambientLight intensity={0.6} />
      <directionalLight intensity={1.0} position={[5, 8, 5]} color="white" />

      {/* Grid — left */}
      <group position={[-7, 0, 0]}>
        <GridGenerator
          key={resetKey}
          gridSize={gridSize}
          spacing={spacing}
          scale={gridScale}
          rotationSpeed={rotationSpeed}
        />
      </group>

      {/* Spiral — center */}
      <group position={[0, 0, 0]}>
        <SpiralGenerator
          turns={turns}
          segments={segments}
          radius={radius}
          height={height}
          scaleVariation={scaleVariation}
          animationSpeed={animationSpeed}
        />
      </group>

      {/* Fractal terrain (vertex manipulation) — right */}
      <group position={[7, 0, 0]}>
        <FractalTerrain
          width={width}
          depth={depth}
          segments={terrainSegments}
          octaves={octaves}
          amplitude={amplitude}
          frequency={frequency}
          speed={terrainSpeed}
          wireframe={wireframe}
        />
      </group>

      <OrbitControls target={[0, 2, 0]} />
    </>
  );
}

export default function Scene() {
  return (
    <Canvas camera={{ position: [0, 5, 18], fov: 60 }}>
      <SceneContent />
    </Canvas>
  );
}
