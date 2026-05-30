#!/usr/bin/env python3
"""Semana 13_7: Simulated Visual SLAM — feature tracking + odometry."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

N_FRAMES = 40
W, H = 400, 300

# Simulate camera motion: circular trajectory with known poses
def get_camera_pose(t):
    angle = t * 0.15
    tx = 3 * np.sin(angle)
    ty = 0
    tz = 3 * np.cos(angle)
    return np.array([tx, ty, tz])

# Generate synthetic 3D feature points
N_FEATURES = 50
points_3d = np.random.randn(N_FEATURES, 3)
points_3d[:, 2] += 5  # in front of camera

# Camera intrinsics
K = np.array([[300, 0, W/2], [0, 300, H/2], [0, 0, 1]], dtype=np.float64)

def project_points(points, pose):
    """Project 3D points with camera at given pose."""
    pts_cam = points - pose
    pts_2d = (K @ pts_cam.T).T
    pts_2d = pts_2d[:, :2] / pts_2d[:, 2:3]
    return pts_2d

def make_frame(pose):
    frame = np.zeros((H, W), dtype=np.uint8)
    frame += 30
    pts_2d = project_points(points_3d, pose)
    for i, (x, y) in enumerate(pts_2d):
        if 0 <= x < W and 0 <= y < H:
            cv2.circle(frame, (int(x), int(y)), 5, 200, -1)
            cv2.circle(frame, (int(x), int(y)), 6, 150, 1)
    return frame, pts_2d

# Visual odometry simulation
estimated_trajectory = [np.zeros(3)]
true_trajectory = []
frame_imgs = []

for t in range(N_FRAMES):
    pose = get_camera_pose(t)
    true_trajectory.append(pose)
    frame, pts_2d = make_frame(pose)
    frame_imgs.append(frame)

# Estimate trajectory with accumulated noise (visual odometry drift)
for t in range(1, N_FRAMES):
    prev_pose = get_camera_pose(t-1)
    curr_pose = get_camera_pose(t)
    delta = curr_pose - prev_pose
    # Add drift noise
    delta_noisy = delta + np.random.randn(3) * 0.05
    estimated_trajectory.append(estimated_trajectory[-1] + delta_noisy)

true_trajectory = np.array(true_trajectory)
estimated_trajectory = np.array(estimated_trajectory)

# Feature tracking GIF
frames_gif = []
lk_params = dict(winSize=(15,15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT, 10, 0.03))
feature_params = dict(maxCorners=30, qualityLevel=0.3, minDistance=10, blockSize=7)

old_frame = frame_imgs[0]
p0 = cv2.goodFeaturesToTrack(old_frame, mask=None, **feature_params)
colors_track = [tuple(np.random.randint(50,255,3).tolist()) for _ in range(30)]
track_history = {i: [tuple(p0[i,0].astype(int))] for i in range(len(p0))}

for fi in range(0, min(20, N_FRAMES), 2):
    if fi > 0:
        p1, st, _ = cv2.calcOpticalFlowPyrLK(frame_imgs[fi-2], frame_imgs[fi], p0, None, **lk_params)
        if p1 is not None and st is not None:
            good_new = p1[st==1]; good_old = p0[st==1]
            for j, new in enumerate(good_new[:len(p0)]):
                if j < len(track_history):
                    track_history[j].append(tuple(new.ravel().astype(int)))
            p0 = good_new.reshape(-1,1,2) if len(good_new)>0 else p0

    frame_color = cv2.cvtColor(frame_imgs[fi], cv2.COLOR_GRAY2BGR)
    for j, traj in enumerate(list(track_history.values())[:15]):
        col = colors_track[j] if j<len(colors_track) else (0,255,0)
        for k in range(1, len(traj)):
            if traj[k-1] and traj[k]:
                cv2.line(frame_color, traj[k-1], traj[k], col, 2)
        if traj:
            cv2.circle(frame_color, traj[-1], 5, col, -1)
    cv2.putText(frame_color, f'Frame {fi}', (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    fig_f, ax_f = plt.subplots(figsize=(6,4.5), facecolor='#0a0a1a')
    ax_f.imshow(cv2.cvtColor(frame_color, cv2.COLOR_BGR2RGB))
    ax_f.set_title(f'Visual SLAM — Feature Tracking (frame {fi})', color='white')
    ax_f.axis('off')
    buf = io.BytesIO()
    fig_f.savefig(buf, format='png', dpi=72, bbox_inches='tight', facecolor=fig_f.get_facecolor())
    plt.close(fig_f)
    buf.seek(0)
    frames_gif.append(Image.open(buf).copy())

if frames_gif:
    frames_gif[0].save('../media/slam_feature_tracking.gif', save_all=True,
                       append_images=frames_gif[1:], duration=150, loop=0)
    print("Saved: slam_feature_tracking.gif")

# Plot 2: Trajectory comparison (top view)
fig2, axes2 = plt.subplots(1, 2, figsize=(13, 5), facecolor='#0a0a1a')
fig2.suptitle('Visual SLAM — Trayectoria Estimada vs Real (Visual Odometry)', color='white', fontsize=12, fontweight='bold')

for ax in axes2:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

axes2[0].plot(true_trajectory[:,0], true_trajectory[:,2], color='#4e4', linewidth=2, label='Trayectoria real')
axes2[0].plot(estimated_trajectory[:,0], estimated_trajectory[:,2], color='#f84', linewidth=2,
              linestyle='--', label='Odometría visual (estimada)')
axes2[0].plot(*true_trajectory[0,[0,2]], 'g*', markersize=15)
axes2[0].plot(*true_trajectory[-1,[0,2]], 'r*', markersize=15)
axes2[0].set_xlabel('X (m)', color='gray'); axes2[0].set_ylabel('Z (m)', color='gray')
axes2[0].set_title('Vista superior: trayectoria real vs estimada', color='white')
axes2[0].legend(facecolor='#0d0d2a', labelcolor='white')
axes2[0].set_aspect('equal')

# Drift error over time
error = np.linalg.norm(true_trajectory - estimated_trajectory, axis=1)
axes2[1].plot(range(N_FRAMES), error, color='#e44', linewidth=2)
axes2[1].fill_between(range(N_FRAMES), error, alpha=0.2, color='#e44')
axes2[1].set_xlabel('Frame', color='gray'); axes2[1].set_ylabel('Error de posición (m)', color='gray')
axes2[1].set_title('Drift acumulado de odometría visual', color='white')
axes2[1].text(N_FRAMES//2, max(error)*0.8, f'Error final: {error[-1]:.2f}m',
              ha='center', color='white', fontsize=11)

plt.tight_layout()
fig2.savefig('../media/slam_trajectory_comparison.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: slam_trajectory_comparison.png")
print("All media generated for semana_13_7")
