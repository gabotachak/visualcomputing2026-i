#!/usr/bin/env python3
"""Semana 11_2: MediaPipe pose estimation simulation."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os, io, math

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# MediaPipe Pose has 33 landmarks. We simulate 3 poses.
# Landmark indices (key ones):
# 0=nose, 11=L_shoulder, 12=R_shoulder, 13=L_elbow, 14=R_elbow,
# 15=L_wrist, 16=R_wrist, 23=L_hip, 24=R_hip, 25=L_knee, 26=R_knee,
# 27=L_ankle, 28=R_ankle

def make_pose_landmarks(pose_name, cx=0.5, cy=0.5, scale=0.35):
    """Simulated 33 landmark (x,y) pairs for different poses."""
    # Base upright pose
    lm = np.zeros((33, 2))
    lm[0]  = [cx, cy - 0.45*scale]  # nose
    lm[1]  = [cx - 0.02*scale, cy - 0.43*scale]  # L eye inner
    lm[2]  = [cx - 0.04*scale, cy - 0.43*scale]  # L eye
    lm[3]  = [cx - 0.06*scale, cy - 0.42*scale]  # L eye outer
    lm[4]  = [cx + 0.02*scale, cy - 0.43*scale]  # R eye inner
    lm[5]  = [cx + 0.04*scale, cy - 0.43*scale]  # R eye
    lm[6]  = [cx + 0.06*scale, cy - 0.42*scale]  # R eye outer
    lm[7]  = [cx - 0.04*scale, cy - 0.41*scale]  # L ear
    lm[8]  = [cx + 0.04*scale, cy - 0.41*scale]  # R ear
    lm[9]  = [cx - 0.02*scale, cy - 0.39*scale]  # L mouth
    lm[10] = [cx + 0.02*scale, cy - 0.39*scale]  # R mouth

    if pose_name == 'standing':
        lm[11] = [cx - 0.12*scale, cy - 0.22*scale]  # L shoulder
        lm[12] = [cx + 0.12*scale, cy - 0.22*scale]  # R shoulder
        lm[13] = [cx - 0.14*scale, cy - 0.02*scale]  # L elbow
        lm[14] = [cx + 0.14*scale, cy - 0.02*scale]  # R elbow
        lm[15] = [cx - 0.13*scale, cy + 0.15*scale]  # L wrist
        lm[16] = [cx + 0.13*scale, cy + 0.15*scale]  # R wrist
        lm[23] = [cx - 0.08*scale, cy + 0.15*scale]  # L hip
        lm[24] = [cx + 0.08*scale, cy + 0.15*scale]  # R hip
        lm[25] = [cx - 0.08*scale, cy + 0.38*scale]  # L knee
        lm[26] = [cx + 0.08*scale, cy + 0.38*scale]  # R knee
        lm[27] = [cx - 0.08*scale, cy + 0.60*scale]  # L ankle
        lm[28] = [cx + 0.08*scale, cy + 0.60*scale]  # R ankle
    elif pose_name == 'arms_up':
        lm[11] = [cx - 0.12*scale, cy - 0.22*scale]
        lm[12] = [cx + 0.12*scale, cy - 0.22*scale]
        lm[13] = [cx - 0.25*scale, cy - 0.40*scale]  # L elbow up
        lm[14] = [cx + 0.25*scale, cy - 0.40*scale]  # R elbow up
        lm[15] = [cx - 0.20*scale, cy - 0.58*scale]  # L wrist up
        lm[16] = [cx + 0.20*scale, cy - 0.58*scale]  # R wrist up
        lm[23] = [cx - 0.08*scale, cy + 0.15*scale]
        lm[24] = [cx + 0.08*scale, cy + 0.15*scale]
        lm[25] = [cx - 0.08*scale, cy + 0.38*scale]
        lm[26] = [cx + 0.08*scale, cy + 0.38*scale]
        lm[27] = [cx - 0.08*scale, cy + 0.60*scale]
        lm[28] = [cx + 0.08*scale, cy + 0.60*scale]
    elif pose_name == 'sitting':
        lm[11] = [cx - 0.12*scale, cy - 0.22*scale]
        lm[12] = [cx + 0.12*scale, cy - 0.22*scale]
        lm[13] = [cx - 0.14*scale, cy - 0.02*scale]
        lm[14] = [cx + 0.14*scale, cy - 0.02*scale]
        lm[15] = [cx - 0.13*scale, cy + 0.12*scale]
        lm[16] = [cx + 0.13*scale, cy + 0.12*scale]
        lm[23] = [cx - 0.10*scale, cy + 0.18*scale]
        lm[24] = [cx + 0.10*scale, cy + 0.18*scale]
        lm[25] = [cx - 0.18*scale, cy + 0.18*scale]  # knees forward
        lm[26] = [cx + 0.18*scale, cy + 0.18*scale]
        lm[27] = [cx - 0.18*scale, cy + 0.38*scale]  # ankles below
        lm[28] = [cx + 0.18*scale, cy + 0.38*scale]
    return lm

CONNECTIONS = [
    (11,12), (11,13), (13,15), (12,14), (14,16),
    (11,23), (12,24), (23,24), (23,25), (24,26),
    (25,27), (26,28), (0,1), (0,4), (1,2), (2,3), (4,5), (5,6)
]

def draw_skeleton(ax, lm, color='#4af', label='', action=''):
    for a, b in CONNECTIONS:
        if np.any(lm[a] != 0) and np.any(lm[b] != 0):
            ax.plot([lm[a,0], lm[b,0]], [1-lm[a,1], 1-lm[b,1]], color=color, linewidth=2, alpha=0.8)
    visible = [(lm[i,0], lm[i,1]) for i in [0,11,12,13,14,15,16,23,24,25,26,27,28] if np.any(lm[i] != 0)]
    if visible:
        xs, ys = zip(*visible)
        ax.scatter(xs, [1-y for y in ys], c=color, s=30, zorder=5)
    if action:
        ax.text(0.5, 0.05, action, ha='center', transform=ax.transAxes,
                fontsize=12, color='white', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor=color, alpha=0.6))

# Plot 1: 3 poses with skeleton
fig, axes = plt.subplots(1, 3, figsize=(14, 6), facecolor='#0a0a1a')
fig.suptitle('MediaPipe Pose — Reconocimiento de Posturas Corporales (Simulado)', color='white', fontsize=13, fontweight='bold')

poses = [
    ('standing', '#4af', 'De pie', 'Acción: Parado'),
    ('arms_up', '#4e4', 'Brazos levantados', 'Acción: Brazos arriba'),
    ('sitting', '#f84', 'Sentado', 'Acción: Sentado'),
]

for ax, (pose, color, title, action) in zip(axes, poses):
    ax.set_facecolor('#111')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title(title, color=color, fontsize=11)
    lm = make_pose_landmarks(pose)
    draw_skeleton(ax, lm, color=color, action=action)

plt.tight_layout()
fig.savefig('../media/pose_recognition_poses.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: pose_recognition_poses.png")

# Plot 2: Angle analysis
def angle(a, b, c):
    """Angle at b between segments ba and bc."""
    ba = a - b; bc = c - b
    cos_a = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8)
    return math.degrees(math.acos(np.clip(cos_a, -1, 1)))

frames = ['standing'] * 10 + ['arms_up'] * 15 + ['sitting'] * 10 + ['standing'] * 15
angles_L_elbow = []
angles_L_knee = []
pose_labels = []

for pose_name in frames:
    lm = make_pose_landmarks(pose_name)
    lm_arr = lm * 480  # scale to pixels
    a_elbow = angle(lm_arr[11], lm_arr[13], lm_arr[15])  # shoulder-elbow-wrist
    a_knee = angle(lm_arr[23], lm_arr[25], lm_arr[27])    # hip-knee-ankle
    angles_L_elbow.append(a_elbow + np.random.randn() * 3)
    angles_L_knee.append(a_knee + np.random.randn() * 3)
    pose_labels.append(pose_name)

fig2, axes2 = plt.subplots(2, 1, figsize=(12, 8), facecolor='#0a0a1a')
fig2.suptitle('Análisis de Ángulos Articulares a lo Largo del Tiempo', color='white', fontsize=12, fontweight='bold')

for ax in axes2:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

frame_nums = range(len(frames))
axes2[0].plot(frame_nums, angles_L_elbow, color='#4af', linewidth=2)
axes2[0].axhline(90, color='yellow', linestyle='--', linewidth=1, label='90° referencia')
axes2[0].set_ylabel('Ángulo (°)', color='gray')
axes2[0].set_title('Ángulo codo izquierdo (hombro-codo-muñeca)', color='white')
axes2[0].legend(facecolor='#0d0d2a', labelcolor='white')
axes2[0].set_ylim(0, 200)

axes2[1].plot(frame_nums, angles_L_knee, color='#4e4', linewidth=2)
axes2[1].axhline(170, color='yellow', linestyle='--', linewidth=1, label='170° (pierna extendida)')
axes2[1].set_xlabel('Frame', color='gray')
axes2[1].set_ylabel('Ángulo (°)', color='gray')
axes2[1].set_title('Ángulo rodilla izquierda (cadera-rodilla-tobillo)', color='white')
axes2[1].legend(facecolor='#0d0d2a', labelcolor='white')
axes2[1].set_ylim(0, 200)

# Add pose change markers
for i, (pname, next_pname) in enumerate(zip(frames[:-1], frames[1:])):
    if pname != next_pname:
        for ax in axes2:
            ax.axvline(i, color='#f84', linestyle=':', linewidth=1.5, alpha=0.7)
            ax.text(i, ax.get_ylim()[1]*0.85, next_pname[:4], color='#f84', fontsize=8, ha='center')

plt.tight_layout()
fig2.savefig('../media/pose_angle_analysis.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: pose_angle_analysis.png")
print("All media generated for semana_11_2")
