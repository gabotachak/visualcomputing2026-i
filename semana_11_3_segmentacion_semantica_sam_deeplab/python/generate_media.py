#!/usr/bin/env python3
"""Semana 11_3: Semantic segmentation simulation (SAM/DeepLab)."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate a semantic segmentation result
# Categories: background=0, person=1, car=2, chair=3, plant=4, sky=5
CATEGORIES = ['background', 'person', 'car', 'chair', 'plant', 'sky']
COLORS_SEG = [
    [20, 20, 30],    # background
    [200, 100, 80],  # person
    [80, 120, 200],  # car
    [200, 180, 80],  # chair
    [80, 200, 80],   # plant
    [120, 160, 220], # sky
]

# Create a synthetic segmentation map
h, w = 400, 600
seg_map = np.zeros((h, w), dtype=np.uint8)

# Sky background (top third)
seg_map[:h//3, :] = 5
# Background mid
seg_map[h//3:, :] = 0
# Person
cv2.ellipse(seg_map, (150, 220), (50, 90), 0, 0, 360, 1, -1)  # body
cv2.ellipse(seg_map, (150, 110), (35, 40), 0, 0, 360, 1, -1)  # head
# Car
cv2.rectangle(seg_map, (320, 220), (540, 360), 2, -1)
cv2.ellipse(seg_map, (360, 360), (35, 15), 0, 0, 360, 2, -1)  # wheel
cv2.ellipse(seg_map, (500, 360), (35, 15), 0, 0, 360, 2, -1)
# Chair
cv2.rectangle(seg_map, (50, 280), (120, 390), 3, -1)
cv2.rectangle(seg_map, (50, 220), (120, 290), 3, -1)  # back
# Plant
cv2.ellipse(seg_map, (260, 250), (45, 60), 0, 0, 360, 4, -1)
cv2.rectangle(seg_map, (255, 305), (265, 380), 4, -1)  # stem

# Apply slight blur for realistic edges
seg_map_smooth = seg_map.copy()

# Colorize segmentation
def colorize_seg(seg, colors):
    colored = np.zeros((*seg.shape, 3), dtype=np.uint8)
    for cls_id, color in enumerate(colors):
        colored[seg == cls_id] = color
    return colored

colored_seg = colorize_seg(seg_map, COLORS_SEG)

# Create a "scene" image from the segmentation
scene = colored_seg.copy().astype(np.float32)
noise = np.random.randn(*scene.shape) * 15
scene = np.clip(scene + noise, 0, 255).astype(np.uint8)
scene = cv2.GaussianBlur(scene, (3, 3), 0)

# Overlay: 50% blend
overlay = cv2.addWeighted(scene, 0.5, colored_seg, 0.5, 0)

# Compute per-class stats
class_stats = []
for cls_id, name in enumerate(CATEGORIES):
    area = np.sum(seg_map == cls_id)
    pct = area / (h * w) * 100
    class_stats.append((name, area, pct))

# Plot 1: Segmentation pipeline
fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='#0a0a1a')
fig.suptitle('Segmentación Semántica — SAM/DeepLabV3 (Simulado)', color='white', fontsize=13, fontweight='bold')

axes[0].imshow(scene)
axes[0].set_title('Imagen de entrada', color='white')
axes[0].axis('off')

axes[1].imshow(colored_seg)
axes[1].set_title('Mapa de segmentación', color='white')
axes[1].axis('off')

# Add legend patches
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=np.array(c)/255, label=n)
                   for n, c in zip(CATEGORIES, COLORS_SEG)]
axes[1].legend(handles=legend_elements, loc='lower right', fontsize=7,
               facecolor='#0a0a1a', labelcolor='white', framealpha=0.8)

axes[2].imshow(overlay)
axes[2].set_title('Overlay (50% blend)', color='white')
axes[2].axis('off')

for ax in axes:
    ax.set_facecolor('#0d0d2a')

plt.tight_layout()
fig.savefig('../media/semantic_segmentation_result.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: semantic_segmentation_result.png")

# Plot 2: Per-class metrics
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
fig2.suptitle('Métricas de Segmentación por Clase', color='white', fontsize=12, fontweight='bold')

for ax in axes2:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

names, areas, pcts = zip(*class_stats)
bar_colors = [np.array(c)/255 for c in COLORS_SEG]
axes2[0].bar(names, pcts, color=bar_colors, alpha=0.85)
axes2[0].set_ylabel('Cobertura (%)', color='gray')
axes2[0].set_title('Área por clase (% de imagen)', color='white')
axes2[0].tick_params(axis='x', rotation=30)
for i, (n, p) in enumerate(zip(names, pcts)):
    axes2[0].text(i, p+0.3, f'{p:.1f}%', ha='center', color='white', fontsize=9)

# IoU scores (simulated)
iou_scores = [0.0, 0.87, 0.82, 0.75, 0.88, 0.91]
axes2[1].bar(names, iou_scores, color=bar_colors, alpha=0.85)
axes2[1].axhline(0.75, color='yellow', linestyle='--', linewidth=1.5, label='Umbral IoU=0.75')
axes2[1].set_ylabel('IoU Score', color='gray')
axes2[1].set_title('IoU por clase (simulado)', color='white')
axes2[1].set_ylim(0, 1.1)
axes2[1].tick_params(axis='x', rotation=30)
axes2[1].legend(facecolor='#0d0d2a', labelcolor='white')
for i, (n, s) in enumerate(zip(names, iou_scores)):
    if s > 0:
        axes2[1].text(i, s+0.02, f'{s:.2f}', ha='center', color='white', fontsize=9)

plt.tight_layout()
fig2.savefig('../media/segmentation_class_metrics.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: segmentation_class_metrics.png")
print("All media generated for semana_11_3")
