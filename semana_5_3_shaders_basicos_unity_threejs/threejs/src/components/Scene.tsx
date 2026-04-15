import React from 'react';
import { OrbitControls } from '@react-three/drei';
import GradientShader from './GradientShader';
import WaveShader from './WaveShader';
import FresnelShader from './FresnelShader';
import { useShaderControls } from './Controls';

export default function Scene() {
  const controls = useShaderControls();

  return (
    <>
      <color attach="background" args={[0x333333]} />
      <ambientLight intensity={0.7} />
      <directionalLight position={[5, 5, 5]} intensity={1.0} />
      <OrbitControls />
      <GradientShader colorTop={controls.colorTop} colorBottom={controls.colorBottom} />
      <WaveShader
        waveFrequency={controls.waveFrequency}
        colorA={controls.colorA}
        colorB={controls.colorB}
        animationSpeed={controls.animationSpeed}
      />
      <FresnelShader
        fresnelPower={controls.fresnelPower}
        baseColor={controls.baseColor}
        glowColor={controls.glowColor}
      />
    </>
  );
}
