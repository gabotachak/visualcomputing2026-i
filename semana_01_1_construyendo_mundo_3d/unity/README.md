# Taller - Construyendo el Mundo 3D: Unity

## Implementación en Unity

### Descripción

Se desarrolló un proyecto interactivo en Unity que permite cargar, visualizar y analizar modelos 3D en formato OBJ. El proyecto incluye análisis de geometría de malla en tiempo real, visualización interactiva con controles de cámara, y estadísticas detalladas de la estructura poligonal.

### Tecnología utilizada

- **Unity 2022 LTS**: Engine de desarrollo de juegos y aplicaciones 3D
- **C# 9.0**: Lenguaje de programación para scripts
- **Universal Render Pipeline (URP)**: Pipeline de renderización avanzado
- **TextMesh Pro**: Sistema de texto mejorado
- **Input System**: Nuevo sistema de entrada

### Funcionalidades implementadas

1. **Carga y visualización de modelos 3D**:
   - Carga de archivos OBJ desde carpeta Assets/Models/
   - Renderización en tiempo real con iluminación realista
   - Visualización de propiedades geométricas

2. **Análisis de estructura de malla**:
   - Cálculo de número de vértices
   - Cálculo de número de triángulos
   - Análisis de bounding box
   - Cálculo de volumen y área superficial
   - Determinación del centro de masa

3. **Visualización interactiva**:
   - Controles de cámara: rotación (mouse izquierdo), zoom (rueda)
   - Paneo de cámara (mouse derecho + arrastrar)
   - Centrado automático (tecla Espacio)
   - Modo wireframe para visualizar estructura triangular

4. **Interfaz de usuario**:
   - Pantalla informativa con estadísticas en tiempo real
   - Información estructurada de geometría
   - Controles visuales para cambiar modos

5. **Pipeline de renderización**:
   - Universal Render Pipeline configurado
   - Iluminación ambiental y direccional optimizada
   - Anti-aliasing habilitado

---

## 📋 Estructura del proyecto

```
MeshVisualizer/
├── Assets/
│   ├── Models/              # Modelos 3D
│   │   └── scene.obj
│   ├── Scenes/              # Escenas de Unity
│   │   └── SampleScene.unity
│   ├── Scripts/             # Scripts C#
│   │   └── MeshAnalyzer.cs
│   ├── Settings/            # Configuración de render
│   │   ├── PC_Renderer.asset
│   │   └── Mobile_Renderer.asset
│   └── TextMesh Pro/        # Fuentes y recursos
├── Packages/                # Dependencias
├── ProjectSettings/         # Configuración del proyecto
└── UserSettings/            # Configuración del usuario
```

---

## 🛠️ Requisitos

- **Unity 2022 LTS** o superior
- **Universal Render Pipeline (URP)** (incluido)
- **C# 9.0** o superior
- 4GB RAM mínimo

---

## 🚀 Cómo usar

### Instalación

```bash
# El proyecto ya está configurado
# Simplemente abre la carpeta en Unity Hub o desde el editor
```

### Ejecutar el proyecto

1. Abre Unity y carga el proyecto desde `unity/MeshVisualizer`
2. En el Project panel, navega a `Assets/Scenes/`
3. Abre `SampleScene.unity` (doble click)
4. Presiona `Play` (Ctrl+P)

### Controles

| Control | Acción |
|---------|--------|
| **Click izquierdo + arrastrar** | Rotar modelo |
| **Rueda del ratón** | Zoom in/out |
| **Click derecho + arrastrar** | Paneo de cámara |
| **Espacio** | Centrar modelo |
| **W** | Toggle wireframe |

---

## 💻 Código relevante

### Análisis de geometría (MeshAnalyzer.cs)

```csharp
public class MeshAnalyzer : MonoBehaviour
{
    private Mesh analyzedMesh;
    private MeshFilter meshFilter;
    
    void Start()
    {
        meshFilter = GetComponent<MeshFilter>();
        analyzedMesh = meshFilter.sharedMesh;
        
        // Análisis de geometría
        int vertexCount = analyzedMesh.vertices.Length;
        int triangleCount = analyzedMesh.triangles.Length / 3;
        
        Debug.Log($"Vértices: {vertexCount}");
        Debug.Log($"Triángulos: {triangleCount}");
    }
    
    public void CalculateMeshBounds()
    {
        Bounds bounds = analyzedMesh.bounds;
        Vector3 center = bounds.center;
        Vector3 extents = bounds.extents;
        
        Debug.Log($"Centro: {center}");
        Debug.Log($"Tamaño: {bounds.size}");
    }
}
```

