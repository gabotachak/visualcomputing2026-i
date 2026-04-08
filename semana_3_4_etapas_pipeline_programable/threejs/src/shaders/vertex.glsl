// ─── Uniforms (datos enviados desde CPU → GPU, constantes por draw call) ──────
uniform float time;

// ─── Varyings (datos interpolados de vértice → fragmento) ────────────────────
varying vec2  vUv;       // coordenadas de textura
varying vec3  vNormal;   // normal en espacio de vista
varying vec3  vPosition; // posición en espacio de vista (para Fresnel)

void main() {
  // ── 1. Pasar varyings ──────────────────────────────────────────────────────
  vUv = uv;

  // Normal transformada al espacio de vista (normalMatrix = inverse-transpose de modelView)
  vNormal = normalize(normalMatrix * normal);

  // ── 2. Deformación sinusoidal en el espacio del modelo ────────────────────
  //   Mueve Z de cada vértice en función de su posición X y del tiempo.
  //   Demuestra que el vertex shader puede modificar posiciones antes
  //   de proyectar (Vertex Processing).
  vec3 pos = position;
  pos.z += sin(pos.x * 5.0 + time) * 0.12;
  pos.z += sin(pos.y * 4.0 + time * 0.7) * 0.08;

  // ── 3. Posición en espacio de vista (para iluminación y Fresnel) ──────────
  vPosition = (modelViewMatrix * vec4(pos, 1.0)).xyz;

  // ── 4. Transformación final: model → clip space ───────────────────────────
  //   projectionMatrix * modelViewMatrix = MVP completo
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
