#!/usr/bin/env python3
"""Semana 13_5: NeRF, Gaussian Splats and SLAM comparison simulation."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate Gaussian Splatting point cloud
n_gaussians = 500
positions = np.random.randn(n_gaussians, 3) * 2
colors = np.random.rand(n_gaussians, 3)
scales = np.abs(np.random.randn(n_gaussians)) * 0.1 + 0.05

# Simulate NeRF volume rendering rays
n_rays = 200
ray_origins = np.random.randn(n_rays, 3) * 0.5
ray_dirs = -ray_origins / np.linalg.norm(ray_origins, axis=1, keepdims=True)
ray_colors = np.random.rand(n_rays, 3)

# Simulate SLAM trajectory + map
t = np.linspace(0, 4*np.pi, 100)
slam_trajectory = np.column_stack([3*np.cos(t), 3*np.sin(t), 0.5*t])
slam_map_pts = np.random.randn(300, 3) * 1.5
slam_map_pts[:, 2] = np.abs(slam_map_pts[:, 2]) * 0.3

# Plot 1: 3D comparison of three approaches
fig = plt.figure(figsize=(16, 6), facecolor='#0a0a1a')
fig.suptitle('Reconstrucción 3D: Gaussian Splats vs NeRF vs SLAM — Comparación', color='white', fontsize=13, fontweight='bold')

ax1 = fig.add_subplot(131, projection='3d')
ax1.scatter(positions[:,0], positions[:,1], positions[:,2], c=colors, s=scales*200, alpha=0.7)
ax1.set_title('Gaussian Splatting\n(nube de gaussianas 3D)', color='white', fontsize=10)
ax1.set_facecolor('#0d0d2a')
ax1.tick_params(colors='gray', labelsize=6)

ax2 = fig.add_subplot(132, projection='3d')
for i in range(0, n_rays, 5):
    ts = np.linspace(0, 3, 20)
    pts = ray_origins[i] + np.outer(ts, ray_dirs[i])
    ax2.plot(pts[:,0], pts[:,1], pts[:,2], color=ray_colors[i], alpha=0.4, linewidth=0.5)
ax2.set_title('NeRF\n(ray marching en volumen implícito)', color='white', fontsize=10)
ax2.set_facecolor('#0d0d2a')
ax2.tick_params(colors='gray', labelsize=6)

ax3 = fig.add_subplot(133, projection='3d')
ax3.scatter(slam_map_pts[:,0], slam_map_pts[:,1], slam_map_pts[:,2], c='#4af', s=5, alpha=0.5, label='Mapa 3D')
ax3.plot(slam_trajectory[:,0], slam_trajectory[:,1], slam_trajectory[:,2], color='#f84', linewidth=2, label='Trayectoria')
ax3.set_title('Visual SLAM\n(mapa + trayectoria)', color='white', fontsize=10)
ax3.set_facecolor('#0d0d2a')
ax3.tick_params(colors='gray', labelsize=6)
ax3.legend(facecolor='#0d0d2a', labelcolor='white', fontsize=7)

plt.tight_layout()
fig.savefig('../media/nerf_slam_gaussian_comparison.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: nerf_slam_gaussian_comparison.png")

# Plot 2: Comparison table
fig2, ax2 = plt.subplots(figsize=(13, 6), facecolor='#0a0a1a')
ax2.set_facecolor('#0d0d2a')
ax2.axis('off')
ax2.set_title('Comparación: NeRF vs Gaussian Splats vs SLAM', color='white', fontsize=13, fontweight='bold')

metrics = [
    ['Métrica', 'NeRF', 'Gaussian Splatting', 'Visual SLAM'],
    ['Representación', 'Volumen implícito\n(MLP)', 'Nube de gaussianas\n3D explícitas', 'Mapa de puntos\n+ pose'],
    ['Calidad visual', '★★★★★', '★★★★★', '★★★☆☆'],
    ['Velocidad entrenamiento', '★★☆☆☆\n(horas)', '★★★★☆\n(minutos)', '★★★★★\n(tiempo real)'],
    ['Velocidad inferencia', '★★★☆☆\n(~30s/img)', '★★★★★\n(>100 FPS)', '★★★★★\n(tiempo real)'],
    ['Edición de escena', 'Difícil', 'Moderada', 'Sí'],
    ['VRAM requerida', '8-16 GB', '4-8 GB', '1-4 GB'],
    ['Aplicación', 'Síntesis de vistas\nnovedosas', 'AR/VR rendering\nen tiempo real', 'Navegación robótica\ny mapping'],
]

table = ax2.table(cellText=metrics[1:], colLabels=metrics[0], cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.5)
for (r, c), cell in table.get_celld().items():
    cell.set_facecolor('#2a2a5e' if r == 0 else ('#1e3a5e' if c == 0 else '#1a1a3e' if r % 2 == 0 else '#141430'))
    cell.set_text_props(color='white')
    cell.set_edgecolor('#444')

plt.tight_layout()
fig2.savefig('../media/reconstruction_methods_comparison.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: reconstruction_methods_comparison.png")
print("All media generated for semana_13_5")
