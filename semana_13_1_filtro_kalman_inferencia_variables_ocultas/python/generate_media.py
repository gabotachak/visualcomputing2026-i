#!/usr/bin/env python3
"""Semana 13_1: Kalman filter for 1D and 2D position estimation."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# 1D Kalman Filter
class KalmanFilter1D:
    def __init__(self, q=0.01, r=1.0, x0=0, p0=1):
        self.q = q  # process noise
        self.r = r  # measurement noise
        self.x = x0  # state estimate
        self.p = p0  # estimate covariance

    def update(self, z):
        # Predict
        self.p += self.q
        # Update
        k = self.p / (self.p + self.r)
        self.x += k * (z - self.x)
        self.p *= (1 - k)
        return self.x

# Simulate 1D tracking
N = 100
true_pos = np.cumsum(np.random.randn(N) * 0.3) + np.sin(np.arange(N) * 0.1) * 5
measured = true_pos + np.random.randn(N) * 2  # noisy measurements

kf = KalmanFilter1D(q=0.05, r=4.0)
estimates = [kf.update(z) for z in measured]

# 2D Kalman filter (constant velocity model)
dt = 1.0
F = np.array([[1,0,dt,0],[0,1,0,dt],[0,0,1,0],[0,0,0,1]])  # state transition
H = np.array([[1,0,0,0],[0,1,0,0]])  # measurement matrix
Q = np.eye(4) * 0.1  # process noise
R = np.eye(2) * 3.0  # measurement noise
x2d = np.zeros(4)
P2d = np.eye(4) * 10

# Simulate 2D trajectory (spiral)
t = np.linspace(0, 4*np.pi, N)
true_x2d = np.column_stack([5*np.cos(t), 5*np.sin(t)])
meas_x2d = true_x2d + np.random.randn(N, 2) * 2

estimates_2d = []
for z in meas_x2d:
    # Predict
    x2d = F @ x2d
    P2d = F @ P2d @ F.T + Q
    # Update
    y = z - H @ x2d
    S = H @ P2d @ H.T + R
    K = P2d @ H.T @ np.linalg.inv(S)
    x2d = x2d + K @ y
    P2d = (np.eye(4) - K @ H) @ P2d
    estimates_2d.append(x2d[:2].copy())
estimates_2d = np.array(estimates_2d)

# Plot 1: 1D tracking
fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor='#0a0a1a')
fig.suptitle('Filtro de Kalman — Estimación de Variables Ocultas', color='white', fontsize=13, fontweight='bold')

for ax in axes:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

axes[0].plot(true_pos, color='#4e4', linewidth=2, label='Posición real (oculta)')
axes[0].scatter(range(N), measured, c='#e44', s=8, alpha=0.6, label='Mediciones ruidosas')
axes[0].plot(estimates, color='#4af', linewidth=2, label='Estimación Kalman')
axes[0].set_xlabel('Tiempo', color='gray'); axes[0].set_ylabel('Posición', color='gray')
axes[0].set_title('Filtro de Kalman 1D — Tracking de posición', color='white')
axes[0].legend(facecolor='#0d0d2a', labelcolor='white', fontsize=9)

# MSE comparison
mse_raw = np.mean((measured - true_pos)**2)
mse_kalman = np.mean((np.array(estimates) - true_pos)**2)
axes[0].text(0.02, 0.02, f'MSE medición: {mse_raw:.2f}\nMSE Kalman: {mse_kalman:.2f}',
             transform=axes[0].transAxes, color='white', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='#1a1a3e', alpha=0.8))

axes[1].plot(true_x2d[:,0], true_x2d[:,1], color='#4e4', linewidth=2, label='Trayectoria real')
axes[1].scatter(meas_x2d[:,0], meas_x2d[:,1], c='#e44', s=10, alpha=0.4, label='Mediciones GPS')
axes[1].plot(estimates_2d[:,0], estimates_2d[:,1], color='#4af', linewidth=2, label='Estimación Kalman 2D')
axes[1].set_xlabel('X', color='gray'); axes[1].set_ylabel('Y', color='gray')
axes[1].set_title('Filtro de Kalman 2D — Trayectoria (modelo vel. constante)', color='white')
axes[1].legend(facecolor='#0d0d2a', labelcolor='white', fontsize=9)
axes[1].set_aspect('equal')

plt.tight_layout()
fig.savefig('../media/kalman_filter_tracking.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: kalman_filter_tracking.png")

# Plot 2: Kalman gain and covariance convergence
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
fig2.suptitle('Análisis del Filtro de Kalman — Ganancia y Covarianza', color='white', fontsize=12, fontweight='bold')
for ax in axes2:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

kf2 = KalmanFilter1D(q=0.05, r=4.0)
gains, covs = [], []
for z in measured:
    kf2.p += kf2.q
    k = kf2.p / (kf2.p + kf2.r)
    gains.append(k)
    kf2.x += k * (z - kf2.x)
    kf2.p *= (1 - k)
    covs.append(kf2.p)

axes2[0].plot(gains, color='#f84', linewidth=2)
axes2[0].set_xlabel('Iteración', color='gray'); axes2[0].set_ylabel('Ganancia K', color='gray')
axes2[0].set_title('Ganancia de Kalman (converge a valor óptimo)', color='white')

axes2[1].plot(covs, color='#4af', linewidth=2)
axes2[1].set_xlabel('Iteración', color='gray'); axes2[1].set_ylabel('Covarianza P', color='gray')
axes2[1].set_title('Covarianza de estimación (converge = confianza)', color='white')

plt.tight_layout()
fig2.savefig('../media/kalman_gain_covariance.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: kalman_gain_covariance.png")
print("All media generated for semana_13_1")
