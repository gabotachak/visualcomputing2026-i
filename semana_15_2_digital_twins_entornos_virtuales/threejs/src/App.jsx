import { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Html } from '@react-three/drei';
import { useControls } from 'leva';
import * as THREE from 'three';

function RobotJoint({ length, color, children, rotationY = 0, rotationZ = 0 }) {
  return (
    <group rotation={[0, rotationY, rotationZ]}>
      {/* Base pivot cylinder */}
      <mesh position={[0, 0, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.25, 0.25, 0.4, 32]} />
        <meshStandardMaterial color="#333" metalness={0.8} roughness={0.2} />
      </mesh>
      
      {/* Segment link */}
      <mesh position={[0, length / 2, 0]}>
        <boxGeometry args={[0.2, length, 0.2]} />
        <meshStandardMaterial color={color} metalness={0.6} roughness={0.3} />
      </mesh>
      
      {/* Children joints attached at the end of this segment */}
      <group position={[0, length, 0]}>
        {children}
      </group>
    </group>
  );
}

function RoboticArm({ baseRot, shoulderRot, elbowRot }) {
  return (
    <group position={[0, 0, 0]}>
      {/* Base platform */}
      <mesh position={[0, 0.1, 0]}>
        <cylinderGeometry args={[0.8, 0.9, 0.2, 32]} />
        <meshStandardMaterial color="#222" metalness={0.9} roughness={0.1} />
      </mesh>

      {/* Segment 1: Base to Shoulder */}
      <RobotJoint length={1} color="#f90" rotationY={baseRot * Math.PI / 180}>
        {/* Segment 2: Shoulder to Elbow */}
        <RobotJoint length={1.5} color="#e51b24" rotationZ={shoulderRot * Math.PI / 180}>
          {/* Segment 3: Elbow to Tool */}
          <RobotJoint length={1.2} color="#007acc" rotationZ={elbowRot * Math.PI / 180}>
            {/* End Effector / Tool */}
            <mesh position={[0, 0.1, 0]}>
              <sphereGeometry args={[0.15, 16, 16]} />
              <meshStandardMaterial color="#0f0" emissive="#0f0" emissiveIntensity={0.5} />
            </mesh>
          </RobotJoint>
        </RobotJoint>
      </RobotJoint>
    </group>
  );
}

export default function App() {
  const { baseAngle, shoulderAngle, elbowAngle } = useControls({
    baseAngle: { value: 45, min: -180, max: 180, step: 1, label: 'Rotación Base (Y)' },
    shoulderAngle: { value: -30, min: -90, max: 90, step: 1, label: 'Hombro (Z)' },
    elbowAngle: { value: 60, min: -120, max: 120, step: 1, label: 'Codo (Z)' },
  });

  const [telemetry, setTelemetry] = useState({ temp: 25, load: 12 });

  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate real-time sensors reacting to arm positions and random thermal noise
      const baseDelta = Math.abs(baseAngle) / 180;
      const armDelta = (Math.abs(shoulderAngle) + Math.abs(elbowAngle)) / 210;
      const targetTemp = 30 + 40 * (baseDelta * 0.4 + armDelta * 0.6) + Math.sin(Date.now() / 2000) * 1.5;
      const targetLoad = 10 + 80 * armDelta + Math.random() * 5;
      
      setTelemetry({
        temp: parseFloat(targetTemp.toFixed(1)),
        load: parseFloat(targetLoad.toFixed(1))
      });
    }, 200);
    return () => clearInterval(interval);
  }, [baseAngle, shoulderAngle, elbowAngle]);

  const isAlarm = telemetry.temp > 65 || telemetry.load > 75;

  return (
    <>
      {/* HUD Panel */}
      <div style={{
        position: 'fixed', top: 15, left: 15, color: 'white',
        background: 'rgba(10,10,20,0.85)', padding: '15px', borderRadius: '10px',
        fontFamily: 'monospace', border: '1px solid #333', zIndex: 100, minWidth: '220px'
      }}>
        <div style={{ color: '#00ffcc', fontWeight: 'bold', fontSize: '14px', marginBottom: '8px' }}>
          INDUSTRIAL TWIN MONITOR
        </div>
        <hr style={{ borderColor: '#333', marginBottom: '10px' }} />
        <div style={{ marginBottom: '6px' }}>
          Estado: <span style={{ color: isAlarm ? '#ff3333' : '#33ff33', fontWeight: 'bold' }}>
            {isAlarm ? '⚠️ CRÍTICO' : '● NOMINAL'}
          </span>
        </div>
        <div style={{ marginBottom: '6px' }}>
          Temperatura: <span style={{ color: telemetry.temp > 60 ? '#ff8800' : '#fff' }}>
            {telemetry.temp} °C
          </span>
        </div>
        <div style={{ marginBottom: '6px' }}>
          Carga Motor: <span style={{ color: telemetry.load > 70 ? '#ff8800' : '#fff' }}>
            {telemetry.load} %
          </span>
        </div>
        <div style={{ fontSize: '10px', color: '#888', marginTop: '10px' }}>
          Base: {baseAngle}° | Hombro: {shoulderAngle}° | Codo: {elbowAngle}°
        </div>
      </div>

      <Canvas camera={{ position: [2, 3, 4], fov: 50 }}>
        <ambientLight intensity={0.4} />
        <directionalLight position={[5, 10, 5]} intensity={1.2} castShadow />
        <pointLight position={[-3, 5, -3]} intensity={0.5} color="#00ffcc" />
        
        <RoboticArm baseRot={baseAngle} shoulderRot={shoulderAngle} elbowRot={elbowAngle} />
        
        <Grid args={[10, 10]} position={[0, -0.01, 0]} cellColor="#333" sectionColor="#555" />
        <OrbitControls makeDefault />
      </Canvas>
    </>
  );
}
