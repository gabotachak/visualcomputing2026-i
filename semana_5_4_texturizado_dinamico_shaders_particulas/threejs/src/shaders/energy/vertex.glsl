uniform float uTime;
uniform vec2 uMousePos;
varying vec2 vUv;
varying vec3 vPosition;
varying float vDistance;

void main() {
    vUv = uv;
    vPosition = position;

    vec3 pos = position;

    // Distancia al mouse (en espacio normalizado)
    float dist = distance(uMousePos, vUv);
    vDistance = dist;

    // Desplazamiento radial basado en distancia al mouse
    float displacement = sin(uTime * 3.0) * 0.05 * (1.0 - dist);
    pos += normalize(pos) * displacement;

    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
