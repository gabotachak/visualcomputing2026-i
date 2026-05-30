#!/usr/bin/env python3
"""Semana 13_2: Interactive satellite maps simulation."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate a satellite-like raster image (false-color composite)
H, W = 400, 600

def make_landsat_sim():
    """Generate a synthetic Landsat-like image with land, water, urban areas."""
    # RGB channels for false color
    r = np.zeros((H, W)); g = np.zeros((H, W)); b = np.zeros((H, W))
    # Water body (blue)
    r[100:250, 50:200] = 0.1; g[100:250, 50:200] = 0.3; b[100:250, 50:200] = 0.8
    # Forest (dark green in NIR = bright in near-IR channel -> red in false color)
    r[50:180, 280:500] = 0.7; g[50:180, 280:500] = 0.4; b[50:180, 280:500] = 0.2
    # Urban (gray)
    r[280:380, 100:380] = 0.6; g[280:380, 100:380] = 0.55; b[280:380, 100:380] = 0.5
    # Agricultural (lighter green)
    r[200:320, 400:580] = 0.4; g[200:320, 400:580] = 0.7; b[200:320, 400:580] = 0.3
    # Bare soil (brown)
    r[300:400, 450:600] = 0.65; g[300:400, 450:600] = 0.45; b[300:400, 450:600] = 0.25
    # Base terrain noise
    noise = np.random.rand(H, W, 3) * 0.05
    img = np.stack([r, g, b], axis=2) + noise
    img = np.clip(img + np.random.randn(H, W, 1) * 0.02, 0, 1)
    return img

img = make_landsat_sim()
gray = np.dot(img, [0.299, 0.587, 0.114])

# NDVI simulation (NIR - RED) / (NIR + RED)
nir = img[:,:,0]  # Using R as NIR proxy for simulation
red = img[:,:,2]  # Using B as RED proxy
ndvi = (nir - red) / (nir + red + 1e-8)
ndvi = np.clip(ndvi, -1, 1)

# K-means segmentation (simplified)
from sklearn.cluster import KMeans
pixels = img.reshape(-1, 3)
km = KMeans(n_clusters=5, random_state=42, n_init=10)
labels = km.fit_predict(pixels).reshape(H, W)
LAND_COLORS = ['#4af', '#4e4', '#888', '#f84', '#a8a']
LAND_NAMES = ['Agua', 'Vegetación', 'Urbano', 'Suelo', 'Otro']

LAND_RGB = [[0.3,0.6,1.0],[0.3,0.9,0.3],[0.6,0.6,0.6],[1.0,0.6,0.3],[0.7,0.5,0.7]]
colored_seg = np.zeros((H, W, 3))
for i, rgb in enumerate(LAND_RGB):
    colored_seg[labels==i] = rgb

# Plot 1: Satellite image analysis
fig, axes = plt.subplots(2, 3, figsize=(15, 9), facecolor='#0a0a1a')
fig.suptitle('Mapas Interactivos con Datos Satelitales — Análisis Multiespectral', color='white', fontsize=13, fontweight='bold')

images_data = [
    (img, 'Composición RGB (simulado Landsat)', None),
    (gray, 'Banda panchromática', 'gray'),
    (ndvi, 'NDVI (índice vegetación)', 'RdYlGn'),
    (img[:,:,0], 'Banda NIR (falso color)', 'Reds'),
    (colored_seg, 'Clasificación k-means (5 clases)', None),
    (np.abs(ndvi) > 0.3, 'Máscara vegetación (NDVI>0.3)', 'Greens'),
]

for ax, (image, title, cmap) in zip(axes.flatten(), images_data):
    ax.set_facecolor('#0d0d2a')
    ax.imshow(image, cmap=cmap)
    ax.set_title(title, color='white', fontsize=9)
    ax.axis('off')
    if cmap == 'RdYlGn':
        plt.colorbar(ax.images[0], ax=ax, shrink=0.8)

plt.tight_layout()
fig.savefig('../media/satellite_map_analysis.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: satellite_map_analysis.png")

# Plot 2: Land use statistics
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
fig2.suptitle('Estadísticas de Uso de Suelo — Clasificación Satelital', color='white', fontsize=12, fontweight='bold')
for ax in axes2:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

# Class distribution
class_counts = [(labels==i).sum() for i in range(5)]
total = sum(class_counts)
pcts = [c/total*100 for c in class_counts]
bar_colors2 = ['#4af', '#4e4', '#888', '#f84', '#a8a']
axes2[0].bar(LAND_NAMES, pcts, color=bar_colors2, alpha=0.85)
axes2[0].set_ylabel('Cobertura (%)', color='gray')
axes2[0].set_title('Distribución de clases de uso de suelo', color='white')
for i, (n, p) in enumerate(zip(LAND_NAMES, pcts)):
    axes2[0].text(i, p+0.3, f'{p:.1f}%', ha='center', color='white', fontsize=10)

# NDVI histogram
axes2[1].hist(ndvi.flatten(), bins=60, color='#4e4', alpha=0.8, edgecolor='none')
axes2[1].axvline(0, color='white', linestyle='--', linewidth=1, label='NDVI=0')
axes2[1].axvline(0.3, color='yellow', linestyle='--', linewidth=1, label='Umbral vegetación')
axes2[1].set_xlabel('NDVI', color='gray'); axes2[1].set_ylabel('Frecuencia', color='gray')
axes2[1].set_title('Distribución NDVI', color='white')
axes2[1].legend(facecolor='#0d0d2a', labelcolor='white')

plt.tight_layout()
fig2.savefig('../media/satellite_land_use_stats.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: satellite_land_use_stats.png")
print("All media generated for semana_13_2")
