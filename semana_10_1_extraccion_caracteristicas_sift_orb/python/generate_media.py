#!/usr/bin/env python3
"""Semana 10_1: Feature extraction with SIFT and ORB."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Create two synthetic test images (original + slightly rotated/scaled)
def make_test_img():
    img = np.zeros((300, 400), dtype=np.uint8)
    cv2.circle(img, (100, 100), 60, 200, -1)
    cv2.rectangle(img, (180, 60), (320, 200), 150, -1)
    cv2.putText(img, 'SIFT', (150, 260), cv2.FONT_HERSHEY_SIMPLEX, 2, 220, 3)
    # Add some texture
    noise = np.random.randint(0, 30, img.shape, dtype=np.uint8)
    return cv2.add(img, noise)

img1 = make_test_img()
# Create a slightly transformed version
M = cv2.getRotationMatrix2D((200, 150), 15, 0.9)
img2 = cv2.warpAffine(img1, M, (400, 300))
img2 = cv2.GaussianBlur(img2, (3, 3), 0)

# SIFT detection
t0 = time.time()
sift = cv2.SIFT_create()
kp1_sift, des1_sift = sift.detectAndCompute(img1, None)
kp2_sift, des2_sift = sift.detectAndCompute(img2, None)
t_sift = time.time() - t0

# ORB detection
t0 = time.time()
orb = cv2.ORB_create(nfeatures=500)
kp1_orb, des1_orb = orb.detectAndCompute(img1, None)
kp2_orb, des2_orb = orb.detectAndCompute(img2, None)
t_orb = time.time() - t0

# Draw keypoints
img1_sift_kp = cv2.drawKeypoints(img1, kp1_sift, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
img1_orb_kp = cv2.drawKeypoints(img1, kp1_orb, None, color=(0, 255, 0))

# Feature matching
if des1_sift is not None and des2_sift is not None:
    bf_sift = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    matches_sift = bf_sift.knnMatch(des1_sift, des2_sift, k=2)
    good_sift = [m for m, n in matches_sift if m.distance < 0.75 * n.distance]
    match_img_sift = cv2.drawMatches(img1, kp1_sift, img2, kp2_sift, good_sift[:20], None,
                                      flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
else:
    match_img_sift = np.zeros((300, 800), dtype=np.uint8)
    good_sift = []

if des1_orb is not None and des2_orb is not None:
    bf_orb = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches_orb = sorted(bf_orb.match(des1_orb, des2_orb), key=lambda x: x.distance)
    match_img_orb = cv2.drawMatches(img1, kp1_orb, img2, kp2_orb, matches_orb[:20], None,
                                     flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
else:
    match_img_orb = np.zeros((300, 800), dtype=np.uint8)
    matches_orb = []

# Plot 1: Keypoints comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 8), facecolor='#0a0a1a')
fig.suptitle(f'SIFT vs ORB — Detección de Puntos Clave y Descriptores', color='white', fontsize=13, fontweight='bold')

axes[0][0].imshow(img1_sift_kp)
axes[0][0].set_title(f'SIFT Keypoints ({len(kp1_sift)} puntos, {t_sift*1000:.1f}ms)', color='white')
axes[0][1].imshow(img1_orb_kp)
axes[0][1].set_title(f'ORB Keypoints ({len(kp1_orb)} puntos, {t_orb*1000:.1f}ms)', color='white')
axes[1][0].imshow(match_img_sift)
axes[1][0].set_title(f'SIFT Matches ({len(good_sift)} buenos)', color='white')
axes[1][1].imshow(match_img_orb)
axes[1][1].set_title(f'ORB Matches ({len(matches_orb[:20])} mostrados)', color='white')

for ax_row in axes:
    for ax in ax_row:
        ax.axis('off')
        ax.set_facecolor('#0d0d2a')

plt.tight_layout()
fig.savefig('../media/sift_orb_comparison.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: sift_orb_comparison.png")

# Plot 2: Comparison table
fig2, ax2 = plt.subplots(figsize=(10, 5), facecolor='#0a0a1a')
ax2.set_facecolor('#0d0d2a')
ax2.axis('off')
ax2.set_title('SIFT vs ORB — Comparación de Características', color='white', fontsize=13, fontweight='bold')

rows = [
    ['Algoritmo', 'SIFT', 'ORB'],
    ['Descriptor', 'Float128 (L2)', 'Binary (Hamming)'],
    ['Puntos detectados', str(len(kp1_sift)), str(len(kp1_orb))],
    ['Tiempo detección', f'{t_sift*1000:.1f} ms', f'{t_orb*1000:.1f} ms'],
    ['Buenos matches', str(len(good_sift)), str(min(20, len(matches_orb)))],
    ['Invarianza escala', 'Sí', 'Parcial'],
    ['Invarianza rotación', 'Sí', 'Sí'],
    ['Patente/Libre', 'Libre (OpenCV 4.4+)', 'BSD'],
    ['Velocidad', 'Lento', 'Rápido (GPU-friendly)'],
    ['Precisión', 'Alta', 'Media-Alta'],
]

table = ax2.table(cellText=rows[1:], colLabels=rows[0], cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.8)
for (r, c), cell in table.get_celld().items():
    if r == 0:
        cell.set_facecolor('#2a2a5e')
    elif c == 0:
        cell.set_facecolor('#1a2a4e')
    else:
        cell.set_facecolor('#1a1a3e' if r % 2 == 0 else '#141430')
    cell.set_text_props(color='white')
    cell.set_edgecolor('#444')

plt.tight_layout()
fig2.savefig('../media/sift_orb_table.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: sift_orb_table.png")
print("All media generated for semana_10_1")
