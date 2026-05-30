import { useEffect, useRef, useState } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Html, Grid } from "@react-three/drei";
import { initializeApp } from "firebase/app";
import { getDatabase, ref, set, onValue } from "firebase/database";

// TODO: paste your Firebase config here (see steps.md → Paso 1)
const firebaseConfig = {
  apiKey:            "REPLACE_ME",
  authDomain:        "REPLACE_ME.firebaseapp.com",
  databaseURL:       "https://REPLACE_ME-default-rtdb.firebaseio.com",
  projectId:         "REPLACE_ME",
  storageBucket:     "REPLACE_ME.appspot.com",
  messagingSenderId: "REPLACE_ME",
  appId:             "REPLACE_ME",
};

const fbApp = initializeApp(firebaseConfig);
const db    = getDatabase(fbApp);

const COLORS = ["#ff4444", "#44ff88", "#4488ff", "#ffee44", "#ff88ee", "#44eeff"];

function PersistentSphere({ pos, color, onClick }) {
  return (
    <mesh position={pos} onClick={onClick}>
      <sphereGeometry args={[0.55, 32, 32]} />
      <meshStandardMaterial color={color} metalness={0.35} roughness={0.25} />
      <Html distanceFactor={6} center>
        <div style={{
          background: "rgba(0,0,0,0.7)", color: "#fff",
          padding: "2px 7px", borderRadius: 4,
          fontSize: 11, fontFamily: "monospace", whiteSpace: "nowrap",
          pointerEvents: "none",
        }}>
          [{pos.map(v => v.toFixed(2)).join(", ")}]
        </div>
      </Html>
    </mesh>
  );
}

export default function App() {
  const [pos,    setPos]    = useState([0, 0, 0]);
  const [color,  setColor]  = useState("#44ff88");
  const [status, setStatus] = useState("Conectando a Firebase...");
  const [lastSaved, setLastSaved] = useState(null);

  // Subscribe to Firebase on mount — loads last saved state in real-time
  useEffect(() => {
    const sphereRef = ref(db, "sphere/state");
    const unsub = onValue(sphereRef, snap => {
      const data = snap.val();
      if (data) {
        setPos([data.x, data.y, data.z]);
        setColor(data.color);
        setStatus("Conectado ✓");
      } else {
        setStatus("Conectado — sin datos aún");
      }
    }, () => setStatus("Error de conexión"));
    return () => unsub();
  }, []);

  const handleClick = () => {
    const newPos = [
      Math.round((Math.random() * 5 - 2.5) * 100) / 100,
      Math.round((Math.random() * 4 - 2)   * 100) / 100,
      Math.round((Math.random() * 2 - 1)   * 100) / 100,
    ];
    const newColor = COLORS[Math.floor(Math.random() * COLORS.length)];
    setPos(newPos);
    setColor(newColor);
    set(ref(db, "sphere/state"), {
      x: newPos[0], y: newPos[1], z: newPos[2],
      color: newColor,
      savedAt: new Date().toISOString(),
    });
    setLastSaved(new Date().toLocaleTimeString());
  };

  return (
    <div style={{ width: "100vw", height: "100vh", background: "#0d0d1a" }}>
      {/* HUD */}
      <div style={{
        position: "absolute", top: 14, left: 14, zIndex: 10,
        color: "#ccc", fontFamily: "monospace", fontSize: 12,
        background: "rgba(0,0,0,0.6)", padding: "10px 14px", borderRadius: 8,
        lineHeight: "1.7",
      }}>
        <div style={{ color: "#58a6ff", fontWeight: "bold", marginBottom: 4 }}>
          Firebase Persistence — semana 15_4
        </div>
        <div>Estado: <span style={{ color: status.startsWith("Conectado") ? "#3fb950" : "#f85149" }}>{status}</span></div>
        <div style={{ color: "#888", marginTop: 4 }}>Haz clic en la esfera para moverla y guardar.</div>
        {lastSaved && (
          <div style={{ color: "#3fb950", marginTop: 4 }}>✓ Guardado a las {lastSaved}</div>
        )}
        <div style={{ color: "#555", marginTop: 6, fontSize: 10 }}>
          Recarga la página — la posición persiste.
        </div>
      </div>

      <Canvas camera={{ position: [0, 2, 7], fov: 50 }}>
        <ambientLight intensity={0.4} />
        <pointLight position={[6, 6, 6]} intensity={1.2} />
        <pointLight position={[-4, -4, 4]} intensity={0.4} color="#4488ff" />

        <PersistentSphere pos={pos} color={color} onClick={handleClick} />

        <Grid
          args={[12, 12]}
          cellColor="#1a1a2e"
          sectionColor="#222244"
          fadeDistance={20}
          position={[0, -2, 0]}
        />
        <OrbitControls makeDefault />
      </Canvas>
    </div>
  );
}
