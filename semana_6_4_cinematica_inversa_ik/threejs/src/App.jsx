import { useRef, useState, useCallback } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Line, Html } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

const SEGMENTS = 3;
const SEG_LEN = 1.5;

function solveIK(target, segLen, numSegs) {
  // FABRIK-like CCD solver (simplified planar 2D in XY)
  const joints = [];
  for (let i = 0; i <= numSegs; i++) joints.push(new THREE.Vector2(i * segLen, 0));

  const totalReach = numSegs * segLen;
  const dist = new THREE.Vector2(target.x, target.y).length();

  if (dist > totalReach) {
    // Stretch toward target
    const dir = new THREE.Vector2(target.x, target.y).normalize();
    for (let i = 0; i <= numSegs; i++) {
      joints[i].set(dir.x * i * segLen, dir.y * i * segLen);
    }
  } else {
    // CCD iterations
    for (let iter = 0; iter < 10; iter++) {
      for (let i = numSegs - 1; i >= 0; i--) {
        const toEnd = new THREE.Vector2(joints[numSegs].x - joints[i].x, joints[numSegs].y - joints[i].y);
        const toTarget = new THREE.Vector2(target.x - joints[i].x, target.y - joints[i].y);
        const angle = Math.atan2(toTarget.y, toTarget.x) - Math.atan2(toEnd.y, toEnd.x);
        const cos = Math.cos(angle), sin = Math.sin(angle);
        for (let j = i + 1; j <= numSegs; j++) {
          const dx = joints[j].x - joints[i].x;
          const dy = joints[j].y - joints[i].y;
          joints[j].set(joints[i].x + dx * cos - dy * sin, joints[i].y + dx * sin + dy * cos);
        }
      }
    }
  }
  return joints;
}

function IKArm({ targetPos }) {
  const joints = solveIK({ x: targetPos[0], y: targetPos[1] }, SEG_LEN, SEGMENTS);
  const points3d = joints.map(j => [j.x, j.y, 0]);

  return (
    <group>
      <Line points={points3d} color="#e44" lineWidth={6} />
      {joints.map((j, i) => (
        <mesh key={i} position={[j.x, j.y, 0]}>
          <sphereGeometry args={[i === 0 ? 0.2 : 0.15, 16, 16]} />
          <meshStandardMaterial color={i === 0 ? '#555' : i === joints.length - 1 ? 'yellow' : '#aaa'}
            emissive={i === joints.length - 1 ? 'yellow' : 'black'} emissiveIntensity={0.5} />
        </mesh>
      ))}
    </group>
  );
}

function DragTarget({ onMove }) {
  const meshRef = useRef();
  const { camera, gl } = useThree();
  const [dragging, setDragging] = useState(false);
  const [pos, setPos] = useState([3, 2, 0]);

  const getWorldPos = useCallback((e) => {
    const rect = gl.domElement.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    const y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    const vec = new THREE.Vector3(x, y, 0.5).unproject(camera);
    vec.sub(camera.position).normalize();
    const t = -camera.position.z / vec.z;
    const point = camera.position.clone().add(vec.multiplyScalar(t));
    return [Math.max(-4, Math.min(4, point.x)), Math.max(-3, Math.min(3, point.y)), 0];
  }, [camera, gl]);

  return (
    <mesh ref={meshRef} position={pos}
      onPointerDown={e => { e.stopPropagation(); setDragging(true); gl.domElement.style.cursor = 'grabbing'; }}
      onPointerUp={() => { setDragging(false); gl.domElement.style.cursor = 'grab'; }}
      onPointerMove={e => {
        if (!dragging) return;
        const p = getWorldPos(e.nativeEvent);
        setPos(p); onMove(p);
      }}
      onPointerOver={() => { if (!dragging) gl.domElement.style.cursor = 'grab'; }}
      onPointerOut={() => { if (!dragging) gl.domElement.style.cursor = 'auto'; }}>
      <sphereGeometry args={[0.25, 16, 16]} />
      <meshStandardMaterial color="cyan" emissive="cyan" emissiveIntensity={0.3} />
      <Html center distanceFactor={8}>
        <div style={{color:'cyan',fontSize:'12px',whiteSpace:'nowrap',userSelect:'none'}}>drag target</div>
      </Html>
    </mesh>
  );
}

export default function App() {
  const [target, setTarget] = useState([3, 2, 0]);

  return (
    <Canvas camera={{ position: [0, 0, 12], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 8, 5]} intensity={1} />
      <IKArm targetPos={target} />
      <DragTarget onMove={p => setTarget(p)} />
      <Line points={[[0,0,0], [target[0], target[1], 0]]} color="#333" lineWidth={1} dashed />
      <gridHelper args={[12, 12, '#222', '#222']} rotation={[Math.PI/2, 0, 0]} />
      <OrbitControls makeDefault enablePan={false} />
    </Canvas>
  );
}
