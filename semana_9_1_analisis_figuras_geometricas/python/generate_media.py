#!/usr/bin/env python3
"""Semana 9_1: Geometric shape analysis — centroid, area, perimeter."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Create a synthetic image with geometric shapes
img = np.zeros((480, 640, 3), dtype=np.uint8)
img[:] = (15, 15, 35)  # dark blue background

# Draw shapes
cv2.circle(img, (120, 120), 60, (255, 80, 80), -1)
cv2.rectangle(img, (220, 60), (380, 200), (80, 255, 80), -1)
pts = np.array([[500, 60], [420, 200], [580, 200]], dtype=np.int32)
cv2.fillPoly(img, [pts], (80, 80, 255))
cv2.ellipse(img, (150, 350), (90, 50), 30, 0, 360, (255, 200, 80), -1)
pts2 = np.array([[350, 300], [280, 440], [420, 440], [490, 380], [490, 300]], dtype=np.int32)
cv2.fillPoly(img, [pts2], (200, 80, 255))
cv2.circle(img, (560, 380), 70, (80, 255, 200), -1)

# Convert to grayscale + threshold
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Analyze each contour
result = img.copy()
shape_data = []
SHAPE_NAMES = {3: 'Triángulo', 4: 'Cuadrilátero', 0: 'Círculo/Elipse'}

for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    M = cv2.moments(cnt)
    if M['m00'] == 0 or area < 100:
        continue
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    # Classify shape
    approx = cv2.approxPolyDP(cnt, 0.04 * perimeter, True)
    n_verts = len(approx)
    shape_name = SHAPE_NAMES.get(n_verts, f'Polígono ({n_verts}v)')

    shape_data.append({'area': area, 'perimeter': perimeter, 'cx': cx, 'cy': cy, 'shape': shape_name})

    # Draw contour
    cv2.drawContours(result, [cnt], -1, (255, 255, 0), 2)
    cv2.circle(result, (cx, cy), 5, (0, 255, 255), -1)
    cv2.putText(result, f'{shape_name}', (cx-40, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
    cv2.putText(result, f'A:{area:.0f} P:{perimeter:.0f}', (cx-40, cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200,200,200), 1)

# Plot results
fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='#0a0a1a')
fig.suptitle('Análisis de Figuras Geométricas — Centroide, Área y Perímetro', color='white', fontsize=13, fontweight='bold')

axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
axes[0].set_title('Imagen original', color='white')
axes[0].axis('off')

axes[1].imshow(binary, cmap='gray')
axes[1].set_title('Imagen binarizada', color='white')
axes[1].axis('off')

axes[2].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
axes[2].set_title('Contornos + métricas', color='white')
axes[2].axis('off')

for ax in axes:
    ax.set_facecolor('#0d0d2a')

plt.tight_layout()
fig.savefig('../media/geometric_analysis.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: geometric_analysis.png")

# Plot shape metrics table
fig2, ax2 = plt.subplots(figsize=(10, 5), facecolor='#0a0a1a')
ax2.set_facecolor('#0d0d2a')
ax2.axis('off')
ax2.set_title('Métricas por Figura Detectada', color='white', fontsize=13, fontweight='bold')

if shape_data:
    col_labels = ['Figura', 'Área (px²)', 'Perímetro (px)', 'Centroide (x,y)']
    rows = [[s['shape'], f"{s['area']:.0f}", f"{s['perimeter']:.1f}", f"({s['cx']}, {s['cy']})"]
            for s in shape_data]
    table = ax2.table(cellText=rows, colLabels=col_labels, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)
    for (r, c), cell in table.get_celld().items():
        cell.set_facecolor('#1a1a3e' if r > 0 else '#2a2a5e')
        cell.set_text_props(color='white')
        cell.set_edgecolor('#444')

plt.tight_layout()
fig2.savefig('../media/shape_metrics_table.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: shape_metrics_table.png")
print("All media generated for semana_9_1")
