import { Canvas } from '@react-three/fiber'
import { OrbitControls, Grid, Stars } from '@react-three/drei'
import { AnimatedObject } from './AnimatedObject'

function App() {
  return (
    <>
      {/* Interfaz de usuario HTML sobrepuesta */}
      <div className="ui-container">
        <h1>Transformaciones 3D</h1>
        <p>Demostración de Traslación, Rotación y Escala animadas en función del tiempo.</p>
        <p>Usa los controles de la derecha para ajustar los parámetros.</p>
        <p style={{ marginTop: '15px', color: '#80d4ff' }}>Arrastra para mover la cámara • Scroll para hacer zoom</p>
      </div>

      {/* Canvas donde se renderiza la escena 3D */}
      <Canvas camera={{ position: [0, 2, 8], fov: 45 }}>
        <color attach="background" args={['#0a0a14']} />

        {/* Iluminación base de la escena */}
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1.5} />
        <pointLight position={[-10, -10, -5]} intensity={0.5} color="#00d2ff" />

        {/* El objeto al que se aplican las transformaciones */}
        <AnimatedObject />

        {/* Elementos de entorno (entorno estático de referencia) */}
        <Grid
          renderOrder={-1}
          position={[0, -3, 0]}
          infiniteGrid
          cellSize={1}
          cellThickness={1}
          sectionSize={5}
          sectionThickness={1.5}
          fadeDistance={30}
          cellColor="#223344"
          sectionColor="#335577"
        />
        <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

        {/* Controles para mover la cámara (Navegación espacial) */}
        <OrbitControls makeDefault enableDamping dampingFactor={0.05} />
      </Canvas>
    </>
  )
}

export default App
