# 📊 Resultados - Conversión de Formatos 3D

Archivos multimedia y resultados generados por el análisis en Python y la aplicación Three.js durante el taller de la Semana 01.2.

---

## 📸 Visualizaciones Estáticas

### format_comparison.png

![Comparación de Formatos en Matplotlib](./python/format_comparison.png)

**Descripción**: Visualización comparativa de las mismas geometrías cargadas desde tres formatos diferentes.
- **Left (OBJ)**: Muestra el render del formato estándar Wavefront.
- **Center (STL)**: Render de la geometría triangulada.
- **Right (GLTF)**: Renderizado desde el formato Khronos GL Transmission Format.

**Especificaciones**:
- Formato: PNG
- Renderizado: Gráfica generada desde Matplotlib para comparar consistencias.

**Utilidad**: Verificar que la estructura fundamental del modelo 3D permanece inalterada tras la conversión de un formato a otro.



## 🎬 Animaciones y Capturas de Pantalla

### python.gif

![Demostración Python](./screenshots/python.gif)

**Descripción**: Grabación animada que demuestra la ejecución del procesamiento en el entorno de Python usando la librería `trimesh`. El flujo valida la geometría (comprobando atributos como estanqueidad, centroide e inercia) y maneja la escritura de los archivos exportados `.obj`, `.stl`, y `.gltf`.

**Utilidad**: Visualizar de primera mano el log y las métricas computadas de las mallas que reporta la consola de salida usando Trimesh.

---

### threejs.gif

![Demostración Three.js](./screenshots/threejs.gif)

**Descripción**: Animación interactiva de la aplicación en React y Three.js. Visualiza al modelo 3D GLTF renderizado en tiempo real dentro del Canvas, respondiendo a los eventos del ratón (paneo, zoom y rotación a través de OrbitControls).

**Utilidad**: Ver la integración viva en Frontend de los assets, validando la solidez de GLTF para rotaciones 360 y respuestas UI dentro de componentes de React.

---

## 📊 Impacto y Metadatos en Conversión

El proceso documenta importantes diferencias y propiedades al pasar entre los formatos tridimensionales:

| Característica            | Observación |
| ------------------------- | ---------------------- |
| **Vértices / Caras**      | Conservan congruencia espacial garantizando identidad visual en el render de Matplotlib. |
| **Volumen / Watertight**  | STL prioriza propiedades como volumen cerrado (watertight) listos para software CAD/Impresión 3D. |
| **Estructura y Carga**    | GLTF carga más de un 30% más rápido en aplicaciones Web que OBJ dada la optimización vía Buffers y JSON. |
| **Tamaño Físico**         | Exportaciones a GLTF reducen sustancialmente la huella en disco frente a archivos de texto puro como OBJ. |

---

## 🔗 Referencias Útiles

- [Documentación Principal del Proyecto](../README.md)
- [Implementación de Conversión en Python](../python/)
- [Implementación Cliente de Renderizado Three.js](../threejs/)
