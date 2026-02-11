# Taller - Construyendo el Mundo 3D: Three.js

## Implementación en Three.js / React Three Fiber

### Descripción

Se desarrolló una aplicación web interactiva construida con React y Three.js (a través de React Three Fiber) que permite visualizar modelos 3D en el navegador con múltiples modos de visualización, controles interactivos y captura automática de screenshots.

### Tecnología utilizada

- **React 18.2.0**: Framework de UI para JavaScript
- **Three.js 0.156.0**: Motor de gráficos 3D basado en WebGL
- **@react-three/fiber 8.14.0**: Renderer de Three.js nativo para React
- **@react-three/drei 9.46.0**: Componentes de uso común (OrbitControls, loaders)
- **Vite 5.4.21**: Servidor de desarrollo y bundler ultra-rápido

### Funcionalidades implementadas

1. **Visualización interactiva de modelos 3D** con carga automática de `scene.obj`
2. **4 modos de visualización**: Sólido, Wireframe, Edges, Points
3. **Controles de cámara**: Rotación, zoom y paneo con OrbitControls
4. **Estadísticas del modelo**: Vértices (25,979), caras (45,386), mallas (1)
5. **Sistema automático de captura de screenshots** en `media/threejs/`
6. **Interfaz minimalista** con panel de control y tema oscuro
7. **Renderizado optimizado** con iluminación ambiental y direccional

---

## 🚀 Cómo Usar

### Instalación

```bash
cd threejs/
npm install
```

### Ejecutar servidor de desarrollo

```bash
npm run dev
```

El servidor abrirá automáticamente la app en `http://localhost:5173`

### Producción

```bash
npm run build
npm run preview
```

---

## 📁 Estructura del proyecto

```
threejs/
├── src/
│   ├── App.jsx         # Componente principal
│   ├── ModelViewer.jsx # Cargador 3D
│   └── styles.css      # Estilos
├── public/models/scene.obj  # Modelo OBJ
├── vite.config.js      # Configuración
└── package.json        # Dependencias
```

---

## 📊 Prompts utilizados

```
"Crea una aplicación React Three Fiber con 4 modos de visualización para modelos OBJ"
"¿Cómo detectar automáticamente los bordes de un modelo en Three.js?"
"Implementa captura automática de screenshots en React Three Fiber"
```

---

## 🎓 Aprendizajes

Aprendí cómo integrar Three.js con React usando React Three Fiber, proporcionando una forma declarativa de trabajar con gráficos 3D. Reforcé conocimientos en renderización WebGL, iluminación 3D, cámaras, geometría y materiales. También adquirí habilidades en optimización de rendimiento en WebGL y creación de interfaces interactivas eficientes.

---

## 🛑 Dificultades encontradas

La principal dificultad fue implementar correctamente el sistema de captura de screenshots, requiriendo configuración especial del contexto WebGL. Otro desafío fue calcular correctamente las aristas (edges) ajustando el parámetro `threshold` para detectar bordes visibles sin sobre-capturar. También fue complejo calcular estadísticas cuando el OBJ contiene múltiples mallas anidadas.

---

## 🚀 Mejoras futuras

1. Implementar más modos de visualización (normal mapping, ambient occlusion)
2. Añadir animaciones y transformaciones del modelo
3. Integrar drag-and-drop para modelos personalizados
4. Crear selector de shaders personalizado
5. Exportación a diferentes formatos (GLTF, Babylon)
6. Análisis de rendimiento y profiling
7. Grabación de video de la visualización
8. Editor de materiales en tiempo real

---

## 🔗 Referencias

- Three.js: https://threejs.org/docs/
- React Three Fiber: https://docs.pmnd.rs/react-three-fiber/
- Drei: https://github.com/pmndrs/drei
- WebGL Fundamentals: https://webglfundamentals.org/
- Formato OBJ: https://en.wikipedia.org/wiki/Wavefront_.obj_file

---

**Última actualización**: 2026-02-10
