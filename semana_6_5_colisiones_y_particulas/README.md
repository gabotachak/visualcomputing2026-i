# Taller - Colisiones y Partículas: Reacciones Visuales Interactivas

## Nombre del estudiante
Gabriel Andrés Anzola Tachak

## Fecha de entrega
`2026-05-29`

---

## Descripción breve

Este taller se centra en el sistema de física de **Unity** para detectar colisiones entre objetos usando `Colliders` y activar efectos de **Particle System** al momento del impacto. El script `ColisionParticulas.cs` escucha el evento `OnCollisionEnter` y reproduce el sistema de partículas en el punto de contacto.

**Nota:** Este taller es exclusivo del entorno Unity (requiere Unity Editor, Rigidbody, Colliders y Particle System). No se implementó en Three.js ya que el spec indica únicamente Unity y las herramientas requeridas son GUI-only (Unity Editor).

---

## Implementaciones

### Unity (versión LTS) — Descripción del diseño

| Componente | Funcionalidad |
|---|---|
| `Rigidbody` | Física de caída libre para los objetos (gravedad, masa) |
| `BoxCollider` / `SphereCollider` | Detección de colisiones físicas |
| `Particle System` | Efecto visual de explosión/impacto en punto de contacto |
| `ColisionParticulas.cs` | Script que escucha `OnCollisionEnter` y activa el sistema de partículas |

**Pseudocódigo del script:**
```csharp
void OnCollisionEnter(Collision collision) {
    efecto.transform.position = collision.contacts[0].point;
    efecto.Play();
}
```

---

## Resultados visuales

*Este taller requiere Unity Editor para su ejecución. No se generaron capturas ya que Unity no puede ejecutarse en entorno headless.*

---

## Código relevante

```csharp
using UnityEngine;

public class ColisionParticulas : MonoBehaviour {
    public ParticleSystem efecto;

    private void OnCollisionEnter(Collision collision) {
        if (efecto != null) {
            efecto.transform.position = collision.contacts[0].point;
            efecto.Play();
        }
    }
}
```

---

## Prompts utilizados
No se utilizaron prompts de IA en este taller.

---

## Aprendizajes y dificultades

### Aprendizajes
- `OnCollisionEnter` vs `OnTriggerEnter`: el primero requiere Rigidbody y Colliders físicos; el segundo solo Colliders con `isTrigger`.
- El Particle System en Unity debe tener `Play On Awake = false` para activarlo manualmente desde código.
- `collision.contacts[0].point` da el punto exacto de contacto en espacio mundo.

### Dificultades
- Este taller fue descrito como Unity-only y requiere el Unity Editor GUI para crear y configurar el Particle System visualmente.

### Mejoras futuras
- Replicar el efecto de partículas en Three.js usando `<Points>` y física custom.
- Agregar sonido de impacto con `AudioSource.PlayOneShot()`.
- Variar el color de partículas según la velocidad del impacto.

---

## Contribuciones grupales
Taller realizado de forma individual.

---

## Estructura del proyecto

```
semana_6_5_colisiones_y_particulas/
├── unity/
│   └── Assets/
│       └── Scripts/
│           └── ColisionParticulas.cs
├── media/
└── README.md
```

---

## Referencias
- Unity Rigidbody: https://docs.unity3d.com/ScriptReference/Rigidbody.html
- Unity Particle System: https://docs.unity3d.com/Manual/ParticleSystems.html
- OnCollisionEnter: https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnCollisionEnter.html

---

## Checklist
- [x] Carpeta con nombre semana_6_5_colisiones_y_particulas
- [x] README completo con todas las secciones
- [x] Commits descriptivos en inglés
