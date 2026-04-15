# Taller: Modelado Procedural Básico - Geometría desde Código

## Arquitectura General

**Generación de geometría procedural con React Three Fiber:**
- Estructuras geométricas básicas generadas por algoritmos (grillas, espirales, fractales)
- Modificación dinámica de vértices
- Transformaciones animadas en tiempo real
- Comparación visual entre geometría estática vs dinámica

---

## Estructura del Proyecto

```
semana_5_2_modelado_procedural_basico/
├── threejs/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Scene.tsx              # Escena principal con 3 generadores
│   │   │   ├── GridGenerator.tsx      # Grilla de cubos procedurales
│   │   │   ├── SpiralGenerator.tsx    # Espiral de cilindros
│   │   │   ├── FractalTree.tsx        # Árbol fractal recursivo
│   │   │   └── Controls.tsx           # Panel Leva para parámetros
│   │   ├── utils/
│   │   │   └── geometryHelpers.ts     # Funciones auxiliares (vertices, indices)
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── vite.config.ts
├── media/
│   ├── grid_rotation.gif               # Grilla rotando
│   ├── spiral_animation.gif            # Espiral expandiéndose/contrayéndose
│   ├── fractal_tree_growth.gif         # Árbol fractal creciendo
│   └── all_generators_overview.png     # Vista estática con las 3 implementaciones
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

---

### 2. Componente Scene.tsx

**Estructura:**
- Canvas de Three.js con tres áreas (grilla, espiral, árbol)
- Luz ambiental + luz direccional (ángulo 45°)
- Cámara posicionada para ver los 3 generadores simultáneamente
- Fondo gris neutral

**Cámara:**
- Posición: (0, 5, 12)
- Mirando al centro (0, 2, 0)
- OrbitControls para interacción

**Iluminación:**
- Ambiental: intensidad 0.6
- Direccional: intensidad 1.0, color blanco

---

### 3. Componente GridGenerator.tsx

**Propósito:** Generar una grilla de cubos transformados proceduralmente

**Parámetros (controlables con Leva):**
- `gridSize`: número de cubos por lado (ej: 5 = 5x5 = 25 cubos)
- `spacing`: distancia entre cubos (ej: 1.5)
- `scale`: tamaño de cada cubo (ej: 0.8)
- `rotationSpeed`: velocidad de rotación animada (ej: 0.01)

**Implementación:**
1. Usar `useFrame()` para animar rotación
2. Generar array de posiciones con doble `for` loop:
   ```
   for (let x = 0; x < gridSize; x++) {
     for (let z = 0; z < gridSize; z++) {
       position = [x * spacing - (gridSize/2 * spacing), 
                   0, 
                   z * spacing - (gridSize/2 * spacing)]
     }
   }
   ```
3. Mapear array a `<mesh>` con `boxGeometry` y material diferenciado por posición
4. Aplicar transformaciones en tiempo real

**Visual:**
- Material básico con color diferenciado por altura o posición
- Todos los cubos rotan alrededor del eje Y

---

### 4. Componente SpiralGenerator.tsx

**Propósito:** Generar una espiral de cilindros con parámetros ajustables

**Parámetros (controlables con Leva):**
- `turns`: número de vueltas de la espiral (ej: 3)
- `segments`: cantidad de cilindros en total (ej: 30)
- `radius`: radio de la espiral (ej: 2.0)
- `height`: altura total (ej: 5.0)
- `scaleVariation`: variación de tamaño (ej: 0.5 a 1.5)
- `animationSpeed`: velocidad de expansión/contracción (ej: 0.01)

**Implementación:**
1. Usar parametrización de espiral:
   ```
   for (let i = 0; i < segments; i++) {
     const t = i / segments
     const angle = t * turns * Math.PI * 2
     const x = radius * Math.cos(angle)
     const z = radius * Math.sin(angle)
     const y = (t * height) - height/2
     positions.push([x, y, z])
   }
   ```
2. Escalar cada cilindro basado en `scaleVariation`
3. Animar con `useFrame()` para cambiar `radius` dinámicamente

**Visual:**
- Material con gradiente de color (inferior = rojo, superior = azul)
- Cilindros conectados visualmente formando espiral

---

### 5. Componente FractalTree.tsx

**Propósito:** Generar un árbol fractal usando recursión

**Parámetros (controlables con Leva):**
- `depth`: profundidad de la recursión (ej: 4)
- `angleSpread`: ángulo entre ramas (ej: 0.5 radianes)
- `lengthReduction`: reducción de largo por nivel (ej: 0.7)
- `branchingFactor`: número de ramas por nodo (ej: 2 o 3)
- `growthTime`: duración de animación de crecimiento (ms)

**Implementación:**
1. Función recursiva que genera ramas:
   ```
   function createBranch(position, direction, depth, length) {
     if (depth === 0) return
     const newPosition = [
       position[0] + direction[0] * length,
       position[1] + direction[1] * length,
       position[2] + direction[2] * length
     ]
     // Crear cilindro de position a newPosition
     // Para cada branchingFactor, llamar recursivamente con ángulo diferente
   }
   ```
2. Generar geometría de cilindros para cada rama
3. Animar `scale` de las ramas de 0 a 1 (efecto de crecimiento)
4. Usar `useFrame()` para controlador progresivo

**Visual:**
- Árbol que "crece" desde raíz hacia arriba/afuera
- Ramas se hacen más pequeñas en cada nivel
- Color gradual de marrón oscuro (base) a verde claro (punta)

---

### 6. Componente Controls.tsx

**Panel Leva con tabs/carpetas:**
- **Grid**: gridSize, spacing, scale, rotationSpeed
- **Spiral**: turns, segments, radius, height, scaleVariation, animationSpeed
- **Tree**: depth, angleSpread, lengthReduction, branchingFactor, growthTime

**Requisitos:**
- Sliders rangos apropiados para cada parámetro
- Botón "Reset" para restaurar valores por defecto
- Botón "Regenerate" para recalcular geometría

---

### 7. Utils: geometryHelpers.ts

**Funciones auxiliares:**
- `createGridPositions(gridSize, spacing)`: retorna array de posiciones
- `createSpiralPositions(turns, segments, radius, height)`: parametrización de espiral
- `createFractalBranches(depth, angle, length, factor)`: generador recursivo de ramas
- `randomColor()`: genera color RGB aleatorio
- `gradientColor(t: 0-1)`: retorna color en gradiente

---

## Generación de Media (GIFs y Screenshots)

**4 archivos requeridos:**
1. **grid_rotation.gif**: Grilla de cubos rotando continuamente (3-4 segundos)
   - Mostrar cómo se distribuyen proceduralmente
2. **spiral_animation.gif**: Espiral expandiéndose/contrayéndose (4-5 segundos)
   - Cambiar `radius` dinámicamente
3. **fractal_tree_growth.gif**: Árbol fractal creciendo desde el tronco (4-5 segundos)
   - Ver cómo las ramas se extienden recursivamente
4. **all_generators_overview.png**: Screenshot PNG estático
   - Vista de los 3 generadores simultáneamente en la escena

**Usar script existente:** `../capture_gifs.mjs` (adaptado)

**Requisitos previos:**
- `node` >= 16
- `ffmpeg` en PATH
- `playwright` instalado: `npm install -D playwright`
- Dev server Vite corriendo: `npm run dev` (escucha en http://localhost:5173)

**Proceso de captura:**
1. Copiar `capture_gifs.mjs` a raíz del proyecto Three.js
2. Configurar array `RECORDINGS` con 4 capturas:
   - `grid_rotation`: duración 3500ms, 12fps, sin interacción
   - `spiral_animation`: duración 4500ms, 10fps, sin interacción
   - `fractal_tree_growth`: duración 4000ms, 12fps, esperar a que crezca
   - `all_generators_overview`: duración 2000ms, 10fps, captura estática
3. Ejecutar: `node capture_gifs.mjs`
4. GIFs se guardan automáticamente en `media/`

---

## README.md - Secciones Obligatorias

1. **Título**: Taller - Modelado Procedural Básico: Geometría desde Código
2. **Estudiante**: [Tu nombre]
3. **Fecha**: YYYY-MM-DD
4. **Descripción breve** (2-3 párrafos):
   - Qué es modelado procedural y por qué es útil
   - Ventajas de generar geometría desde código
   - Tres implementaciones distintas (grilla, espiral, fractal)
5. **Implementaciones**:
   - Subsección Grilla: loops anidados, transformaciones, animación de rotación
   - Subsección Espiral: parametrización matemática, animación de expansión
   - Subsección Árbol Fractal: recursión, crecimiento animado, autosimilaridad
6. **Resultados visuales**: 4 GIFs/screenshots + descripción breve (1-2 líneas) de cada
7. **Código relevante**: 
   - Snippet: generación de posiciones en grilla
   - Snippet: parametrización de espiral
   - Snippet: función recursiva para fractales
8. **Prompts de IA** (si aplica): listar cualquier prompt usado
9. **Aprendizajes**:
   - Cómo loops y recursión generan geometría compleja
   - Ventajas del modelado procedural vs manual
   - Cómo parámetros afectan la geometría dinámicamente
   - Diferencia entre geometría estática y animada
10. **Dificultades** (si aplica): cómo se resolvieron

---

## Checklist de Entrega

- [ ] Carpeta `semana_5_2_modelado_procedural_basico/` existe
- [ ] `threejs/` con estructura completa (src/, package.json, vite.config.ts)
- [ ] 3 componentes generadores funcionales (Grid, Spiral, FractalTree)
- [ ] Componente Controls.tsx con Leva panels
- [ ] `geometryHelpers.ts` con funciones auxiliares
- [ ] 4 GIFs en `media/` con nombres descriptivos
- [ ] Grid rota visiblemente
- [ ] Spiral se expande/contrae dinámicamente
- [ ] Árbol fractal crece de forma observable
- [ ] README.md con todas las 10 secciones completadas
- [ ] Commits descriptivos en inglés:
  - `feat: setup three.js project with react and fiber`
  - `feat: implement grid generator with procedural positioning`
  - `feat: implement spiral generator with mathematical parametrization`
  - `feat: implement fractal tree with recursive branch generation`
  - `feat: add leva controls for all generators`
  - `feat: generate media assets with capture script`
  - `feat: complete documentation and readme`
- [ ] Repositorio público y README visible

---

## Notas Técnicas

### Ventajas del Modelado Procedural
- **Reutilizable**: cambiar un parámetro regenera toda la estructura
- **Escalable**: modificar gridSize genera grillas de cualquier tamaño
- **Eficiente**: crear 1000 cubos con loop vs importar mesh manual
- **Animable**: parámetros pueden cambiar en tiempo real

### Diferencia con Modelado Manual
- **Manual**: esculpir en Blender, exportar `.gltf`, cargar en código
- **Procedural**: definir reglas matemáticas, generar en tiempo de ejecución
- Este taller usa procedural porque permite explorar generación dinámica

### Estructura de Componentes
- Cada generador es independiente: puede quitarse/agregarse sin afectar otros
- `Controls` centraliza todos los sliders: cambios propagan a través de props
- `useFrame()` es clave para animaciones: se ejecuta 60 veces/segundo

### Validación Visual
El éxito está en **ver claramente** cada generador funcionando:
- Grilla debe mostrar matriz clara de cubos
- Espiral debe formar patrón helicoidal visible
- Árbol debe mostrar bifurcaciones recursivas
- Parámetros deben causar cambios visuales inmediatos
