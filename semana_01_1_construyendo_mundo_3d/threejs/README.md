# Three.js — Construyendo Mundo 3D (React + R3F)

Instrucciones para la actividad Three.js (React Three Fiber + Vite).

Estructura del proyecto:

- `index.html` — entrada Vite
- `src/` — código fuente React
- `public/models/scene.glb` — coloca aquí tu modelo (opcional)

Instalación y ejecución:

1. Desde la carpeta `threejs/` ejecutar:

```bash
npm install
npm run dev
```

2. Abrir el servidor dev que muestra la app (por defecto http://localhost:5173)

Dónde poner modelos:

- Por defecto el visor intenta cargar `/models/scene.glb`. Coloca tu archivo glTF/GLB en `threejs/public/models/scene.glb`.
- También puedes cambiar la ruta en `src/App.jsx` (prop `src` del componente `ModelViewer`).

Qué incluye:

- Un visor R3F con `OrbitControls`.
- Múltiples modos de visualización: Sólido, Wireframe, Edges y Points.
- Estadísticas básicas del modelo (vértices, caras, número de mallas).

Notas:

- Si no tienes un modelo, la app muestra un cubo de prueba.
- Para mejores resultados usa modelos triangulados (GLTF / GLB).
