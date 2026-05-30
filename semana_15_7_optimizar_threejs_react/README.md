# Taller - Optimización de Renderizado en Three.js (InstancedMesh & LOD)

## Nombre del estudiante
Gabriel Andrés Anzola Tachak

## Fecha de entrega
2026-05-29

---

## Descripción breve

Este taller aborda las técnicas esenciales de **optimización de rendimiento gráfico (WebGL)** para aplicaciones web interactivas utilizando **Three.js** y **React Three Fiber**. La aplicación compara de forma práctica dos metodologías de renderizado para 3,000 esferas independientes en el espacio:
1. **No Optimizado (Separate Meshes):** Crea 3,000 mallas individuales, forzando a la GPU a procesar 3,000 llamadas de dibujo (draw calls) por frame. Esto genera un cuello de botella sustancial en la CPU por la sobrecarga del controlador (driver overhead), reduciendo la tasa de FPS notablemente.
2. **Optimizado (InstancedMesh):** Agrupa las 3,000 esferas en una única malla instanciada (`instancedMesh`), enviando la geometría una sola vez a la GPU y realizando **1 sola llamada de dibujo** para toda la escena, manteniendo una tasa de 60 FPS estables.

Además, se incluye una demostración de **Level of Detail (LOD)** que reduce la complejidad geométrica (número de segmentos de las mallas) en función de la distancia del objeto a la cámara.

---

## Implementaciones

### Three.js / React Three Fiber

**Herramientas:** React 18 · Three.js r160 · @react-three/fiber r8 · @react-three/drei r9 · Vite · Leva

| Componente / Técnica | Funcionalidad |
|---|---|
| `<instancedMesh>` | Malla instanciada de Three.js que recibe una sola geometría y material, y actualiza las matrices de transformación de las 3,000 instancias mediante un buffer indexado. |
| `<Detailed>` | Componente de Drei que implementa Level of Detail (LOD), alternando dinámicamente entre esferas High Poly (64x64 segmentos), Medium Poly (16x16) y Low Poly (4x4) según la distancia de la cámara. |
| `FpsMonitor` | Panel HUD en pantalla que despliega las estadísticas del renderizado (modo activo, cantidad de draw calls de WebGL y tasa de frames por segundo calculada de forma dinámica). |

---

## Resultados visuales

### Escena Optimizada con InstancedMesh (60 FPS)

![Optimization Static](./media/optimization.png)
Captura de la escena con 3,000 esferas de color verde renderizadas en un solo draw call con un rendimiento nominal óptimo a 60 FPS estables.

### Comparación e Interacción Dinámica del Panel

![Optimization Animation](./media/optimization.gif)
GIF demostrando el comportamiento del visualizador al rotar la escena y el panel de estadísticas performance adaptándose según el modo activo.

---

## Código relevante

Configuración de matrices en `instancedMesh` en `App.jsx`:

```jsx
function OptimizedSpheres() {
  const meshRef = useRef();

  useEffect(() => {
    for (let i = 0; i < COUNT; i++) {
      // Posición aleatoria en el espacio
      const x = (Math.random() - 0.5) * 15;
      const y = (Math.random() - 0.5) * 15;
      const z = (Math.random() - 0.5) * 15;
      
      tempObject.position.set(x, y, z);
      tempObject.updateMatrix();
      
      // Asignar matriz de transformación a la instancia i
      meshRef.current.setMatrixAt(i, tempObject.matrix);
    }
    meshRef.current.instanceMatrix.needsUpdate = true;
  }, []);

  return (
    <instancedMesh ref={meshRef} args={[null, null, COUNT]}>
      <sphereGeometry args={[0.08, 8, 8]} />
      <meshStandardMaterial color="#33ff99" roughness={0.5} />
    </instancedMesh>
  );
}
```

---

## Prompts utilizados

- No se utilizaron prompts de IA para la generación de imágenes.

---

## Aprendizajes y dificultades

### Aprendizajes
- Diferencia fundamental entre cuellos de botella de GPU (límites de fill-rate o fragment shader) y de CPU (sobrecarga de draw calls en el hilo principal).
- Uso de matrices de transformación (`THREE.Matrix4`) para posicionar y escalar de forma masiva miles de instancias de objetos mediante un único búfer de datos.
- Aplicación de técnicas de Level of Detail (LOD) para economizar recursos en objetos lejanos.

### Dificultades
- La actualización interactiva de instancias individuales en tiempo real es compleja dado que todas comparten la misma geometría y material. Para animar el giro de las esferas de forma coordinada, se optó por rotar el contenedor principal `instancedMesh` completo en el loop de `useFrame`, preservando el beneficio de 1 solo draw call.

### Mejoras futuras
- Implementar frustum culling manual en GPU mediante compute shaders o shaders personalizados para no procesar instancias que estén fuera del campo visual de la cámara.
- Utilizar texturas comprimidas (como formatos KTX2 o Basis Universal) para disminuir sustancialmente la carga de memoria de texturas en la GPU.

---

## Contribuciones grupales
Taller realizado de forma individual.

---

## Estructura del proyecto

```
semana_15_7_optimizar_threejs_react/
├── threejs/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       └── styles.css
├── media/
│   ├── optimization.png
│   └── optimization.gif
└── README.md
```

---

## Referencias
- WebGL Drawing Performance (MDN): https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices
- Three.js InstancedMesh Documentation: https://threejs.org/docs/#api/en/objects/InstancedMesh

---

## Checklist
- [x] Carpeta con nombre semana_15_7_optimizar_threejs_react
- [x] Código limpio y funcional
- [x] GIFs/imágenes en media/ con nombres descriptivos
- [x] README completo con todas las secciones
- [x] Mínimo 2 capturas/GIFs por implementación
- [x] Commits descriptivos en inglés
