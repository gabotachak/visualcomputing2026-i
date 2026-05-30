#!/usr/bin/env python3
"""Generate media for semana_7_2 BCI simulation."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal
import os

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate EEG signal
fs = 256  # Hz
duration = 4  # seconds
t = np.linspace(0, duration, fs * duration)

# Compose EEG: alpha (10 Hz) + beta (20 Hz) + noise
alpha = 2.0 * np.sin(2 * np.pi * 10 * t)
beta = 0.8 * np.sin(2 * np.pi * 20 * t)
noise = np.random.randn(len(t)) * 0.5
eeg = alpha + beta + noise

# Bandpass filters
def bandpass(data, low, high, fs):
    b, a = signal.butter(4, [low / (fs/2), high / (fs/2)], btype='band')
    return signal.filtfilt(b, a, data)

alpha_filtered = bandpass(eeg, 8, 12, fs)
beta_filtered = bandpass(eeg, 12, 30, fs)

# Plot 1: Raw EEG + filtered bands
fig, axes = plt.subplots(3, 1, figsize=(12, 8), facecolor='#0a0a1a')
fig.suptitle('Señales EEG Simuladas — BCI', color='white', fontsize=14, fontweight='bold')

for ax in axes:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values():
        spine.set_color('#333')

axes[0].plot(t, eeg, color='#4af', linewidth=0.8, label='EEG raw')
axes[0].set_ylabel('Amplitud (µV)', color='gray')
axes[0].legend(loc='upper right', facecolor='#0d0d2a', labelcolor='white')
axes[0].set_title('Señal EEG Bruta', color='white', fontsize=11)

axes[1].plot(t, alpha_filtered, color='#4e4', linewidth=1.2, label='Alpha (8–12 Hz)')
axes[1].set_ylabel('Amplitud (µV)', color='gray')
axes[1].legend(loc='upper right', facecolor='#0d0d2a', labelcolor='white')
axes[1].set_title('Banda Alpha Filtrada', color='white', fontsize=11)

axes[2].plot(t, beta_filtered, color='#f84', linewidth=1.2, label='Beta (12–30 Hz)')
axes[2].set_xlabel('Tiempo (s)', color='gray')
axes[2].set_ylabel('Amplitud (µV)', color='gray')
axes[2].legend(loc='upper right', facecolor='#0d0d2a', labelcolor='white')
axes[2].set_title('Banda Beta Filtrada', color='white', fontsize=11)

plt.tight_layout()
fig.savefig('../media/eeg_signals_filtered.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: eeg_signals_filtered.png")

# Plot 2: Power spectrum + attention indicator
window_size = fs  # 1 second windows
attention_levels = []
time_points = []
for i in range(0, len(eeg) - window_size, window_size // 4):
    seg = eeg[i:i + window_size]
    freqs, psd = signal.welch(seg, fs, nperseg=window_size)
    alpha_power = np.trapezoid(psd[(freqs >= 8) & (freqs <= 12)], freqs[(freqs >= 8) & (freqs <= 12)])
    beta_power = np.trapezoid(psd[(freqs >= 12) & (freqs <= 30)], freqs[(freqs >= 12) & (freqs <= 30)])
    attention = beta_power / (alpha_power + 1e-6)
    attention_levels.append(attention)
    time_points.append(t[i + window_size // 2])

threshold = np.percentile(attention_levels, 60)
activated = [a > threshold for a in attention_levels]

fig, axes = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
fig.suptitle('Análisis BCI — Nivel de Atención Simulado', color='white', fontsize=13, fontweight='bold')

for ax in axes:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values():
        spine.set_color('#333')

# Power spectrum
freqs_full, psd_full = signal.welch(eeg, fs, nperseg=fs)
axes[0].fill_between(freqs_full[(freqs_full >= 8) & (freqs_full <= 12)],
                     psd_full[(freqs_full >= 8) & (freqs_full <= 12)], alpha=0.5, color='#4e4', label='Alpha')
axes[0].fill_between(freqs_full[(freqs_full >= 12) & (freqs_full <= 30)],
                     psd_full[(freqs_full >= 12) & (freqs_full <= 30)], alpha=0.5, color='#f84', label='Beta')
axes[0].plot(freqs_full[:60], psd_full[:60], color='#4af', linewidth=1.2)
axes[0].set_xlabel('Frecuencia (Hz)', color='gray')
axes[0].set_ylabel('PSD (µV²/Hz)', color='gray')
axes[0].set_title('Espectro de Potencia', color='white')
axes[0].legend(facecolor='#0d0d2a', labelcolor='white')

# Attention level over time
colors = ['#4e4' if a else '#e44' for a in activated]
axes[1].bar(time_points, attention_levels, color=colors, alpha=0.8, width=0.22)
axes[1].axhline(threshold, color='yellow', linestyle='--', linewidth=1.5, label=f'Umbral ({threshold:.2f})')
axes[1].set_xlabel('Tiempo (s)', color='gray')
axes[1].set_ylabel('Índice Beta/Alpha', color='gray')
axes[1].set_title('Nivel de Atención Simulado', color='white')
axes[1].legend(facecolor='#0d0d2a', labelcolor='white')

plt.tight_layout()
fig.savefig('../media/bci_attention_analysis.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: bci_attention_analysis.png")
print("All media generated for semana_7_2")
