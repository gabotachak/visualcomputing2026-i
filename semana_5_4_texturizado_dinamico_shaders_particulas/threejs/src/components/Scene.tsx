import React, { useRef, useEffect } from 'react';
import { useThree } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import type { OrbitControls as OrbitControlsImpl } from 'three-stdlib';
import * as THREE from 'three';
import EnergyMaterial from './EnergyMaterial';
import FluidMaterial from './FluidMaterial';
import { useSceneControls } from './Controls';

export default function Scene() {
  const { gl } = useThree();
  const mouse = useRef(new THREE.Vector2());
  const controlsRef = useRef<OrbitControlsImpl>(null);

  const {
    intensity,
    colorCore,
    colorEdge,
    energyParticleCount,
    waveStrength,
    flowSpeed,
    colorA,
    colorB,
    fluidParticleCount,
    showParticles,
  } = useSceneControls();

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      mouse.current.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouse.current.y = -(e.clientY / window.innerHeight) * 2 + 1;
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Expose controls to window for capture scripts
  useEffect(() => {
    if (controlsRef.current) {
      (window as any).__r3fControls = controlsRef.current;
    }
  });


  return (
    <>
      <color attach="background" args={[0x000000]} />
      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 5, 5]} intensity={1.0} />
      <OrbitControls ref={controlsRef} />

      <EnergyMaterial
        position={[-3.5, 0, 0]}
        mouse={mouse}
        intensity={intensity}
        colorCore={colorCore}
        colorEdge={colorEdge}
        particleCount={energyParticleCount}
        showParticles={showParticles}
      />

      <FluidMaterial
        position={[3.5, 0, 0]}
        waveStrength={waveStrength}
        flowSpeed={flowSpeed}
        colorA={colorA}
        colorB={colorB}
        particleCount={fluidParticleCount}
        showParticles={showParticles}
      />
    </>
  );
}
