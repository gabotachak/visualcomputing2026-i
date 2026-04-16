import { useMemo } from 'react';
import { OrbitControls } from '@react-three/drei';
import * as THREE from 'three';
import ModelViewer from './ModelViewer';
import {
  createBoxCorrectUV,
  createBoxStretchedUV,
  createSphereOverlappingUV,
} from '../utils/modelHelpers';

interface SceneProps {
  texture: THREE.Texture;
  uvRepeat: [number, number];
  uvOffset: [number, number];
  uvRotation: number;
  showModelA: boolean;
  showModelB: boolean;
  showModelC: boolean;
}

export default function Scene({
  texture,
  uvRepeat,
  uvOffset,
  uvRotation,
  showModelA,
  showModelB,
  showModelC,
}: SceneProps) {
  const geometryA = useMemo(() => createBoxCorrectUV(), []);
  const geometryB = useMemo(() => createBoxStretchedUV(), []);
  const geometryC = useMemo(() => createSphereOverlappingUV(), []);

  return (
    <>
      <color attach="background" args={[0xffffff]} />
      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 8, 5]} intensity={1.0} castShadow />

      {showModelA && (
        <ModelViewer
          geometry={geometryA}
          label="Correct UV (cube)"
          position={[-4, 0, 0]}
          texture={texture}
          uvRepeat={uvRepeat}
          uvOffset={uvOffset}
          uvRotation={uvRotation}
        />
      )}

      {showModelB && (
        <ModelViewer
          geometry={geometryB}
          label="Stretched UV (cube)"
          position={[0, 0, 0]}
          texture={texture}
          uvRepeat={uvRepeat}
          uvOffset={uvOffset}
          uvRotation={uvRotation}
        />
      )}

      {showModelC && (
        <ModelViewer
          geometry={geometryC}
          label="Overlapping UV (sphere)"
          position={[4, 0, 0]}
          texture={texture}
          uvRepeat={uvRepeat}
          uvOffset={uvOffset}
          uvRotation={uvRotation}
        />
      )}

      <OrbitControls makeDefault />
    </>
  );
}
