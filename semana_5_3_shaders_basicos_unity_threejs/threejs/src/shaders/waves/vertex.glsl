uniform float uTime;
varying vec3 vPosition;

void main() {
    vPosition = position;
    vec3 pos = position;
    pos.z += sin(pos.x * 3.0 + uTime) * 0.2;
    pos.z += sin(pos.y * 2.0 + uTime * 0.7) * 0.15;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
