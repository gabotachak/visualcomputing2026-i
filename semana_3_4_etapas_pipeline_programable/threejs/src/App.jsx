import { Canvas, useThree, useFrame } from "@react-three/fiber";
import { useState, useEffect, useRef, useMemo } from "react";
import * as THREE from "three";
import { OrbitControls as OrbitControlsImpl } from 'three/addons/controls/OrbitControls.js';

// ─── Importar shaders desde archivos .glsl (Vite los carga como texto) ────────
import vertexShader   from './shaders/vertex.glsl?raw';
import fragmentShader from './shaders/fragment.glsl?raw';

// ─── Constantes ───────────────────────────────────────────────────────────────
const LIGHT_DIR    = new THREE.Vector3(1.5, 2.0, 2.5).normalize();
const INITIAL_FREQ = 5.0;   // frecuencia de la onda del vertex shader (uniforme)
const INITIAL_AMP  = 0.12;  // amplitud (en el shader está fija, aquí lo mostramos)
const INITIAL_FPS  = 3.0;   // exponente Fresnel inicial

// ─── Etapas del pipeline para el panel de información ─────────────────────────
const PIPELINE_STAGES = [
  {
    key: "vertex",
    label: "1. Vertex Processing",
    color: "#fca311",
    desc: "El vertex shader recibe cada vértice en model space, aplica la deformación sinusoidal y lo transforma a clip space mediante projectionMatrix × modelViewMatrix.",
  },
  {
    key: "primitive",
    label: "2. Primitive Assembly",
    color: "#61dafb",
    desc: "La GPU agrupa los vértices procesados en triángulos y realiza clipping (descarta lo que está fuera del frustum) y perspective divide (→ NDC).",
  },
  {
    key: "raster",
    label: "3. Rasterization",
    color: "#a8ff78",
    desc: "Cada triángulo se convierte en fragmentos (píxeles candidatos). Los varyings (vUv, vNormal, vPosition) se interpolan baricentricamente.",
  },
  {
    key: "fragment",
    label: "4. Fragment Processing",
    color: "#ff8fab",
    desc: "El fragment shader calcula el color final: color UV + Lambert + Fresnel. Resultado → framebuffer.",
  },
];

// ─── Controlador de cámara ────────────────────────────────────────────────────
const CameraController = () => {
  const { camera, gl } = useThree();
  useEffect(() => {
    const controls = new OrbitControlsImpl(camera, gl.domElement);
    controls.minDistance = 2;
    controls.maxDistance = 15;
    return () => controls.dispose();
  }, [camera, gl]);
  return null;
};

// ─── Malla con ShaderMaterial animado ─────────────────────────────────────────
function AnimatedMesh({ fresnelPow }) {
  const meshRef  = useRef();
  const matRef   = useRef();
  const clockRef = useRef(0);

  // ShaderMaterial creado una sola vez; actualizamos uniforms en useFrame
  const material = useMemo(() => new THREE.ShaderMaterial({
    vertexShader,
    fragmentShader,
    uniforms: {
      time:       { value: 0 },
      lightDir:   { value: LIGHT_DIR },
      fresnelPow: { value: INITIAL_FPS },
    },
    side: THREE.DoubleSide,
  }), []);

  // Actualizar uniforms en cada fotograma
  useFrame((_, delta) => {
    clockRef.current += delta;
    material.uniforms.time.value       = clockRef.current;
    material.uniforms.fresnelPow.value = fresnelPow;
  });

  // Geometría con suficientes segmentos para que la deformación sea visible
  const geometry = useMemo(
    () => new THREE.SphereGeometry(1.4, 64, 64),
    []
  );

  return (
    <mesh ref={meshRef} geometry={geometry} material={material} />
  );
}

// ─── Panel de pipeline ────────────────────────────────────────────────────────
function PipelinePanel({ activeStage, onStageClick, fresnelPow, onFresnelChange }) {
  return (
    <div style={{
      position: "absolute", top: 10, left: 10, zIndex: 10,
      background: "rgba(0,0,0,0.8)", color: "white",
      padding: "16px", borderRadius: "8px",
      fontFamily: "monospace", fontSize: "12px",
      width: "300px", backdropFilter: "blur(4px)",
      maxHeight: "95vh", overflowY: "auto",
    }}>
      <h3 style={{ margin: "0 0 12px 0", color: "#61dafb" }}>
        Pipeline Programable — 3.4
      </h3>

      {PIPELINE_STAGES.map(({ key, label, color, desc }) => (
        <div
          key={key}
          onClick={() => onStageClick(key)}
          style={{
            marginBottom: 8, padding: "8px 10px",
            borderRadius: 6, cursor: "pointer",
            border: `1px solid ${activeStage === key ? color : "#333"}`,
            background: activeStage === key ? `${color}22` : "transparent",
            transition: "all 0.15s",
          }}
        >
          <div style={{ color, fontWeight: "bold", marginBottom: 4 }}>{label}</div>
          {activeStage === key && (
            <div style={{ color: "#ccc", fontSize: "11px", lineHeight: 1.5 }}>{desc}</div>
          )}
        </div>
      ))}

      <div style={{ marginTop: 14, borderTop: "1px solid #333", paddingTop: 12 }}>
        <div style={{ marginBottom: 6, color: "#aaa" }}>Fresnel power: <strong style={{ color: "#ff8fab" }}>{fresnelPow.toFixed(1)}</strong></div>
        <input
          type="range" min="1" max="8" step="0.1"
          value={fresnelPow}
          onChange={e => onFresnelChange(parseFloat(e.target.value))}
          style={{ width: "100%", accentColor: "#ff8fab" }}
        />
      </div>

      <div style={{ marginTop: 12, fontSize: "10px", color: "#555", borderTop: "1px solid #222", paddingTop: 10 }}>
        <div>Vertex shader: <code style={{ color: "#fca311" }}>vertex.glsl</code></div>
        <div>Fragment shader: <code style={{ color: "#ff8fab" }}>fragment.glsl</code></div>
        <div>Uniforms: <code style={{ color: "#a8ff78" }}>time · lightDir · fresnelPow</code></div>
        <div>Varyings: <code style={{ color: "#61dafb" }}>vUv · vNormal · vPosition</code></div>
      </div>
    </div>
  );
}

// ─── App ──────────────────────────────────────────────────────────────────────
export default function App() {
  const [activeStage, setActiveStage] = useState("vertex");
  const [fresnelPow, setFresnelPow]   = useState(INITIAL_FPS);

  return (
    <div style={{ width: "100%", height: "100%", position: "absolute", top: 0, left: 0 }}>
      <PipelinePanel
        activeStage={activeStage}
        onStageClick={setActiveStage}
        fresnelPow={fresnelPow}
        onFresnelChange={setFresnelPow}
      />
      <Canvas camera={{ position: [0, 1.5, 4], fov: 50 }}>
        <color attach="background" args={['#050510']} />
        <AnimatedMesh fresnelPow={fresnelPow} />
        <CameraController />
      </Canvas>
    </div>
  );
}
