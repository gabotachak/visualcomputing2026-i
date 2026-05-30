#!/usr/bin/env python3
"""Semana 9_2: Custom convolutions with various kernels."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)

# Generate a synthetic test image with details
img = np.zeros((300, 400, 3), dtype=np.uint8)
for i in range(0, 400, 20):
    cv2.line(img, (i, 0), (i, 300), (100, 100, 100), 1)
for j in range(0, 300, 20):
    cv2.line(img, (0, j), (400, j), (100, 100, 100), 1)
cv2.circle(img, (100, 150), 60, (200, 100, 50), -1)
cv2.rectangle(img, (200, 80), (340, 220), (50, 150, 200), -1)
cv2.putText(img, 'CV', (230, 175), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 200, 50), 4)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0

# Custom convolution from scratch
def convolve2d_manual(image, kernel):
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    result = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            result[i, j] = np.sum(padded[i:i+kh, j:j+kw] * kernel)
    return np.clip(result, 0, 1)

# Define kernels
kernels = {
    'Identidad': np.array([[0,0,0],[0,1,0],[0,0,0]], dtype=np.float32),
    'Blur (Box)': np.ones((5,5), dtype=np.float32) / 25,
    'Sharpen': np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]], dtype=np.float32),
    'Sobel X': np.array([[-1,0,1],[-2,0,2],[-1,0,1]], dtype=np.float32),
    'Sobel Y': np.array([[-1,-2,-1],[0,0,0],[1,2,1]], dtype=np.float32),
    'Laplacian': np.array([[0,1,0],[1,-4,1],[0,1,0]], dtype=np.float32),
}

# Apply each kernel (using cv2.filter2D for speed)
results = {}
for name, kernel in kernels.items():
    filtered = cv2.filter2D(gray, -1, kernel)
    results[name] = np.clip(filtered, 0, 1)

# Also apply Sobel manually for demonstration
sobel_x_manual = convolve2d_manual(gray, kernels['Sobel X'])

# Plot 1: All kernels comparison
fig, axes = plt.subplots(2, 4, figsize=(16, 8), facecolor='#0a0a1a')
fig.suptitle('Convoluciones Personalizadas — Comparación de Kernels', color='white', fontsize=13, fontweight='bold')

axes_flat = axes.flatten()
axes_flat[0].imshow(gray, cmap='gray')
axes_flat[0].set_title('Original', color='white')

for ax, (name, result) in zip(axes_flat[1:], results.items()):
    disp = np.abs(result)
    if name in ['Sobel X', 'Sobel Y', 'Laplacian']:
        disp = np.abs(result - result.min()) / (result.max() - result.min() + 1e-8)
    ax.imshow(disp, cmap='gray')
    ax.set_title(name, color='white', fontsize=10)

for ax in axes_flat:
    ax.axis('off')
    ax.set_facecolor('#0d0d2a')

# Last axis: kernel visualization
axes_flat[-1].axis('off')
axes_flat[-1].set_title('Sobel X (manual)', color='white', fontsize=10)
axes_flat[-1].imshow(sobel_x_manual, cmap='gray')

plt.tight_layout()
fig.savefig('../media/convolution_kernels.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: convolution_kernels.png")

# Plot 2: Kernel matrices visualization
fig2, axes2 = plt.subplots(2, 3, figsize=(12, 8), facecolor='#0a0a1a')
fig2.suptitle('Matrices de Kernels — Visualización', color='white', fontsize=13, fontweight='bold')

kernel_items = list(kernels.items())
for ax, (name, k) in zip(axes2.flatten(), kernel_items):
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values():
        spine.set_color('#333')

    # Show kernel matrix as heatmap
    k_norm = (k - k.min()) / (k.max() - k.min() + 1e-8)
    im = ax.imshow(k_norm, cmap='RdBu_r', vmin=0, vmax=1, aspect='auto')
    ax.set_title(name, color='white', fontsize=11)
    # Annotate values
    for i in range(k.shape[0]):
        for j in range(k.shape[1]):
            ax.text(j, i, f'{k[i,j]:.2f}', ha='center', va='center',
                   color='white' if abs(k_norm[i,j]-0.5) > 0.3 else 'black', fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])

plt.tight_layout()
fig2.savefig('../media/kernel_matrices.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: kernel_matrices.png")
print("All media generated for semana_9_2")
