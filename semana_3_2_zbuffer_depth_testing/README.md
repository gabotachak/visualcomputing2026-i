# Taller 3.2 — Z-Buffer y Depth Testing

**Estudiante:** Gabriel Andres Anzola Tachak  
**Fecha de entrega:** 2026-04-08  

---

## Descripción

Este taller explora el mecanismo de **Z-buffer (depth buffer)** como solución al problema de la visibilidad en el renderizado 3D.

En la primera parte (Python) se implementa desde cero un rasterizador con y sin Z-buffer, se visualiza el depth buffer en escala de grises, se comparan ambos métodos lado a lado, y se estudian los efectos de precisión numérica que causan **Z-fighting**.

En la segunda parte (Three.js / React Three Fiber) se construye una escena interactiva que permite activar un **depth shader** (`gl_FragCoord.z`), desactivar `depthTest` para reproducir los artefactos del algoritmo del pintor, variar los planos `near`/`far` de la cámara en tiempo real y demostrar Z-fighting con dos polígonos casi co-planares.

---

## Implementaciones

### Python — `python/zbuffer_depth_testing.ipynb`

| Sección | Descripción |
|---|---|
| Painter's Algorithm | Renderizado sin depth test; triángulos dibujados de atrás a adelante |
| Z-buffer | Matriz `depth_buf` inicializada en `np.inf`; actualización condicional por píxel |
| Depth buffer visual | Normalización `[0,1]` e inversión (cercano = blanco) |
| Comparación | Panel 1×3 mostrando Painter / Z-buffer / Depth map |
| Precisión near/far | Curvas NDC-z para ratios 1:100, 1:10 000, 1:10^6 |
| Z-fighting | Dos triángulos co-planares con Δz decreciente (0.5 → 0.0005) |
| GIF animado | 36 fotogramas rotando la escena, Painter vs Z-buffer lado a lado |

### Three.js — `threejs/src/main.jsx`

| Feature | Detalle |
|---|---|
| Múltiples objetos | Cubo, esfera, cono, toro, octaedro a distintas profundidades |
| PerspectiveCamera | `near` y `far` controlados en tiempo real con sliders |
| Depth shader | Fragment shader que visualiza `gl_FragCoord.z` en escala de grises |
| depthTest toggle | Botón para activar/desactivar depth test y ver artefactos |
| Z-fighting demo | Dos quads co-planares con Δz = 0.002 |
| OrbitControls | Rotación libre de la escena |

---

## Resultados visuales

| Imagen | Descripción |
|---|---|
| `media/painter_no_zbuffer.png` | Escena con Painter's Algorithm — artefactos de solapamiento |
| `media/zbuffer_correct.png` | Misma escena con Z-buffer — oclusiones correctas |
| `media/depth_buffer_grayscale.png` | Depth buffer normalizado en escala de grises |
| `media/comparacion_zbuffer.png` | Comparación lado a lado: Painter / Z-buffer / Depth map |
| `media/zbuffer_precision_nearfar.png` | Curvas de precisión para distintos ratios near/far |
| `media/zfighting_demo.png` | Z-fighting con separación Δz decreciente |
| `media/zbuffer_rotation.gif` | GIF animado — rotación de la escena Painter vs Z-buffer |

---

## Código relevante

### Núcleo del Z-buffer (Python)

```python
if use_zbuffer:
    update_mask = z_interp < depth_buf[px_y, px_x]
    depth_buf[px_y, px_x][update_mask] = z_interp[update_mask]
    color_buf[px_y, px_x][update_mask] = color
else:
    color_buf[px_y, px_x] = color  # siempre escribe
```

### Fragment shader de profundidad (Three.js)

```glsl
void main() {
  // gl_FragCoord.z es la profundidad en espacio ventana [0, 1]
  gl_FragColor = vec4(vec3(gl_FragCoord.z), 1.0);
}
```

### Toggle de depthTest (Three.js)

```jsx
const shaderMat = new THREE.ShaderMaterial({
  vertexShader, fragmentShader,
  depthTest: depthTest,  // false → artefactos del pintor
})
```

---

## Prompts utilizados

Se utilizó Claude Code (Sonnet 4.6) como asistente de scaffolding y escritura inicial del código. Toda la lógica matemática del Z-buffer (interpolación baricéntrica, proyección perspectiva, comparación de profundidad) fue revisada y validada manualmente.

---

## Aprendizajes y dificultades

- El **algoritmo del pintor** falla silenciosamente cuando dos triángulos se intersecan en profundidad — el Z-buffer resuelve esto de forma perfecta a nivel de píxel.
- La precisión del Z-buffer depende críticamente del **ratio far/near**: un ratio de 10⁶ comprime casi todos los valores de profundidad en los últimos dígitos significativos de un float32.
- El **Z-fighting** se manifiesta incluso con diferencias de Δz ≈ 0.001 a Z = 3.0 unidades, lo que confirma la pérdida de precisión lejos de la cámara.
- En Three.js, `gl_FragCoord.z` ya viene en espacio ventana [0, 1], lo que hace trivial la visualización del depth buffer.

---

## Estructura del proyecto

```
semana_3_2_zbuffer_depth_testing/
├── python/
│   └── zbuffer_depth_testing.ipynb
├── threejs/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── eslint.config.js
│   └── src/
│       └── main.jsx
├── media/
│   ├── painter_no_zbuffer.png
│   ├── zbuffer_correct.png
│   ├── depth_buffer_grayscale.png
│   ├── comparacion_zbuffer.png
│   ├── zbuffer_precision_nearfar.png
│   ├── zfighting_demo.png
│   └── zbuffer_rotation.gif
└── README.md
```
