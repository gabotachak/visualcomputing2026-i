#!/usr/bin/env python3
"""Semana 13_4: Stereo 3D reconstruction from simulated satellite images."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

H, W = 300, 400

def make_stereo_pair():
    """Create left and right stereo images of a synthetic terrain."""
    # Height map (DEM simulation)
    x = np.linspace(0, 4*np.pi, W)
    y = np.linspace(0, 4*np.pi, H)
    X, Y = np.meshgrid(x, y)
    height = np.sin(X*0.5)*np.cos(Y*0.5)*30 + np.random.randn(H, W)*2

    # Render left image (gray with shading from height)
    grad_x = np.gradient(height, axis=1)
    grad_y = np.gradient(height, axis=0)
    normal_z = 1 / np.sqrt(1 + grad_x**2 + grad_y**2)
    left = np.clip(normal_z * 200 + 30, 0, 255).astype(np.uint8)

    # Right image: shift horizontally by disparity proportional to height
    disparity_true = (height - height.min()) / (height.max() - height.min()) * 30
    right = np.zeros_like(left)
    for row in range(H):
        for col in range(W):
            d = int(disparity_true[row, col])
            if col + d < W:
                right[row, col] = left[row, min(col+d, W-1)]

    return left, right, height, disparity_true

left_img, right_img, dem_true, disp_true = make_stereo_pair()

# Compute disparity with StereoBM
stereo = cv2.StereoBM_create(numDisparities=32, blockSize=15)
disparity = stereo.compute(left_img, right_img).astype(np.float32) / 16.0
disparity[disparity < 0] = 0

# Reconstruct 3D points (simplified projection)
focal = 300.0
baseline = 1.0
depth = np.where(disparity > 0, focal * baseline / (disparity + 1e-8), 0)

# Plot 1: Stereo pipeline
fig, axes = plt.subplots(2, 3, figsize=(15, 9), facecolor='#0a0a1a')
fig.suptitle('Reconstrucción 3D Estéreo Satelital — Visión Binocular', color='white', fontsize=13, fontweight='bold')

images_data = [
    (left_img, 'Imagen izquierda (vista L)', 'gray'),
    (right_img, 'Imagen derecha (vista R)', 'gray'),
    (np.abs(left_img.astype(int) - right_img.astype(int)).astype(np.uint8), 'Diferencia L-R', 'hot'),
    (disp_true, 'Disparidad real (ground truth)', 'plasma'),
    (disparity, 'Disparidad estimada (StereoBM)', 'plasma'),
    (depth, 'Mapa de profundidad estimado', 'jet'),
]

for ax, (img, title, cmap) in zip(axes.flatten(), images_data):
    ax.set_facecolor('#0d0d2a')
    ax.imshow(img, cmap=cmap)
    ax.set_title(title, color='white', fontsize=9)
    ax.axis('off')

plt.tight_layout()
fig.savefig('../media/stereo_reconstruction_pipeline.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: stereo_reconstruction_pipeline.png")

# Plot 2: 3D terrain visualization
fig2 = plt.figure(figsize=(14, 6), facecolor='#0a0a1a')
fig2.suptitle('Reconstrucción 3D del Terreno — DEM Simulado', color='white', fontsize=12, fontweight='bold')

ax3d = fig2.add_subplot(121, projection='3d')
ax3d.set_facecolor('#0d0d2a')
xx = np.linspace(0, 1, W//4)
yy = np.linspace(0, 1, H//4)
XX, YY = np.meshgrid(xx, yy)
ZZ = dem_true[::4, ::4]
surf = ax3d.plot_surface(XX, YY, ZZ, cmap='terrain', alpha=0.9)
ax3d.set_title('DEM Real (ground truth)', color='white')
ax3d.tick_params(colors='gray', labelsize=7)
fig2.colorbar(surf, ax=ax3d, shrink=0.6)

ax_depth = fig2.add_subplot(122)
ax_depth.set_facecolor('#0d0d2a')
ax_depth.tick_params(colors='gray')
for spine in ax_depth.spines.values(): spine.set_color('#333')
ax_depth.plot(depth[H//2, :], color='#4af', linewidth=2, label='Profundidad estimada')
ax_depth.plot(disp_true[H//2, :] * 10, color='#4e4', linewidth=2, linestyle='--', label='Disparidad real ×10')
ax_depth.set_xlabel('Columna', color='gray'); ax_depth.set_ylabel('Profundidad (u.a.)', color='gray')
ax_depth.set_title('Perfil de profundidad (fila central)', color='white')
ax_depth.legend(facecolor='#0d0d2a', labelcolor='white')

plt.tight_layout()
fig2.savefig('../media/stereo_3d_terrain.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: stereo_3d_terrain.png")
print("All media generated for semana_13_4")
