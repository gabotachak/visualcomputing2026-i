#!/usr/bin/env python3
"""Semana 12_1: CLIP text+image classification simulation."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate CLIP classification results
CATEGORIES = ['radiografía de tórax normal', 'radiografía con neumonía',
              'pintura renacentista', 'pintura abstracta', 'fotografía moderna']
N_IMAGES = 20

# Simulated CLIP similarity scores (text-image cosine similarity)
np.random.seed(42)
# True labels
true_labels = np.repeat(np.arange(5), 4)
# Simulate similarity matrix
sim_matrix = np.random.dirichlet([1]*5, N_IMAGES) * 0.3
for i, label in enumerate(true_labels):
    sim_matrix[i, label] += 0.6  # boost true class
sim_matrix = sim_matrix / sim_matrix.sum(axis=1, keepdims=True)

pred_labels = sim_matrix.argmax(axis=1)
accuracy = (pred_labels == true_labels).mean()

# Plot 1: Similarity heatmap + accuracy
fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='#0a0a1a')
fig.suptitle('CLIP Text+Image — Clasificación Asistida (Simulado)', color='white', fontsize=13, fontweight='bold')

ax_heat = axes[0]
ax_heat.set_facecolor('#0d0d2a')
im = ax_heat.imshow(sim_matrix[:15].T, cmap='viridis', aspect='auto')
ax_heat.set_yticks(range(5))
ax_heat.set_yticklabels([c[:25] for c in CATEGORIES], color='gray', fontsize=8)
ax_heat.set_xlabel('Imagen #', color='gray')
ax_heat.set_title('Similitud coseno CLIP (imagen ↔ texto)', color='white')
plt.colorbar(im, ax=ax_heat)

# Per-category accuracy
cat_accs = []
for cat_id in range(5):
    mask = true_labels == cat_id
    cat_acc = (pred_labels[mask] == true_labels[mask]).mean()
    cat_accs.append(cat_acc)

ax_acc = axes[1]
ax_acc.set_facecolor('#0d0d2a')
ax_acc.tick_params(colors='gray')
for spine in ax_acc.spines.values(): spine.set_color('#333')

colors_cat = ['#4af', '#e44', '#4e4', '#f84', '#a4e']
bars = ax_acc.bar([c[:20] for c in CATEGORIES], cat_accs, color=colors_cat, alpha=0.85)
ax_acc.axhline(accuracy, color='yellow', linestyle='--', linewidth=1.5, label=f'Global: {accuracy:.1%}')
ax_acc.set_ylabel('Accuracy', color='gray')
ax_acc.set_title('Exactitud CLIP por categoría', color='white')
ax_acc.set_ylim(0, 1.15)
ax_acc.tick_params(axis='x', rotation=30)
ax_acc.legend(facecolor='#0d0d2a', labelcolor='white')
for bar, v in zip(bars, cat_accs):
    ax_acc.text(bar.get_x()+bar.get_width()/2, v+0.02, f'{v:.0%}', ha='center', color='white', fontsize=10)

plt.tight_layout()
fig.savefig('../media/clip_classification_results.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: clip_classification_results.png")

# Plot 2: CLIP vs traditional classifier comparison
methods = ['k-NN (pixel)', 'SVM (HOG)', 'ResNet-50', 'CLIP (zero-shot)']
accuracies = [0.42, 0.68, 0.87, accuracy]
times = [0.5, 2.1, 15.0, 8.3]  # inference time (ms)

fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
fig2.suptitle('CLIP vs Clasificadores Tradicionales', color='white', fontsize=12, fontweight='bold')

for ax in axes2:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

bar_colors2 = ['#888', '#888', '#4af', '#4e4']
axes2[0].bar(methods, [a*100 for a in accuracies], color=bar_colors2, alpha=0.85)
axes2[0].set_ylabel('Accuracy (%)', color='gray')
axes2[0].set_title('Exactitud por método', color='white')
axes2[0].tick_params(axis='x', rotation=20)
for i, v in enumerate(accuracies):
    axes2[0].text(i, v*100+0.5, f'{v:.0%}', ha='center', color='white', fontsize=10)

axes2[1].scatter(times, [a*100 for a in accuracies], c=bar_colors2, s=200, alpha=0.9, edgecolors='white')
for i, (m, t, a) in enumerate(zip(methods, times, accuracies)):
    axes2[1].annotate(m, (t, a*100), textcoords='offset points', xytext=(5, 5), color=bar_colors2[i], fontsize=9)
axes2[1].set_xlabel('Tiempo inferencia (ms)', color='gray')
axes2[1].set_ylabel('Accuracy (%)', color='gray')
axes2[1].set_title('Trade-off: Velocidad vs Precisión', color='white')

plt.tight_layout()
fig2.savefig('../media/clip_vs_traditional.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: clip_vs_traditional.png")
print("All media generated for semana_12_1")
