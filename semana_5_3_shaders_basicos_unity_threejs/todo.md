# Taller: Shaders Básicos - Primeros Efectos Visuales desde Código GLSL

## Arquitectura General

**Creación e implementación de shaders personalizados con Three.js:**
- 3 shaders GLSL distintos (gradiente, ondas, fresnel)
- Modificación de uniforms en tiempo real con controles
- Comparación visual de diferentes técnicas de shader
- Estructura vertex/fragment shader claramente documentada

---

## Estructura del Proyecto

```
semana_5_3_shaders_basicos_unity_threejs/
├── threejs/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Scene.tsx                    # Escena principal con 3 shaders
│   │   │   ├── GradientShader.tsx           # Shader de gradiente vertical
│   │   │   ├── WaveShader.tsx               # Shader de ondas animadas
│   │   │   ├── FresnelShader.tsx            # Shader de fresnel (bordes brillantes)
│   │   │   └── Controls.tsx                 # Panel Leva para uniformes
│   │   ├── shaders/
│   │   │   ├── gradient/
│   │   │   │   ├── vertex.glsl
│   │   │   │   └── fragment.glsl
│   │   │   ├── waves/
│   │   │   │   ├── vertex.glsl
│   │   │   │   └── fragment.glsl
│   │   │   └── fresnel/
│   │   │       ├── vertex.glsl
│   │   │       └── fragment.glsl
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── vite.config.ts
├── media/
│   ├── gradient_shader_demo.gif              # Gradiente vertical estático
│   ├── waves_shader_animation.gif            # Ondas animadas
│   ├── fresnel_shader_rotation.gif           # Fresnel rotando
│   └── all_shaders_overview.png              # Vista de los 3 shaders
└── README.md
```

---

## Tareas Principales

### 1. Setup inicial (Vite + React Three Fiber)

```bash
npm create vite@latest threejs -- --template react-ts
cd threejs
npm install three @react-three/fiber @react-three/drei leva
```

**Nota:** Vite carga automáticamente archivos `.glsl` si se configura correctamente. Alternativa: importar shaders como strings en los componentes.

---

### 2. Configuración de Vite para cargar .glsl

**En `vite.config.ts`:**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  assetsInclude: ['**/*.glsl'],
})
```

**Importar en componentes:**
```typescript
import vertexShader from '../shaders/gradient/vertex.glsl?raw'
import fragmentShader from '../shaders/gradient/fragment.glsl?raw'
```

---

### 3. Componente Scene.tsx

**Estructura:**
- Canvas de Three.js con tres áreas (gradiente, ondas, fresnel)
- Luz ambiental (0.7) + luz direccional (1.0, ángulo 45°)
- Cámara: posición (0, 0, 8), mirando al centro
- Fondo gris claro (0x333333)
- OrbitControls para interacción

**3 esferas:**
- Lado izquierdo (-3, 0, 0): GradientShader
- Centro (0, 0, 0): WaveShader
- Lado derecho (3, 0, 0): FresnelShader

---

### 4. Shader 1: Gradiente Vertical (GradientShader.tsx)

**Vertex Shader (`shaders/gradient/vertex.glsl`):**
```glsl
varying vec2 vUv;

void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
```

**Fragment Shader (`shaders/gradient/fragment.glsl`):**
```glsl
varying vec2 vUv;
uniform vec3 colorTop;
uniform vec3 colorBottom;

void main() {
    vec3 color = mix(colorBottom, colorTop, vUv.y);
    gl_FragColor = vec4(color, 1.0);
}
```

**Componente GradientShader.tsx:**
- Uniforms controlables:
  - `colorTop`: vec3 (default: azul claro, 0.2, 0.5, 1.0)
  - `colorBottom`: vec3 (default: rojo, 1.0, 0.3, 0.2)
- Material: THREE.ShaderMaterial con vertex + fragment
- Geometría: sphereGeometry (32 divisiones)
- No requiere animación

**Efecto visual:**
- Gradiente suave de rojo abajo a azul arriba
- Cambiar colores con sliders Leva

---

### 5. Shader 2: Ondas Animadas (WaveShader.tsx)

**Vertex Shader (`shaders/waves/vertex.glsl`):**
```glsl
uniform float uTime;
varying vec3 vPosition;

