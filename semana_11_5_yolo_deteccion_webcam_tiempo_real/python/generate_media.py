#!/usr/bin/env python3
"""Semana 11_5: YOLO real-time detection — performance benchmark simulation."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate YOLOv8 model comparison: nano, small, medium
MODELS = {
    'YOLOv8n\n(nano)':   {'fps': 85, 'map50': 0.372, 'params': 3.2, 'color': '#4e4'},
    'YOLOv8s\n(small)':  {'fps': 55, 'map50': 0.448, 'params': 11.2, 'color': '#4af'},
    'YOLOv8m\n(medium)': {'fps': 32, 'map50': 0.502, 'params': 25.9, 'color': '#f84'},
}
N_FRAMES = 200

# Simulate FPS over time for each model
t = np.arange(N_FRAMES)
fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor='#0a0a1a')
fig.suptitle('YOLO Real-Time Benchmark — Nano vs Small vs Medium (Simulado)', color='white', fontsize=13, fontweight='bold')

for ax in axes.flatten():
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

# FPS time series
for name, info in MODELS.items():
    base_fps = info['fps']
    fps_series = base_fps + np.random.randn(N_FRAMES) * (base_fps * 0.05) + 3 * np.sin(t * 0.1)
    fps_series = np.clip(fps_series, base_fps * 0.7, base_fps * 1.2)
    axes[0][0].plot(t, fps_series, color=info['color'], linewidth=1.5, label=name.replace('\n',' '), alpha=0.9)

axes[0][0].axhline(30, color='yellow', linestyle='--', linewidth=1, label='Target 30 FPS')
axes[0][0].set_title('FPS en tiempo real por modelo', color='white')
axes[0][0].set_xlabel('Frame', color='gray')
axes[0][0].set_ylabel('FPS', color='gray')
axes[0][0].legend(facecolor='#0d0d2a', labelcolor='white', fontsize=9)

# Bar: avg FPS comparison
names_short = [n.replace('\n', ' ') for n in MODELS.keys()]
fps_vals = [info['fps'] for info in MODELS.values()]
colors_b = [info['color'] for info in MODELS.values()]
bars = axes[0][1].bar(names_short, fps_vals, color=colors_b, alpha=0.85)
axes[0][1].axhline(30, color='yellow', linestyle='--', linewidth=1, label='Target 30 FPS')
axes[0][1].set_title('FPS promedio por modelo', color='white')
axes[0][1].set_ylabel('FPS', color='gray')
axes[0][1].legend(facecolor='#0d0d2a', labelcolor='white')
for bar, v in zip(bars, fps_vals):
    axes[0][1].text(bar.get_x()+bar.get_width()/2, v+1, str(v), ha='center', color='white')

# Scatter: FPS vs mAP trade-off
for name, info in MODELS.items():
    axes[1][0].scatter(info['fps'], info['map50'], c=info['color'], s=info['params']*10,
                       alpha=0.9, edgecolors='white', linewidth=1.5, zorder=5)
    axes[1][0].annotate(name.replace('\n', ' '), (info['fps'], info['map50']),
                        textcoords='offset points', xytext=(5, 5), color=info['color'], fontsize=9)
axes[1][0].set_title('Trade-off: Velocidad vs Precisión\n(tamaño = parámetros)', color='white')
axes[1][0].set_xlabel('FPS promedio', color='gray')
axes[1][0].set_ylabel('mAP@0.5 (COCO)', color='gray')

# Object count histogram over frames (simulated)
object_counts = np.random.poisson(3.5, N_FRAMES)
conf_threshold = 0.5
axes[1][1].hist(object_counts, bins=range(0, 12), color='#4af', alpha=0.8, edgecolor='white')
axes[1][1].axvline(object_counts.mean(), color='yellow', linestyle='--', linewidth=1.5,
                   label=f'Media: {object_counts.mean():.1f}')
axes[1][1].set_title(f'Distribución de objetos detectados\n(conf≥{conf_threshold}, {N_FRAMES} frames)', color='white')
axes[1][1].set_xlabel('Objetos por frame', color='gray')
axes[1][1].set_ylabel('Frecuencia', color='gray')
axes[1][1].legend(facecolor='#0d0d2a', labelcolor='white')

plt.tight_layout()
fig.savefig('../media/yolo_realtime_benchmark.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: yolo_realtime_benchmark.png")

# Plot 2: Confidence threshold analysis
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
fig2.suptitle('Análisis de Umbral de Confianza YOLO', color='white', fontsize=12, fontweight='bold')

for ax in axes2:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

thresholds = np.arange(0.1, 0.95, 0.05)
detections_per_frame = 8 * (1 - thresholds)**1.5 + np.random.randn(len(thresholds)) * 0.2
precision_vs_thresh = 0.4 + 0.55 * thresholds + np.random.randn(len(thresholds)) * 0.02
recall_vs_thresh = 1 - 0.7 * thresholds**0.8 + np.random.randn(len(thresholds)) * 0.02

axes2[0].plot(thresholds, detections_per_frame, color='#4af', linewidth=2, marker='o', markersize=4)
axes2[0].axvline(0.5, color='yellow', linestyle='--', linewidth=1, label='conf=0.5 (default)')
axes2[0].set_xlabel('Umbral de confianza', color='gray')
axes2[0].set_ylabel('Detecciones / frame', color='gray')
axes2[0].set_title('Detecciones vs umbral de confianza', color='white')
axes2[0].legend(facecolor='#0d0d2a', labelcolor='white')

axes2[1].plot(thresholds, precision_vs_thresh, color='#4af', linewidth=2, label='Precision')
axes2[1].plot(thresholds, recall_vs_thresh, color='#a4e', linewidth=2, label='Recall')
axes2[1].axvline(0.5, color='yellow', linestyle='--', linewidth=1, label='conf=0.5')
axes2[1].set_xlabel('Umbral de confianza', color='gray')
axes2[1].set_ylabel('Score', color='gray')
axes2[1].set_title('Precision/Recall vs umbral', color='white')
axes2[1].legend(facecolor='#0d0d2a', labelcolor='white')
axes2[1].set_ylim(0, 1.1)

plt.tight_layout()
fig2.savefig('../media/yolo_confidence_analysis.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: yolo_confidence_analysis.png")
print("All media generated for semana_11_5")
