// ─── Uniforms ─────────────────────────────────────────────────────────────────
uniform float time;
uniform vec3  lightDir;   // dirección de luz (espacio de vista)
uniform float fresnelPow; // exponente del efecto Fresnel

// ─── Varyings (interpolados por el rasterizador desde los vértices) ───────────
varying vec2  vUv;
varying vec3  vNormal;
varying vec3  vPosition;

void main() {
  vec3 n = normalize(vNormal);

  // ── 1. Color base desde coordenadas UV + tiempo ───────────────────────────
  //   Los UVs van de (0,0) a (1,1); los mapeamos a colores vivos.
  //   El tiempo anima el canal azul para dar sensación de vida.
  vec3 baseColor = vec3(
    vUv.x,
    vUv.y,
    0.5 + 0.5 * sin(time * 0.8)
  );

  // ── 2. Iluminación difusa Lambert ─────────────────────────────────────────
  //   diffuse = max(dot(N, L), 0)
  vec3 l = normalize(lightDir);
  float diff = max(dot(n, l), 0.0);

  vec3 litColor = baseColor * (0.15 + 0.85 * diff);

  // ── 3. Fresnel (rim) ──────────────────────────────────────────────────────
  //   Cuanto más perpendicular es la normal respecto a la cámara,
  //   más brillante se ve el borde. Demuestra el uso de vPosition (view space).
  vec3 viewDir = normalize(-vPosition);
  float fresnel = pow(1.0 - max(dot(n, viewDir), 0.0), fresnelPow);

  vec3 rimColor = vec3(0.2, 0.6, 1.0) * fresnel;

  // ── 4. Color final ────────────────────────────────────────────────────────
  vec3 finalColor = litColor + rimColor;

  gl_FragColor = vec4(finalColor, 1.0);
}
