# Taller - Construyendo el Mundo 3D: Python

## Implementación en Python

### Descripción

Se desarrolló un notebook Jupyter completo (`model_visualization.ipynb`) que permite la carga, análisis y visualización interactiva de modelos 3D en formatos OBJ, STL o GLTF. El proyecto demuestra cómo trabajar con mallas poligonales 3D, extrayendo información estructural (vértices, aristas, caras) y generando visualizaciones desde múltiples perspectivas.

### Herramientas utilizadas

- **trimesh**: Librería principal para procesamiento de mallas 3D
- **matplotlib**: Visualizaciones 3D estáticas
- **numpy**: Cálculos numéricos y manipulación de arrays
- **imageio**: Generación de animaciones GIF
- **vedo** (opcional): Visualización interactiva avanzada

### Funcionalidades implementadas

1. **Carga de modelos 3D**: Carga automática de archivos OBJ desde carpeta local
2. **Extracción de información estructural**:
   - Número de vértices: 25,979
   - Número de aristas: 71,871
   - Número de caras: 45,386
   - Propiedades topológicas y geométricas

3. **Cálculo de propiedades geométricas**:
   - Área superficial: 2.44 u²
   - Bounding box (caja delimitadora)
   - Centro de masa
   - Verificación de malla cerrada (watertight)

4. **Visualizaciones múltiples**: 6 vistas simultáneas mostrando:
   - Modelo renderizado normal
   - Vértices como puntos rojos
   - Aristas como líneas azules
   - Caras triangulares coloreadas
   - Vista wireframe (estructura triangular)
   - Tabla de estadísticas

5. **Componentes por separado**: Desglose visual de vértices, aristas y caras

6. **Animaciones GIF**: 3 animaciones de rotación 3D:
   - Modelo completo en rotación
   - Visualización de vértices con gradiente de colores
   - Visualización de caras coloreadas aleatoriamente

---

## 📋 Contenido del notebook

El notebook `model_visualization.ipynb` incluye las siguientes secciones:

1. **Instalación Automática de Dependencias** - Instala automáticamente todas las librerías necesarias
2. **Cargar Modelo 3D** - Carga del modelo `scene.obj` desde la carpeta local
3. **Información Estructural** - Extrae datos del modelo con estadísticas completas
4. **Visualización 3D** - Múltiples vistas con matplotlib y vedo
5. **Animación Rotatoria** - Genera GIF y video MP4 con rotación 3D

---

## 🛠️ Requisitos de Instalación

### Opción 1: Automático (Recomendado)

El notebook instala automáticamente todas las dependencias al ejecutar la primera celda:

1. Abre el notebook en Jupyter
2. Ejecuta la primera celda
3. ¡Listo! Todas las librerías se instalarán automáticamente

### Opción 2: Instalación Manual

```bash
pip install trimesh numpy matplotlib vedo imageio imageio-ffmpeg
```

### Opción 3: Google Colab

```python
!pip install trimesh vedo imageio imageio-ffmpeg
```

---

## 🚀 Cómo usar

### En Jupyter Local (Recomendado)

```bash
cd python/
jupyter notebook model_visualization.ipynb
```

Ejecuta todas las celdas en orden. La primera celda instalará automáticamente todas las dependencias.

### En VS Code con Jupyter Extension

1. Abre el archivo `model_visualization.ipynb`
2. Selecciona un kernel Python
3. Ejecuta todas las celdas con "Run All"

### En Google Colab

1. Sube el notebook y el archivo `scene.obj` a Google Colab
2. Ejecuta todas las celdas en orden
3. Las dependencias se instalarán en la primera celda

---

## 📁 Archivos generados

El notebook genera los siguientes archivos (guardados en `../media/python/`):

| Archivo | Descripción | Formato |
|---------|-------------|---------|
| `modelo_completo.png` | 6 vistas del modelo completo | PNG (150 DPI) |
| `vertices_edges_faces.png` | Desglose de vértices, aristas, caras | PNG (150 DPI) |
| `modelo_rotacion.gif` | Animación de rotación completa | GIF (36 frames, 3.6s) |
| `vertices_rotation.gif` | Animación de vértices | GIF (36 frames, 3.6s) |
| `faces_rotation.gif` | Animación de caras | GIF (36 frames, 3.6s) |

### Grabación de Pantalla (Ejecución)

![Ejecución del Notebook](../media/screenshots/python.gif)

---

## 💡 Código relevante

### Carga y análisis del modelo

```python
import trimesh
from pathlib import Path

# Cargar modelo 3D
mesh = trimesh.load('scene.obj')

# Extraer información estructural
vertices = mesh.vertices
faces = mesh.faces
num_vertices = len(vertices)
num_faces = len(faces)

# Calcular aristas
edges = set()
for face in faces:
    for i in range(len(face)):
        v1, v2 = face[i], face[(i + 1) % len(face)]
        edge = tuple(sorted([v1, v2]))
        edges.add(edge)
num_edges = len(edges)

print(f"Vértices: {num_vertices:,}")
print(f"Aristas: {num_edges:,}")
print(f"Caras: {num_faces:,}")
print(f"Volumen: {mesh.volume:.6f}")
print(f"Área superficial: {mesh.area:.6f}")
```