### Cálculo de volumen

```csharp
public float CalculateVolume()
{
    Vector3[] vertices = analyzedMesh.vertices;
    int[] triangles = analyzedMesh.triangles;
    
    float volume = 0f;
    
    for (int i = 0; i < triangles.Length; i += 3)
    {
        Vector3 a = vertices[triangles[i]];
        Vector3 b = vertices[triangles[i + 1]];
        Vector3 c = vertices[triangles[i + 2]];
        
        volume += Vector3.Dot(a, Vector3.Cross(b, c));
    }
    
    return Mathf.Abs(volume) / 6f;
}
```

---

## 📊 Prompts utilizados

Se utilizó asistencia de IA generativa para optimizar la implementación:

```
"¿Cómo analizar la geometría de una malla 3D en Unity?"
"Crea un script que calcule el volumen de un mesh triangular"
"Implementa controles de cámara libres en Unity"
"¿Cómo visualizar datos de un modelo 3D en pantalla usando Canvas?"
"Optimiza el renderizado de modelos 3D complejos en Unity"
```

---

## 🎓 Aprendizajes

En esta parte del taller aprendí cómo trabajar con geometría 3D en Unity, específicamente cómo acceder a datos de mallas poligonales (vértices, triángulos) y extraer información estructural. Reforcé conocimientos en:

- **Geometría 3D**: Vértices, triángulos, normales y tangentes
- **Physics-based rendering**: Cómo Universal RP renderiza realísticamente
- **Scripting en C#**: Acceso a datos de geometría, iteración eficiente
- **Controles de cámara**: Implementación de navegación 3D intuitiva
- **Optimización**: Cómo mantener buen rendimiento con geometry complejos

---

## 🛑 Dificultades encontradas

La principal dificultad fue calcular correctamente el volumen de una malla triangular. La fórmula requiere el producto escalar triple de los vértices de cada triángulo, y inicialmente tenía un factor de escala incorrecto. Tuve que investigar y ajustar a `volume / 6f`.

Otro desafío fue acceder correctamente a la geometría de modelos OBJ cargados. Unity requiere usar `meshFilter.sharedMesh` para modelos estáticos, no `mesh`, para evitar crear copias innecesarias en memoria.

La visualización en modo wireframe también fue complicada. Unity no proporciona un shader wireframe directamente; tuve que usar un shader personalizado o el renderizado de líneas (GL.Lines para depuración).

---

## 🚀 Mejoras futuras

1. Implementar exportación de análisis a archivo (JSON, CSV)
2. Añadir soporte para más formatos (GLTF, FBX, STL)
3. Crear herramientas de simplificación de malla automática
4. Visualización de normales y normales suavizadas
5. Detección automática de bordes y esquinas agudas
6. Análisis de topología más avanzado (agujeros, manifold, etc.)
7. Integración con herramientas externas (Blender, 3DS Max)
8. Modo de comparación multi-modelo
9. Exportación de vistas (screenshots, video)
10. Análisis de UV mapping y texturas

---

## 🔗 Referencias

- Documentación oficial de Unity: https://docs.unity3d.com/
- Universal Render Pipeline: https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal/
- C# Language Reference: https://docs.microsoft.com/en-us/dotnet/csharp/
- Computación gráfica: https://learnopengl.com/ (conceptos aplicables a Unity)
- Formato OBJ: https://en.wikipedia.org/wiki/Wavefront_.obj_file

---

## 🐛 Troubleshooting

### El modelo no se visualiza

- Verifica que `scene.obj` esté en `Assets/Models/`
- Comprueba que el MeshFilter tenga un mesh asignado
- Revisa la consola (Window > General > Console) para errores

### Bajo rendimiento

- Reduce la complejidad del modelo (simplifica en Blender)
- Desactiva Post-Processing
- Usa configuración de calidad reducida (Mobile_Renderer)

### Controles no responden

- Asegúrate de hacer click dentro de la ventana del Game View
- Verifica que el EventSystem de Canvas no esté bloqueando entrada
- Revisa que el script esté en un GameObject activo

---

**Última actualización**: 2026-02-10
**Unity Version**: 2022 LTS o superior
**Render Pipeline**: Universal Render Pipeline (URP)
