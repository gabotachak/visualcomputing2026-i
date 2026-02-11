# MeshVisualizer - Proyecto Unity

Proyecto interactivo en Unity para visualizar, analizar e interactuar con modelos 3D en tiempo real.

## 📋 Descripción

MeshVisualizer es una aplicación Unity que permite cargar y visualizar modelos 3D (OBJ, STL, GLTF, etc.), mostrando información estructural detallada y permitiendo interacción en tiempo real con la malla 3D.

## 🏗️ Estructura del Proyecto

```
MeshVisualizer/
├── Assets/
│   ├── Models/              # Modelos 3D (OBJ, STL, etc.)
│   │   └── scene.obj
│   ├── Scenes/              # Escenas de Unity
│   │   └── SampleScene.unity
│   ├── Scripts/             # Scripts C#
│   │   └── MeshAnalyzer.cs
│   └── Settings/            # Configuración y perfiles
├── Packages/                # Dependencias
├── ProjectSettings/         # Configuración del proyecto
└── UserSettings/            # Configuración del usuario
```

## 🎯 Funcionalidades

### Visualización
- ✅ Carga de modelos 3D (OBJ, STL, GLTF, FBX)
- ✅ Visualización en tiempo real
- ✅ Rotación y zoom interactivos
- ✅ Iluminación realista (Universal Render Pipeline)

### Análisis
- ✅ Análisis de geometría de malla
- ✅ Cálculo de información estructural:
  - Número de vértices
  - Número de caras (triángulos)
  - Número de aristas
  - Volumen y área superficial
  - Centro de masa

### Interacción
- ✅ Controles de cámara (rotación, zoom, pan)
- ✅ Renderización en tiempo real
- ✅ Visualización de estadísticas en pantalla
- ✅ Soporte para múltiples modelos

## 🚀 Cómo Empezar

### Requisitos
- **Unity 2022 LTS** o superior
- **Universal Render Pipeline (URP)** - Incluido en el proyecto
- **C# 9.0** o superior

### Instalación y Ejecución

1. **Abre el proyecto en Unity**
   ```bash
   # El proyecto está en la carpeta unity/MeshVisualizer
   # Abre Unity Hub y selecciona esta carpeta como proyecto existente
   ```

2. **Carga la escena principal**
   - En el Project panel, navega a `Assets/Scenes/`
   - Abre `SampleScene.unity` (doble click)

3. **Ejecuta el proyecto**
   - Presiona `Play` en el editor (Ctrl+P o Cmd+P)
   - Usa el ratón para rotar, zoom y pan la cámara
   - Observa la información del modelo en pantalla

## 🎮 Controles

| Control                    | Acción         |
| -------------------------- | -------------- |
| **Mouse Drag (Izquierdo)** | Rotar modelo   |
| **Mouse Wheel**            | Zoom in/out    |
| **Right Click + Drag**     | Pan de cámara  |
| **Espacio**                | Centrar modelo |

## 📊 Script Principal: MeshAnalyzer.cs

El script `MeshAnalyzer.cs` proporciona:

- Análisis de geometría de malla en tiempo real
- Cálculo de propiedades físicas (volumen, área)
- Información estructural del modelo
- Renderización de líneas de depuración (wireframe)

### Características del Script

```csharp
[SerializeField] private Material meshMaterial;      // Material para renderizar
[SerializeField] private bool useWireframe = true;   // Mostrar wireframe
[SerializeField] private bool showVertices = true;   // Mostrar vértices
```

## 📁 Archivos Importantes

| Archivo             | Descripción                                            |
| ------------------- | ------------------------------------------------------ |
| `MeshAnalyzer.cs`   | Script principal de análisis y visualización           |
| `SampleScene.unity` | Escena principal del proyecto                          |
| `scene.obj`         | Modelo 3D de ejemplo (cargable en tiempo de ejecución) |
| `manifest.json`     | Dependencias del proyecto                              |

## ⚙️ Configuración

### Perfiles de Render

El proyecto incluye varios perfiles de calidad:

- **PC_Renderer.asset** - Calidad alta para escritorio
- **Mobile_Renderer.asset** - Calidad optimizada para móviles
- **DefaultVolumeProfile.asset** - Configuración de efectos visuales

### Ajustar Calidad

1. En el editor, ve a `Assets/Settings/`
2. Selecciona el perfil deseado
3. Ajusta los parámetros según necesites

## 🔧 Personalización

### Cambiar Modelo
1. Coloca tu modelo OBJ/STL en `Assets/Models/`
2. En el Inspector, selecciona el modelo
3. En el componente MeshAnalyzer, asigna el nuevo modelo

### Cambiar Colores
En `MeshAnalyzer.cs`, modifica:
```csharp
// Color del material
meshMaterial.color = new Color(0.2f, 0.8f, 1f, 0.8f); // Cian
```

### Cambiar Escala
```csharp
// En la jerarquía o inspector
transform.localScale = new Vector3(2f, 2f, 2f); // 2x más grande
```

## 📝 Ejemplo de Uso

1. **Abre la escena** `SampleScene.unity`
2. **Verás automáticamente:**
   - El modelo cargado
   - Información del modelo en pantalla
   - Estadísticas en tiempo real

3. **Usa los controles** para explorar el modelo interactivamente

## 🎨 Rendering Pipeline

El proyecto utiliza **Universal Render Pipeline (URP)** para:
- Mejor rendimiento multi-plataforma
- Soporte para dispositivos móviles
- Efectos visuales avanzados
- Optimización automática

## 📚 Librerías y Dependencias

| Paquete      | Versión  | Uso                   |
| ------------ | -------- | --------------------- |
| Universal RP | Incluida | Renderización gráfica |
| TextMesh Pro | Incluida | Interfaz de usuario   |
| Input System | Incluida | Gestión de entrada    |

## 🐛 Solución de Problemas

### El modelo no se carga
- Verifica que el archivo esté en `Assets/Models/`
- Comprueba que el formato sea compatible (OBJ preferible)
- Revisa la consola de errores (Window > General > Console)

### Bajo rendimiento
- Reduce la cantidad de triángulos del modelo
- Desactiva efectos visuales (PostProcessing)
- Reduce la resolución de pantalla

### Problemas de renderización
- Asegúrate de que el material esté asignado correctamente
- Verifica que Universal RP esté instalado
- Reconstruye el cache de sombreadores (Edit > Render Pipeline)

## 📈 Estadísticas del Modelo Actual

Cuando ejecutes el proyecto, verás en pantalla:
```
Mesh Information:
Vertices: XXXX
Triangles: XXXX
Bounds: (x, y, z) to (x, y, z)
Volume: XXX units³
Surface Area: XXX units²
```

## 🎓 Aprendizaje

Este proyecto demuestra:
- Carga de geometría 3D en tiempo real
- Análisis de mallas 3D
- Interacción con controles de cámara
- Rendering en tiempo real con URP
- Interfaz de usuario en mundo 3D

## 📄 Notas

- El proyecto usa URP (Universal Render Pipeline) para mejor compatibilidad
- Compatible con Unity 2022 LTS y versiones posteriores
- Optimizado para PC, pero puede ejecutarse en dispositivos móviles
- Los modelos se cargan en tiempo de ejecución desde Assets/Models/

## 📬 Contacto

Parte del proyecto **Seminario de Computación Visual 2026**

---

**Última actualización**: Febrero 2026
**Unity Version**: 2022 LTS o superior
**Render Pipeline**: Universal Render Pipeline (URP)
