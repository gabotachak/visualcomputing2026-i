#!/usr/bin/env python3
"""Generate media for semana_7_11 real-time data visualization."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Plot 1: Simulated real-time line chart (multiple signals)
fig, axes = plt.subplots(2, 1, figsize=(12, 8), facecolor='#0a0a1a')
fig.suptitle('Visualización de Datos en Tiempo Real — Señales Simuladas', color='white', fontsize=13, fontweight='bold')

t = np.linspace(0, 10, 500)
signals = {
    'Temperatura (°C)': (20 + 5 * np.sin(t * 0.8) + np.random.randn(500) * 0.5, '#f84'),
    'Pulso (bpm)': (70 + 10 * np.sin(t * 1.2 + 1) + np.random.randn(500) * 2, '#e44'),
    'Actividad Alpha (µV)': (2 + 1.5 * np.sin(t * 2.5) + np.random.randn(500) * 0.3, '#4e4'),
    'Actividad Beta (µV)': (0.8 + 0.5 * np.cos(t * 4) + np.random.randn(500) * 0.2, '#4af'),
}

for ax in axes:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values():
        spine.set_color('#333')

signal_items = list(signals.items())
for i, (label, (data, color)) in enumerate(signal_items[:2]):
    axes[i].plot(t, data, color=color, linewidth=1.5, label=label)
    axes[i].fill_between(t, data, alpha=0.15, color=color)
    axes[i].set_ylabel(label, color='gray', fontsize=10)
    axes[i].legend(loc='upper right', facecolor='#0d0d2a', labelcolor='white')
    axes[i].grid(True, alpha=0.1, color='gray')

axes[1].set_xlabel('Tiempo (s)', color='gray')
plt.tight_layout()
fig.savefig('../media/realtime_line_chart.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: realtime_line_chart.png")

# Plot 2: Bar chart with rolling window + stats
fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
fig.suptitle('Dashboard de Métricas en Tiempo Real', color='white', fontsize=13, fontweight='bold')

for ax in axes:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values():
        spine.set_color('#333')

# Simulated object count over time (like YOLO detector)
counts = np.clip(np.random.poisson(5, 30) + np.sin(np.arange(30) * 0.5) * 2, 0, 15).astype(int)
colors = ['#4e4' if c > 5 else '#f84' if c > 2 else '#e44' for c in counts]
axes[0].bar(range(len(counts)), counts, color=colors, alpha=0.8)
axes[0].axhline(counts.mean(), color='yellow', linestyle='--', linewidth=1.5, label=f'Media: {counts.mean():.1f}')
axes[0].set_xlabel('Frame', color='gray')
axes[0].set_ylabel('Objetos detectados', color='gray')
axes[0].set_title('Conteo de Objetos (simulado YOLO)', color='white')
axes[0].legend(facecolor='#0d0d2a', labelcolor='white')

# Rolling average
window = 5
rolling_avg = np.convolve(counts, np.ones(window)/window, mode='valid')
rolling_x = range(window-1, len(counts))
axes[0].plot(rolling_x, rolling_avg, color='cyan', linewidth=2, label=f'Media móvil ({window}f)')
axes[0].legend(facecolor='#0d0d2a', labelcolor='white')

# Histogram of all signals
for (label, (data, color)) in list(signals.items()):
    data_norm = (data - data.min()) / (data.max() - data.min() + 1e-8)
    axes[1].hist(data_norm, bins=30, alpha=0.5, color=color, label=label[:15], density=True)
axes[1].set_xlabel('Valor normalizado', color='gray')
axes[1].set_ylabel('Densidad', color='gray')
axes[1].set_title('Distribución de Señales', color='white')
axes[1].legend(facecolor='#0d0d2a', labelcolor='white', fontsize=8)

plt.tight_layout()
fig.savefig('../media/realtime_dashboard_stats.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: realtime_dashboard_stats.png")

# Generate animated GIF of live chart
frames = []
n_frames = 20
data_line = 20 + 5 * np.sin(np.linspace(0, 8, 200)) + np.random.randn(200) * 0.5

for i in range(n_frames):
    fig2, ax2 = plt.subplots(figsize=(8, 4), facecolor='#0a0a1a')
    ax2.set_facecolor('#0d0d2a')
    ax2.tick_params(colors='gray')
    for spine in ax2.spines.values():
        spine.set_color('#333')

    end = 20 + i * 9  # sliding window
    start = max(0, end - 80)
    x = np.arange(start, min(end, 200))
    y = data_line[start:min(end, 200)]

    ax2.plot(x / 20, y, color='#4af', linewidth=2)
    ax2.fill_between(x / 20, y, 15, alpha=0.2, color='#4af')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(12, 28)
    ax2.set_xlabel('Tiempo (s)', color='gray')
    ax2.set_ylabel('Temperatura (°C)', color='gray')
    ax2.set_title(f'Temperatura en tiempo real — t={x[-1]/20:.1f}s', color='white')
    ax2.axhline(20, color='yellow', linestyle='--', alpha=0.5, linewidth=1)
    ax2.grid(True, alpha=0.1, color='gray')

    buf = io.BytesIO()
    fig2.savefig(buf, format='png', dpi=80, bbox_inches='tight', facecolor=fig2.get_facecolor())
    plt.close(fig2)
    buf.seek(0)
    frames.append(Image.open(buf).copy())

frames[0].save('../media/realtime_animation.gif', save_all=True,
               append_images=frames[1:], duration=150, loop=0)
print("Saved: realtime_animation.gif")
print("All media generated for semana_7_11")
