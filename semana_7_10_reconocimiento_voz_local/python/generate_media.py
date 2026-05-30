#!/usr/bin/env python3
"""Generate media for semana_7_10 voice recognition."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Plot 1: Simulated audio waveform + command recognition
COMMANDS = ['rojo', 'azul', 'girar', 'iniciar', 'detener', 'verde', 'ampliar']
COLORS = {'rojo': '#e44', 'azul': '#44e', 'girar': '#4ae', 'iniciar': '#4e4',
          'detener': '#e44', 'verde': '#4e4', 'ampliar': '#f84'}

fig, axes = plt.subplots(2, 1, figsize=(12, 8), facecolor='#0a0a1a')
fig.suptitle('Reconocimiento de Voz Local — speech_recognition (Simulado)', color='white', fontsize=13, fontweight='bold')

for ax in axes:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values():
        spine.set_color('#333')

# Simulated audio waveform with command regions
t = np.linspace(0, 5, 5000)
audio = np.zeros_like(t)
cmd_times = [0.5, 1.3, 2.1, 2.9, 3.7, 4.3]
cmd_words = COMMANDS[:len(cmd_times)]

for ct in cmd_times:
    mask = (t >= ct) & (t < ct + 0.4)
    audio[mask] = np.random.randn(mask.sum()) * (0.5 + np.sin((t[mask]-ct)*20) * 0.3)
audio += np.random.randn(len(t)) * 0.03  # background noise

axes[0].plot(t, audio, color='#4af', linewidth=0.5, alpha=0.8)
axes[0].set_ylabel('Amplitud', color='gray')
axes[0].set_title('Señal de Audio (micrófono simulado)', color='white')

for ct, word in zip(cmd_times, cmd_words):
    color = COLORS.get(word, '#fff')
    axes[0].axvspan(ct, ct + 0.4, alpha=0.2, color=color)
    axes[0].text(ct + 0.2, 0.8, word, ha='center', fontsize=9, color=color,
                transform=axes[0].get_xaxis_transform())

# Command timeline
timeline_data = [(ct, word) for ct, word in zip(cmd_times, cmd_words)]
axes[1].set_xlim(0, 5)
axes[1].set_ylim(-0.5, 1.5)
axes[1].set_xlabel('Tiempo (s)', color='gray')
axes[1].set_title('Timeline de Comandos Reconocidos', color='white')
axes[1].axhline(0.5, color='#333', linewidth=1)

for ct, word in timeline_data:
    color = COLORS.get(word, '#fff')
    axes[1].annotate('', xy=(ct + 0.2, 0.5), xytext=(ct + 0.2, 1.1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    axes[1].text(ct + 0.2, 1.2, word, ha='center', fontsize=10, color=color, fontweight='bold')
    axes[1].add_patch(plt.Rectangle((ct, 0.3), 0.4, 0.4, color=color, alpha=0.3))

plt.tight_layout()
fig.savefig('../media/voice_recognition_timeline.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: voice_recognition_timeline.png")

# Plot 2: Visual response to commands (animated GIF)
frames = []
BG_COLORS = {'rojo': (180,30,30), 'azul': (30,60,180), 'verde': (30,150,50),
             'girar': (30,100,140), 'iniciar': (50,150,50), 'detener': (150,30,30)}

for i, (ct, word) in enumerate(timeline_data + [('', 'idle')]):
    bg = BG_COLORS.get(word, (20, 20, 60))
    color = COLORS.get(word, '#888')

    fig2, ax2 = plt.subplots(figsize=(7, 5), facecolor='#{:02x}{:02x}{:02x}'.format(*[max(10,c//4) for c in bg]))
    ax2.set_facecolor('#{:02x}{:02x}{:02x}'.format(*[max(10,c//4) for c in bg]))
    ax2.set_xlim(-2, 2); ax2.set_ylim(-2, 2); ax2.axis('off')
    ax2.set_title(f'🎤 Comando: "{word}"' if word != 'idle' else '🎤 Escuchando...', color='white', fontsize=13)

    # Visual object responding to command
    angle = i * 45 if word == 'girar' else 0
    size = 1.4 if word == 'ampliar' else 0.8
    circle_color = color
    circle = plt.Circle((0, 0), size, color=circle_color, alpha=0.7)
    ax2.add_patch(circle)
    ax2.text(0, 0, word[:3].upper() if word != 'idle' else '...', ha='center', va='center',
             fontsize=18, color='white', fontweight='bold')
    action_map = {"rojo":"color rojo","azul":"color azul","verde":"color verde","girar":"rotar objeto","iniciar":"iniciar animación","detener":"detener","ampliar":"zoom in"}
    ax2.text(0, -1.7, f'Acción: {action_map.get(word, "esperando")}',
             ha='center', fontsize=10, color='#aaa')

    buf = io.BytesIO()
    fig2.savefig(buf, format='png', dpi=80, bbox_inches='tight', facecolor=fig2.get_facecolor())
    plt.close(fig2)
    buf.seek(0)
    frames.append(Image.open(buf).copy())

frames[0].save('../media/voice_visual_response.gif', save_all=True,
               append_images=frames[1:], duration=700, loop=0)
print("Saved: voice_visual_response.gif")
print("All media generated for semana_7_10")
