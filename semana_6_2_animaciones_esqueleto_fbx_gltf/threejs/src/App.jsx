import React, { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import AnimatedModel from './components/AnimatedModel.jsx';
import AnimationController from './components/AnimationController.jsx';

export default function App() {
  const [activeAnimation, setActiveAnimation] = useState('Idle');
  const [isPlaying, setIsPlaying] = useState(true);
  const [speed, setSpeed] = useState(1);
  const [animationList, setAnimationList] = useState([]);

  return (
    <div className="app-layout">
      <AnimationController
        animations={animationList}
        activeAnimation={activeAnimation}
        isPlaying={isPlaying}
        speed={speed}
        onAnimationChange={setActiveAnimation}
        onPlayPause={setIsPlaying}
        onSpeedChange={setSpeed}
      />
      <div className="canvas-container">
        <Canvas camera={{ position: [0, 1, 6], fov: 50 }}>
          <ambientLight intensity={0.5} />
          <directionalLight position={[5, 10, 5]} intensity={1} />
          <Suspense fallback={null}>
            <AnimatedModel
              activeAnimation={activeAnimation}
              isPlaying={isPlaying}
              speed={speed}
              onAnimationsLoaded={setAnimationList}
            />
          </Suspense>
          <OrbitControls />
        </Canvas>
      </div>
    </div>
  );
}
