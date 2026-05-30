#!/usr/bin/env python3
"""Semana 12_6: Full DL training pipeline with PyTorch."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

try:
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, TensorDataset
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

N_CLASSES = 5
CLASS_NAMES = ['Cat', 'Dog', 'Bird', 'Fish', 'Car']
EPOCHS = 20

# Simulate full pipeline data
def sim_history():
    ep = np.arange(EPOCHS)
    tl = 1.6 * np.exp(-ep*0.15) + 0.25 + np.random.randn(EPOCHS)*0.02
    vl = 1.8 * np.exp(-ep*0.12) + 0.30 + np.random.randn(EPOCHS)*0.03
    ta = np.clip(1-0.65*np.exp(-ep*0.2) + np.random.randn(EPOCHS)*0.01, 0.3, 0.98)
    va = np.clip(1-0.70*np.exp(-ep*0.18) + np.random.randn(EPOCHS)*0.015, 0.25, 0.95)
    lr = [0.001 * (0.5 ** (e // 7)) for e in ep]
    return tl, vl, ta, va, lr

train_loss, val_loss, train_acc, val_acc, lr_schedule = sim_history()

# Simulated confusion matrix
n_test = 200
y_true = np.repeat(np.arange(N_CLASSES), n_test // N_CLASSES)
y_pred = y_true.copy()
# Add ~12% errors
error_mask = np.random.rand(len(y_true)) < 0.12
y_pred[error_mask] = np.random.randint(0, N_CLASSES, error_mask.sum())
cm = confusion_matrix(y_true, y_pred)
cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)

# Plot 1: Full training dashboard
fig, axes = plt.subplots(2, 3, figsize=(16, 10), facecolor='#0a0a1a')
fig.suptitle('Pipeline Completo de Deep Learning — Entrenamiento, Validación y Evaluación', color='white', fontsize=13, fontweight='bold')

for ax in axes.flatten():
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

ep = range(1, EPOCHS+1)

# Loss
axes[0][0].plot(ep, train_loss, color='#4af', linewidth=2, label='Train')
axes[0][0].plot(ep, val_loss, color='#f84', linewidth=2, linestyle='--', label='Val')
axes[0][0].set_title('Pérdida (Cross-Entropy)', color='white')
axes[0][0].set_xlabel('Época', color='gray'); axes[0][0].set_ylabel('Loss', color='gray')
axes[0][0].legend(facecolor='#0d0d2a', labelcolor='white')

# Accuracy
axes[0][1].plot(ep, [a*100 for a in train_acc], color='#4af', linewidth=2, label='Train')
axes[0][1].plot(ep, [a*100 for a in val_acc], color='#f84', linewidth=2, linestyle='--', label='Val')
axes[0][1].set_title('Exactitud (%)', color='white')
axes[0][1].set_xlabel('Época', color='gray'); axes[0][1].set_ylabel('Acc %', color='gray')
axes[0][1].legend(facecolor='#0d0d2a', labelcolor='white')

# Learning rate schedule
axes[0][2].semilogy(ep, lr_schedule, color='#a4e', linewidth=2)
axes[0][2].set_title('Learning Rate Schedule', color='white')
axes[0][2].set_xlabel('Época', color='gray'); axes[0][2].set_ylabel('LR', color='gray')

# Confusion matrix
im = axes[1][0].imshow(cm_norm, cmap='Blues', vmin=0, vmax=1)
axes[1][0].set_xticks(range(N_CLASSES)); axes[1][0].set_xticklabels(CLASS_NAMES, color='gray', rotation=30)
axes[1][0].set_yticks(range(N_CLASSES)); axes[1][0].set_yticklabels(CLASS_NAMES, color='gray')
axes[1][0].set_title('Matriz de Confusión', color='white')
for i in range(N_CLASSES):
    for j in range(N_CLASSES):
        axes[1][0].text(j, i, f'{cm_norm[i,j]:.2f}', ha='center', va='center',
                        color='white' if cm_norm[i,j]>0.5 else 'black', fontsize=9)

# Per-class metrics
report = classification_report(y_true, y_pred, target_names=CLASS_NAMES, output_dict=True)
precisions = [report[c]['precision'] for c in CLASS_NAMES]
recalls = [report[c]['recall'] for c in CLASS_NAMES]
f1s = [report[c]['f1-score'] for c in CLASS_NAMES]
x = np.arange(N_CLASSES)
w = 0.25
axes[1][1].bar(x-w, precisions, w, color='#4af', alpha=0.85, label='Precision')
axes[1][1].bar(x, recalls, w, color='#4e4', alpha=0.85, label='Recall')
axes[1][1].bar(x+w, f1s, w, color='#f84', alpha=0.85, label='F1')
axes[1][1].set_xticks(x); axes[1][1].set_xticklabels(CLASS_NAMES, color='gray')
axes[1][1].set_title('Métricas por clase', color='white')
axes[1][1].legend(facecolor='#0d0d2a', labelcolor='white', fontsize=8)
axes[1][1].set_ylim(0, 1.15)

# Train/Val gap (overfitting analysis)
gap = [t - v for t, v in zip(train_acc, val_acc)]
axes[1][2].fill_between(ep, gap, 0, where=[g > 0 for g in gap], color='#e44', alpha=0.4, label='Overfitting gap')
axes[1][2].plot(ep, gap, color='#e44', linewidth=2)
axes[1][2].axhline(0, color='gray', linewidth=1)
axes[1][2].set_title('Gap Train/Val (análisis overfitting)', color='white')
axes[1][2].set_xlabel('Época', color='gray'); axes[1][2].set_ylabel('Train Acc - Val Acc', color='gray')
axes[1][2].legend(facecolor='#0d0d2a', labelcolor='white')

plt.tight_layout()
fig.savefig('../media/dl_full_pipeline_dashboard.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: dl_full_pipeline_dashboard.png")

# Plot 2: Architecture diagram
fig2, ax2 = plt.subplots(figsize=(14, 5), facecolor='#0a0a1a')
ax2.set_facecolor('#0a0a1a')
ax2.set_xlim(0, 14); ax2.set_ylim(0, 5)
ax2.axis('off')
ax2.set_title('Arquitectura CNN — Pipeline de Entrenamiento Completo', color='white', fontsize=13, fontweight='bold')

import matplotlib.patches as mpatches

blocks = [
    (0.3, 'Input\n(H×W×C)', '#1a3a6e'),
    (2.3, 'Conv2D\nReLU + BN', '#1e5e3e'),
    (4.3, 'MaxPool\n+ Dropout', '#1e5e3e'),
    (6.3, 'Conv2D\nReLU + BN', '#1e5e3e'),
    (8.3, 'GAP\nFlatten', '#5e4e1e'),
    (10.3, 'FC + ReLU\nDropout', '#5e1e3e'),
    (12.3, 'FC + Softmax\nN classes', '#3e1e5e'),
]

for x, label, color in blocks:
    rect = mpatches.FancyBboxPatch((x, 1.5), 1.8, 2, boxstyle='round,pad=0.1',
                                    facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.9)
    ax2.add_patch(rect)
    ax2.text(x+0.9, 2.5, label, ha='center', va='center', color='white', fontsize=9, fontweight='bold')
    if x < 12.3:
        ax2.annotate('', xy=(x+2.1, 2.5), xytext=(x+1.9, 2.5),
                    arrowprops=dict(arrowstyle='->', color='white', lw=1.5))

ax2.text(7, 0.5, 'Train: Adam (lr=0.001) | Scheduler: StepLR(gamma=0.5, step=7) | Loss: CrossEntropy | Regularization: L2 + Dropout',
         ha='center', color='#aaa', fontsize=9)

fig2.savefig('../media/dl_architecture_diagram.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: dl_architecture_diagram.png")
print("All media generated for semana_12_6")
