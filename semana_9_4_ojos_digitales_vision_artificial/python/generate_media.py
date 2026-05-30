#!/usr/bin/env python3
"""Semana 9_4: Digital eyes — grayscale conversion, filters, edge detection."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)

# Generate test image
img_color = np.zeros((300, 400, 3), dtype=np.uint8)
for i in range(0, 300, 40):
    cv2.line(img_color, (0, i), (400, i), (50, 80, 120), 1)
for j in range(0, 400, 40):
    cv2.line(img_color, (j, 0), (j, 300), (50, 80, 120), 1)
cv2.circle(img_color, (100, 120), 70, (200, 80, 50), -1)
cv2.circle(img_color, (300, 180), 90, (50, 160, 80), -1)
cv2.rectangle(img_color, (150, 30), (260, 200), (80, 80, 220), -1)

gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# Apply filters
blur_box = cv2.blur(gray, (7, 7))
blur_gaussian = cv2.GaussianBlur(gray, (7, 7), 0)
sharpened = cv2.filter2D(gray, -1, np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]], np.float32))

# Edge detection
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobel_mag = np.sqrt(sobel_x**2 + sobel_y**2)
sobel_mag = (sobel_mag / sobel_mag.max() * 255).astype(np.uint8)

laplacian = np.abs(cv2.Laplacian(gray, cv2.CV_64F))
laplacian = (laplacian / laplacian.max() * 255).astype(np.uint8)

canny = cv2.Canny(gray, 50, 150)

# Plot 1: Color → Gray → Filters
fig, axes = plt.subplots(2, 4, figsize=(16, 8), facecolor='#0a0a1a')
fig.suptitle('Ojos Digitales — Visión Artificial: Filtros y Detección de Bordes', color='white', fontsize=13, fontweight='bold')

images = [
    (cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB), 'Color (BGR→RGB)', None),
    (gray, 'Escala de grises', 'gray'),
    (blur_box, 'Box Blur (7×7)', 'gray'),
    (blur_gaussian, 'Gaussian Blur (7×7)', 'gray'),
    (sharpened, 'Sharpening', 'gray'),
    (sobel_mag, 'Sobel (magnitud)', 'gray'),
    (laplacian, 'Laplaciano', 'gray'),
    (canny, 'Canny (50, 150)', 'gray'),
]

for ax, (image, title, cmap) in zip(axes.flatten(), images):
    ax.set_facecolor('#0d0d2a')
    if cmap:
        ax.imshow(image, cmap=cmap)
    else:
        ax.imshow(image)
    ax.set_title(title, color='white', fontsize=9)
    ax.axis('off')

plt.tight_layout()
fig.savefig('../media/digital_vision_filters.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: digital_vision_filters.png")

# Plot 2: Sobel X, Y, magnitude + directions
fig2, axes2 = plt.subplots(1, 4, figsize=(16, 4), facecolor='#0a0a1a')
fig2.suptitle('Operador Sobel: Gradientes Direccionales', color='white', fontsize=12, fontweight='bold')

sobel_x_disp = np.abs(sobel_x)
sobel_x_disp = (sobel_x_disp / sobel_x_disp.max() * 255).astype(np.uint8)
sobel_y_disp = np.abs(sobel_y)
sobel_y_disp = (sobel_y_disp / sobel_y_disp.max() * 255).astype(np.uint8)

# Direction
direction = np.arctan2(sobel_y, sobel_x)

for ax, (image, title) in zip(axes2, [
    (gray, 'Original (Gray)'),
    (sobel_x_disp, 'Sobel X (horizontal)'),
    (sobel_y_disp, 'Sobel Y (vertical)'),
    (sobel_mag, 'Magnitud del gradiente'),
]):
    ax.set_facecolor('#0d0d2a')
    ax.imshow(image, cmap='gray')
    ax.set_title(title, color='white', fontsize=10)
    ax.axis('off')

plt.tight_layout()
fig2.savefig('../media/sobel_gradients.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: sobel_gradients.png")
print("All media generated for semana_9_4")
