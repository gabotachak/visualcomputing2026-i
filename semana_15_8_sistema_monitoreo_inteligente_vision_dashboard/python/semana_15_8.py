import os
import time
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def run_monitoring_dashboard():
    # Make directories
    os.makedirs('../media', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    print("Initializing Smart Monitoring System...")
    time.sleep(0.5)

    # 1. Log simulation events to CSV
    log_file_path = 'logs/monitoring_log.csv'
    events = [
        {"timestamp": "2026-05-29 23:50:01", "event": "Person detected", "confidence": 0.92, "zone": "Entrada"},
        {"timestamp": "2026-05-29 23:50:14", "event": "Person detected", "confidence": 0.88, "zone": "Entrada"},
        {"timestamp": "2026-05-29 23:51:02", "event": "Backpack detected", "confidence": 0.74, "zone": "Pasillo A"},
        {"timestamp": "2026-05-29 23:52:45", "event": "Intrusion Alert!", "confidence": 0.96, "zone": "Bodega"},
        {"timestamp": "2026-05-29 23:53:10", "event": "Person detected", "confidence": 0.82, "zone": "Pasillo A"}
    ]

    with open(log_file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Event", "Confidence", "Zone"])
        for ev in events:
            writer.writerow([ev["timestamp"], ev["event"], ev["confidence"], ev["zone"]])
            
    print(f"Logged {len(events)} security events to {log_file_path}")

    # 2. Draw mock dashboard video feed (OpenCV frame simulation)
    feed_img = Image.new('RGB', (800, 500), color='#101018')
    draw = ImageDraw.Draw(feed_img)
    
    # Draw camera grid / scanner lines
    for i in range(0, 800, 80):
        draw.line([i, 0, i, 500], fill='#1e1e24')
    for j in range(0, 500, 80):
        draw.line([0, j, 800, j], fill='#1e1e24')

    # Draw simulated intruder in Bodega zone
    # Bounding box
    draw.rectangle([320, 120, 480, 420], outline='#ff3333', width=4)
    # Target label
    draw.rectangle([320, 90, 480, 120], fill='#ff3333')
    draw.text((330, 95), "INTRUDER: 96%", fill='#ffffff')
    
    # Draw some "Bodega" background boxes
    draw.rectangle([60, 200, 180, 450], fill='#2d2d3a', outline='#444')
    draw.rectangle([620, 250, 740, 450], fill='#2d2d3a', outline='#444')
    
    # Camera metadata overlays
    draw.text((15, 15), "CAM_04: BODEGA - LIVE STREAM", fill='#33ff33')
    draw.text((15, 35), "FPS: 29.8 | RESOLUTION: 1920x1080", fill='#888')
    draw.text((620, 15), "STATUS: ⚠️ ALERT", fill='#ff3333')
    draw.text((620, 35), "2026-05-29 23:52:45", fill='#888')

    feed_img.save('../media/dashboard_feed.png')
    print("Saved simulated camera feed to media/dashboard_feed.png")

    # 3. Draw dashboard analytics chart using Matplotlib
    timestamps = ["23:48", "23:49", "23:50", "23:51", "23:52", "23:53"]
    person_counts = [1, 2, 2, 1, 3, 2]
    alert_counts = [0, 0, 0, 0, 1, 0]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(timestamps, person_counts, marker='o', color='#a4e', label='Personas Detectadas', linewidth=2)
    ax.bar(timestamps, alert_counts, color='#ff3333', alpha=0.6, label='Alertas de Intrusión', width=0.4)
    
    ax.set_xlabel('Tiempo (Minutos)')
    ax.set_ylabel('Recuento / Frecuencia')
    ax.set_title('Métricas de Monitoreo y Eventos de Seguridad')
    ax.set_ylim(0, 4)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    fig.tight_layout()
    fig.savefig('../media/dashboard_analytics.png', dpi=150)
    plt.close()
    print("Saved security analytics chart to media/dashboard_analytics.png")

if __name__ == '__main__':
    run_monitoring_dashboard()
