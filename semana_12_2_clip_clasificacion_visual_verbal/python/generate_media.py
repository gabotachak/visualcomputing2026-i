#!/usr/bin/env python3
"""Semana 12_2: CLIP visual-verbal classification simulation."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

IMAGE_CLASSES = ['dog', 'cat', 'car', 'airplane', 'pizza', 'sunset', 'mountain', 'book']
N = 40

# Simulate CLIP embedding space (project 512-dim to 2D)
centers = np.random.randn(len(IMAGE_CLASSES), 2) * 3
labels = np.repeat(np.arange(len(IMAGE_CLASSES)), N // len(IMAGE_CLASSES))
points = centers[labels] + np.random.randn(N, 2) * 0.5
text_points = centers + np.random.randn(len(IMAGE_CLASSES), 2) * 0.2

# Similarity scores for one test image (car)
test_class = 2
sim_scores = np.random.randn(len(IMAGE_CLASSES)) * 0.1
sim_scores[test_class] = 0.85
sim_scores = np.exp(sim_scores) / np.exp(sim_scores).sum()

COLORS = plt.cm.tab10(np.linspace(0, 1, len(IMAGE_CLASSES)))

# Plot 1: Embedding space + similarity
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), facecolor='#0a0a1a')
fig.suptitle('CLIP — Clasificación Visual-Verbal por Similitud Coseno (Simulado)', color='white', fontsize=13, fontweight='bold')

ax_emb = axes[0]
ax_emb.set_facecolor('#111')
for cls_id, (cls_name, color) in enumerate(zip(IMAGE_CLASSES, COLORS)):
    mask = labels == cls_id
    ax_emb.scatter(points[mask, 0], points[mask, 1], c=[color], s=30, alpha=0.7, label=cls_name)
    ax_emb.scatter(text_points[cls_id, 0], text_points[cls_id, 1], c=[color], s=200,
                   marker='*', edgecolors='white', linewidth=1.5, zorder=5)
ax_emb.set_title('Espacio embeddings CLIP 2D\n(★ = prompt texto, ● = imagen)', color='white')
ax_emb.legend(bbox_to_anchor=(1.01, 1), loc='upper left', facecolor='#0d0d2a', labelcolor='white', fontsize=8)

ax_sim = axes[1]
ax_sim.set_facecolor('#0d0d2a')
ax_sim.tick_params(colors='gray')
for spine in ax_sim.spines.values():
    spine.set_color('#333')
bar_colors = ['#4e4' if i == test_class else '#4af' for i in range(len(IMAGE_CLASSES))]
ax_sim.bar(IMAGE_CLASSES, sim_scores, color=bar_colors, alpha=0.85)
ax_sim.set_ylabel('Similitud coseno (softmax)', color='gray')
ax_sim.set_title(f'Query: "a photo of a {IMAGE_CLASSES[test_class]}"', color='white')
ax_sim.tick_params(axis='x', rotation=30)

plt.tight_layout()
fig.savefig('../media/clip_embedding_space.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: clip_embedding_space.png")

# Plot 2: Zero-shot vs few-shot accuracy
n_shots = [0, 1, 5, 10, 20, 50]
zs_acc   = [0.72, 0.74, 0.79, 0.83, 0.87, 0.89]
trad_acc = [0.00, 0.35, 0.55, 0.68, 0.78, 0.85]

fig2, ax2 = plt.subplots(figsize=(10, 5), facecolor='#0a0a1a')
ax2.set_facecolor('#0d0d2a')
ax2.tick_params(colors='gray')
for spine in ax2.spines.values():
    spine.set_color('#333')
ax2.plot(n_shots, [a*100 for a in zs_acc], color='#4e4', linewidth=2, marker='o', label='CLIP (zero/few-shot)')
ax2.plot(n_shots, [a*100 for a in trad_acc], color='#f84', linewidth=2, marker='s', linestyle='--', label='ResNet fine-tuned')
ax2.set_xlabel('# ejemplos de entrenamiento por clase', color='gray')
ax2.set_ylabel('Accuracy (%)', color='gray')
ax2.set_title('CLIP Zero-Shot vs Fine-Tuning Tradicional', color='white', fontsize=12, fontweight='bold')
ax2.legend(facecolor='#0d0d2a', labelcolor='white')
ax2.set_ylim(0, 100)

plt.tight_layout()
fig2.savefig('../media/clip_zeroshot_vs_finetuned.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: clip_zeroshot_vs_finetuned.png")
print("All media generated for semana_12_2")
