import os
import json
import time

def simulate_detection():
    # Target folders
    threejs_public_dir = '../threejs/public'
    os.makedirs(threejs_public_dir, exist_ok=True)
    os.makedirs('../media', exist_ok=True)

    print("Simulating visual AI detection...")
    time.sleep(1.0) # Simulate CPU time

    # Mock detection result objects
    # Coordinates normalized for a 3D coordinate system where the image plane is at z = -2, w = 4, h = 3
    detection_data = {
        "timestamp": "2026-05-29T23:45:00Z",
        "image_width": 800,
        "image_height": 600,
        "detections": [
            {
                "class": "laptop",
                "confidence": 0.94,
                "position": [0.0, -0.4, -2.0], # x, y, z
                "scale": [1.2, 0.8, 0.2]       # w, h, d
            },
            {
                "class": "cup",
                "confidence": 0.82,
                "position": [0.9, -0.5, -1.8],
                "scale": [0.25, 0.35, 0.25]
            },
            {
                "class": "person",
                "confidence": 0.89,
                "position": [-1.1, 0.3, -2.5],
                "scale": [0.8, 1.8, 0.5]
            }
        ]
    }

    # Write detections.json to Vite public directory
    json_path = os.path.join(threejs_public_dir, 'detections.json')
    with open(json_path, 'w') as f:
        json.dump(detection_data, f, indent=2)
    
    print(f"Exported detections.json to {json_path}")

    # Generate a dummy annotated image in public folder and media folder
    # We can create a simple canvas representing the detection HUD
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (800, 600), color='#1e1e2e')
    draw = ImageDraw.Draw(img)
    
    # Draw mock background grid
    for i in range(0, 800, 40):
        draw.line([i, 0, i, 600], fill='#2d2d3f')
    for j in range(0, 600, 40):
        draw.line([0, j, 800, j], fill='#2d2d3f')
        
    # Draw detections on 2D image
    # Laptop bounding box
    draw.rectangle([280, 360, 520, 480], outline='#00ffcc', width=3)
    draw.text((290, 340), "laptop: 94%", fill='#00ffcc')
    
    # Cup bounding box
    draw.rectangle([560, 400, 630, 490], outline='#f84', width=3)
    draw.text((570, 380), "cup: 82%", fill='#f84')

    # Person bounding box
    draw.rectangle([120, 100, 240, 500], outline='#a4e', width=3)
    draw.text((130, 80), "person: 89%", fill='#a4e')

    # Save to media for README reference
    img.save('../media/detection_annotated.png')
    # Save to public for web dashboard background
    img.save(os.path.join(threejs_public_dir, 'detection.png'))
    print("Saved annotated detection image.")

if __name__ == '__main__':
    simulate_detection()
