# Taller - Guardado y Persistencia: Firebase + Three.js

## Nombre del estudiante
Gabriel Andrés Anzola Tachak

## Fecha de entrega
`2026-05-30`

---

## Descripción breve

Este taller implementa **persistencia de estado 3D en tiempo real** mediante Firebase Realtime Database integrado con una escena React Three Fiber. El sistema guarda la posición y color de una esfera 3D interactiva en la nube cada vez que el usuario hace clic en ella; al recargar la página, el cliente suscribe al mismo nodo de Firebase y restaura el último estado guardado sin recarga manual.

La arquitectura desacopla almacenamiento (Firebase SDK) de renderizado (Three.js), demostrando cómo integrar un backend de tiempo real sin servidor propio. La esfera actúa como objeto de estado persistente: su coordenada `[x, y, z]` y `color` se sincronizan entre cualquier número de pestañas abiertas simultáneamente.

---

## Implementaciones

### Three.js / React Three Fiber

**Herramientas:** React 18 · Three.js r160 · @react-three/fiber r8 · @react-three/drei r9 · Firebase 10 · Vite 5

| Componente / Hook | Funcionalidad |
|---|---|
| `initializeApp(firebaseConfig)` | Inicializa el SDK de Firebase con las credenciales del proyecto |
| `getDatabase()` | Obtiene instancia de Realtime Database |
| `onValue(ref, cb)` | Suscripción en tiempo real al nodo `sphere/state`; actualiza el estado React al cambiar |
| `set(ref, data)` | Escribe `{x, y, z, color, savedAt}` a Firebase al hacer clic en la esfera |
| `PersistentSphere` | Componente mesh que muestra posición actual con etiqueta HUD flotante |
| HUD overlay | Panel de estado (conectado/error) y timestamp del último guardado |
| `OrbitControls` | Navegación libre de cámara alrededor de la esfera |
| `Grid` | Plano reticulado de referencia espacial |

---

## Resultados visuales

### Escena 3D y estado persistido

<!-- TODO: toma la captura, guárdala en media/threejs_connected.png -->
![Firebase Connected](./media/threejs_connected.png)
Escena con la esfera en posición guardada y HUD mostrando "Conectado ✓" con timestamp del último guardado.

<!-- TODO: toma la captura, guárdala en media/threejs_firebase_console.png -->
![Firebase Console](./media/threejs_firebase_console.png)
Navegador con la app Three.js a la izquierda y Firebase Console (Realtime Database) a la derecha mostrando el nodo `sphere/state` con los valores `{x, y, z, color, savedAt}` en tiempo real.

---

## Código relevante

**Suscripción en tiempo real y restauración de estado:**

```jsx
useEffect(() => {
  const sphereRef = ref(db, "sphere/state");
  const unsub = onValue(sphereRef, snap => {
    const data = snap.val();
    if (data) {
      setPos([data.x, data.y, data.z]);
      setColor(data.color);
      setStatus("Conectado ✓");
    }
  });
  return () => unsub();
}, []);
```

**Guardado a Firebase al hacer clic:**

```jsx
set(ref(db, "sphere/state"), {
  x: newPos[0], y: newPos[1], z: newPos[2],
  color: newColor,
  savedAt: new Date().toISOString(),
});
```

---

## Prompts utilizados

```
"React Three Fiber sphere that saves its position and color to Firebase Realtime Database
on click, and restores the last saved position on page reload using onValue subscription"
```

---

## Aprendizajes y dificultades

### Aprendizajes
- Firebase Realtime Database usa suscripciones (`onValue`) en lugar de polling, lo que permite sincronización en tiempo real entre múltiples clientes sin infraestructura propia.
- El hook `useEffect` con retorno de función de cleanup es el patrón correcto para suscribirse y desuscribirse de listeners externos en React.
- `set()` sobreescribe completamente el nodo, lo que es adecuado para estado singleton; para listas se usaría `push()`.

### Dificultades
- El SDK de Firebase v10 usa imports modulares (`firebase/app`, `firebase/database`) incompatibles con el patrón de import v8 (`import firebase from 'firebase'`). Fue necesario usar la API modular correcta.
- La configuración de reglas de Realtime Database en modo de prueba expira a los 30 días; en producción se requieren reglas de autenticación.

### Mejoras futuras
- Agregar autenticación Firebase (Google Auth) para que cada usuario tenga su propia esfera persistida bajo `users/{uid}/sphere`.
- Implementar historial de posiciones con `push()` para trazar el recorrido de la esfera en el tiempo.

---

## Contribuciones grupales
Taller realizado de forma individual.

---

## Estructura del proyecto

```
semana_15_4_guardado_persistencia_firebase_unity_threejs/
├── threejs/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       └── styles.css
├── media/
│   ├── threejs_connected.png
│   └── threejs_firebase_console.png
├── steps.md
└── README.md
```

---

## Referencias
- Firebase Realtime Database — Get Started: https://firebase.google.com/docs/database/web/start
- Firebase SDK Modular API: https://firebase.google.com/docs/web/modular-upgrade
- React Three Fiber — useEffect with external subscriptions: https://docs.pmnd.rs/react-three-fiber/api/hooks

---

## Checklist de entrega

- [x] Carpeta con nombre `semana_15_4_guardado_persistencia_firebase_unity_threejs`
- [x] Código limpio y funcional en `threejs/`
- [ ] GIFs/imágenes en `media/` con nombres descriptivos — **PENDIENTE: tomar capturas**
- [ ] README completo con todas las secciones — **PENDIENTE: agregar imágenes reales**
- [ ] Mínimo 2 capturas/GIFs por implementación
- [x] Commits descriptivos en inglés