void main() {
    vPosition = position;
    vec3 pos = position;
    pos.z += sin(pos.x * 3.0 + uTime) * 0.2;
    pos.z += sin(pos.y * 2.0 + uTime * 0.7) * 0.15;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

**Fragment Shader (`shaders/waves/fragment.glsl`):**
```glsl
uniform float uTime;
varying vec3 vPosition;
uniform float uWaveFrequency;
uniform vec3 uColorA;
uniform vec3 uColorB;

void main() {
    float wave = sin(vPosition.x * uWaveFrequency + uTime) * 0.5 + 0.5;
    vec3 color = mix(uColorA, uColorB, wave);
    gl_FragColor = vec4(color, 1.0);
}
```

**Componente WaveShader.tsx:**
- Uniforms controlables:
  - `uTime`: actualizado por `useFrame()`
  - `uWaveFrequency`: controlar densidad de ondas (default: 5.0)
  - `uColorA`: color 1 (default: cian, 0.2, 1.0, 1.0)
  - `uColorB`: color 2 (default: magenta, 1.0, 0.2, 1.0)
- Material: THREE.ShaderMaterial
- Geometría: sphereGeometry (32 divisiones)
- **Animación:** `useFrame()` incrementa `uTime`
  ```typescript
  useFrame(() => {
    materialRef.current.uniforms.uTime.value += 0.01
  })
  ```

**Efecto visual:**
- Superficie ondulante con colores que transicionan
- Colores cambian basados en amplitud de onda
- Ver deformación en tiempo real

---

### 6. Shader 3: Fresnel (FresnelShader.tsx)

**Vertex Shader (`shaders/fresnel/vertex.glsl`):**
```glsl
varying vec3 vNormal;
varying vec3 vPosition;

void main() {
    vNormal = normalize(normalMatrix * normal);
    vPosition = (modelViewMatrix * vec4(position, 1.0)).xyz;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
```

**Fragment Shader (`shaders/fresnel/fragment.glsl`):**
```glsl
varying vec3 vNormal;
varying vec3 vPosition;
uniform float uFresnelPower;
uniform vec3 uBaseColor;
uniform vec3 uGlowColor;

void main() {
    vec3 viewDirection = normalize(-vPosition);
    float fresnel = pow(1.0 - dot(viewDirection, vNormal), uFresnelPower);

    vec3 finalColor = mix(uBaseColor, uGlowColor, fresnel);
    gl_FragColor = vec4(finalColor, 1.0);
}
```

**Componente FresnelShader.tsx:**
- Uniforms controlables:
  - `uFresnelPower`: potencia del efecto fresnel (default: 3.0, rango: 1-5)
  - `uBaseColor`: color base (default: azul oscuro, 0.1, 0.2, 0.4)
  - `uGlowColor`: color en bordes (default: cyan brillante, 0.3, 0.8, 1.0)
- Material: THREE.ShaderMaterial
- Geometría: sphereGeometry (32 divisiones)
- **Animación:** rotar esfera para ver efecto fresnel cambiar
  ```typescript
  useFrame((state) => {
    meshRef.current.rotation.y += 0.01
  })
  ```

**Efecto visual:**
- Bordes brillantes tipo holográfico
- Efecto más intenso en ángulos rasantes
- Centro oscuro, bordes brillantes

---

### 7. Componente Controls.tsx

**Panel Leva con carpetas:**

**Gradient Shader:**
- `colorTop` (color picker): azul claro
- `colorBottom` (color picker): rojo

**Wave Shader:**
- `waveFrequency` slider (0.5 - 20, step 0.5): densidad de ondas
- `colorA` (color picker): cian
- `colorB` (color picker): magenta
- `animationSpeed` slider (0.01 - 0.1, step 0.01): velocidad de ondas

**Fresnel Shader:**
- `fresnelPower` slider (0.5 - 5, step 0.1): intensidad del efecto
- `baseColor` (color picker): azul oscuro
- `glowColor` (color picker): cyan

**Global:**
- Botón "Reset All": restaurar valores por defecto

---

## Generación de Media (GIFs y Screenshots)

**4 archivos requeridos:**
1. **gradient_shader_demo.gif**: Esfera gradiente estática mostrando transición (2-3 segundos)
   - Sin animación, solo captura del resultado
2. **waves_shader_animation.gif**: Esfera con ondas animadas (4-5 segundos)
   - Ver deformación y cambios de color
3. **fresnel_shader_rotation.gif**: Esfera fresnel rotando (4-5 segundos)
   - Ver cómo el efecto cambio según ángulo
4. **all_shaders_overview.png**: Screenshot PNG estático
   - Las 3 esferas side-by-side para comparación

**Usar script existente:** `../capture_gifs.mjs` (adaptado)

**Requisitos previos:**
- `node` >= 16
- `ffmpeg` en PATH
- `playwright` instalado: `npm install -D playwright`
- Dev server Vite corriendo: `npm run dev` (http://localhost:5173)

**Proceso de captura:**
1. Copiar `capture_gifs.mjs` a raíz del proyecto Three.js
2. Configurar array `RECORDINGS` con 4 capturas:
   - `gradient_shader_demo`: duración 2500ms, 12fps
   - `waves_shader_animation`: duración 4500ms, 12fps
   - `fresnel_shader_rotation`: duración 4500ms, 10fps
   - `all_shaders_overview`: duración 2000ms, 10fps
3. Ejecutar: `node capture_gifs.mjs`
4. GIFs se guardan automáticamente en `media/`

---

## README.md - Secciones Obligatorias

1. **Título**: Taller - Shaders Básicos: Primeros Efectos Visuales desde Código GLSL
2. **Estudiante**: [Tu nombre]
3. **Fecha**: YYYY-MM-DD
4. **Descripción breve** (2-3 párrafos):
   - Qué son shaders y por qué son fundamentales en gráficos 3D
   - Diferencia entre vertex shader y fragment shader
   - Tres implementaciones: gradiente, ondas, fresnel
5. **Implementaciones**:
   - Subsección Gradiente: UV mapping, mix/blend de colores
   - Subsección Ondas: función sin(), modificación de vértices, animación con uniforms
   - Subsección Fresnel: normal vectors, dot product, efecto realista de reflexión
6. **Resultados visuales**: 4 GIFs/screenshots + descripción (1-2 líneas) de cada
7. **Código relevante**: 
   - Snippet: estructura básica vertex shader
   - Snippet: estructura básica fragment shader
   - Snippet: cómo pasar uniforms desde React a shaders
   - Snippet: cómo actualizar uniforms en loop de animación
8. **Prompts de IA** (si aplica): listar cualquier prompt usado
9. **Aprendizajes**:
   - Diferencia entre vertex y fragment shaders
   - Cómo uniforms permiten controlar shaders sin recompilar
   - Cómo técnicas como fresnel crean efectos realistas
   - Importancia del mapping (UV, normal vectors)
10. **Dificultades** (si aplica): cómo se resolvieron

---

## Checklist de Entrega

- [ ] Carpeta `semana_5_3_shaders_basicos_unity_threejs/` existe
- [ ] `threejs/` con estructura completa (src/, shaders/, package.json)
- [ ] Carpeta `shaders/` con 3 subcarpetas (gradient, waves, fresnel)
- [ ] Cada shader tiene vertex.glsl y fragment.glsl
- [ ] 3 componentes funcionales (GradientShader, WaveShader, FresnelShader)
- [ ] Componente Controls.tsx con todos los sliders
- [ ] 4 GIFs en `media/` con nombres descriptivos
- [ ] Gradiente muestra transición clara de color
- [ ] Ondas se deforman y colorean dinámicamente
- [ ] Fresnel brilla en bordes cuando rota
- [ ] README.md con todas las 10 secciones completadas
- [ ] Commits descriptivos en inglés:
  - `feat: setup three.js project with shader support`
  - `feat: implement gradient shader with color mixing`
  - `feat: implement wave shader with vertex displacement`
  - `feat: implement fresnel shader with holographic effect`
  - `feat: add leva controls for shader uniforms`
  - `feat: generate media assets and documentation`
- [ ] Repositorio público y README visible

---

## Notas Técnicas

### Estructura de un Shader
- **Vertex Shader**: ejecuta por cada vértice, modifica posición o pasa datos
- **Fragment Shader**: ejecuta por cada píxel, determina color final
- **Uniforms**: variables globales que no cambian dentro de un shader call
- **Varying**: variables interpoladas entre vertex y fragment shader

### Variables Built-in en GLSL
- `position`: posición del vértice en espacio local
- `normal`: normal del vértice
- `uv`: coordenadas de textura (0-1)
- `gl_Position`: posición final del vértice (DEBE ser asignada en vertex shader)
- `gl_FragColor`: color final (asignado en fragment shader)
- `projectionMatrix`, `modelViewMatrix`: matrices de transformación
- `normalMatrix`: matriz para transformar normales correctamente

### Por qué Three.js en lugar de Unity
- **GLSL más directo**: escribir shaders sin intermediarios
- **Control total**: acceso completo a vertex/fragment sin limitaciones
- **Prototipado rápido**: cambiar shaders en hot-reload con Vite
- **Menos overhead**: no necesitas compilar shaders en tiempo de construcción

### Validación Visual
El éxito está en **ver claramente** cada shader funcionando:
- Gradiente debe mostrar transición suave entre dos colores
- Ondas deben deformar la geometría visiblemente
- Fresnel debe brillar en bordes especialmente en ángulos rasantes
- Todos deben ser diferenciables visualmente cuando están lado a lado

### Recursos GLSL
- Tipos: `vec2`, `vec3`, `vec4`, `mat4`, `sampler2D`
- Funciones útiles: `sin`, `cos`, `mix`, `step`, `smoothstep`, `dot`, `cross`
- Operadores: pueden aplicarse por componente (vectorizado)
