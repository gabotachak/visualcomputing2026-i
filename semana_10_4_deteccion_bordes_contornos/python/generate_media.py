#!/usr/bin/env python3
"""Semana 10_4: Edge and contour detection — Sobel, Prewitt, Canny, scikit-image."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage import filters, feature, color
from skimage.draw import disk, rectangle_perimeter
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Create test image
img = np.zeros((300, 400, 3), dtype=np.uint8)
cv2.circle(img, (100, 150), 70, (180, 80, 50), -1)
cv2.rectangle(img, (200, 80), (360, 240), (50, 150, 200), -1)
pts = np.array([[330, 50], [270, 200], [390, 200]], dtype=np.int32)
cv2.fillPoly(img, [pts], (180, 50, 200))
# Add some noise
noise = np.random.randint(0, 25, img.shape, dtype=np.uint8)
img = cv2.add(img, noise)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_float = gray.astype(np.float64) / 255.0

# OpenCV edge detectors
# Sobel
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobel_mag = np.sqrt(sobel_x**2 + sobel_y**2)
sobel_mag = (sobel_mag / sobel_mag.max() * 255).astype(np.uint8)

# Prewitt (manual kernel)
kernel_px = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float32)
kernel_py = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
prewitt_x = cv2.filter2D(gray.astype(np.float32), -1, kernel_px)
prewitt_y = cv2.filter2D(gray.astype(np.float32), -1, kernel_py)
prewitt_mag = np.sqrt(prewitt_x**2 + prewitt_y**2)
prewitt_mag = (prewitt_mag / prewitt_mag.max() * 255).astype(np.uint8)

# Laplacian
laplacian = np.abs(cv2.Laplacian(gray, cv2.CV_64F))
laplacian = (laplacian / laplacian.max() * 255).astype(np.uint8)

# Canny (multiple thresholds)
canny_low = cv2.Canny(gray, 20, 60)
canny_high = cv2.Canny(gray, 80, 200)

# scikit-image: Canny + Roberts
sk_canny = feature.canny(gray_float, sigma=2.0)
sk_sobel = filters.sobel(gray_float)
sk_scharr = filters.scharr(gray_float)

# Contour analysis on Canny
contours, _ = cv2.findContours(canny_high, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
cv2.drawContours(contour_img, contours, -1, (0, 255, 100), 2)

# Plot 1: Edge detectors comparison
fig, axes = plt.subplots(3, 4, figsize=(16, 12), facecolor='#0a0a1a')
fig.suptitle('Detección de Bordes — Sobel, Prewitt, Laplaciano, Canny (OpenCV + scikit-image)', color='white', fontsize=13, fontweight='bold')

images_data = [
    (cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 'Original', None),
    (gray, 'Escala de grises', 'gray'),
    (sobel_mag, 'Sobel (OpenCV)\n(magnitud)', 'gray'),
    (prewitt_mag, 'Prewitt (manual)\n(magnitud)', 'gray'),
    (np.abs(sobel_x).astype(np.uint8), 'Sobel X', 'gray'),
    (np.abs(sobel_y).astype(np.uint8), 'Sobel Y', 'gray'),
    (laplacian, 'Laplaciano', 'gray'),
    (canny_low, 'Canny (20,60)', 'gray'),
    (canny_high, 'Canny (80,200)', 'gray'),
    ((sk_canny * 255).astype(np.uint8), 'scikit Canny (σ=2)', 'gray'),
    ((sk_sobel * 255 / sk_sobel.max()).astype(np.uint8), 'scikit Sobel', 'gray'),
    (cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB), f'Contornos ({len(contours)})', None),
]

for ax, (image, title, cmap) in zip(axes.flatten(), images_data):
    ax.set_facecolor('#0d0d2a')
    if cmap:
        ax.imshow(image, cmap=cmap)
    else:
        ax.imshow(image)
    ax.set_title(title, color='white', fontsize=9)
    ax.axis('off')

plt.tight_layout()
fig.savefig('../media/edge_detection_comparison.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: edge_detection_comparison.png")

# Plot 2: Canny threshold sensitivity
fig2, axes2 = plt.subplots(1, 4, figsize=(16, 4), facecolor='#0a0a1a')
fig2.suptitle('Sensibilidad al Umbral — Canny Edge Detector', color='white', fontsize=12, fontweight='bold')

threshold_pairs = [(10, 30), (40, 100), (80, 200), (120, 300)]
for ax, (t1, t2) in zip(axes2, threshold_pairs):
    edges = cv2.Canny(gray, t1, t2)
    ax.set_facecolor('#0d0d2a')
    ax.imshow(edges, cmap='gray')
    n_px = np.sum(edges > 0)
    ax.set_title(f'Canny ({t1},{t2})\n{n_px} píxeles de borde', color='white', fontsize=10)
    ax.axis('off')

plt.tight_layout()
fig2.savefig('../media/canny_threshold_sensitivity.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: canny_threshold_sensitivity.png")
print("All media generated for semana_10_4")
