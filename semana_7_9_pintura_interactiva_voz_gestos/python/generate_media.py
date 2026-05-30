#!/usr/bin/env python3
"""Generate media for semana_7_9 interactive painting with voice+gestures."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate a painting canvas with brush strokes from hand tracking
WIDTH, HEIGHT = 640, 480

def make_canvas_frame(strokes, bg_color=(10, 10, 26)):
    img = Image.new('RGB', (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)
    for stroke in strokes:
        pts = stroke['points']
        color = stroke['color']
        width = stroke['width']
        if len(pts) > 1:
            for i in range(len(pts) - 1):
                draw.line([pts[i], pts[i+1]], fill=color, width=width)
    return img

# Generate spiral brush stroke paths
def spiral_stroke(cx, cy, r_max, turns, n=80):
    angles = np.linspace(0, turns * 2 * np.pi, n)
    radii = np.linspace(0, r_max, n)
    return [(int(cx + r * np.cos(a)), int(cy + r * np.sin(a))) for r, a in zip(radii, angles)]

COLORS = [(78, 170, 255), (78, 220, 78), (255, 130, 50), (200, 78, 255), (255, 220, 78)]

base_strokes = [
    {'points': spiral_stroke(200, 200, 80, 3), 'color': COLORS[0], 'width': 4},
    {'points': spiral_stroke(440, 200, 60, 2), 'color': COLORS[1], 'width': 3},
    {'points': spiral_stroke(320, 350, 70, 2.5), 'color': COLORS[2], 'width': 5},
    {'points': [(100+i*3, 380 - int(30*np.sin(i*0.3))) for i in range(130)], 'color': COLORS[3], 'width': 6},
    {'points': [(320+int(100*np.cos(i*0.1)), 240+int(80*np.sin(i*0.13))) for i in range(90)], 'color': COLORS[4], 'width': 3},
]

# Plot 1: Final painting result
canvas = make_canvas_frame(base_strokes)
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), facecolor='#0a0a1a')
fig.suptitle('Pintura Interactiva con Voz y Gestos (Simulado)', color='white', fontsize=13, fontweight='bold')

axes[0].imshow(canvas)
axes[0].axis('off')
axes[0].set_title('Lienzo — pintado con dedo índice', color='white')

# Simulated command panel
axes[1].set_facecolor('#0d0d2a')
axes[1].axis('off')
axes[1].set_title('Comandos de Voz Activos', color='white')

commands = [
    ('🔴 "rojo"', COLORS[2], 'Color: rojo'),
    ('🟢 "verde"', COLORS[1], 'Color: verde'),
    ('🔵 "azul"', COLORS[0], 'Color: azul'),
    ('🗑️ "limpiar"', (150,150,150), 'Limpia canvas'),
    ('💾 "guardar"', (200,200,100), 'Guarda imagen'),
    ('✏️ Dedo índice', (255,255,255), 'Pinta en pantalla'),
]

for i, (cmd, col, desc) in enumerate(commands):
    y = 0.85 - i * 0.14
    c_hex = '#{:02x}{:02x}{:02x}'.format(*col)
    axes[1].text(0.05, y, cmd, color=c_hex, fontsize=13, fontweight='bold',
                 transform=axes[1].transAxes, va='center')
    axes[1].text(0.55, y, desc, color='#aaa', fontsize=11,
                 transform=axes[1].transAxes, va='center')

plt.tight_layout()
fig.savefig('../media/painting_canvas_result.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: painting_canvas_result.png")

# Plot 2: Animated GIF showing painting in progress
frames = []
cumulative_strokes = []
all_points = [(s['color'], s['width'], p, i)
              for s in base_strokes for i, p in enumerate(s['points'])]
all_points_by_stroke = []
for s in base_strokes:
    all_points_by_stroke.append(s)

for frame_i in range(16):
    progress = (frame_i + 1) / 16
    visible_strokes = []
    for stroke in base_strokes:
        n = max(2, int(len(stroke['points']) * progress))
        visible_strokes.append({**stroke, 'points': stroke['points'][:n]})

    canvas_frame = make_canvas_frame(visible_strokes)
    # Overlay simulated hand landmark (index finger tip)
    last_point = None
    for stroke in visible_strokes:
        if stroke['points']:
            last_point = stroke['points'][-1]

    if last_point:
        draw = ImageDraw.Draw(canvas_frame)
        x, y = last_point
        draw.ellipse([x-8, y-8, x+8, y+8], fill=(255,255,100), outline=(255,255,255), width=2)

    # Add voice command overlay
    if frame_i % 4 == 0:
        cmds = ['rojo', 'verde', 'azul', 'limpiar']
        draw = ImageDraw.Draw(canvas_frame)
        cmd = cmds[(frame_i // 4) % len(cmds)]
        draw.rectangle([5, 5, 140, 35], fill=(0, 0, 0, 180))
        draw.text((10, 10), f'🎤 "{cmd}"', fill=(255, 220, 50))

    fig2, ax2 = plt.subplots(figsize=(8, 6), facecolor='#0a0a1a')
    ax2.imshow(canvas_frame)
    ax2.axis('off')
    ax2.set_title(f'Pintando... {int(progress*100)}%', color='white')
    buf = io.BytesIO()
    fig2.savefig(buf, format='png', dpi=72, bbox_inches='tight', facecolor=fig2.get_facecolor())
    plt.close(fig2)
    buf.seek(0)
    frames.append(Image.open(buf).copy())

frames[0].save('../media/painting_process.gif', save_all=True,
               append_images=frames[1:], duration=250, loop=0)
print("Saved: painting_process.gif")
print("All media generated for semana_7_9")
