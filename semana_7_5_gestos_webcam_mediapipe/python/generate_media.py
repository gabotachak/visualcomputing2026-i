#!/usr/bin/env python3
"""Generate simulation media for semana_7_5 MediaPipe gesture detection."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate hand landmark visualization
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),     # thumb
    (0,5),(5,6),(6,7),(7,8),     # index
    (5,9),(9,10),(10,11),(11,12), # middle
    (9,13),(13,14),(14,15),(15,16), # ring
    (13,17),(17,18),(18,19),(19,20), # pinky
    (0,17),
]

def simulate_hand_landmarks(gesture='open', cx=0.5, cy=0.5):
    """Simulate normalized 21 hand landmarks for a given gesture."""
    # Base hand shape (closed fist roughly)
    base = np.array([
        [0.5, 0.9],  # 0: wrist
        [0.4, 0.75], # 1: thumb CMC
        [0.35, 0.65],# 2: thumb MCP
        [0.3, 0.58], # 3: thumb IP
        [0.27, 0.52],# 4: thumb tip
        [0.5, 0.7],  # 5: index MCP
        [0.5, 0.58], # 6: index PIP
        [0.5, 0.48], # 7: index DIP
        [0.5, 0.4],  # 8: index tip
        [0.55, 0.68],# 9: middle MCP
        [0.55, 0.56],# 10: middle PIP
        [0.55, 0.46],# 11: middle DIP
        [0.55, 0.38],# 12: middle tip
        [0.6, 0.68], # 13: ring MCP
        [0.6, 0.58], # 14: ring PIP
        [0.6, 0.5],  # 15: ring DIP
        [0.6, 0.44], # 16: ring tip
        [0.65, 0.72],# 17: pinky MCP
        [0.65, 0.63],# 18: pinky PIP
        [0.65, 0.56],# 19: pinky DIP
        [0.65, 0.5], # 20: pinky tip
    ])

    if gesture == 'closed':
        # Curl all fingers
        for i in [6,7,8,10,11,12,14,15,16,18,19,20]:
            base[i,1] += 0.12
    elif gesture == 'peace':
        # Only index and middle extended
        pass  # base is peace-like
    elif gesture == 'pointing':
        # Only index extended
        for i in [10,11,12,14,15,16,18,19,20]:
            base[i,1] += 0.1

    # Center around (cx, cy)
    base[:,0] = base[:,0] - 0.5 + cx
    base[:,1] = base[:,1] - 0.65 + cy
    return base

# Plot 1: Gesture detection demo
fig, axes = plt.subplots(1, 3, figsize=(14, 5), facecolor='#0a0a1a')
fig.suptitle('MediaPipe Hands — Detección de Gestos (Simulado)', color='white', fontsize=13, fontweight='bold')

gestures = [('open', 'Palma Abierta\n→ Cambiar Escena', '#4af', 0.5, 0.5),
            ('pointing', 'Señalando\n→ Mover Objeto', '#4e4', 0.5, 0.5),
            ('closed', 'Puño Cerrado\n→ Acción Especial', '#f84', 0.5, 0.5)]

for ax, (gesture, label, color, cx, cy) in zip(axes, gestures):
    ax.set_facecolor('#111')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(label, color=color, fontsize=10)

    lms = simulate_hand_landmarks(gesture, cx, cy)
    # Draw connections
    for a, b in HAND_CONNECTIONS:
        ax.plot([lms[a,0], lms[b,0]], [1-lms[a,1], 1-lms[b,1]],
                color='white', linewidth=2, alpha=0.6)
    # Draw landmarks
    ax.scatter(lms[:,0], 1-lms[:,1], c=color, s=40, zorder=5)
    # Fingertip highlights
    for tip in [4, 8, 12, 16, 20]:
        ax.scatter(lms[tip,0], 1-lms[tip,1], c='white', s=80, zorder=6)

    # Simulated frame border
    ax.add_patch(plt.Rectangle((0,0), 1, 1, fill=False, edgecolor=color, linewidth=3))

plt.tight_layout()
fig.savefig('../media/gesture_detection_demo.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: gesture_detection_demo.png")

# Plot 2: Finger count + visual feedback
frames = []
n_frames = 16
for frame_i in range(n_frames):
    t = frame_i / n_frames
    finger_count = int(t * 5) % 6  # cycles 0-5

    fig2, axes2 = plt.subplots(1, 2, figsize=(10, 5), facecolor='#0a0a1a')
    fig2.suptitle(f'Detección de Dedos — {finger_count} dedos extendidos', color='white', fontsize=12)

    ax_hand, ax_fb = axes2
    ax_hand.set_facecolor('#111')
    ax_hand.set_xlim(0, 1); ax_hand.set_ylim(0, 1)
    ax_hand.set_aspect('equal')
    ax_hand.axis('off')
    ax_hand.set_title('Vista de mano', color='gray')

    gesture = 'open' if finger_count >= 4 else 'pointing' if finger_count >= 1 else 'closed'
    lms = simulate_hand_landmarks(gesture)
    for a, b in HAND_CONNECTIONS:
        ax_hand.plot([lms[a,0], lms[b,0]], [1-lms[a,1], 1-lms[b,1]], color='white', linewidth=1.5, alpha=0.5)
    ax_hand.scatter(lms[:,0], 1-lms[:,1], c='#4af', s=30)

    ax_fb.set_facecolor('#0d0d2a')
    ax_fb.axis('off')
    ax_fb.set_title('Acción ejecutada', color='gray')
    actions = ['Sin acción', 'Mover →', 'Zoom', 'Rotar', 'Cambiar color', 'Palma: Reset']
    action = actions[finger_count]
    color = ['#e44', '#4af', '#4e4', '#f84', '#a4e', '#4af'][finger_count]
    ax_fb.text(0.5, 0.6, f'{finger_count}', ha='center', va='center',
               fontsize=60, color=color, fontweight='bold')
    ax_fb.text(0.5, 0.25, action, ha='center', va='center',
               fontsize=16, color='white')

    buf = io.BytesIO()
    fig2.savefig(buf, format='png', dpi=80, bbox_inches='tight', facecolor=fig2.get_facecolor())
    plt.close(fig2)
    buf.seek(0)
    frames.append(Image.open(buf).copy())

frames[0].save('../media/gesture_finger_count.gif', save_all=True,
               append_images=frames[1:], duration=300, loop=0)
print("Saved: gesture_finger_count.gif")
print("All media generated for semana_7_5")
