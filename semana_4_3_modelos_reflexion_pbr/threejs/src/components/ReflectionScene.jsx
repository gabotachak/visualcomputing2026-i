import { Html } from "@react-three/drei";

// Each sphere demonstrates a different reflection model.
// They share the same geometry (sphere r=1.4) and lighting setup.
// Spacing: 5 units between sphere centers on the X axis.

const SPACING = 5;
const Y = 0;
const SPHERE_ARGS = [1.4, 64, 64];

// Shared directional light color and intensity
const LIGHT_COLOR = "#ffffff";

function Sphere({ position, label, formula, children }) {
  return (
    <group position={position}>
      <mesh castShadow receiveShadow>
        <sphereGeometry args={SPHERE_ARGS} />
        {children}
      </mesh>

      {/* Label below sphere */}
      <Html
        position={[0, -2.2, 0]}
        center
        style={{
          textAlign: "center",
          pointerEvents: "none",
          userSelect: "none",
          width: "160px",
        }}
      >
        <div
          style={{
            color: "#f1f5f9",
            fontFamily: "monospace",
            fontSize: "13px",
            fontWeight: "bold",
            background: "rgba(0,0,0,0.55)",
            borderRadius: "6px",
            padding: "4px 8px",
            lineHeight: "1.4",
          }}
        >
          {label}
          {formula && (
            <div
              style={{
                fontSize: "10px",
                color: "#94a3b8",
                marginTop: "2px",
              }}
            >
              {formula}
            </div>
          )}
        </div>
      </Html>
    </group>
  );
}

export default function ReflectionScene() {
  // Five spheres centred at x = -10, -5, 0, 5, 10
  const baseX = -10;

  return (
    <>
      {/* ── Lighting ──────────────────────────────────────────── */}
      {/* Ambient: low-level fill so unlit sides are not pitch black */}
      <ambientLight intensity={0.25} color={LIGHT_COLOR} />

      {/* Key directional light — drives all reflection calculations */}
      <directionalLight
        color={LIGHT_COLOR}
        intensity={3}
        position={[8, 10, 8]}
        castShadow
      />

      {/* Rim light from opposite side to help distinguish spheres */}
      <directionalLight
        color="#6080ff"
        intensity={0.8}
        position={[-6, 4, -8]}
      />

      {/* ── Ground plane ─────────────────────────────────────── */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -2.5, 0]} receiveShadow>
        <planeGeometry args={[60, 30]} />
        <meshStandardMaterial color="#1e293b" roughness={1} metalness={0} />
      </mesh>

      {/* ── Sphere 1: Lambert (pure diffuse) ─────────────────── */}
      {/* I = I_light * k_d * max(N·L, 0)                        */}
      <Sphere
        position={[baseX + SPACING * 0, Y, 0]}
        label="Lambert"
        formula="I = Kd · max(N·L, 0)"
      >
        <meshLambertMaterial color="#e74c3c" />
      </Sphere>

      {/* ── Sphere 2: Phong (diffuse + specular, R·V) ─────────── */}
      {/* I_spec = Ks · max(R·V, 0)^shininess                     */}
      <Sphere
        position={[baseX + SPACING * 1, Y, 0]}
        label="Phong"
        formula="I += Ks · max(R·V,0)^n"
      >
        <meshPhongMaterial
          color="#e74c3c"
          specular="#ffffff"
          shininess={60}
        />
      </Sphere>

      {/* ── Sphere 3: Blinn-Phong (half-vector H = norm(L+V)) ─── */}
      {/* I_spec = Ks · max(N·H, 0)^shininess                     */}
      {/* Three.js MeshPhongMaterial uses Blinn-Phong internally   */}
      <Sphere
        position={[baseX + SPACING * 2, Y, 0]}
        label="Blinn-Phong"
        formula="I += Ks · max(N·H,0)^n"
      >
        <meshPhongMaterial
          color="#e74c3c"
          specular="#ffffff"
          shininess={120}
        />
      </Sphere>

      {/* ── Sphere 4: PBR — dielectric (plastic-like) ────────── */}
      {/* metalness=0 → Fresnel F0=0.04, roughness=0.8 → wide lobe */}
      <Sphere
        position={[baseX + SPACING * 3, Y, 0]}
        label="PBR Dieléctrico"
        formula="metalness=0  roughness=0.8"
      >
        <meshStandardMaterial
          color="#e74c3c"
          metalness={0}
          roughness={0.8}
        />
      </Sphere>

      {/* ── Sphere 5: PBR — metallic (mirror-like) ───────────── */}
      {/* metalness=1 → tinted reflections, roughness=0.1 → sharp */}
      <Sphere
        position={[baseX + SPACING * 4, Y, 0]}
        label="PBR Metálico"
        formula="metalness=1  roughness=0.1"
      >
        <meshStandardMaterial
          color="#e74c3c"
          metalness={1}
          roughness={0.1}
        />
      </Sphere>
    </>
  );
}
