#!/usr/bin/env python3
"""Semana 10_2: Pattern matching and homographies with RANSAC."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Create template image (pattern to find)
template = np.zeros((200, 200), dtype=np.uint8)
cv2.rectangle(template, (30, 30), (170, 170), 200, -1)
cv2.circle(template, (100, 100), 50, 100, -1)
cv2.putText(template, 'PAT', (55, 115), cv2.FONT_HERSHEY_SIMPLEX, 1.2, 220, 3)

# Create scene image with pattern embedded + perspective transform
scene = np.full((400, 600), 50, dtype=np.uint8)
# Add noise texture to scene
scene += np.random.randint(0, 30, scene.shape, dtype=np.uint8)

# Apply perspective transform to template and embed in scene
pts_src = np.float32([[0,0], [200,0], [200,200], [0,200]])
pts_dst = np.float32([[150,80], [320,60], [350,220], [130,250]])
M_persp = cv2.getPerspectiveTransform(pts_src, pts_dst)
warped_template = cv2.warpPerspective(template, M_persp, (600, 400))

# Blend into scene
mask = warped_template > 0
scene[mask] = warped_template[mask]
# Add more objects to scene
cv2.circle(scene, (80, 350), 50, 150, -1)
cv2.rectangle(scene, (450, 280), (550, 380), 160, -1)

# SIFT feature matching
sift = cv2.SIFT_create()
kp_tmpl, des_tmpl = sift.detectAndCompute(template, None)
kp_scene, des_scene = sift.detectAndCompute(scene, None)

# Match with FLANN
if des_tmpl is not None and des_scene is not None and len(des_tmpl) > 2 and len(des_scene) > 2:
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des_tmpl, des_scene, k=2)
    good = [m for m, n in matches if m.distance < 0.7 * n.distance]
else:
    good = []

# Compute homography if enough matches
result_img = cv2.cvtColor(scene, cv2.COLOR_GRAY2BGR)
if len(good) >= 4:
    src_pts = np.float32([kp_tmpl[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp_scene[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if H is not None:
        h, w = template.shape
        pts = np.float32([[0,0],[0,h-1],[w-1,h-1],[w-1,0]]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts, H)
        result_img = cv2.polylines(result_img, [np.int32(dst)], True, (0, 255, 0), 3)
        inliers = mask.ravel().tolist()
        good_inliers = [good[i] for i in range(len(good)) if inliers[i]]
    else:
        good_inliers = good
else:
    good_inliers = good

# Draw matches
match_img = cv2.drawMatches(
    template, kp_tmpl, scene, kp_scene,
    good_inliers[:30], None,
    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)

# Plot 1: Full pipeline
fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor='#0a0a1a')
fig.suptitle('Coincidencia de Patrones y Homografías — SIFT + RANSAC', color='white', fontsize=13, fontweight='bold')

axes[0][0].imshow(template, cmap='gray')
axes[0][0].set_title(f'Template ({len(kp_tmpl)} keypoints SIFT)', color='white')
axes[0][1].imshow(scene, cmap='gray')
axes[0][1].set_title(f'Escena ({len(kp_scene)} keypoints SIFT)', color='white')
axes[1][0].imshow(match_img)
axes[1][0].set_title(f'Matches filtrados con Lowe ratio test ({len(good)} good, {len(good_inliers)} inliers)', color='white')
axes[1][1].imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
axes[1][1].set_title('Homografía + RANSAC — borde verde = objeto detectado', color='white')

for ax_row in axes:
    for ax in ax_row:
        ax.axis('off')
        ax.set_facecolor('#0d0d2a')

plt.tight_layout()
fig.savefig('../media/pattern_matching_homography.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: pattern_matching_homography.png")

# Plot 2: Distance distribution of matches
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
fig2.suptitle('Análisis de Calidad del Matching', color='white', fontsize=12, fontweight='bold')

for ax in axes2:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

if len(good) > 0:
    all_matches_sorted = sorted(good, key=lambda x: x.distance)
    distances = [m.distance for m in all_matches_sorted]
    axes2[0].bar(range(len(distances)), distances, color=['#4e4' if m in good_inliers else '#e44' for m in all_matches_sorted], alpha=0.8)
    axes2[0].set_xlabel('Match index', color='gray')
    axes2[0].set_ylabel('Distancia del descriptor', color='gray')
    axes2[0].set_title('Distancias de matches\n(verde=inlier, rojo=outlier)', color='white')

    # Confidence metrics
    metrics = {
        'Total keypoints\ntemplate': len(kp_tmpl),
        'Total keypoints\nescena': len(kp_scene),
        'Good matches\n(Lowe ratio)': len(good),
        'Inliers\n(RANSAC)': len(good_inliers),
    }
    colors_bar = ['#4af', '#4af', '#4e4', '#f84']
    axes2[1].bar(range(len(metrics)), list(metrics.values()), color=colors_bar, alpha=0.8)
    axes2[1].set_xticks(range(len(metrics)))
    axes2[1].set_xticklabels(list(metrics.keys()), color='gray', fontsize=8)
    axes2[1].set_ylabel('Cantidad', color='gray')
    axes2[1].set_title('Métricas del matching', color='white')

plt.tight_layout()
fig2.savefig('../media/matching_quality_analysis.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: matching_quality_analysis.png")
print("All media generated for semana_10_2")
