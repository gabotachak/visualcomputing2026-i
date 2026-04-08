# Taller 3.3 — Cálculo y Visualización de Normales

**Nombre:** Gabriel Andres Anzola Tachak  
**Fecha de entrega:** 2026-04-08  
**Curso:** Computación Visual 2026-I

---

## Descripción

Este taller aborda el cálculo de vectores normales desde cero, sin depender de funciones
de biblioteca que los entreguen automáticamente. A partir de una malla triangular se
derivan las **normales de cara** (usando el producto cruz de las aristas) y las
**normales de vértice** (promediando las normales de las caras adyacentes).

Se compara el resultado manual contra `trimesh` para verificar la corrección, y se
visualizan ambos tipos de normales como flechas sobre el modelo. Finalmente se ilustra
cómo la elección de la normal —por cara o por vértice— produce los efectos visuales
de *flat shading* y *smooth shading* bajo iluminación Lambert.

El entorno Three.js añade una visualización interactiva con `VertexNormalsHelper` y
un `ShaderMaterial` que colorea cada píxel según la dirección de su normal (mapeando
el vector XYZ al espacio de color RGB).

---

## Implementaciones por entorno

| Entorno  | Archivo principal              | Descripción |
|----------|-------------------------------|-------------|
| Python   | `python/calculo_normales.ipynb` | Cálculo manual + validación + flat vs smooth |
| Three.js | `threejs/src/App.jsx`          | Visualización interactiva con helper y shader |

---

## Resultados visuales

### Python

| Imagen | Descripción |
|--------|-------------|
| `media/normales_cara_vertice.png` | Normales de cara (rojo) y de vértice (verde) como flechas |
| `media/flat_vs_smooth_shading.png` | Comparación lado a lado flat vs smooth |
| `media/normal_map.png` | Mapa de normales: XYZ → RGB |

### Three.js

Capturas disponibles en `media/` tras ejecutar `npm run dev`.

![Cálculo y Visualización de Normales gif](./media/normales_test.gif)

---

## Código relevante

### Producto cruz para normal de cara (Python)

```python
edge1 = v1 - v0
edge2 = v2 - v0
normal = np.cross(edge1, edge2)
normal = normal / np.linalg.norm(normal)
```

### Promedio de normales adyacentes para vértice (Python)

```python
for fi, (i0, i1, i2) in enumerate(faces):
    vertex_normals[i0] += face_normals[fi]
    vertex_normals[i1] += face_normals[fi]
    vertex_normals[i2] += face_normals[fi]
vertex_normals /= np.linalg.norm(vertex_normals, axis=1, keepdims=True)
```

### Fragment shader — normal como color (Three.js)

```glsl
varying vec3 vNormal;

void main() {
    vec3 color = vNormal * 0.5 + 0.5;   // [-1,1] → [0,1]
    gl_FragColor = vec4(color, 1.0);
}
```

### VertexNormalsHelper (Three.js)

```js
import { VertexNormalsHelper } from 'three/addons/helpers/VertexNormalsHelper.js';

const helper = new VertexNormalsHelper(mesh, 0.1, 0x00ff00);
scene.add(helper);
```

---

## Prompts utilizados

Se usó IA (Claude) como asistente para generar el scaffolding del taller y estructurar
el notebook. La lógica matemática (producto cruz, promedio ponderado, validación) fue
revisada y verificada manualmente.

---

## Aprendizajes y dificultades

- El producto cruz `(v1-v0) × (v2-v0)` depende del **orden** de los vértices (winding
  order): invertirlo cambia el signo de la normal. Es importante verificar que las
  normales apunten hacia afuera antes de usarlas en iluminación.
- El *smooth shading* no requiere más geometría: solo interpola las normales en los
  vértices en lugar de usar una normal plana por cara, lo que da la ilusión de una
  superficie curva.
- `VertexNormalsHelper` en three.js ≥ r166 se importa desde `three/addons/`, no desde
  `three/examples/jsm/`.
- `trimesh` calcula normales de vértice usando el ángulo de apertura de cada cara como
  peso (no simple promedio); eso explica pequeñas diferencias respecto al promedio
  simple implementado aquí.

---

## Estructura del proyecto

```
semana_3_3_calculo_visualizacion_normales/
├── python/
│   └── calculo_normales.ipynb
├── threejs/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── eslint.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       └── index.css
├── media/
└── README.md
```
