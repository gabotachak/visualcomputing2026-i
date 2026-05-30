#!/usr/bin/env python3
"""Semana 12_7: Stable Diffusion diffusers simulation."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate SD denoising process (latent space noise -> image)
def make_noisy_image(noise_level, w=256, h=256):
    """Simulate image at different denoising steps."""
    # Start: pure noise; end: coherent image
    base = np.zeros((h, w, 3), dtype=np.float32)
    # "Coherent" scene: blue sky, green hills, orange sunset
    base[:h//3, :] = [0.4, 0.6, 0.9]   # sky
    base[h//3:2*h//3, :] = [0.3, 0.7, 0.3]  # hills
    base[2*h//3:, :] = [0.8, 0.5, 0.2]  # foreground

    # Add gaussian details
    for _ in range(5):
        cx, cy = np.random.randint(20, w-20), np.random.randint(20, h-20)
        r = np.random.randint(5, 25)
        yy, xx = np.ogrid[:h, :w]
        mask = (xx-cx)**2 + (yy-cy)**2 < r**2
        color = np.random.rand(3) * 0.5 + 0.25
        base[mask] = base[mask] * 0.7 + color * 0.3

    noise = np.random.randn(h, w, 3) * noise_level
    result = np.clip(base + noise, 0, 1)
    return (result * 255).astype(np.uint8)

# Simulate denoising steps
TIMESTEPS = [1000, 800, 600, 400, 200, 100, 50, 0]
step_images = [make_noisy_image(1 - t/1000 * 0.95) for t in TIMESTEPS]

# Plot 1: Denoising process
fig, axes = plt.subplots(1, len(TIMESTEPS), figsize=(16, 3), facecolor='#0a0a1a')
fig.suptitle('Stable Diffusion — Proceso de Denoising Paso a Paso', color='white', fontsize=13, fontweight='bold')

for ax, img, t in zip(axes, step_images, TIMESTEPS):
    ax.set_facecolor('#0d0d2a')
    ax.imshow(img)
    ax.set_title(f't={t}', color='white', fontsize=9)
    ax.axis('off')

plt.tight_layout()
fig.savefig('../media/sd_denoising_steps.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: sd_denoising_steps.png")

# Plot 2: Prompt influence + sampling comparison
PROMPTS = [
    'sunset landscape, digital art',
    'oil painting mountains',
    'cyberpunk city night',
    'watercolor forest',
]

prompt_images = []
for i, prompt in enumerate(PROMPTS):
    # Different color palettes to simulate different prompts
    palettes = [
        ([0.9, 0.5, 0.2], [0.3, 0.2, 0.1]),   # sunset
        ([0.5, 0.7, 0.9], [0.2, 0.5, 0.2]),   # mountains
        ([0.1, 0.1, 0.3], [0.7, 0.1, 0.8]),   # cyberpunk
        ([0.3, 0.6, 0.2], [0.6, 0.8, 0.4]),   # forest
    ]
    h, w = 200, 200
    img = np.zeros((h, w, 3), dtype=np.float32)
    sky_col, ground_col = palettes[i]
    img[:h//2, :] = sky_col
    img[h//2:, :] = ground_col
    noise = np.random.randn(h, w, 3) * 0.08
    img = np.clip(img + noise, 0, 1)
    img = (img * 255).astype(np.uint8)
    # Smooth
    import cv2
    img = cv2.GaussianBlur(img, (5, 5), 0)
    prompt_images.append(img)

fig2, axes2 = plt.subplots(2, len(PROMPTS), figsize=(14, 6), facecolor='#0a0a1a')
fig2.suptitle('Stable Diffusion — Influencia del Prompt y Samplers', color='white', fontsize=12, fontweight='bold')

SAMPLERS = ['DDIM (25 steps)', 'PNDM (20 steps)', 'Euler-A (20 steps)', 'DPM++ (15 steps)']
for j, (img, prompt) in enumerate(zip(prompt_images, PROMPTS)):
    axes2[0][j].imshow(img)
    axes2[0][j].set_title(f'"{prompt[:20]}..."', color='white', fontsize=8)
    axes2[0][j].axis('off')
    axes2[0][j].set_facecolor('#0d0d2a')

# Sampler comparison (speed vs quality)
speeds = [20, 25, 18, 12]
qualities = [0.82, 0.80, 0.85, 0.87]
for j, (ax, sampler, speed, quality) in enumerate(zip(axes2[1], SAMPLERS, speeds, qualities)):
    ax.set_facecolor('#0d0d2a')
    ax.axis('off')
    ax.text(0.5, 0.7, sampler, ha='center', va='center', color='#4af',
            fontsize=9, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.45, f'{speed}s/img', ha='center', va='center', color='#f84',
            fontsize=11, transform=ax.transAxes)
    ax.text(0.5, 0.2, f'FID: {quality:.2f}', ha='center', va='center', color='#4e4',
            fontsize=11, transform=ax.transAxes)

plt.tight_layout()
fig2.savefig('../media/sd_prompts_samplers.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: sd_prompts_samplers.png")
print("All media generated for semana_12_7")