### Visualización de componentes

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig, axes = plt.subplots(1, 3, figsize=(18, 5), subplot_kw={'projection': '3d'})

# Vértices
axes[0].scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
                c='red', s=20, alpha=0.7)
axes[0].set_title(f'Vértices\nTotal: {num_vertices:,}')

# Aristas
for edge in list(edges)[:10000]:
    v1, v2 = edge
    axes[1].plot(vertices[[v1, v2], 0], vertices[[v1, v2], 1], 
                 vertices[[v1, v2], 2], 'b-', linewidth=0.3, alpha=0.5)
axes[1].set_title(f'Aristas\nTotal: {num_edges:,}')

# Caras
poly_collection = Poly3DCollection([vertices[face] for face in faces], alpha=0.8)
axes[2].add_collection3d(poly_collection)
axes[2].set_title(f'Caras\nTotal: {num_faces:,}')

plt.tight_layout()
plt.show()
```

### Generación de animaciones GIF

```python
import imageio
import numpy as np

frames = []
num_frames = 36

for angle in np.linspace(0, 360, num_frames, endpoint=False):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Dibujar modelo
    poly_collection = Poly3DCollection([vertices[face] for face in faces],
                                      alpha=0.8, edgecolor='gray')
    ax.add_collection3d(poly_collection)
    ax.view_init(elev=20, azim=angle)
    
    # Convertir a imagen
    fig.canvas.draw()
    image_data = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
    image = image_data.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    frames.append(image[:, :, :3])
    plt.close(fig)

# Guardar como GIF
imageio.mimsave('modelo_rotacion.gif', frames, duration=0.1)
```

---

## 📊 Prompts utilizados

Se utilizó asistencia de IA generativa para optimizar el código:

```
"Crea un notebook Jupyter que cargue un archivo OBJ usando trimesh 
y genere visualizaciones 3D mostrando vértices, aristas y caras por separado"

"¿Cómo puedo generar animaciones GIF de un modelo 3D rotando en matplotlib?"

"Corrige el código para extraer el número exacto de aristas de una malla triangular"

"¿Cómo calculo propiedades topológicas de una malla 3D como la característica de Euler?"

"Optimiza el código de generación de GIF para que sea más eficiente"
```

---

## 🎓 Aprendizajes

En esta parte del taller comprendí las estructuras fundamentales de modelos 3D. Aprendí que una malla poligonal se compone de tres elementos básicos: vértices (puntos en el espacio 3D), aristas (líneas que conectan vértices) y caras (polígonos que forman la superficie). La librería `trimesh` simplifica enormemente el trabajo con mallas 3D, permitiendo carga, análisis y manipulación de modelos complejos con pocas líneas de código.

Reforcé mis habilidades en visualización 3D con `matplotlib` y aprendí técnicas para generar animaciones GIF a partir de múltiples frames, lo cual es muy útil para documentación y análisis de datos 3D. También adquirí conocimiento sobre propiedades topológicas y geométricas de mallas, como la característica de Euler.

---

## 🛑 Dificultades encontradas

La principal dificultad fue manejar el método `tostring_rgb()` de matplotlib que ha sido deprecado en versiones recientes. Tuve que investigar y cambiar a `buffer_rgba()` para obtener correctamente los datos de píxeles de la figura.

Otra desafío fue entender cómo calcular correctamente el número de aristas en una malla triangular. Inicialmente contaba aristas duplicadas hasta que implementé un conjunto (`set`) con aristas canónicas para evitar duplicados.

La generación de múltiples GIFs fue computacionalmente intensiva, requiriendo optimización de resolución y número de frames para completarse en tiempo razonable en máquinas con recursos limitados.

---

## 🚀 Mejoras futuras

Para mejoras futuras me gustaría:

1. Integrar `vedo` para visualización interactiva con rotación en tiempo real
2. Añadir análisis más avanzados como detección de características o simplificación de malla
3. Implementar exportación a diferentes formatos (GLTF, STL, PLY)
4. Crear una interfaz gráfica interactiva con sliders para controlar parámetros de visualización
5. Optimizar el código para manejar mallas de mayor complejidad (millones de vértices)
6. Añadir análisis de suavidad de superficies y detección de bordes

---

## 🔗 Referencias

- Documentación oficial trimesh: https://trimesh.org/
- Documentación matplotlib 3D: https://matplotlib.org/stable/tutorials/toolkits/mplot3d.html
- Tutorial imageio: https://imageio.readthedocs.io/
- Formato OBJ Wikipedia: https://en.wikipedia.org/wiki/Wavefront_.obj_file
- Topología de mallas 3D: https://en.wikipedia.org/wiki/Euler_characteristic
- Paper: "Polygon Mesh Processing" - Botsch et al.

---

**Última actualización**: 2026-02-10
