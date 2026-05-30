#!/usr/bin/env python3
"""Semana 9_3: Image as pixel matrix — channels, histograms, brightness/contrast."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Create a colorful synthetic image
h, w = 300, 400
img = np.zeros((h, w, 3), dtype=np.uint8)
# Gradient background
for i in range(h):
    for j in range(w):
        img[i, j] = [int(i * 255 / h), int(j * 255 / w), 150]

# Add shapes
cv2.circle(img, (100, 100), 70, (255, 50, 50), -1)
cv2.rectangle(img, (200, 50), (360, 200), (50, 200, 100), -1)
cv2.putText(img, 'Pixel', (180, 260), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 50), 3)

# Split channels
b, g, r = cv2.split(img)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Pixel manipulation: change color of a region
modified = img.copy()
modified[50:150, 250:350] = [255, 128, 0]  # replace rectangle with orange
modified[150:250, 50:150] = img[0:100, 250:350]  # copy a region

# Brightness and contrast adjustment
alpha = 1.5  # contrast
beta = 30    # brightness
bright_contrast = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

# Plot 1: Channels and manipulations
fig, axes = plt.subplots(3, 3, figsize=(14, 11), facecolor='#0a0a1a')
fig.suptitle('Imagen como Matriz de Píxeles — Canales, Histograma y Ajustes', color='white', fontsize=13, fontweight='bold')

imgs_to_show = [
    (cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 'Original (RGB)', None),
    (r, 'Canal R', 'Reds'),
    (g, 'Canal G', 'Greens'),
    (b, 'Canal B', 'Blues'),
    (hsv[:,:,0], 'HSV — Hue', 'hsv'),
    (hsv[:,:,1], 'HSV — Saturation', 'plasma'),
    (hsv[:,:,2], 'HSV — Value', 'gray'),
    (cv2.cvtColor(modified, cv2.COLOR_BGR2RGB), 'Modificación de región', None),
    (cv2.cvtColor(bright_contrast, cv2.COLOR_BGR2RGB), f'α={alpha}, β={beta}', None),
]

for ax, (image, title, cmap) in zip(axes.flatten(), imgs_to_show):
    ax.set_facecolor('#0d0d2a')
    if cmap:
        ax.imshow(image, cmap=cmap)
    else:
        ax.imshow(image)
    ax.set_title(title, color='white', fontsize=9)
    ax.axis('off')

plt.tight_layout()
fig.savefig('../media/pixel_matrix_channels.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: pixel_matrix_channels.png")

# Plot 2: Histogram analysis
fig2, axes2 = plt.subplots(2, 2, figsize=(12, 8), facecolor='#0a0a1a')
fig2.suptitle('Análisis de Histogramas por Canal', color='white', fontsize=13, fontweight='bold')

channel_names = ['Blue', 'Green', 'Red']
channel_colors = ['#44f', '#4f4', '#f44']
channels = [b, g, r]

for i, (ch, name, col) in enumerate(zip(channels, channel_names, channel_colors)):
    ax = axes2[i // 2][i % 2]
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')
    hist = cv2.calcHist([ch], [0], None, [256], [0, 256])
    ax.fill_between(range(256), hist[:,0], alpha=0.6, color=col)
    ax.plot(hist[:,0], color=col, linewidth=1.5)
    ax.set_title(f'Histograma {name}', color='white')
    ax.set_xlabel('Intensidad', color='gray')
    ax.set_ylabel('Frecuencia', color='gray')

# Combined histogram
ax_comb = axes2[1][1]
ax_comb.set_facecolor('#0d0d2a')
ax_comb.tick_params(colors='gray')
for spine in ax_comb.spines.values(): spine.set_color('#333')
for ch, name, col in zip(channels, channel_names, channel_colors):
    hist = cv2.calcHist([ch], [0], None, [256], [0, 256])
    ax_comb.plot(hist[:,0], color=col, linewidth=1.5, alpha=0.8, label=name)
ax_comb.set_title('Histograma combinado', color='white')
ax_comb.set_xlabel('Intensidad', color='gray')
ax_comb.legend(facecolor='#0d0d2a', labelcolor='white')

plt.tight_layout()
fig2.savefig('../media/pixel_histograms.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: pixel_histograms.png")
print("All media generated for semana_9_3")
