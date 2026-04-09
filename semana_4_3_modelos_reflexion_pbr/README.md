# Taller Modelos Reflexion PBR

**Estudiante:** Gabriel Andrés Anzola Tachak  
**Fecha:** 2026-04-08

---

## Descripción

Implementación y comparación visual de cinco modelos de reflexión de luz sobre esferas idénticas, usando React Three Fiber + Vite. Todos los objetos comparten la misma geometría y condiciones de iluminación para que las diferencias sean atribuibles exclusivamente al modelo de material.

---

## Implementaciones

### Three.js — React Three Fiber

| Esfera | Material | Parámetros clave |
|--------|----------|-----------------|
| Lambert | `MeshLambertMaterial` | Solo difuso: `I = Kd · max(N·L, 0)` |
| Phong | `MeshPhongMaterial` | Especular Phong: `I += Ks · max(R·V, 0)^n`, shininess=60 |
| Blinn-Phong | `MeshPhongMaterial` | Half-vector: `I += Ks · max(N·H, 0)^n`, shininess=120 |
| PBR Dieléctrico | `MeshStandardMaterial` | metalness=0, roughness=0.8 |
| PBR Metálico | `MeshStandardMaterial` | metalness=1, roughness=0.1 |

**Iluminación de la escena:**
- `<ambientLight intensity={0.25}>` — relleno base
- `<directionalLight intensity={3} position={[8,10,8]}>` — luz clave
- `<directionalLight intensity={0.8} color="#6080ff">` — luz de borde/contraluz

---

## Resultados Visuales

> Ejecutar `npm run dev` y abrir `http://localhost:5173` para ver la escena interactiva.  
> Usar OrbitControls para rotar la cámara y apreciar los reflejos especulares desde distintos ángulos.

*(Capturas a añadir en `media/` después de ejecución local)*

---

## Código Relevante

### Lambert — solo componente difuso
```jsx
<meshLambertMaterial color="#e74c3c" />
// Three.js calcula internamente: I = Kd · max(N·L, 0)
```

### Phong — difuso + especular (R·V)
```jsx
<meshPhongMaterial color="#e74c3c" specular="#ffffff" shininess={60} />
// I_spec = Ks · max(R·V, 0)^shininess
```

### Blinn-Phong — half-vector H = normalize(L+V)
```jsx
<meshPhongMaterial color="#e74c3c" specular="#ffffff" shininess={120} />
// I_spec = Ks · max(N·H, 0)^shininess
// Three.js MeshPhongMaterial usa Blinn-Phong internamente
```

### PBR — dieléctrico y metálico
```jsx
// Dieléctrico (plástico): F0 ≈ 0.04, lóbulo especular ancho
<meshStandardMaterial color="#e74c3c" metalness={0} roughness={0.8} />

// Metálico: tinted reflections, lóbulo especular estrecho
<meshStandardMaterial color="#e74c3c" metalness={1} roughness={0.1} />
```

---

## Prompts Utilizados (IA Generativa)

- "Crea un componente React Three Fiber que muestre 5 esferas con diferentes modelos de reflexión: Lambert, Phong, Blinn-Phong, PBR dieléctrico y PBR metálico, con etiquetas HTML usando @react-three/drei"
- "Configura iluminación con directionalLight + ambientLight para resaltar diferencias entre modelos especulares"

---

## Aprendizajes y Dificultades

- **Lambert vs. Phong:** Lambert produce transiciones suaves sin punto de brillo; Phong añade el lóbulo especular que crea el destello blanco visible en plásticos.
- **Phong vs. Blinn-Phong:** Blinn-Phong usa el half-vector `H = normalize(L+V)` en lugar del vector de reflexión `R`, lo que resulta en un lóbulo especular más suave y físicamente más estable. Three.js implementa Blinn-Phong dentro de `MeshPhongMaterial`.
- **PBR:** `MeshStandardMaterial` implementa un flujo de trabajo de metalness/roughness basado en microfacetas (GGX BRDF). metalness=1 hace que el color de la esfera tiña los reflejos; roughness controla el ancho del lóbulo especular.
- **Dificultad:** Sin una luz de entorno (environment map), las esferas PBR metálicas se ven oscuras. Se compensó con una luz de borde azulada para mostrar la diferencia de reflexión.

---

## Estructura del Proyecto

```
semana_4_3_modelos_reflexion_pbr/
├── threejs/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   └── components/
│   │       └── ReflectionScene.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── .gitignore
├── media/
└── README.md
```

---

## Referencias

- Three.js Docs: [MeshLambertMaterial](https://threejs.org/docs/#api/en/materials/MeshLambertMaterial), [MeshPhongMaterial](https://threejs.org/docs/#api/en/materials/MeshPhongMaterial), [MeshStandardMaterial](https://threejs.org/docs/#api/en/materials/MeshStandardMaterial)
- Phong, B.T. (1975). Illumination for computer generated pictures. *CACM 18*(6).
- Blinn, J.F. (1977). Models of light reflection for computer synthesized pictures. *SIGGRAPH '77*.

---

## Checklist

- [x] Esfera con `MeshLambertMaterial` (difuso puro)
- [x] Esfera con `MeshPhongMaterial` shininess=60 (Phong especular)
- [x] Esfera con `MeshPhongMaterial` shininess=120 (Blinn-Phong)
- [x] Esfera con `MeshStandardMaterial` metalness=0, roughness=0.8 (PBR dieléctrico)
- [x] Esfera con `MeshStandardMaterial` metalness=1, roughness=0.1 (PBR metálico)
- [x] Luz direccional + luz ambiente
- [x] OrbitControls para navegación
- [x] Etiquetas con fórmula por esfera (Html de @react-three/drei)
- [x] Build sin errores
