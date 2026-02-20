/**
 * Taller 0 - Transformaciones Básicas en Computación Visual
 * Implementación en Processing (3D)
 */

float angle = 0;

void setup() {
  size(800, 600, P3D);
  smooth(8);
}

void draw() {
  background(20, 20, 30); // Fondo oscuro
  
  // Luces para dar volumen al objeto 3D
  lights();
  directionalLight(255, 255, 255, -1, 1, -1);
  ambientLight(100, 100, 100);
  
  // Posicionar la cámara
  camera(0, -300, 500,  // Ojo (posición)
         0, 0, 0,       // Centro (hacia donde mira)
         0, 1, 0);      // Arriba (orientación Y)
         
  // Definir estilo de dibujo
  strokeWeight(2);
  stroke(0, 255, 255); // Bordes cyan
  fill(0, 150, 255, 200); // Relleno azul semitransparente

  // Tiempo en segundos
  float t = millis() / 1000.0;
  
  // ==========================================
  // TRANSFORMACIONES
  // ==========================================
  
  pushMatrix(); // Aislar transformaciones
  
  // 1. TRASLACIÓN: Movimiento oscilante u ondulado
  // Se mueve en el eje X con sin() y en el Y con cos()
  float tx = sin(t) * 150;
  float ty = cos(t * 1.5) * 100;
  float tz = sin(t * 0.5) * 50;
  translate(tx, ty, tz);
  
  // 2. ROTACIÓN: Gira continuamente en los ejes X e Y
  rotateX(t * 1.2);
  rotateY(t * 0.8);
  rotateZ(t * 0.5);
  
  // 3. ESCALADO: Efecto de "respiración" o latido cíclico
  // El factor varía entre 0.5 y 1.5
  float scaleFactor = 1.0 + 0.5 * sin(t * 3);
  scale(scaleFactor);
  
  // DIBUJAR LA GEOMETRÍA
  box(100); // Cubo de tamaño base 100
  
  // Opcional: Dibujar ejes locales dentro del bloque para ver cómo rotan con el objeto
  strokeCap(ROUND);
  strokeWeight(4);
  // Eje X rojo
  stroke(255, 0, 0); line(0, 0, 0, 100, 0, 0);
  // Eje Y verde
  stroke(0, 255, 0); line(0, 0, 0, 0, 100, 0);
  // Eje Z azul
  stroke(0, 0, 255); line(0, 0, 0, 0, 0, 100);
  
  popMatrix(); // Restaurar el estado de transformación
  
  // UI superpuesta (No afectada por las transformaciones anteriores gracias a push/pop)
  hint(DISABLE_DEPTH_TEST); // Dibujar siempre arriba
  camera(); // Reset cámara a 2D para la UI
  noLights(); // Textos sin iluminación
  
  fill(255);
  textSize(20);
  textAlign(LEFT, TOP);
  text("Transformaciones 3D - Processing", 20, 20);
  
  textSize(14);
  fill(200);
  text("Traslación: X=" + nf(tx, 0, 1) + ", Y=" + nf(ty, 0, 1) + ", Z=" + nf(tz, 0, 1), 20, 50);
  text("Rotación Continua (XYZ)", 20, 70);
  text("Escala: " + nf(scaleFactor, 0, 2) + "x", 20, 90);
  text("Tiempo: " + nf(t, 0, 1) + "s", 20, 110);
  
  hint(ENABLE_DEPTH_TEST);
}
