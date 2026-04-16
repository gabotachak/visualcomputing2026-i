uniform float uTime;
uniform float uIntensity;
uniform vec3 uColorCore;
uniform vec3 uColorEdge;
varying vec2 vUv;
varying float vDistance;

void main() {
    // Efecto de energía pulsante
    float pulse = sin(uTime * 2.0) * 0.5 + 0.5;
    float glow = 1.0 - vDistance;

    // Patrón concéntrico
    float circles = sin(vDistance * 20.0 + uTime * 3.0) * 0.5 + 0.5;

    // Mezcla de colores basada en intensidad
    vec3 color = mix(uColorEdge, uColorCore, glow * pulse);
    color += circles * 0.3;

    float alpha = glow * pulse * uIntensity;
    gl_FragColor = vec4(color, alpha);
}
