#!/usr/bin/env python3
"""Semana 10_3: Optical flow and motion tracking simulation."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate a sequence of frames with moving objects
def make_frame(t, w=400, h=300):
    frame = np.full((h, w), 40, dtype=np.uint8)
    # Moving circle
    cx = int(50 + t * 2.5)
    cy = int(150 + 50 * np.sin(t * 0.2))
    cv2.circle(frame, (cx % w, cy), 30, 200, -1)
    # Another moving object
    cx2 = int(300 - t * 1.5)
    cy2 = int(100 + 30 * np.cos(t * 0.3))
    cv2.rectangle(frame, (cx2 % w - 20, cy2 - 20), (cx2 % w + 20, cy2 + 20), 160, -1)
    # Add slight noise
    frame = cv2.add(frame, np.random.randint(0, 15, frame.shape, dtype=np.uint8))
    return frame

# Generate frames
n_frames = 50
frames = [make_frame(t) for t in range(n_frames)]

# Lucas-Kanade sparse optical flow
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
feature_params = dict(maxCorners=50, qualityLevel=0.3, minDistance=7, blockSize=7)

# Initial frame and points
old_frame = frames[0]
p0 = cv2.goodFeaturesToTrack(old_frame, mask=None, **feature_params)

# Track over frames
trajectories = {i: [tuple(p0[i,0].astype(int))] for i in range(len(p0))}
colors = [tuple(np.random.randint(50, 255, 3).tolist()) for _ in range(len(p0))]

result_frame = cv2.cvtColor(frames[20], cv2.COLOR_GRAY2BGR)

for i in range(1, 21):
    new_frame = frames[i]
    if p0 is None or len(p0) == 0:
        break
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_frame, new_frame, p0, None, **lk_params)
    if p1 is None:
        break
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    for j, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel().astype(int)
        c, d = old.ravel().astype(int)
        if j < len(trajectories):
            trajectories[j].append((a, b))

    old_frame = new_frame.copy()
    p0 = good_new.reshape(-1, 1, 2)

# Draw trajectories on result frame
for j, traj in enumerate(list(trajectories.values())[:15]):
    col = colors[j] if j < len(colors) else (0, 255, 0)
    for k in range(1, len(traj)):
        if traj[k-1] and traj[k]:
            cv2.line(result_frame, traj[k-1], traj[k], col, 2)
    if traj:
        cv2.circle(result_frame, traj[-1], 5, col, -1)

# Dense optical flow (Farneback)
frame_a = frames[10]
frame_b = frames[15]
flow = cv2.calcOpticalFlowFarneback(frame_a, frame_b, None, 0.5, 3, 15, 3, 5, 1.2, 0)
mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
hsv = np.zeros((frames[0].shape[0], frames[0].shape[1], 3), dtype=np.uint8)
hsv[..., 0] = ang * 180 / np.pi / 2
hsv[..., 1] = 255
hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
dense_flow_rgb = cv2.cvtColor(cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2RGB)

# Plot 1: LK sparse + dense flow
fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor='#0a0a1a')
fig.suptitle('Flujo Óptico — Sparse (Lucas-Kanade) y Dense (Farneback)', color='white', fontsize=13, fontweight='bold')

axes[0][0].imshow(frames[0], cmap='gray')
axes[0][0].set_title('Frame inicial con puntos detectados', color='white')
if p0 is not None:
    init_pts = cv2.goodFeaturesToTrack(frames[0], mask=None, **feature_params)
    if init_pts is not None:
        for pt in init_pts:
            x, y = pt.ravel().astype(int)
            axes[0][0].plot(x, y, 'g.', markersize=5)

axes[0][1].imshow(cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB))
axes[0][1].set_title('Trayectorias LK (20 frames)', color='white')

axes[1][0].imshow(frame_a, cmap='gray')
axes[1][0].set_title('Frame A (para flujo denso)', color='white')

axes[1][1].imshow(dense_flow_rgb)
axes[1][1].set_title('Flujo denso Farneback\n(color=dirección, brillo=magnitud)', color='white')

for ax_row in axes:
    for ax in ax_row:
        ax.axis('off')
        ax.set_facecolor('#0d0d2a')

plt.tight_layout()
fig.savefig('../media/optical_flow_comparison.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: optical_flow_comparison.png")

# Generate animated GIF of tracking
anim_frames = []
old_frame = frames[0]
p0_anim = cv2.goodFeaturesToTrack(old_frame, mask=None, **feature_params)
if p0_anim is None:
    p0_anim = np.array([[[100., 150.]], [[300., 100.]]], dtype=np.float32)
track_history = {i: [tuple(p0_anim[i,0].astype(int))] for i in range(len(p0_anim))}

for fi in range(0, min(25, n_frames), 2):
    if fi > 0:
        p1_anim, st_anim, _ = cv2.calcOpticalFlowPyrLK(frames[fi-2], frames[fi], p0_anim, None, **lk_params)
        if p1_anim is not None and st_anim is not None:
            good_new_a = p1_anim[st_anim == 1]
            good_old_a = p0_anim[st_anim == 1]
            for j, new in enumerate(good_new_a[:len(p0_anim)]):
                if j < len(track_history):
                    track_history[j].append(tuple(new.ravel().astype(int)))
            p0_anim = good_new_a.reshape(-1, 1, 2) if len(good_new_a) > 0 else p0_anim

    frame_color = cv2.cvtColor(frames[fi], cv2.COLOR_GRAY2BGR)
    for j, traj in enumerate(list(track_history.values())[:10]):
        col = colors[j] if j < len(colors) else (0, 255, 0)
        for k in range(1, len(traj)):
            if traj[k-1] and traj[k]:
                cv2.line(frame_color, traj[k-1], traj[k], col, 2)
        if traj:
            cv2.circle(frame_color, traj[-1], 6, col, -1)

    cv2.putText(frame_color, f'Frame {fi}', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    fig2, ax2 = plt.subplots(figsize=(6, 4.5), facecolor='#0a0a1a')
    ax2.set_facecolor('#0d0d2a')
    ax2.imshow(cv2.cvtColor(frame_color, cv2.COLOR_BGR2RGB))
    ax2.set_title(f'LK Tracking — Frame {fi}', color='white')
    ax2.axis('off')
    buf = io.BytesIO()
    fig2.savefig(buf, format='png', dpi=72, bbox_inches='tight', facecolor=fig2.get_facecolor())
    plt.close(fig2)
    buf.seek(0)
    anim_frames.append(Image.open(buf).copy())

if anim_frames:
    anim_frames[0].save('../media/optical_flow_tracking.gif', save_all=True,
                        append_images=anim_frames[1:], duration=100, loop=0)
    print("Saved: optical_flow_tracking.gif")

print("All media generated for semana_10_3")
