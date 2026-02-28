# Simulación de Cámara Pinhole: Calibración y Distorsión

Entregado: 27 Feb 2026

## Objetivo

El objetivo de este ejercicio es implementar y visualizar los principios de una cámara pinhole (cámara oscura) utilizando Three.js. Esto incluye la proyección de coordenadas 3D a 2D de pantalla, la visualización del frustum de la cámara y la simulación interactiva de la distorsión radial de lente (efectos de barril y acerico).

## Implementaciones

### Three.js (React Three Fiber)

Se creó una escena 3D con un cubo, una esfera, una malla de piso (GridHelper) y ejes (AxesHelper) para tener puntos de referencia conocidos.

La herramienta cuenta con un panel de control interactivo (Leva) que permite:
* Cambiar entre **Modo Pinhole** (vista de la cámara en estudio) y **Modo Observador** (vista externa).
* Ajustar el **FOV (Field of View)**, los planos de recorte y la posición de la cámara.
* Modificar los coeficientes de **Distorsión Radial (k1, k2)**.

#### Proyección 3D a 2D

Para simular la proyección de la cámara, se implementó una función que mapea las posiciones globales de los objetos a píxeles de pantalla:

```javascript
const project3DTo2D = (position, camera, width, height) => {
  const vec = position.clone()
  // Proyecta el vector al espacio NDC [-1, 1]
  vec.project(camera)
  
  // Convierte coordenadas normalizadas a píxeles (X, Y)
  const x = ((vec.x + 1) / 2) * width
  const y = (-(vec.y - 1) / 2) * height
  
  return { x, y, z: vec.z }
}
```

Esta lógica permite superponer etiquetas HTML (`Html` de `@react-three/drei`) que muestran dinámicamente las coordenadas proyectadas.

#### Distorsión de Lente Radial

Se implementó un shader de post-procesado que aplica el modelo de distorsión polinomial: $p' = p(1 + k_1 r^2 + k_2 r^4)$.

```glsl
// Fragmento del shader de distorsión
float r2 = dot(p, p);
float f = 1.0 + k1 * r2 + k2 * r2 * r2;
vec2 pDistorted = p * f;
```

#### Escena en ejecución

En el 'Modo Observador' se puede apreciar el Frustum (volumen de visión) de la cámara pinhole:

![Frustum y Escena](./media/frustum_view.png)

En el 'Modo Pinhole', se observan las etiquetas de coordenadas y el efecto de distorsión al ajustar los parámetros:

![Distorsión y Proyección](./media/distortion_view.png)

![Distorsión y Proyección](./media/distortion_view2.png)

![Distorsión y Proyección](./media/distortion_view3.png)

![Distorsión y Proyección gif](./media/distortion_view_vid.gif)

## Aprendizajes y dificultades

* **Pipeline de Proyección**: Entender cómo `camera.project()` transforma coordenadas del mundo mediante la matriz de vista y proyección es fundamental para la visión artificial.
* **Distorsión Óptica**: La distorsión radial no es una transformación de geometría, sino un efecto de muestreo en la imagen final, por lo que el post-procesado (shaders) es la técnica adecuada para simularlo.
* **Coordinación de Cámaras**: Mantener una cámara observadora independiente ayuda enormemente a depurar la posición y el volumen de visión de la cámara principal.
