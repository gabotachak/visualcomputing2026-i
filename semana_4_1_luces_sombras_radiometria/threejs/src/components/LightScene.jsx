import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

/**
 * Scene — all 3D objects and lights live here, inside the Canvas context.
 *
 * Radiometry summary:
 *   - Ambient light:     constant irradiance, no direction, no shadows.
 *                        Simulates global indirect illumination.
 *   - Directional light: parallel rays (infinite distance source).
 *                        Simulates sunlight; position defines direction only.
 *                        Configured with shadow-map for PCF shadow rendering.
 *   - Point light:       omnidirectional, attenuates with distance (1/r²).
 *                        Simulates a local lamp or candle.
 *
 * Materials:
 *   - Matte (box):        roughness=1, metalness=0 → Lambertian diffuse response.
 *   - Metallic (sphere):  roughness=0.05, metalness=1 → mirror-like specular.
 *   - Transparent (torus):transparent=true, opacity=0.5 → partial light transmission.
 */
function Scene() {
  return (
    <>
      {/* ── LIGHTS ─────────────────────────────────────────────────── */}

      {/* Ambient: fills the whole scene with constant, directionless light.
          Low intensity so it doesn't wash out shadows. */}
      <ambientLight intensity={0.25} color="#ffffff" />

      {/* Directional: warm sunlight from the upper-right.
          shadow-mapSize 2048×2048 gives crisp shadow edges. */}
      <directionalLight
        position={[5, 8, 5]}
        intensity={1.8}
        color="#fff5e0"
        castShadow
        shadow-mapSize={[2048, 2048]}
        shadow-camera-near={0.1}
        shadow-camera-far={60}
        shadow-camera-left={-12}
        shadow-camera-right={12}
        shadow-camera-top={12}
        shadow-camera-bottom={-12}
      />

      {/* Point: cool blue accent from the opposite side.
          Intensity in physical units (candela); falls off with distance. */}
      <pointLight position={[-5, 4, -4]} intensity={40} color="#5599ff" />

      {/* ── FLOOR (shadow receiver) ─────────────────────────────────── */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]} receiveShadow>
        <planeGeometry args={[24, 24]} />
        {/* Dark concrete-like surface — high roughness to show diffuse shading */}
        <meshStandardMaterial color="#2a2a35" roughness={1} metalness={0} />
      </mesh>

      {/* ── OBJECT 1: Matte box ────────────────────────────────────── */}
      {/* roughness=1, metalness=0 → only diffuse (Lambertian) response.
          No specular highlight visible. */}
      <mesh position={[-2.5, 0.75, 0]} castShadow receiveShadow>
        <boxGeometry args={[1.5, 1.5, 1.5]} />
        <meshStandardMaterial color="#d94f4f" roughness={1} metalness={0} />
      </mesh>

      {/* ── OBJECT 2: Metallic sphere ──────────────────────────────── */}
      {/* roughness≈0, metalness=1 → dominant specular reflection.
          Reflects environment and lights like a mirror. */}
      <mesh position={[0, 0.75, 0]} castShadow receiveShadow>
        <sphereGeometry args={[0.75, 64, 64]} />
        <meshStandardMaterial color="#c0c8d0" roughness={0.05} metalness={1} />
      </mesh>

      {/* ── OBJECT 3: Semi-transparent torus ──────────────────────── */}
      {/* opacity=0.5 → light partially passes through (transmission).
          depthWrite=false prevents z-fighting artefacts on overlapping faces. */}
      <mesh position={[2.5, 0.85, 0]} castShadow receiveShadow>
        <torusGeometry args={[0.65, 0.27, 32, 80]} />
        <meshStandardMaterial
          color="#52c0e8"
          transparent
          opacity={0.5}
          roughness={0.15}
          metalness={0}
          depthWrite={false}
        />
      </mesh>

      {/* ── CAMERA CONTROLS ────────────────────────────────────────── */}
      <OrbitControls
        minDistance={3}
        maxDistance={40}
        maxPolarAngle={Math.PI / 2 - 0.05}
      />
    </>
  );
}

/**
 * LightScene — top-level component.
 * The Canvas is configured with `shadows` to enable the WebGL shadow-map pipeline.
 */
export default function LightScene() {
  return (
    <Canvas
      shadows
      camera={{ position: [7, 6, 10], fov: 45 }}
      style={{ width: "100%", height: "100%" }}
    >
      <color attach="background" args={["#1a1a2e"]} />
      <Scene />
    </Canvas>
  );
}
