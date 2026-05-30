#!/usr/bin/env python3
"""Semana 12_4: ControlNet + Stable Diffusion simulation."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

def make_synthetic_scene():
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    img[:150, :] = (120, 160, 210)  # sky
    img[150:, :] = (80, 90, 80)    # ground
    cv2.rectangle(img, (50, 150), (170, 380), (180, 120, 60), -1)
    cv2.rectangle(img, (200, 100), (360, 380), (160, 100, 50), -1)
    for y in range(170, 380, 40):
        for x in range(60, 170, 30):
            cv2.rectangle(img, (x, y), (x+18, y+28), (100, 130, 200), -1)
    for y in range(120, 380, 50):
        for x in range(210, 360, 35):
            cv2.rectangle(img, (x, y), (x+22, y+32), (80, 110, 180), -1)
    return img

scene = make_synthetic_scene()
gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
canny_edges = cv2.Canny(gray, 50, 150)

# Simulate "generated" image (stylized)
generated = scene.copy().astype(np.float32)
generated[:, :, 0] = np.clip(generated[:, :, 0] * 1.3 + 20, 0, 255)
generated[:, :, 2] = np.clip(generated[:, :, 2] * 0.7 + 10, 0, 255)
generated = cv2.GaussianBlur(generated.astype(np.uint8), (7, 7), 0)
noise = (np.random.randn(*generated.shape[:2]) * 10).astype(np.int16)
for c in range(3):
    generated[:, :, c] = np.clip(generated[:, :, c].astype(np.int16) + noise, 0, 255).astype(np.uint8)

# Plot 1: ControlNet pipeline
fig, axes = plt.subplots(1, 4, figsize=(16, 4.5), facecolor='#0a0a1a')
fig.suptitle('ControlNet + Stable Diffusion — Control Visual de Generación (Simulado)', color='white', fontsize=13, fontweight='bold')

items = [
    (cv2.cvtColor(scene, cv2.COLOR_BGR2RGB), 'Imagen original'),
    (canny_edges, 'Condición: Canny edges'),
    (cv2.cvtColor(scene, cv2.COLOR_BGR2RGB), 'Prompt + Canny → SD'),
    (cv2.cvtColor(generated, cv2.COLOR_BGR2RGB), 'Salida generada\n(estilo oil painting)'),
]

for ax, (img, lbl) in zip(axes, items):
    ax.set_facecolor('#0d0d2a')
    ax.imshow(img, cmap='gray' if img.ndim == 2 else None)
    ax.set_title(lbl, color='white', fontsize=9)
    ax.axis('off')

plt.tight_layout()
fig.savefig('../media/controlnet_pipeline.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: controlnet_pipeline.png")

# Plot 2: Compare with/without ControlNet
uncontrolled = np.random.randint(50, 200, (400, 400, 3), dtype=np.uint8)
uncontrolled = cv2.GaussianBlur(uncontrolled, (21, 21), 0)

fig2, axes2 = plt.subplots(1, 3, figsize=(13, 4.5), facecolor='#0a0a1a')
fig2.suptitle('Con vs Sin ControlNet — Control de Estructura', color='white', fontsize=12, fontweight='bold')

for ax, (img, lbl) in zip(axes2, [
    (canny_edges, 'Condición (Canny)'),
    (cv2.cvtColor(generated, cv2.COLOR_BGR2RGB), 'Con ControlNet\n(estructura preservada)'),
    (uncontrolled, 'Sin ControlNet\n(sin control de estructura)'),
]):
    ax.set_facecolor('#0d0d2a')
    ax.imshow(img, cmap='gray' if img.ndim == 2 else None)
    ax.set_title(lbl, color='white', fontsize=10)
    ax.axis('off')

plt.tight_layout()
fig2.savefig('../media/controlnet_with_without.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: controlnet_with_without.png")
print("All media generated for semana_12_4")
