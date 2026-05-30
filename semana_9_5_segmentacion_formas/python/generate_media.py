#!/usr/bin/env python3
"""Semana 9_5: Image segmentation — thresholding and shape recognition."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Create test image with overlapping shapes on gradient background
img = np.zeros((400, 500, 3), dtype=np.uint8)
# Add gradient noise background
noise = np.random.randint(20, 60, (400, 500, 3), dtype=np.uint8)
img = noise.copy()

# Draw shapes
cv2.circle(img, (100, 100), 70, (220, 180, 100), -1)
cv2.rectangle(img, (200, 50), (360, 200), (180, 220, 100), -1)
pts = np.array([[420, 50], [350, 200], [490, 200]], dtype=np.int32)
cv2.fillPoly(img, [pts], (100, 180, 220))
cv2.circle(img, (130, 300), 80, (220, 100, 180), -1)
pts2 = np.array([[280, 250], [350, 350], [430, 300], [460, 180]], dtype=np.int32)
cv2.fillPoly(img, [pts2], (180, 100, 220))
cv2.ellipse(img, (400, 320), (70, 50), 0, 0, 360, (100, 220, 180), -1)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Thresholding methods
_, thresh_fixed = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
thresh_adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, 21, 5)
_, thresh_otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Morphological operations to clean binary image
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
cleaned = cv2.morphologyEx(thresh_otsu, cv2.MORPH_OPEN, kernel)
cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)

# Find and analyze contours
contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
result = img.copy()
areas = []
perimeters = []

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 500:
        continue
    perimeter = cv2.arcLength(cnt, True)
    areas.append(area)
    perimeters.append(perimeter)
    M = cv2.moments(cnt)
    if M['m00'] == 0:
        continue
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    x, y, bw, bh = cv2.boundingRect(cnt)

    cv2.drawContours(result, [cnt], -1, (0, 255, 255), 2)
    cv2.rectangle(result, (x, y), (x+bw, y+bh), (255, 100, 0), 1)
    cv2.circle(result, (cx, cy), 5, (255, 255, 0), -1)

# Plot
fig, axes = plt.subplots(2, 3, figsize=(15, 10), facecolor='#0a0a1a')
fig.suptitle('Segmentación de Formas — Umbralización y Análisis Morfológico', color='white', fontsize=13, fontweight='bold')

imgs_to_show = [
    (cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 'Original', None),
    (gray, 'Escala de grises', 'gray'),
    (thresh_fixed, 'Umbral fijo (80)', 'gray'),
    (thresh_otsu, f'Umbral Otsu', 'gray'),
    (cleaned, 'Después de morfología', 'gray'),
    (cv2.cvtColor(result, cv2.COLOR_BGR2RGB), f'Contornos ({len([a for a in areas if a>500])} formas)', None),
]

for ax, (image, title, cmap) in zip(axes.flatten(), imgs_to_show):
    ax.set_facecolor('#0d0d2a')
    if cmap:
        ax.imshow(image, cmap=cmap)
    else:
        ax.imshow(image)
    ax.set_title(title, color='white', fontsize=10)
    ax.axis('off')

plt.tight_layout()
fig.savefig('../media/segmentation_shapes.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: segmentation_shapes.png")

# Plot 2: Metrics
if areas:
    fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
    fig2.suptitle('Métricas de Formas Segmentadas', color='white', fontsize=12, fontweight='bold')
    for ax in axes2:
        ax.set_facecolor('#0d0d2a')
        ax.tick_params(colors='gray')
        for spine in ax.spines.values(): spine.set_color('#333')

    axes2[0].bar(range(len(areas)), areas, color='#4af', alpha=0.8)
    axes2[0].axhline(np.mean(areas), color='yellow', linestyle='--', label=f'Media: {np.mean(areas):.0f}')
    axes2[0].set_xlabel('Forma #', color='gray')
    axes2[0].set_ylabel('Área (px²)', color='gray')
    axes2[0].set_title('Área por forma detectada', color='white')
    axes2[0].legend(facecolor='#0d0d2a', labelcolor='white')

    axes2[1].scatter(areas, perimeters, c='#f84', s=100, alpha=0.8)
    axes2[1].set_xlabel('Área (px²)', color='gray')
    axes2[1].set_ylabel('Perímetro (px)', color='gray')
    axes2[1].set_title('Área vs Perímetro', color='white')
    for i, (a, p) in enumerate(zip(areas, perimeters)):
        axes2[1].annotate(f'#{i+1}', (a, p), textcoords='offset points', xytext=(5,5), color='white', fontsize=9)

    plt.tight_layout()
    fig2.savefig('../media/segmentation_metrics.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
    plt.close()
    print("Saved: segmentation_metrics.png")

print(f"Detected {len(areas)} shapes. Area avg: {np.mean(areas) if areas else 0:.0f}")
print("All media generated for semana_9_5")
