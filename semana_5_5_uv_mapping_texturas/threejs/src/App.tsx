import { Suspense, useMemo } from 'react';
import { Canvas } from '@react-three/fiber';
import { useControls, folder } from 'leva';
import Scene from './components/Scene';
import TextureDisplay from './components/TextureDisplay';
import { createTexture, TextureType } from './utils/textureGenerator';

export default function App() {
  const {
    textureType,
    repeatX,
    repeatY,
    offsetX,
    offsetY,
    rotation,
    showModelA,
    showModelB,
    showModelC,
  } = useControls({
    'Texture': folder({
      textureType: {
        label: 'Type',
        value: 'checkerboard' as TextureType,
        options: {
          Checkerboard: 'checkerboard',
          Grid: 'grid',
          'Numbered Grid': 'numbered',
        },
      },
    }),
    'UV Adjustments': folder({
      repeatX: { label: 'Repeat X', value: 1, min: 0.5, max: 4, step: 0.5 },
      repeatY: { label: 'Repeat Y', value: 1, min: 0.5, max: 4, step: 0.5 },
      offsetX: { label: 'Offset X', value: 0, min: -1, max: 1, step: 0.1 },
      offsetY: { label: 'Offset Y', value: 0, min: -1, max: 1, step: 0.1 },
      rotation: {
        label: 'Rotation',
        value: 0,
        min: -Math.PI,
        max: Math.PI,
        step: 0.1,
      },
    }),
    'Models': folder({
      showModelA: { label: 'Correct UV (cube)', value: true },
      showModelB: { label: 'Stretched UV (cube)', value: true },
      showModelC: { label: 'Overlapping UV (sphere)', value: true },
    }),
  });

  const texture = useMemo(
    () => createTexture(textureType as TextureType),
    [textureType]
  );

  return (
    <div className="app-layout">
      <div className="canvas-container">
        <Canvas camera={{ position: [0, 2, 10], fov: 50 }}>
          <Suspense fallback={null}>
            <Scene
              texture={texture}
              uvRepeat={[repeatX, repeatY]}
              uvOffset={[offsetX, offsetY]}
              uvRotation={rotation}
              showModelA={showModelA}
              showModelB={showModelB}
              showModelC={showModelC}
            />
          </Suspense>
        </Canvas>
      </div>
      <div className="texture-preview-panel">
        <TextureDisplay texture={texture} label="Active Texture" />
      </div>
    </div>
  );
}
