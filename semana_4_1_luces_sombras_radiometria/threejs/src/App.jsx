import LightScene from "./components/LightScene";

/**
 * Legend overlay — describes the 3 light types and 3 material types in the scene.
 * Rendered on top of the Canvas (absolute positioning).
 */
function Legend() {
  const panelStyle = {
    position: "absolute",
    top: 12,
    left: 12,
    zIndex: 10,
    background: "rgba(0, 0, 0, 0.65)",
    color: "#f0f0f0",
    padding: "14px 18px",
    borderRadius: "8px",
    fontFamily: "monospace",
    fontSize: "12px",
    lineHeight: "1.8",
    backdropFilter: "blur(4px)",
    userSelect: "none",
  };

  const dotStyle = (color) => ({
    display: "inline-block",
    width: 10,
    height: 10,
    borderRadius: "50%",
    background: color,
    marginRight: 7,
    verticalAlign: "middle",
  });

  return (
    <div style={panelStyle}>
      <div style={{ marginBottom: 8, color: "#ffd580", fontWeight: "bold" }}>
        💡 Luces
      </div>
      <div><span style={dotStyle("#fff5e0")} />Direccional (luz solar)</div>
      <div><span style={dotStyle("#5599ff")} />Puntual (lámpara azul)</div>
      <div><span style={dotStyle("#888888")} />Ambiental (relleno global)</div>

      <div style={{ margin: "10px 0 8px", color: "#80d4ff", fontWeight: "bold" }}>
        🎨 Materiales
      </div>
      <div><span style={dotStyle("#d94f4f")} />Mate — roughness=1, metalness=0</div>
      <div><span style={dotStyle("#c0c8d0")} />Metálico — roughness=0.05, metalness=1</div>
      <div><span style={dotStyle("#52c0e8")} />Semi-transparente — opacity=0.5</div>

      <div style={{ marginTop: 10, color: "#aaaaaa", fontSize: 11 }}>
        Arrastra para orbitar · Scroll para zoom
      </div>
    </div>
  );
}

export default function App() {
  return (
    <div style={{ width: "100%", height: "100%", position: "absolute", top: 0, left: 0 }}>
      <Legend />
      <LightScene />
    </div>
  );
}
