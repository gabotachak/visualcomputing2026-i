import { StrictMode, useState, useRef } from 'react'
import { createRoot } from 'react-dom/client'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import * as THREE from 'three'

// ─────────────────────────────────────────────
// Depth-visualising shader: maps gl_FragCoord.z to greyscale
// ─────────────────────────────────────────────
const depthVertexShader = /* glsl */ `
  varying float vDepth;
  void main() {
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    // normalized device z in [0,1] after perspective divide
    vDepth = gl_Position.z / gl_Position.w * 0.5 + 0.5;
  }
`

const depthFragmentShader = /* glsl */ `
  varying float vDepth;
  void main() {
    // gl_FragCoord.z is the window-space depth [0,1]
    gl_FragColor = vec4(vec3(gl_FragCoord.z), 1.0);
  }
`

// ─────────────────────────────────────────────
// A single mesh that can toggle between normal and depth material
// ─────────────────────────────────────────────
function DepthMesh({ geometry, color, position, depthView, depthTest }) {
  const normalMat = new THREE.MeshStandardMaterial({ color, depthTest })
  const shaderMat = new THREE.ShaderMaterial({
    vertexShader: depthVertexShader,
    fragmentShader: depthFragmentShader,
    depthTest,
  })

  return (
    <mesh position={position} material={depthView ? shaderMat : normalMat}>
      <primitive object={geometry} attach="geometry" />
    </mesh>
  )
}

// ─────────────────────────────────────────────
// Scene objects: multiple shapes at different Z depths
// ─────────────────────────────────────────────
const OBJECTS = [
  { geometry: new THREE.BoxGeometry(1.5, 1.5, 1.5),     color: '#e74c3c', position: [-2.5,  0,  0]  },
  { geometry: new THREE.SphereGeometry(0.9, 32, 32),    color: '#2ecc71', position: [  0,   0, -1]  },
  { geometry: new THREE.ConeGeometry(0.8, 2, 32),       color: '#3498db', position: [ 2.5,  0,  1]  },
  { geometry: new THREE.TorusGeometry(0.7, 0.3, 16, 60),color: '#f39c12', position: [  0, 1.5, -3]  },
  { geometry: new THREE.OctahedronGeometry(1),          color: '#9b59b6', position: [  0,  -1,  2]  },
]

// ─────────────────────────────────────────────
// Slowly-rotating group wrapper so objects slide past each other
// ─────────────────────────────────────────────
function RotatingScene({ depthView, depthTest }) {
  const groupRef = useRef()
  useFrame(({ clock }) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = clock.getElapsedTime() * 0.3
    }
  })
  return (
    <group ref={groupRef}>
      {OBJECTS.map((obj, i) => (
        <DepthMesh key={i} {...obj} depthView={depthView} depthTest={depthTest} />
      ))}
    </group>
  )
}

// ─────────────────────────────────────────────
// Z-fighting demo: two quads nearly co-planar
// ─────────────────────────────────────────────
function ZFightingDemo({ active }) {
  if (!active) return null
  const mat1 = new THREE.MeshBasicMaterial({ color: '#ff0000', side: THREE.DoubleSide })
  const mat2 = new THREE.MeshBasicMaterial({ color: '#0000ff', side: THREE.DoubleSide })
  const geo = new THREE.PlaneGeometry(3, 3)
  return (
    <group position={[0, 0, 0]}>
      <mesh geometry={geo} material={mat1} position={[0, 0, 0]} />
      {/* offset by a tiny epsilon to trigger z-fighting */}
      <mesh geometry={geo} material={mat2} position={[0, 0, 0.002]} />
    </group>
  )
}

// ─────────────────────────────────────────────
// UI overlay
// ─────────────────────────────────────────────
const overlayStyle = {
  position: 'absolute', top: 12, left: 12, zIndex: 10,
  background: 'rgba(0,0,0,0.75)', color: '#fff',
  padding: '14px 18px', borderRadius: 8, fontFamily: 'monospace',
  fontSize: 13, userSelect: 'none', maxWidth: 280,
}
const btnStyle = (active) => ({
  display: 'block', width: '100%', margin: '6px 0',
  padding: '6px 10px', borderRadius: 4, border: 'none',
  cursor: 'pointer', fontFamily: 'monospace', fontSize: 12,
  background: active ? '#2ecc71' : '#555', color: '#fff',
})

// ─────────────────────────────────────────────
// App
// ─────────────────────────────────────────────
function App() {
  const [depthView, setDepthView] = useState(false)
  const [depthTest, setDepthTest] = useState(true)
  const [zFighting, setZFighting] = useState(false)
  const [near, setNear] = useState(0.1)
  const [far, setFar] = useState(100)

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative', background: '#111' }}>
      {/* ── Controls ── */}
      <div style={overlayStyle}>
        <h3 style={{ margin: '0 0 10px', color: '#61dafb' }}>Z-Buffer & Depth Testing</h3>

        <button style={btnStyle(depthView)} onClick={() => setDepthView(v => !v)}>
          {depthView ? '✓ Depth Shader ON' : '  Depth Shader OFF'}
        </button>

        <button style={btnStyle(depthTest)} onClick={() => setDepthTest(v => !v)}>
          {depthTest ? '✓ depthTest ON' : '  depthTest OFF'}
        </button>

        <button style={btnStyle(zFighting)} onClick={() => setZFighting(v => !v)}>
          {zFighting ? '✓ Z-Fighting Demo ON' : '  Z-Fighting Demo OFF'}
        </button>

        <div style={{ marginTop: 10 }}>
          <label>near: <b>{near}</b></label><br />
          <input type="range" min="0.01" max="5" step="0.01" value={near}
            onChange={e => setNear(parseFloat(e.target.value))}
            style={{ width: '100%' }} />
          <label>far: <b>{far}</b></label><br />
          <input type="range" min="10" max="1000" step="10" value={far}
            onChange={e => setFar(parseFloat(e.target.value))}
            style={{ width: '100%' }} />
        </div>

        <div style={{ marginTop: 10, fontSize: 11, color: '#aaa', lineHeight: 1.5 }}>
          <b>Depth shader</b>: visualises gl_FragCoord.z<br />
          <b>depthTest OFF</b>: painter's algorithm artefacts<br />
          <b>Z-Fighting</b>: two co-planar polygons
        </div>
      </div>

      {/* ── Canvas ── */}
      <Canvas gl={{ logarithmicDepthBuffer: false }}>
        <PerspectiveCamera makeDefault position={[0, 2, 8]} near={near} far={far} fov={60} />
        <color attach="background" args={['#111']} />
        <ambientLight intensity={0.6} />
        <directionalLight position={[5, 8, 5]} intensity={1.2} />

        {zFighting
          ? <ZFightingDemo active={zFighting} />
          : <RotatingScene depthView={depthView} depthTest={depthTest} />
        }

        <OrbitControls enablePan />
      </Canvas>
    </div>
  )
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
)
