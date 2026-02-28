# Three.js - Conversión de Formatos 3D

Aplicación web desarrollada con React Three Fiber para visualizar y comparar modelos interactivos en los formatos estructurales OBJ, STL y GLTF.

## Ejecución

```bash
npm install
npm run dev
```

## Características
- Integración de múltiples cargadores en runtime (`OBJLoader`, `STLLoader`, `GLTFLoader`).
- Panel de estadísticas para analizar métricas de rendimiento en tiempo real como vértices cargados y polígonos.
- Renderizado optimizado contrastando el manejo nativo de los recursos de malla frente al WebGL API.
