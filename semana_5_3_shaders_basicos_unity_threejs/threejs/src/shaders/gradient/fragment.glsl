varying vec2 vUv;
uniform vec3 colorTop;
uniform vec3 colorBottom;

void main() {
    vec3 color = mix(colorBottom, colorTop, vUv.y);
    gl_FragColor = vec4(color, 1.0);
}
