# Three.js - Jerarquías y Transformaciones

Proyecto React Three Fiber para visualizar sistemas de coordenadas jerárquicos y la herencia de transformaciones matriciales en WebGL.

## Iniciar servidor local

```bash
cd threejs
npm install
npm run dev
```

El servidor estará corriendo en `http://localhost:5173/`.

## Características
- Implementa una cadena Padre -> Hijo -> Nieto utilizando `<group>` y Refs de React.
- Cuenta con controles UI implementados con `leva` que modifican instantáneamente la rotación global y translación de las figuras.
- Posee la herramienta `<axesHelper>` adjuntada a cada nodo para visualizar el estado exacto de sus respectivos sistemas de rotación locales.
- Botón para exportar canvas (descarga directa de screenshot).
