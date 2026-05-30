import { useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Line } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

const ARM_LENGTHS = [2, 1.5, 1];

function RobotArm({ angles }) {
  const joint1Ref = useRef();
  const joint2Ref = useRef();
  const joint3Ref = useRef();
  const [trail, setTrail] = useState([]);

  useFrame(() => {
    if (joint1Ref.current) joint1Ref.current.rotation.z = angles[0];
    if (joint2Ref.current) joint2Ref.current.rotation.z = angles[1];
    if (joint3Ref.current) joint3Ref.current.rotation.z = angles[2];

    // Track end effector position in world space
    const endPos = new THREE.Vector3();
    if (joint3Ref.current) {
      const mesh = joint3Ref.current.children[0];
      if (mesh) {
        mesh.getWorldPosition(endPos);
        setTrail(prev => {
          const next = [...prev, [endPos.x, endPos.y, endPos.z]];
          return next.length > 80 ? next.slice(-80) : next;
        });
      }
    }
  });

  return (
    <group position={[0, -2, 0]}>
      {/* Base */}
      <mesh>
        <cylinderGeometry args={[0.4, 0.5, 0.3, 16]} />
        <meshStandardMaterial color="#555" />
      </mesh>

      {/* Joint 1 */}
      <group ref={joint1Ref} position={[0, 0.15, 0]}>
        <mesh position={[ARM_LENGTHS[0] / 2, 0, 0]}>
          <boxGeometry args={[ARM_LENGTHS[0], 0.25, 0.25]} />
          <meshStandardMaterial color="#e44" />
        </mesh>
        {/* Joint sphere */}
        <mesh><sphereGeometry args={[0.18, 16, 16]} /><meshStandardMaterial color="#aaa" /></mesh>

        {/* Joint 2 */}
        <group ref={joint2Ref} position={[ARM_LENGTHS[0], 0, 0]}>
          <mesh position={[ARM_LENGTHS[1] / 2, 0, 0]}>
            <boxGeometry args={[ARM_LENGTHS[1], 0.2, 0.2]} />
            <meshStandardMaterial color="#4a4" />
          </mesh>
          <mesh><sphereGeometry args={[0.15, 16, 16]} /><meshStandardMaterial color="#aaa" /></mesh>

          {/* Joint 3 */}
          <group ref={joint3Ref} position={[ARM_LENGTHS[1], 0, 0]}>
            <mesh position={[ARM_LENGTHS[2] / 2, 0, 0]}>
              <boxGeometry args={[ARM_LENGTHS[2], 0.15, 0.15]} />
              <meshStandardMaterial color="#44e" />
            </mesh>
            {/* End effector marker */}
            <mesh position={[ARM_LENGTHS[2], 0, 0]}>
              <sphereGeometry args={[0.12, 16, 16]} />
              <meshStandardMaterial color="yellow" emissive="yellow" emissiveIntensity={0.5} />
            </mesh>
            <mesh><sphereGeometry args={[0.12, 16, 16]} /><meshStandardMaterial color="#aaa" /></mesh>
          </group>
        </group>
      </group>

      {trail.length > 1 && (
        <Line points={trail} color="yellow" lineWidth={1} opacity={0.5} transparent />
      )}
    </group>
  );
}

export default function App() {
  const { 'Joint 1 (deg)': j1, 'Joint 2 (deg)': j2, 'Joint 3 (deg)': j3, 'Auto-animate': autoAnimate } = useControls({
    'Joint 1 (deg)': { value: 0, min: -180, max: 180, step: 1 },
    'Joint 2 (deg)': { value: 0, min: -150, max: 150, step: 1 },
    'Joint 3 (deg)': { value: 0, min: -120, max: 120, step: 1 },
    'Auto-animate': false,
  });

  const toRad = deg => (deg * Math.PI) / 180;

  function AnimatedArm() {
    const timeRef = useRef(0);
    const [dynAngles, setDynAngles] = useState([0, 0, 0]);

    useFrame((_, delta) => {
      if (!autoAnimate) return;
      timeRef.current += delta;
      const t = timeRef.current;
      setDynAngles([
        Math.sin(t * 0.7) * 1.2,
        Math.sin(t * 1.1 + 1) * 0.9,
        Math.sin(t * 1.5 + 2) * 0.7,
      ]);
    });

    const angles = autoAnimate
      ? dynAngles
      : [toRad(j1), toRad(j2), toRad(j3)];
    return <RobotArm angles={angles} />;
  }

  return (
    <Canvas camera={{ position: [6, 4, 6], fov: 50 }}>
      <ambientLight intensity={0.6} />
      <directionalLight position={[5, 8, 5]} intensity={1} />
      <AnimatedArm />
      <gridHelper args={[12, 12, '#333', '#333']} position={[0, -2.15, 0]} />
      <OrbitControls makeDefault />
    </Canvas>
  );
}
