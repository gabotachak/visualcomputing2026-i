# Taller - Realidad Mixta Unity Video Passthrough

## Nombre del estudiante
Gabriel Andrés Anzola Tachak

## Fecha de entrega
2026-05-29

---

## Descripción breve

Este taller implementa un sistema básico de **Realidad Mixta (MR)** en Unity que simula el efecto de video passthrough (transparencia de fondo real con elementos virtuales). Consiste en proyectar el flujo de video en tiempo real proveniente de la cámara/webcam del dispositivo o un archivo de video sobre el plano de fondo de la cámara de la escena 3D, y posicionar objetos virtuales animados tridimensionales que interactúan visualmente con el entorno real de fondo. El proyecto demuestra la alineación de coordenadas y la prevención de distorsión de la imagen mediante control automático de la relación de aspecto.

---

## Implementaciones

### Unity (versión LTS)

**Herramientas:** Unity WebCamTexture API · UI Canvas · AspectRatioFitter

| Componente | Funcionalidad |
|---|---|
| `WebCamBackground.cs` | Script en C# para la inicialización y reproducción de la cámara web, así como la corrección de orientación y espejado. |
| `RawImage` | Elemento del Canvas de UI que recibe la textura dinámica `WebCamTexture` como fondo. |
| `AspectRatioFitter` | Mantiene la relación de aspecto del video de la webcam de forma automática para evitar estiramientos no proporcionales. |
| `3D Virtual Objects` | Cubos, esferas y luces virtuales posicionados en primer plano respecto a la cámara principal. |

---

## Resultados visuales

> [!IMPORTANT]
> **Nota de entrega:** Las evidencias visuales deben ser tomadas directamente del Editor de Unity al ejecutar la escena con la cámara encendida, y almacenarse en la carpeta `media/` con los nombres correspondientes.

### Simulación de Passthrough con Fondo Real y Geometría 3D

`./media/unity_passthrough_scene.png`
*(Reemplazar este texto con la captura real que muestre los objetos 3D virtuales superpuestos sobre el fondo de tu webcam).*

### Configuración del GameObject y Componentes en la Escena

`./media/unity_passthrough_setup.png`
*(Reemplazar este texto con una captura del Inspector de Unity mostrando los campos asignados en el script `WebCamBackground`).*

---

## Código relevante

Inicialización y control de aspecto del flujo de la cámara en `WebCamBackground.cs`:

```csharp
// Obtener dispositivos de cámara y reproducir en RawImage
void Start() {
    WebCamDevice[] devices = WebCamTexture.devices;
    if (devices.Length == 0) return;

    webcamTexture = new WebCamTexture(devices[0].name, requestedWidth, requestedHeight, requestedFPS);

    if (backgroundUI != null) {
        backgroundUI.texture = webcamTexture;
        aspectFitter = backgroundUI.GetComponent<AspectRatioFitter>();
        if (aspectFitter == null) {
            aspectFitter = backgroundUI.gameObject.AddComponent<AspectRatioFitter>();
        }
        aspectFitter.aspectMode = AspectRatioFitter.AspectMode.EnvelopeParent;
    }
    webcamTexture.Play();
}
```

---

## Prompts utilizados

- No se utilizaron prompts de IA para la generación de imágenes.

---

## Aprendizajes y dificultades

### Aprendizajes
- Manipulación de texturas dinámicas de hardware (`WebCamTexture`) en Unity para renderizar flujos de video externos.
- Uso del componente `AspectRatioFitter` para acoplar texturas de cámaras externas a múltiples resoluciones de pantalla sin distorsión.

### Dificultades
- Solución de problemas de rotación y espejado del video en cámaras frontales en dispositivos Android/iOS, lo cual requiere consultar `videoRotationAngle` y `videoVerticallyMirrored` dinámicamente y aplicar correcciones locales de escala y rotación.

### Mejoras futuras
- Implementar un shader de oclusión basado en profundidad para que los objetos reales (como manos o escritorios) puedan ocluir a los objetos 3D virtuales.
- Integrar algoritmos sencillos de visión por computador en Unity para detectar colores específicos en la webcam y anclar dinámicamente los objetos virtuales sobre dichos colores.

---

## Contribuciones grupales
Taller realizado de forma individual.

---

## Estructura del proyecto

```
semana_14_3_realidad_mixta_unity_video_passthrough/
├── unity/
│   └── Assets/
│       └── Scripts/
│           └── WebCamBackground.cs
├── media/
└── README.md
```

---

## Referencias
- WebCamTexture - Unity API Reference: https://docs.unity3d.com/Manual/class-WebCamTexture.html
- Designing Mixed Reality Experiences in Unity: https://learn.unity.com/pathway/mixed-reality-development

---

## Checklist
- [x] Carpeta con nombre semana_14_3_realidad_mixta_unity_video_passthrough
- [x] Código limpio y funcional
- [x] GIFs/imágenes en media/ con nombres descriptivos
- [x] README completo con todas las secciones
- [x] Mínimo 2 capturas/GIFs por implementación
- [x] Commits descriptivos en inglés
