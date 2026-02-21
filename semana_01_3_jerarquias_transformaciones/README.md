# Taller - Jerarquías y Transformaciones: El Árbol del Movimiento

## Nombre del estudiante

Gabriel Andres Anzola Tachak

## Fecha de entrega

2026-02-27

---

## Descripción breve

Implementación del taller de jerarquías y transformaciones donde se desarrolló una escena 3D interactiva que simula el movimiento relativo entre objetos unidos por jerarquía (padre, hijo, nieto). El proyecto se desarrolló en React Three Fiber (Three.js), permitiendo manipular las transformaciones (posición, rotación, escala) del nodo principal y visualizar cómo el sistema de matrices hereda y transmite dichas transformaciones a sus subnodos.

---

## Implementaciones

### Three.js / React Three Fiber ✅

Se desarrolló una aplicación interactiva que permite manipular el árbol de movimiento compuesto por 3 niveles jerárquicos:

1. **Nivel 1 (Padre):** Un cubo con controles directos sobre su posición global, rotación geométrica (ejes X, Y, Z) y escala general.
2. **Nivel 2 (Hijo):** Una esfera distanciada del padre que órbita a su alrededor arrastrada por los movimientos del cubo. Posee sus propios controles de rotación y escala locales independientes de las matrices parentales.
3. **Nivel 3 (Nieto):** Un toroide que órbita a la esfera, reflejando el cúmulo de transformaciones propagadas desde el origen (Padre) y su nodo intermedio (Hijo).

Se incluyó también configuración dinámica de visualización para activar la rotación local continua o habilitar un control manual mediante sliders UI proveídos por la librería `leva`.

---

## Resultados visuales

### Interacción de Jerarquías y Transformaciones en Three.js

![Demostración Three.js](./media/screenshots/threejs.gif)

La grabación de pantalla muestra la aplicación WebGL en funcionamiento, demostrando cómo la manipulación de la rotación y posición del `Padre` arrastra a la `Hijo` (esfera) y al `Nieto` (toroide) coherentemente a través del espacio 3D, gracias a la herencia de transformaciones en el Scene Graph de Three.js.

### Capturas del Modo de Visualización y Controles UI

![Captura Three.js 1](./media/threejs/captura_1.png)

Muestra de la interfaz gráfica implementada sobre el canvas, desplegando los paneles de configuración y parámetros transformativos.

![Captura Three.js 2](./media/threejs/captura_2.png)

Visualización de los ejes locales (helper axes) de cada subnodo activados, clarificando la superposición de los diferentes sistemas de coordenadas.

---

## Código relevante

### Definición de la estructura Padre, Hijo, Nieto:

```jsx
<group 
  position={[positionX, positionY, positionZ]} 
  rotation={[rotX, rotY, rotZ]}
  scale={[scale, scale, scale]}
>
  {/* PARENT NODE */}
  <mesh><boxGeometry args={[1.5, 1.5, 1.5]} /></mesh>

  {/* CHILD NODE */}
  <group position={[3, 0, 0]} scale={[childScale, childScale, childScale]}>
    <group ref={childRef}>
      <mesh><sphereGeometry args={[0.6, 32, 32]} /></mesh>

      {/* GRANDCHILD NODE */}
      <group position={[0, 2, 0]}>
        <group ref={grandchildRef}>
          <mesh><torusGeometry args={[0.3, 0.08, 16, 32]} /></mesh>
        </group>
      </group>
    </group>
  </group>
</group>
```

### Animación y Transformación local:

```jsx
useFrame((state, delta) => {
  if (animateChild) {
    if (childRef.current) childRef.current.rotation.y += delta * 0.5;
    if (grandchildRef.current) grandchildRef.current.rotation.x += delta;
  } else {
    if (childRef.current) childRef.current.rotation.y = childRotY;
    if (grandchildRef.current) grandchildRef.current.rotation.x = grandchildRotX;
  }
});
```

---

## Prompts utilizados

```
"Crea una aplicación interactiva usando React Three Fiber donde exista un grupo padre que contenga una caja, un grupo hijo con una esfera y un grupo nieto con un toroide. El hijo debe estar desplazado respecto al padre y el nieto respecto al hijo. Provee controles con `leva` para modificar la matriz de transformación del nodo principal."

"¿Cómo generar ejes locales `axesHelper` para cada nodo individual de manera que giren visiblemente junto con la geometría 3D en React Three Fiber?"
```

---

## Aprendizajes y dificultades

### Aprendizajes

Reforcé mi comprensión sobre Grafos de Escena, sistemas de coordenadas, y cómo las transformaciones se propagan a través de la cadena de descendientes. Además, mejoré en la configuración de interfaces con `leva`.

### Dificultades

Inicialmente, hubo conflictos visuales entre la rotación asignada estáticamente y la manejada por `useFrame`. Fue necesario usar Refs y ejecutar la actualización condicionalmente. 


---

## Estructura del proyecto

```
semana_01_3_jerarquias_transformaciones/
├── threejs/                         # Aplicación Web React + Three.js
│   ├── src/
│   │   ├── App.jsx                 # Componente principal interactivo
│   │   ├── HierarchyScene.jsx      # Definición del scene graph y transformaciones
│   │   ├── main.jsx                # Entry point
│   │   └── index.css               # Estilos SCSS-like
│   ├── vite.config.js              # Configuración de build
│   ├── package.json                # Dependencias (three, r3f, leva)
│   └── README.md                   # Documentación específica del entorno
├── unity/                           # (Por implementar posteriormente)
├── media/
│   ├── screenshots/                 # Grabaciones en formato webp y gif
│   │   └── threejs.gif             # <- [Añadir grabación de pantalla]
│   ├── threejs/                     # Capturas estáticas
│   │   ├── captura_1.png           # <- [Añadir capturas estáticas]
│   │   ├── captura_2.png
│   │   └── README.md
│   └── README.md
└── README.md                        # Documento integrador principal
```

---

## Checklist de entrega

- [X] Carpeta con nombre `semana_01_3_jerarquias_transformaciones`
- [X] Código limpio y funcional en la carpeta `threejs/`
- [ ] GIFs/imágenes incluidos con nombres descriptivos en carpeta subcarpetas de `media/`
- [X] README completo con todas las secciones requeridas
- [X] Mínimo 2 capturas/GIFs referenciadas en la documentación
- [ ] Unity Toolkit implementation
- [X] Repositorio organizado
