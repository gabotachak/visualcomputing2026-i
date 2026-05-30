#!/usr/bin/env python3
"""Semana 13_3: Mini satellite radar - k-means color segmentation."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import os
os.makedirs('../media', exist_ok=True)
np.random.seed(42)

H, W = 400, 500

def make_aerial_image():
    img = np.zeros((H, W, 3), dtype=np.uint8)
    # Water
    img[50:180, 20:180] = [30, 80, 180]
    # Forest
    img[20:200, 250:450] = [30, 100, 40]
    # Urban
    img[220:380, 60:320] = [130, 120, 110]
    # Agricultural
    img[200:380, 350:490] = [90, 150, 60]
    # Bare soil
    img[300:400, 20:100] = [160, 130, 80]
    noise = np.random.randint(-15, 15, (H, W, 3), dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    return img

img = make_aerial_image()
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# K-means segmentation
for k in [3, 5]:
    pixels = img_rgb.reshape(-1, 3).astype(np.float32)
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(pixels).reshape(H, W)
    centers = km.cluster_centers_.astype(np.uint8)
    segmented = centers[labels]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5), facecolor='#0a0a1a')
    fig.suptitle(f'Mini Radar Satelital — Segmentación K-Means (k={k})', color='white', fontsize=13, fontweight='bold')

    axes[0].imshow(img_rgb); axes[0].set_title('Imagen satelital original', color='white'); axes[0].axis('off')
    axes[1].imshow(segmented); axes[1].set_title(f'Segmentación k-means (k={k})', color='white'); axes[1].axis('off')
    axes[2].imshow(labels, cmap='tab10', vmin=0, vmax=9); axes[2].set_title('Mapa de clases', color='white'); axes[2].axis('off')

    for ax in axes:
        ax.set_facecolor('#0d0d2a')

    plt.tight_layout()
    fig.savefig(f'../media/radar_kmeans_k{k}.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"Saved: radar_kmeans_k{k}.png")

# Color threshold segmentation (HSV)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
water_mask = cv2.inRange(hsv, (100, 50, 30), (130, 255, 255))
vegetation_mask = cv2.inRange(hsv, (35, 30, 30), (85, 255, 200))

fig2, axes2 = plt.subplots(1, 3, figsize=(14, 5), facecolor='#0a0a1a')
fig2.suptitle('Segmentación por Umbral de Color HSV — Agua y Vegetación', color='white', fontsize=12, fontweight='bold')
axes2[0].imshow(img_rgb); axes2[0].set_title('Original', color='white'); axes2[0].axis('off')
axes2[1].imshow(water_mask, cmap='Blues'); axes2[1].set_title('Máscara Agua (HSV)', color='white'); axes2[1].axis('off')
axes2[2].imshow(vegetation_mask, cmap='Greens'); axes2[2].set_title('Máscara Vegetación (HSV)', color='white'); axes2[2].axis('off')
for ax in axes2:
    ax.set_facecolor('#0d0d2a')
plt.tight_layout()
fig2.savefig('../media/radar_color_masks.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: radar_color_masks.png")
print("All media generated for semana_13_3")
