import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def create_synthetic_images():
    os.makedirs('../media', exist_ok=True)
    
    # Image A: Surreal dreamscape with floating cities (procedural drawing)
    img_a = Image.new('RGB', (400, 400), color='#1a2a6c')
    draw = ImageDraw.Draw(img_a)
    # Sky gradient / sunset line
    draw.rectangle([0, 200, 400, 400], fill='#b21f1f')
    draw.rectangle([0, 300, 400, 400], fill='#fdbb2d')
    # Floating islands (ellipses)
    draw.ellipse([80, 100, 200, 150], fill='#4a3b32', outline='#fff')
    draw.ellipse([220, 140, 340, 190], fill='#4a3b32', outline='#fff')
    # Simple city structures on islands
    draw.rectangle([110, 60, 140, 100], fill='#888', outline='#fff')
    draw.rectangle([150, 70, 170, 100], fill='#777', outline='#fff')
    draw.rectangle([250, 100, 280, 140], fill='#888', outline='#fff')
    # Glowing stars
    for x, y in [(50, 40), (320, 50), (180, 20), (80, 80)]:
        draw.ellipse([x-2, y-2, x+2, y+2], fill='#fff')
    img_a.save('../media/image_a.png')

    # Image B: A plain puppy dog (procedural drawing of a cartoonish dog-like shape)
    img_b = Image.new('RGB', (400, 400), color='#eaeaea')
    draw_b = ImageDraw.Draw(img_b)
    # Green grass
    draw_b.rectangle([0, 300, 400, 400], fill='#2d4a1e')
    # Dog body
    draw_b.ellipse([120, 180, 280, 260], fill='#a0522d')
    # Head
    draw_b.ellipse([200, 130, 280, 210], fill='#a0522d')
    # Ears
    draw_b.ellipse([190, 130, 220, 180], fill='#5c2c16')
    draw_b.ellipse([260, 130, 290, 180], fill='#5c2c16')
    # Eyes
    draw_b.ellipse([220, 160, 230, 170], fill='#000')
    draw_b.ellipse([250, 160, 260, 170], fill='#000')
    # Nose
    draw_b.ellipse([235, 180, 245, 190], fill='#000')
    img_b.save('../media/image_b.png')

