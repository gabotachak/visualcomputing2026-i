uniform float uTime;
uniform float uFlowSpeed;
uniform vec3 uColorA;
uniform vec3 uColorB;
varying vec2 vUv;
varying vec3 vPosition;

void main() {
    // Patrón de flujo usando ruido sine
    float flow = sin(vUv.x * 8.0 + uTime * uFlowSpeed) * 0.5 + 0.5;
    flow += sin(vUv.y * 6.0 - uTime * uFlowSpeed * 0.5) * 0.5;
    flow *= 0.5;

    // Distorsión tipo turbulencia
    float turbulence = sin(vUv.x + uTime) * sin(vUv.y + uTime * 0.7);

    // Mezcla de colores
    vec3 color = mix(uColorA, uColorB, flow + turbulence * 0.3);

    // Luz especular simulada
    float specular = pow(flow, 2.0) * 0.5;
    color += specular;

    gl_FragColor = vec4(color, 0.9);
}
