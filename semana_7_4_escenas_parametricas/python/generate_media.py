#!/usr/bin/env python3
"""Generate media for semana_7_4 parametric scenes (Python side)."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Plot 1: Parametric 3D scene - objects from coordinate data
fig = plt.figure(figsize=(12, 5), facecolor='#0a0a1a')
fig.suptitle('Escenas Paramétricas — Objetos 3D desde Datos', color='white', fontsize=13, fontweight='bold')

ax1 = fig.add_subplot(121, projection='3d', facecolor='#0d0d2a')
ax2 = fig.add_subplot(122, projection='3d', facecolor='#0d0d2a')

# Dataset 1: Spiral galaxy of spheres
n = 60
angles = np.linspace(0, 4 * np.pi, n)
radii = np.linspace(0.1, 5, n)
xs = radii * np.cos(angles)
ys = radii * np.sin(angles)
zs = np.sin(radii * 0.5) * 2
sizes = 20 + radii * 15
hues = np.linspace(0, 1, n)
colors = plt.cm.hsv(hues)

ax1.scatter(xs, ys, zs, c=colors, s=sizes, alpha=0.8, depthshade=True)
ax1.set_facecolor('#0d0d2a')
ax1.tick_params(colors='gray', labelsize=7)
ax1.set_title('Espiral Galáctica\n(60 objetos paramétricos)', color='white', fontsize=10)
ax1.set_xlabel('X', color='gray', fontsize=8)
ax1.set_ylabel('Y', color='gray', fontsize=8)
ax1.set_zlabel('Z', color='gray', fontsize=8)
for pane in [ax1.xaxis.pane, ax1.yaxis.pane, ax1.zaxis.pane]:
    pane.fill = False
    pane.set_edgecolor('#333')

# Dataset 2: Grid of parametric cubes with varied scale/color
grid_n = 5
for i in range(grid_n):
    for j in range(grid_n):
        x, y = i * 2 - 4, j * 2 - 4
        z = np.sin(i * 0.7) * np.cos(j * 0.7) * 2
        size = abs(z) * 20 + 10
        color = plt.cm.cool((i + j) / (2 * grid_n))
        ax2.scatter([x], [y], [z], c=[color], s=[size * 8], alpha=0.8)

ax2.set_facecolor('#0d0d2a')
ax2.tick_params(colors='gray', labelsize=7)
ax2.set_title('Grid Paramétrico 5×5\n(altura = f(x,y))', color='white', fontsize=10)
ax2.set_xlabel('X', color='gray', fontsize=8)
ax2.set_ylabel('Y', color='gray', fontsize=8)
ax2.set_zlabel('Z', color='gray', fontsize=8)
for pane in [ax2.xaxis.pane, ax2.yaxis.pane, ax2.zaxis.pane]:
    pane.fill = False
    pane.set_edgecolor('#333')

plt.tight_layout()
fig.savefig('../media/python_parametric_3d.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: python_parametric_3d.png")

# Plot 2: Parametric scene from CSV-like data
data = {
    'x': [0, 2, -2, 1, -1, 3, -3, 0, 2, -2],
    'y': [0, 1, 1, -1, -1, 0, 0, 2, -2, 0],
    'z': [0, 1, -1, 2, -2, 0.5, -0.5, 1, 1, -1],
    'size': [100, 80, 60, 120, 70, 90, 110, 85, 75, 95],
    'shape': ['cube', 'sphere', 'cylinder', 'cube', 'sphere', 'cylinder', 'cube', 'sphere', 'cylinder', 'cube'],
}

colors_map = {'cube': '#e44', 'sphere': '#4e4', 'cylinder': '#44e'}
shape_markers = {'cube': 's', 'sphere': 'o', 'cylinder': '^'}

fig2 = plt.figure(figsize=(10, 5), facecolor='#0a0a1a')
fig2.suptitle('Generación desde Datos Estructurados (tipo CSV)', color='white', fontsize=12, fontweight='bold')

ax3 = fig2.add_subplot(121, projection='3d', facecolor='#0d0d2a')
for shape in ['cube', 'sphere', 'cylinder']:
    mask = [s == shape for s in data['shape']]
    xs = [data['x'][i] for i, m in enumerate(mask) if m]
    ys = [data['y'][i] for i, m in enumerate(mask) if m]
    zs = [data['z'][i] for i, m in enumerate(mask) if m]
    ss = [data['size'][i] for i, m in enumerate(mask) if m]
    ax3.scatter(xs, ys, zs, c=colors_map[shape], s=ss, marker=shape_markers[shape],
                label=shape, alpha=0.9, depthshade=False)

ax3.set_facecolor('#0d0d2a')
ax3.tick_params(colors='gray', labelsize=7)
ax3.set_title('Objetos por tipo\n(cubo/esfera/cilindro)', color='white', fontsize=10)
ax3.legend(facecolor='#0d0d2a', labelcolor='white', fontsize=8)
for pane in [ax3.xaxis.pane, ax3.yaxis.pane, ax3.zaxis.pane]:
    pane.fill = False; pane.set_edgecolor('#333')

ax4 = fig2.add_subplot(122, facecolor='#0d0d2a')
ax4.tick_params(colors='gray')
for spine in ax4.spines.values(): spine.set_color('#333')
shape_counts = {s: data['shape'].count(s) for s in ['cube', 'sphere', 'cylinder']}
ax4.bar(shape_counts.keys(), shape_counts.values(),
        color=[colors_map[s] for s in shape_counts], alpha=0.8)
ax4.set_ylabel('Cantidad', color='gray')
ax4.set_title('Distribución de objetos\npor tipo', color='white', fontsize=10)

plt.tight_layout()
fig2.savefig('../media/python_parametric_from_data.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: python_parametric_from_data.png")
print("All media generated for semana_7_4")
