#!/usr/bin/env python3
"""Semana 12_5: CLIP visual embeddings + PCA/t-SNE projection."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate CLIP 512-dim embeddings for 6 image categories (40 images each)
CATEGORIES = ['animals', 'vehicles', 'food', 'landscapes', 'people', 'architecture']
N_PER_CLASS = 40
EMBED_DIM = 512

# Generate clustered embeddings (simulate CLIP feature space)
cat_centers = np.random.randn(len(CATEGORIES), EMBED_DIM) * 2
embeddings = []
labels = []
for cls_id, center in enumerate(cat_centers):
    cluster = center + np.random.randn(N_PER_CLASS, EMBED_DIM) * 0.5
    embeddings.append(cluster)
    labels.extend([cls_id] * N_PER_CLASS)
embeddings = np.vstack(embeddings)
labels = np.array(labels)

# PCA to 2D
pca = PCA(n_components=2)
pca_2d = pca.fit_transform(embeddings)

# t-SNE to 2D
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
tsne_2d = tsne.fit_transform(embeddings)

# PCA to 3D
pca_3d = PCA(n_components=3).fit_transform(embeddings)

COLORS = plt.cm.Set1(np.linspace(0, 0.9, len(CATEGORIES)))

# Plot 1: PCA vs t-SNE
fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='#0a0a1a')
fig.suptitle('CLIP Visual Embeddings — Reducción de Dimensionalidad (PCA vs t-SNE)', color='white', fontsize=13, fontweight='bold')

for ax, (data, title) in zip(axes, [(pca_2d, f'PCA 2D\n(var explicada: {pca.explained_variance_ratio_.sum():.1%})'),
                                      (tsne_2d, 't-SNE 2D\n(perplexity=30)')]):
    ax.set_facecolor('#111')
    for cls_id, (cat, color) in enumerate(zip(CATEGORIES, COLORS)):
        mask = labels == cls_id
        ax.scatter(data[mask, 0], data[mask, 1], c=[color], s=30, alpha=0.8, label=cat)
    ax.set_title(title, color='white')
    ax.legend(facecolor='#0d0d2a', labelcolor='white', fontsize=9)
    ax.set_facecolor('#111')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values():
        spine.set_color('#333')

plt.tight_layout()
fig.savefig('../media/clip_pca_tsne.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: clip_pca_tsne.png")

# Plot 2: PCA variance + inter-cluster distances
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
fig2.suptitle('Análisis de Embeddings CLIP — Varianza y Separabilidad', color='white', fontsize=12, fontweight='bold')

for ax in axes2:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values():
        spine.set_color('#333')

# Cumulative variance explained
pca_full = PCA(n_components=50)
pca_full.fit(embeddings)
cum_var = np.cumsum(pca_full.explained_variance_ratio_)
axes2[0].plot(range(1, 51), cum_var * 100, color='#4af', linewidth=2)
axes2[0].axhline(90, color='yellow', linestyle='--', linewidth=1, label='90% varianza')
axes2[0].axhline(95, color='#f84', linestyle='--', linewidth=1, label='95% varianza')
axes2[0].set_xlabel('Número de componentes PCA', color='gray')
axes2[0].set_ylabel('Varianza acumulada (%)', color='gray')
axes2[0].set_title('Varianza explicada por PCA', color='white')
axes2[0].legend(facecolor='#0d0d2a', labelcolor='white')

# Inter-cluster cosine distances
centers_norm = cat_centers / np.linalg.norm(cat_centers, axis=1, keepdims=True)
cos_sim = centers_norm @ centers_norm.T
im = axes2[1].imshow(cos_sim, cmap='RdYlGn', vmin=-0.5, vmax=1)
axes2[1].set_xticks(range(len(CATEGORIES)))
axes2[1].set_xticklabels(CATEGORIES, color='gray', rotation=30, fontsize=9)
axes2[1].set_yticks(range(len(CATEGORIES)))
axes2[1].set_yticklabels(CATEGORIES, color='gray', fontsize=9)
axes2[1].set_title('Similitud coseno entre centros de cluster', color='white')
for i in range(len(CATEGORIES)):
    for j in range(len(CATEGORIES)):
        axes2[1].text(j, i, f'{cos_sim[i,j]:.2f}', ha='center', va='center',
                      color='black' if cos_sim[i,j] > 0.3 else 'white', fontsize=8)
plt.colorbar(im, ax=axes2[1])

plt.tight_layout()
fig2.savefig('../media/clip_embedding_analysis.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: clip_embedding_analysis.png")
print("All media generated for semana_12_5")
