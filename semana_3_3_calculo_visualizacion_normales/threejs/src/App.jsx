import { Canvas, useThree, useFrame } from "@react-three/fiber";
import { useState, useEffect, useRef, useMemo } from "react";
import * as THREE from "three";
import { OrbitControls as OrbitControlsImpl } from 'three/addons/controls/OrbitControls.js';
import { VertexNormalsHelper } from 'three/addons/helpers/VertexNormalsHelper.js';

// ─── Constants ────────────────────────────────────────────────────────────────
const NORMAL_SHADER = {
  vertexShader: /* glsl */ `
    varying vec3 vNormal;
    varying vec3 vPosition;

    void main() {
      vNormal = normalize(normalMatrix * normal);
      vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: /* glsl */ `
    varying vec3 vNormal;
    varying vec3 vPosition;

    void main() {
      // Map normal direction [-1,1] -> color [0,1]
      vec3 color = vNormal * 0.5 + 0.5;
      gl_FragColor = vec4(color, 1.0);
    }
  `,
};

const LAMBERT_SHADER = {
  vertexShader: /* glsl */ `
    varying vec3 vNormal;
    varying vec3 vPosition;

    void main() {
      vNormal = normalize(normalMatrix * normal);
      vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: /* glsl */ `
    varying vec3 vNormal;
    varying vec3 vPosition;

    uniform vec3 lightDir;
    uniform vec3 baseColor;

    void main() {
      float diff = max(dot(normalize(vNormal), normalize(lightDir)), 0.0);
      vec3 ambient = baseColor * 0.2;
      vec3 diffuse = baseColor * diff * 0.8;
      gl_FragColor = vec4(ambient + diffuse, 1.0);
    }
  `,
};

// ─── Camera Controller ────────────────────────────────────────────────────────
const CameraController = () => {
  const { camera, gl } = useThree();
  useEffect(() => {
    const controls = new OrbitControlsImpl(camera, gl.domElement);
    controls.minDistance = 2;
    controls.maxDistance = 20;
    return () => controls.dispose();
  }, [camera, gl]);
  return null;
};

// ─── Mesh with VertexNormalsHelper ────────────────────────────────────────────
function MeshWithNormalsHelper({ geometry, material, showHelper, helperSize = 0.15 }) {
  const meshRef = useRef();
  const helperRef = useRef(null);
  const { scene } = useThree();

  useEffect(() => {
    if (!meshRef.current) return;

    if (showHelper) {
      const helper = new VertexNormalsHelper(meshRef.current, helperSize, 0x00ff00);
      helperRef.current = helper;
      scene.add(helper);
    }

    return () => {
      if (helperRef.current) {
        scene.remove(helperRef.current);
        helperRef.current.dispose?.();
        helperRef.current = null;
      }
    };
  }, [showHelper, scene, helperSize]);

  return <mesh ref={meshRef} geometry={geometry} material={material} />;
}

// ─── Normal Info Panel ────────────────────────────────────────────────────────
function NormalInfoPanel({ mode, showHelper, onModeChange, onToggleHelper }) {
  const modeDescriptions = {
    normal_color:   "Colorea cada píxel según la dirección de su normal (RGB ← XYZ).",
    flat_lambert:   "Flat shading: misma normal para toda la cara. Iluminación Lambert.",
    smooth_lambert: "Smooth shading: normales interpoladas por vértice. Iluminación Lambert.",
  };

  return (
    <div style={{
      position: "absolute", top: 10, left: 10, zIndex: 10,
      background: "rgba(0,0,0,0.75)", color: "white",
      padding: "16px", borderRadius: "8px",
      fontFamily: "monospace", fontSize: "12px",
      width: "280px", backdropFilter: "blur(4px)"
    }}>
      <h3 style={{ margin: "0 0 12px 0", color: "#61dafb" }}>Normales — Taller 3.3</h3>

      <div style={{ marginBottom: 10 }}>
        <strong style={{ color: "#fca311" }}>Modo de visualización</strong>
        {[
          ["normal_color",   "Normal → Color RGB"],
          ["flat_lambert",   "Flat Shading (Lambert)"],
          ["smooth_lambert", "Smooth Shading (Lambert)"],
        ].map(([key, label]) => (
          <label key={key} style={{ display: "block", marginTop: 6, cursor: "pointer" }}>
            <input
              type="radio"
              name="mode"
              value={key}
              checked={mode === key}
              onChange={() => onModeChange(key)}
              style={{ marginRight: 6 }}
            />
            {label}
          </label>
        ))}
      </div>

      <p style={{ margin: "8px 0", color: "#aaa", fontSize: "11px" }}>
        {modeDescriptions[mode]}
      </p>

      <label style={{ display: "flex", alignItems: "center", gap: 6, cursor: "pointer", marginTop: 10 }}>
        <input type="checkbox" checked={showHelper} onChange={onToggleHelper} />
        Mostrar VertexNormalsHelper
      </label>

      <div style={{ marginTop: 14, borderTop: "1px solid #333", paddingTop: 10, fontSize: "11px", color: "#aaa" }}>
        <div>Geometría: TorusKnotGeometry</div>
        <div>Vértices: depende del LOD</div>
        <div style={{ marginTop: 4 }}>
          Flat: <code style={{ color: "#ff8" }}>flatShading = true</code><br />
          Smooth: <code style={{ color: "#8ff" }}>computeVertexNormals()</code>
        </div>
      </div>
    </div>
  );
}

// ─── Scene ────────────────────────────────────────────────────────────────────
function NormalsScene({ mode, showHelper }) {
  // Build two versions of the same geometry: flat and smooth
  const flatGeometry = useMemo(() => {
    const geo = new THREE.TorusKnotGeometry(1, 0.35, 64, 12);
    // For flat shading we need non-indexed geometry so each face has its own vertices
    return geo.toNonIndexed();
  }, []);

  const smoothGeometry = useMemo(() => {
    const geo = new THREE.TorusKnotGeometry(1, 0.35, 64, 12);
    geo.computeVertexNormals();
    return geo;
  }, []);

  const normalMaterial = useMemo(() => new THREE.ShaderMaterial({
    vertexShader: NORMAL_SHADER.vertexShader,
    fragmentShader: NORMAL_SHADER.fragmentShader,
    side: THREE.DoubleSide,
  }), []);

  const flatMaterial = useMemo(() => new THREE.ShaderMaterial({
    vertexShader: LAMBERT_SHADER.vertexShader,
    fragmentShader: LAMBERT_SHADER.fragmentShader,
    uniforms: {
      lightDir:  { value: new THREE.Vector3(1, 2, 3) },
      baseColor: { value: new THREE.Vector3(0.3, 0.6, 1.0) },
    },
    flatShading: true,
    side: THREE.DoubleSide,
  }), []);

  const smoothMaterial = useMemo(() => new THREE.ShaderMaterial({
    vertexShader: LAMBERT_SHADER.vertexShader,
    fragmentShader: LAMBERT_SHADER.fragmentShader,
    uniforms: {
      lightDir:  { value: new THREE.Vector3(1, 2, 3) },
      baseColor: { value: new THREE.Vector3(1.0, 0.5, 0.2) },
    },
    side: THREE.DoubleSide,
  }), []);

  const activeGeometry = mode === "smooth_lambert" ? smoothGeometry : flatGeometry;
  const activeMaterial =
    mode === "normal_color"   ? normalMaterial  :
    mode === "flat_lambert"   ? flatMaterial    :
                                smoothMaterial;

  return (
    <>
      <ambientLight intensity={0.3} />
      <directionalLight position={[5, 5, 5]} intensity={1} />
      <MeshWithNormalsHelper
        geometry={activeGeometry}
        material={activeMaterial}
        showHelper={showHelper}
        helperSize={0.1}
      />
      <CameraController />
    </>
  );
}

// ─── App ──────────────────────────────────────────────────────────────────────
export default function App() {
  const [mode, setMode] = useState("normal_color");
  const [showHelper, setShowHelper] = useState(true);

  return (
    <div style={{ width: "100%", height: "100%", position: "absolute", top: 0, left: 0 }}>
      <NormalInfoPanel
        mode={mode}
        showHelper={showHelper}
        onModeChange={setMode}
        onToggleHelper={() => setShowHelper(v => !v)}
      />
      <Canvas camera={{ position: [0, 2, 5], fov: 50 }}>
        <color attach="background" args={['#050510']} />
        <NormalsScene mode={mode} showHelper={showHelper} />
      </Canvas>
    </div>
  );
}
