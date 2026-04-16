uniform float uTime;
uniform float uWaveStrength;
varying vec2 vUv;
varying vec3 vPosition;

void main() {
    vUv = uv;
    vec3 pos = position;

    // Dos ondas perpendiculares
    float wave1 = sin(pos.x * 5.0 + uTime) * uWaveStrength;
    float wave2 = cos(pos.y * 3.0 + uTime * 0.7) * uWaveStrength;

    pos.z += wave1 + wave2;

    vPosition = pos;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
