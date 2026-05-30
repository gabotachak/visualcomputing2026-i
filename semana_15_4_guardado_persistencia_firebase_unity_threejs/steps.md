# Steps — semana_15_4 (lo que SOLO TÚ puedes hacer)

## Lo que ya está listo (no tocar)
- `threejs/src/App.jsx` — implementación completa
- `threejs/src/main.jsx`, `styles.css`, `index.html`, `vite.config.js` — sin cambios
- `firebase` agregado a `package.json`
- `README.md` — pre-llenado, solo faltan las capturas

---

## Paso 1 — Crear proyecto Firebase y obtener config (~10 min)

1. Ve a **https://console.firebase.google.com/**
2. Clic **"Agregar proyecto"** → nombre: `visualcomputing-15-4` → Continuar
3. Desactiva Google Analytics → **Crear proyecto** → espera → Continuar
4. Panel izquierdo → **Compilación** → **Realtime Database** → **Crear una base de datos**
5. Región: cualquiera → Siguiente → selecciona **"Modo de prueba"** → **Habilitar**
6. Clic ⚙️ (arriba izquierda) → **Configuración del proyecto** → baja a **"Tus apps"**
7. Clic icono `</>` (Web) → apodo: `threejs-app` → **Registrar app**
8. Copia el objeto `firebaseConfig = { apiKey: "...", ... }` que aparece

---

## Paso 2 — Pegar config en App.jsx

Abre `threejs/src/App.jsx`. Busca el bloque:

```js
const firebaseConfig = {
  apiKey:            "REPLACE_ME",
  ...
};
```

Reemplaza **todos** los `"REPLACE_ME"` con los valores que copiaste en el Paso 1.

---

## Paso 3 — Instalar dependencias y correr

```bash
cd semana_15_4_guardado_persistencia_firebase_unity_threejs/threejs
npm install
npm run dev
```

Abre **http://localhost:5173**

Verifica:
- HUD dice "Conectado ✓"
- Al hacer clic en la esfera: se mueve, cambia de color, aparece timestamp de guardado
- Al recargar la página: la esfera vuelve a la última posición

---

## Paso 4 — Tomar 2 capturas y guardarlas en `media/`

**Captura 1 → `media/threejs_connected.png`**
Toma captura de la app mostrando la esfera en posición guardada con HUD "Conectado ✓" y timestamp visible.

**Captura 2 → `media/threejs_firebase_console.png`**
Pon la app a la izquierda de la pantalla y abre **Firebase Console → Realtime Database** a la derecha.
Haz clic en la esfera (para que los datos estén en Firebase) y toma captura de ambas ventanas juntas mostrando el nodo `sphere/state` con los datos.

Herramienta rápida (Linux):
```bash
# región interactiva → archivo directo
scrot -s media/threejs_connected.png
```

---

## Paso 5 — Actualizar README.md

En `README.md`, los dos comentarios `<!-- TODO: ... -->` ya tienen los nombres de archivo correctos.
Solo verifica que las imágenes existen en `media/` y cambia el Checklist:

```markdown
- [x] GIFs/imágenes en `media/` con nombres descriptivos
- [x] README completo con todas las secciones
- [x] Mínimo 2 capturas/GIFs por implementación
```

---

## Hecho — puedes eliminar este archivo antes de hacer commit.
