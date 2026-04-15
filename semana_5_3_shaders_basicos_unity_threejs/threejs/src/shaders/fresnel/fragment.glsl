varying vec3 vNormal;
varying vec3 vPosition;
uniform float uFresnelPower;
uniform vec3 uBaseColor;
uniform vec3 uGlowColor;

void main() {
    vec3 viewDirection = normalize(-vPosition);
    float fresnel = pow(1.0 - dot(viewDirection, vNormal), uFresnelPower);

    vec3 finalColor = mix(uBaseColor, uGlowColor, fresnel);
    gl_FragColor = vec4(finalColor, 1.0);
}
