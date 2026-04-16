import { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface TextureDisplayProps {
  texture: THREE.Texture;
  label: string;
}

export default function TextureDisplay({ texture, label }: TextureDisplayProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const src = texture.image as HTMLCanvasElement | null;
    if (!src) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(src, 0, 0, canvas.width, canvas.height);
  }, [texture]);

  const src = texture.image as HTMLCanvasElement | null;
  const size = src ? `${src.width}×${src.height}` : '–';

  return (
    <div className="texture-canvas-wrapper">
      <span className="texture-preview-title">{label}</span>
      <canvas ref={canvasRef} width={200} height={200} />
      <span className="texture-info">Size: {size}px</span>
    </div>
  );
}
