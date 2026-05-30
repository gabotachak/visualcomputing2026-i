#!/usr/bin/env python3
"""Generate media for semana_7_7 multimodal interfaces (voice + gestures)."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image, ImageDraw
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Plot 1: System architecture diagram
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0a0a1a')
ax.set_facecolor('#0a0a1a')
ax.set_xlim(0, 12); ax.set_ylim(0, 6)
ax.axis('off')
ax.set_title('Arquitectura del Sistema Multimodal — Voz + Gestos', color='white', fontsize=13, fontweight='bold')

def draw_box(ax, x, y, w, h, label, sublabel, color, text_color='white'):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                               facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.85)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.65, label, ha='center', va='center', color=text_color, fontsize=10, fontweight='bold')
    ax.text(x + w/2, y + h*0.3, sublabel, ha='center', va='center', color='#ccc', fontsize=8)

def draw_arrow(ax, x1, y1, x2, y2, label='', color='white'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my+0.1, label, ha='center', fontsize=8, color=color)

# Input sources
draw_box(ax, 0.3, 4.0, 2.2, 1.4, '📷 Cámara Web', 'MediaPipe Hands', '#1a3a6e')
draw_box(ax, 0.3, 2.0, 2.2, 1.4, '🎤 Micrófono', 'speech_recognition', '#3a1a6e')

# Processing
draw_box(ax, 4.0, 4.0, 2.5, 1.4, '🖐 Detección\nde Gestos', 'Landmark tracking', '#1e5e3e')
draw_box(ax, 4.0, 2.0, 2.5, 1.4, '🗣️ Reconocimiento\nde Voz', 'CMU Sphinx / Google', '#5e1e3e')

# Logic
draw_box(ax, 7.2, 2.8, 2.5, 1.8, '🧠 Lógica\nMultimodal', 'Condiciones combinadas', '#5e4e1e')

# Output
draw_box(ax, 10.0, 2.8, 1.7, 1.8, '🎨 Escena\nVisual', 'pygame / tkinter', '#1e3e5e')

# Arrows
draw_arrow(ax, 2.5, 4.7, 4.0, 4.7, 'landmarks', '#4af')
draw_arrow(ax, 2.5, 2.7, 4.0, 2.7, 'texto', '#a4e')
draw_arrow(ax, 6.5, 4.7, 7.2, 3.9, 'gesto', '#4e4')
draw_arrow(ax, 6.5, 2.7, 7.2, 3.5, 'comando', '#f84')
draw_arrow(ax, 9.7, 3.7, 10.0, 3.7, 'acción', '#4af')

# Condition example
ax.text(7.2, 1.8, 'Ejemplo: mano_abierta AND "cambiar"\n→ cambiar escena', ha='left',
        fontsize=9, color='#aaa', style='italic')

plt.tight_layout()
fig.savefig('../media/multimodal_architecture.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: multimodal_architecture.png")

# Plot 2: Animated demo of multimodal interaction
STATES = [
    ('mano_abierta', None, 'Esperando comando...', (30,30,60), '5 dedos'),
    ('mano_abierta', 'cambiar', '¡Cambiar escena!', (30,80,30), '5 dedos + voz'),
    ('dos_dedos', None, 'Gesto: 2 dedos', (30,30,60), '2 dedos'),
    ('dos_dedos', 'mover', '¡Mover objeto!', (80,80,20), '2 dedos + voz'),
    ('puño', None, 'Gesto: puño', (30,30,60), '0 dedos'),
    ('puño', 'stop', '¡Detener!', (120,30,30), '0 dedos + voz'),
]

frames = []
for gesture, voice, action, bg, gesture_label in STATES:
    bg_hex = '#{:02x}{:02x}{:02x}'.format(*[max(10, c//3) for c in bg])
    action_color = '#4e4' if 'Cambiar' in action or 'Mover' in action or 'Detener' in action else '#888'

    fig2, axes2 = plt.subplots(1, 2, figsize=(10, 5), facecolor=bg_hex)
    fig2.suptitle('Sistema Multimodal en Acción', color='white', fontsize=12, fontweight='bold')

    ax_status, ax_scene = axes2
    ax_status.set_facecolor('#0d0d2a'); ax_status.axis('off')
    ax_status.set_title('Entradas detectadas', color='gray')

    # Status boxes
    g_color = '#4af' if voice else '#555'
    v_color = '#a4e' if voice else '#555'
    ax_status.text(0.5, 0.8, f'🖐 Gesto: {gesture_label}', ha='center', fontsize=12,
                   color=g_color, transform=ax_status.transAxes, fontweight='bold')
    ax_status.text(0.5, 0.6, f'🎤 Voz: "{voice}"' if voice else '🎤 Voz: (ninguna)',
                   ha='center', fontsize=12, color=v_color, transform=ax_status.transAxes)
    ax_status.text(0.5, 0.35, '→ ' + action, ha='center', fontsize=13,
                   color=action_color, transform=ax_status.transAxes, fontweight='bold')

    # Scene visualization
    ax_scene.set_facecolor('#0d0d2a')
    ax_scene.set_xlim(-2, 2); ax_scene.set_ylim(-2, 2); ax_scene.axis('off')
    ax_scene.set_title('Escena visual', color='gray')
    size = 1.2 if 'Mover' in action else 0.8
    c = '#{:02x}{:02x}{:02x}'.format(*[min(255, c) for c in bg])
    circle = plt.Circle((0, 0), size, color=c if c != '#1e1e3c' else '#4af', alpha=0.8)
    ax_scene.add_patch(circle)
    ax_scene.text(0, 0, gesture[0].upper(), ha='center', va='center', fontsize=20, color='white', fontweight='bold')

    buf = io.BytesIO()
    fig2.savefig(buf, format='png', dpi=80, bbox_inches='tight', facecolor=fig2.get_facecolor())
    plt.close(fig2)
    buf.seek(0)
    frames.append(Image.open(buf).copy())

frames[0].save('../media/multimodal_interaction_demo.gif', save_all=True,
               append_images=frames[1:], duration=1000, loop=0)
print("Saved: multimodal_interaction_demo.gif")
print("All media generated for semana_7_7")
