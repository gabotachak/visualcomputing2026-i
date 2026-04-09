import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import ReflectionScene from "./components/ReflectionScene";

export default function App() {
  return (
    <div style={{ width: "100vw", height: "100vh", background: "#111" }}>
      <Canvas
        camera={{ position: [0, 4, 18], fov: 50 }}
        style={{ width: "100%", height: "100%" }}
      >
        <color attach="background" args={["#111827"]} />
        <ReflectionScene />
        <OrbitControls makeDefault />
      </Canvas>
    </div>
  );
}
