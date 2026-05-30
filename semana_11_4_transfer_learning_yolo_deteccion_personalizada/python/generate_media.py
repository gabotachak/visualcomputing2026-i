#!/usr/bin/env python3
"""Semana 11_4: Transfer learning YOLO simulation — training curves + evaluation."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate training curves for YOLOv8 fine-tuning
epochs = np.arange(1, 51)

# Loss curves
train_box_loss = 2.5 * np.exp(-epochs * 0.08) + 0.3 + np.random.randn(50) * 0.04
val_box_loss = 2.8 * np.exp(-epochs * 0.07) + 0.35 + np.random.randn(50) * 0.06
train_cls_loss = 1.8 * np.exp(-epochs * 0.1) + 0.2 + np.random.randn(50) * 0.03
val_cls_loss = 2.0 * np.exp(-epochs * 0.09) + 0.25 + np.random.randn(50) * 0.05

# mAP curves
map50 = 1 - 0.75 * np.exp(-epochs * 0.09) + np.random.randn(50) * 0.01
map50_95 = 1 - 0.8 * np.exp(-epochs * 0.08) + np.random.randn(50) * 0.01
map50 = np.clip(map50, 0, 0.98)
map50_95 = np.clip(map50_95, 0, 0.85)

# Precision / Recall
precision = 1 - 0.4 * np.exp(-epochs * 0.1) + np.random.randn(50) * 0.01
recall = 1 - 0.5 * np.exp(-epochs * 0.08) + np.random.randn(50) * 0.01
precision = np.clip(precision, 0, 0.98)
recall = np.clip(recall, 0, 0.97)

# Plot 1: Training curves
fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor='#0a0a1a')
fig.suptitle('Transfer Learning YOLOv8 — Curvas de Entrenamiento (50 épocas)', color='white', fontsize=13, fontweight='bold')

for ax in axes.flatten():
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

axes[0][0].plot(epochs, train_box_loss, color='#4af', linewidth=2, label='Train')
axes[0][0].plot(epochs, val_box_loss, color='#f84', linewidth=2, label='Val', linestyle='--')
axes[0][0].set_title('Box Loss', color='white')
axes[0][0].set_ylabel('Loss', color='gray')
axes[0][0].legend(facecolor='#0d0d2a', labelcolor='white')

axes[0][1].plot(epochs, train_cls_loss, color='#4af', linewidth=2, label='Train')
axes[0][1].plot(epochs, val_cls_loss, color='#f84', linewidth=2, label='Val', linestyle='--')
axes[0][1].set_title('Classification Loss', color='white')
axes[0][1].set_ylabel('Loss', color='gray')
axes[0][1].legend(facecolor='#0d0d2a', labelcolor='white')

axes[1][0].plot(epochs, map50, color='#4e4', linewidth=2, label='mAP@0.5')
axes[1][0].plot(epochs, map50_95, color='#4af', linewidth=2, label='mAP@0.5:0.95')
axes[1][0].axhline(0.60, color='yellow', linestyle=':', linewidth=1, label='Target mAP=0.60')
axes[1][0].set_title('mAP', color='white')
axes[1][0].set_ylabel('mAP', color='gray')
axes[1][0].set_xlabel('Época', color='gray')
axes[1][0].legend(facecolor='#0d0d2a', labelcolor='white')
axes[1][0].set_ylim(0, 1.05)

axes[1][1].plot(epochs, precision, color='#4af', linewidth=2, label='Precision')
axes[1][1].plot(epochs, recall, color='#a4e', linewidth=2, label='Recall')
axes[1][1].set_title('Precision / Recall', color='white')
axes[1][1].set_ylabel('Score', color='gray')
axes[1][1].set_xlabel('Época', color='gray')
axes[1][1].legend(facecolor='#0d0d2a', labelcolor='white')
axes[1][1].set_ylim(0, 1.05)

plt.tight_layout()
fig.savefig('../media/yolo_training_curves.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: yolo_training_curves.png")

# Plot 2: Confusion matrix + final metrics
fig2, axes2 = plt.subplots(1, 2, figsize=(13, 6), facecolor='#0a0a1a')
fig2.suptitle('Evaluación Final — Detección Personalizada con Transfer Learning', color='white', fontsize=12, fontweight='bold')

# Simulated confusion matrix (5 custom classes)
CUSTOM_CLASSES = ['helmet', 'vest', 'glove', 'boot', 'background']
conf_matrix = np.array([
    [87, 3, 2, 0, 8],
    [4, 91, 1, 2, 2],
    [3, 2, 85, 4, 6],
    [1, 3, 5, 88, 3],
    [5, 2, 3, 2, 88],
])
# Normalize
conf_matrix_norm = conf_matrix / conf_matrix.sum(axis=1, keepdims=True)

ax_cm = axes2[0]
ax_cm.set_facecolor('#0d0d2a')
im = ax_cm.imshow(conf_matrix_norm, cmap='Blues', vmin=0, vmax=1)
ax_cm.set_xticks(range(5)); ax_cm.set_xticklabels(CUSTOM_CLASSES, color='gray', rotation=30, fontsize=9)
ax_cm.set_yticks(range(5)); ax_cm.set_yticklabels(CUSTOM_CLASSES, color='gray', fontsize=9)
ax_cm.set_title('Matriz de Confusión (normalizada)', color='white')
ax_cm.set_xlabel('Predicho', color='gray'); ax_cm.set_ylabel('Real', color='gray')
for i in range(5):
    for j in range(5):
        val = conf_matrix_norm[i, j]
        ax_cm.text(j, i, f'{val:.2f}', ha='center', va='center',
                   color='white' if val > 0.5 else 'black', fontsize=9)
plt.colorbar(im, ax=ax_cm)

# Final metrics per class
ax_m = axes2[1]
ax_m.set_facecolor('#0d0d2a')
ax_m.tick_params(colors='gray')
for spine in ax_m.spines.values(): spine.set_color('#333')

per_class_map = [0.87, 0.91, 0.85, 0.88, 0.0]  # background has no mAP
bar_colors_cls = ['#4af', '#4e4', '#f84', '#a4e', '#888']
bars = ax_m.bar(CUSTOM_CLASSES, per_class_map, color=bar_colors_cls, alpha=0.85)
ax_m.axhline(0.60, color='yellow', linestyle='--', linewidth=1.5, label='Target mAP=0.60')
ax_m.set_ylabel('mAP@0.5', color='gray')
ax_m.set_title('mAP@0.5 por clase (epoch 50)', color='white')
ax_m.set_ylim(0, 1.1)
ax_m.tick_params(axis='x', rotation=15)
ax_m.legend(facecolor='#0d0d2a', labelcolor='white')
for bar, v in zip(bars, per_class_map):
    if v > 0:
        ax_m.text(bar.get_x() + bar.get_width()/2, v+0.02, f'{v:.2f}', ha='center', color='white', fontsize=10)

# Final summary text
final_map = np.mean([m for m in per_class_map if m > 0])
ax_m.text(0.5, 0.05, f'mAP@0.5 global: {final_map:.3f}', ha='center', transform=ax_m.transAxes,
          fontsize=11, color='#4e4', fontweight='bold')

plt.tight_layout()
fig2.savefig('../media/yolo_evaluation_metrics.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: yolo_evaluation_metrics.png")
print("All media generated for semana_11_4")
