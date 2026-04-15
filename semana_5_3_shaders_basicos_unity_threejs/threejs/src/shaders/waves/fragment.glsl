uniform float uTime;
varying vec3 vPosition;
uniform float uWaveFrequency;
uniform vec3 uColorA;
uniform vec3 uColorB;

void main() {
    float wave = sin(vPosition.x * uWaveFrequency + uTime) * 0.5 + 0.5;
    vec3 color = mix(uColorA, uColorB, wave);
    gl_FragColor = vec4(color, 1.0);
}
