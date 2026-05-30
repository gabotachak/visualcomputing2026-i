import os
import json
import time
import math

def run_monitor():
    threejs_public_dir = '../threejs/public'
    os.makedirs(threejs_public_dir, exist_ok=True)
    os.makedirs('../media', exist_ok=True)

    print("Running activity monitor generator...")

    # We will simulate a continuous feed. For the static delivery, we write one sample
    # representing active coordinates of tracked objects.
    timestamp = time.time()
    
    # 4 monitored zones with activity counts
    monitor_data = {
        "timestamp": timestamp,
        "active_count": 8,
        "zones": [
            { "id": 1, "name": "Entrada", "activity": 0.85, "coordinates": [-1.5, 0, -1.0] },
            { "id": 2, "name": "Pasillo A", "activity": 0.35, "coordinates": [-0.5, 0, 1.2] },
            { "id": 3, "name": "Oficina Principal", "activity": 0.95, "coordinates": [1.0, 0, -0.5] },
            { "id": 4, "name": "Bodega", "activity": 0.12, "coordinates": [0.2, 0, -2.0] }
        ]
    }

    # Write JSON to public folder
    json_path = os.path.join(threejs_public_dir, 'monitor_data.json')
    with open(json_path, 'w') as f:
        json.dump(monitor_data, f, indent=2)
    print(f"Saved monitor data to {json_path}")

    # Generate a dummy plot of the historical activity to save to media
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    zones = [z['name'] for z in monitor_data['zones']]
    activities = [z['activity'] * 100 for z in monitor_data['zones']]
    colors = ['#ff3333' if a > 80 else '#f84' if a > 30 else '#33ff33' for a in activities]

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(zones, activities, color=colors, edgecolor='#333', width=0.5)
    ax.set_ylabel('Nivel de Actividad (%)')
    ax.set_title('Monitoreo de Actividad por Zona - Sensor de Visión')
    ax.set_ylim(0, 100)
    ax.bar_label(bars, fmt='%.0f%%')
    
    fig.tight_layout()
    fig.savefig('../media/activity_chart.png', dpi=150)
    plt.close()
    print("Saved activity history chart to media.")

if __name__ == '__main__':
    run_monitor()