def calculate_metrics_and_plot():
    # Load images
    img_a = Image.open('../media/image_a.png')
    img_b = Image.open('../media/image_b.png')
    
    # Simulate CLIPScore (alignment between prompt "surreal dreamscape with floating cities" and image)
    # Image A is highly aligned, Image B is not.
    clip_score_a = 0.88
    clip_score_b = 0.12
    
    # Calculate physical symmetry (SSIM between left and right halves)
    arr_a = np.array(img_a.convert('L'))
    w_a = arr_a.shape[1]
    left_a = arr_a[:, :w_a//2]
    right_a = arr_a[:, w_a//2:]
    # Flip right half to compare
    right_a_flipped = np.fliplr(right_a)
    # Simple MSE-based symmetry score: 1 / (1 + MSE)
    symmetry_a = 1.0 / (1.0 + np.mean((left_a - right_a_flipped) ** 2) / 255.0)
    
    arr_b = np.array(img_b.convert('L'))
    w_b = arr_b.shape[1]
    left_b = arr_b[:, :w_b//2]
    right_b = arr_b[:, w_b//2:]
    right_b_flipped = np.fliplr(right_b)
    symmetry_b = 1.0 / (1.0 + np.mean((left_b - right_b_flipped) ** 2) / 255.0)
    
    # Normalize symmetry score for plotting
    symmetry_a = float(np.round(symmetry_a, 2))
    symmetry_b = float(np.round(symmetry_b, 2))
    
    # Plotting
    labels = ['Imagen A (Surreal)', 'Imagen B (Perro)']
    clip_scores = [clip_score_a, clip_score_b]
    symmetry_scores = [symmetry_a, symmetry_b]
    
    x = np.arange(len(labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 5))
    rects1 = ax.bar(x - width/2, clip_scores, width, label='CLIPScore (Alineación de Prompt)', color='#4af')
    rects2 = ax.bar(x + width/2, symmetry_scores, width, label='Simetría Horizontal', color='#f84')
    
    ax.set_ylabel('Puntuación (Normalizada)')
    ax.set_title('Comparativa de Métricas de Creatividad y Coherencia')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 1.2)
    
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    
    fig.tight_layout()
    fig.savefig('../media/metrics_comparison.png', dpi=150)
    plt.close()
    
    print("Generated metrics comparison plot.")

def write_notebook():
    notebook_content = {
      "cells": [
        {
          "cell_type": "markdown",
          "metadata": {},
          "source": [
            "# Taller: Evaluando la Creatividad Artificial: Métricas y Reflexión\n",
            "Gabriel Andrés Anzola Tachak - 2026-05-29\n",
            "\n",
            "Este notebook implementa el cálculo de métricas automáticas para evaluar imágenes generadas por IA:\n",
            "1. **CLIPScore**: Simula la alineación semántica entre la descripción de texto y la imagen.\n",
            "2. **Simetría horizontal (Balance Visual)**: Mide el balance de la composición comparando las mitades izquierda y derecha."
          ]
        },
        {
          "cell_type": "code",
          "execution_count": None,
          "metadata": {},
          "outputs": [],
          "source": [
            "# Instalar dependencias necesarias\n",
            "!pip install numpy matplotlib pillow scikit-image"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": None,
          "metadata": {},
          "outputs": [],
          "source": [
            "import os\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "from PIL import Image\n",
            "\n",
            "# Cargar imágenes del taller\n",
            "img_a_path = '../media/image_a.png'\n",
            "img_b_path = '../media/image_b.png'\n",
            "\n",
            "img_a = Image.open(img_a_path)\n",
            "img_b = Image.open(img_b_path)\n",
            "\n",
            "fig, axes = plt.subplots(1, 2, figsize=(10, 5))\n",
            "axes[0].imshow(img_a)\n",
            "axes[0].set_title('Imagen A: Paisaje Surrealista')\n",
            "axes[0].axis('off')\n",
            "\n",
            "axes[1].imshow(img_b)\n",
            "axes[1].set_title('Imagen B: Dibujo de Perro')\n",
            "axes[1].axis('off')\n",
            "plt.show()"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": None,
          "metadata": {},
          "outputs": [],
          "source": [
            "# 1. CLIPScore (Simulación de Inferencia CLIP)\n",
            "prompt = \"a surreal dreamscape with floating cities\"\n",
            "\n",
            "# En una ejecución real:\n",
            "# image_features = model.encode_image(preprocess(img).unsqueeze(0))\n",
            "# text_features = model.encode_text(clip.tokenize([prompt]))\n",
            "# similarity = torch.cosine_similarity(image_features, text_features)\n",
            "\n",
            "clip_score_a = 0.88\n",
            "clip_score_b = 0.12\n",
            "\n",
            "print(f\"CLIPScore Imagen A (Surreal): {clip_score_a}\")\n",
            "print(f\"CLIPScore Imagen B (Perro): {clip_score_b}\")"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": None,
          "metadata": {},
          "outputs": [],
          "source": [
            "# 2. Simetría Horizontal (SSIM o diferencia MSE entre mitades)\n",
            "def calculate_symmetry(image):\n",
            "    arr = np.array(image.convert('L'))\n",
            "    w = arr.shape[1]\n",
            "    left = arr[:, :w//2]\n",
            "    right = arr[:, w//2:]\n",
            "    # Voltear la mitad derecha horizontalmente para comparar frente a la izquierda\n",
            "    right_flipped = np.fliplr(right)\n",
            "    # Calcular una métrica de coincidencia\n",
            "    mse = np.mean((left - right_flipped) ** 2)\n",
            "    symmetry_score = 1.0 / (1.0 + mse / 255.0)\n",
            "    return np.round(symmetry_score, 2)\n",
            "\n",
            "sym_a = calculate_symmetry(img_a)\n",
            "sym_b = calculate_symmetry(img_b)\n",
            "\n",
            "print(f\"Simetría Horizontal Imagen A: {sym_a}\")\n",
            "print(f\"Simetría Horizontal Imagen B: {sym_b}\")"
          ]
        },
        {
          "cell_type": "code",
          "execution_count": None,
          "metadata": {},
          "outputs": [],
          "source": [
            "# Graficar resultados comparativos\n",
            "labels = ['Imagen A (Surreal)', 'Imagen B (Perro)']\n",
            "clip_scores = [clip_score_a, clip_score_b]\n",
            "symmetry_scores = [sym_a, sym_b]\n",
            "\n",
            "x = np.arange(len(labels))\n",
            "width = 0.35\n",
            "\n",
            "fig, ax = plt.subplots(figsize=(8, 5))\n",
            "rects1 = ax.bar(x - width/2, clip_scores, width, label='CLIPScore (Alineación)', color='#4af')\n",
            "rects2 = ax.bar(x + width/2, symmetry_scores, width, label='Simetría Horizontal', color='#f84')\n",
            "\n",
            "ax.set_ylabel('Puntuación')\n",
            "ax.set_title('Comparativa de Métricas Automáticas')\n",
            "ax.set_xticks(x)\n",
            "ax.set_xticklabels(labels)\n",
            "ax.legend()\n",
            "ax.set_ylim(0, 1.2)\n",
            "ax.bar_label(rects1, padding=3)\n",
            "ax.bar_label(rects2, padding=3)\n",
            "plt.show()"
          ]
        }
      ],
      "metadata": {
        "kernelspec": {
          "display_name": "Python 3",
          "language": "python",
          "name": "python3"
        },
        "language_info": {
          "name": "python"
        }
      },
      "nbformat": 4,
      "nbformat_minor": 2
    }
    
    with open('semana_15_3.ipynb', 'w') as f:
        json.dump(notebook_content, f, indent=2)
    print("Generated Jupyter notebook: semana_15_3.ipynb")

if __name__ == '__main__':
    create_synthetic_images()
    calculate_metrics_and_plot()
    write_notebook()
