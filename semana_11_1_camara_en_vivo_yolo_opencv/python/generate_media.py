#!/usr/bin/env python3
"""Semana 11_1: YOLO real-time detection simulation."""
import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Simulate a YOLO detection result on a synthetic frame
COCO_CLASSES = ['person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck',
                'chair', 'couch', 'potted plant', 'laptop', 'cell phone', 'book']
COLORS = [(np.random.randint(80,255), np.random.randint(80,255), np.random.randint(80,255))
          for _ in COCO_CLASSES]

def make_fake_frame(w=640, h=480, t=0):
    frame = np.zeros((h, w, 3), dtype=np.uint8)
    frame[:] = (15, 20, 30)
    # Simulated background
    for i in range(0, w, 40):
        cv2.line(frame, (i, 0), (i, h), (25, 30, 45), 1)
    for j in range(0, h, 40):
        cv2.line(frame, (0, j), (w, j), (25, 30, 45), 1)
    return frame

def draw_yolo_detections(frame, detections):
    result = frame.copy()
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        cls = det['class']
        conf = det['confidence']
        color = COLORS[COCO_CLASSES.index(cls) % len(COLORS)]
        cv2.rectangle(result, (x1, y1), (x2, y2), color, 2)
        label = f"{cls} {conf:.2f}"
        (lw, lh), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(result, (x1, y1-lh-4), (x1+lw, y1), color, -1)
        cv2.putText(result, label, (x1, y1-2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    return result

# Simulated detections
frame = make_fake_frame()
# Add some objects
cv2.rectangle(frame, (50, 100), (180, 380), (60, 80, 100), -1)   # person
cv2.ellipse(frame, (130, 90), (45, 45), 0, 0, 360, (80, 100, 120), -1)  # head
cv2.rectangle(frame, (250, 200), (450, 400), (40, 70, 90), -1)   # couch
cv2.rectangle(frame, (480, 150), (590, 280), (50, 80, 60), -1)   # laptop
cv2.rectangle(frame, (300, 50), (400, 150), (70, 50, 80), -1)    # chair

detections = [
    {'bbox': (45, 85, 185, 390), 'class': 'person', 'confidence': 0.92},
    {'bbox': (245, 195, 455, 410), 'class': 'couch', 'confidence': 0.87},
    {'bbox': (475, 145, 595, 285), 'class': 'laptop', 'confidence': 0.81},
    {'bbox': (295, 45, 405, 155), 'class': 'chair', 'confidence': 0.73},
]

result_frame = draw_yolo_detections(frame, detections)

# Add FPS overlay
fps = 42.3
h, w = frame.shape[:2]
cv2.putText(result_frame, f'FPS: {fps:.1f}', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
cv2.putText(result_frame, f'Objects: {len(detections)}', (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
cv2.putText(result_frame, 'YOLOv8n | Press: G=gray F=filter P=pause', (10, h-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

# Plot 1: Detection result
fig, axes = plt.subplots(1, 3, figsize=(15, 5), facecolor='#0a0a1a')
fig.suptitle('YOLO en Tiempo Real — Detección de Objetos con Webcam (Simulado)', color='white', fontsize=13, fontweight='bold')

axes[0].imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
axes[0].set_title('Frame original', color='white')
axes[0].axis('off')

axes[1].imshow(cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB))
axes[1].set_title(f'YOLO detections ({len(detections)} objetos, {fps:.0f} FPS)', color='white')
axes[1].axis('off')

# Canny overlay (filter mode)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
axes[2].imshow(edges, cmap='gray')
axes[2].set_title('Modo filtro: Canny edges (tecla F)', color='white')
axes[2].axis('off')

for ax in axes:
    ax.set_facecolor('#0d0d2a')

plt.tight_layout()
fig.savefig('../media/yolo_detection_result.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Saved: yolo_detection_result.png")

# Plot 2: Class distribution + FPS simulation
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0a0a1a')
fig2.suptitle('Métricas de Detección YOLO', color='white', fontsize=12, fontweight='bold')

for ax in axes2:
    ax.set_facecolor('#0d0d2a')
    ax.tick_params(colors='gray')
    for spine in ax.spines.values(): spine.set_color('#333')

# Object count per class (simulated 100 frames)
classes_detected = ['person', 'car', 'chair', 'laptop', 'couch', 'cell phone', 'book', 'bicycle']
counts = [145, 89, 67, 54, 43, 38, 21, 15]
colors_bar = [f'#{np.random.randint(80,200):02x}{np.random.randint(80,200):02x}{np.random.randint(80,200):02x}' for _ in classes_detected]

axes2[0].barh(classes_detected, counts, color=colors_bar, alpha=0.8)
axes2[0].set_xlabel('Detecciones (100 frames)', color='gray')
axes2[0].set_title('Objetos detectados por clase', color='white')
for i, v in enumerate(counts):
    axes2[0].text(v+1, i, str(v), color='white', va='center', fontsize=9)

# FPS over time
t_fps = np.arange(100)
fps_data = 40 + 5 * np.sin(t_fps * 0.3) + np.random.randn(100) * 2
axes2[1].plot(t_fps, fps_data, color='#4af', linewidth=1.5)
axes2[1].fill_between(t_fps, fps_data, 20, alpha=0.2, color='#4af')
axes2[1].axhline(30, color='yellow', linestyle='--', linewidth=1, label='Target 30 FPS')
axes2[1].set_xlabel('Frame', color='gray')
axes2[1].set_ylabel('FPS', color='gray')
axes2[1].set_title('FPS a lo largo del tiempo', color='white')
axes2[1].legend(facecolor='#0d0d2a', labelcolor='white')
axes2[1].set_ylim(0, 55)

plt.tight_layout()
fig2.savefig('../media/yolo_performance_metrics.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: yolo_performance_metrics.png")
print("All media generated for semana_11_1")
