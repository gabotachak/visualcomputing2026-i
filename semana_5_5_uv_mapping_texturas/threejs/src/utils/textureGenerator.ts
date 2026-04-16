import * as THREE from 'three';

export function createCheckerboardTexture(
  size = 512,
  squareSize = 32,
  color1 = '#FFFFFF',
  color2 = '#000000'
): THREE.Texture {
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d')!;

  for (let y = 0; y < size; y += squareSize) {
    for (let x = 0; x < size; x += squareSize) {
      const isEven = (x / squareSize + y / squareSize) % 2 === 0;
      ctx.fillStyle = isEven ? color1 : color2;
      ctx.fillRect(x, y, squareSize, squareSize);
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.magFilter = THREE.NearestFilter;
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  return texture;
}

export function createGridTexture(
  size = 512,
  gridSize = 32,
  lineColor = '#FF0000',
  bgColor = '#FFFFFF'
): THREE.Texture {
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = bgColor;
  ctx.fillRect(0, 0, size, size);

  ctx.strokeStyle = lineColor;
  ctx.lineWidth = 2;
  for (let i = 0; i <= size; i += gridSize) {
    ctx.beginPath();
    ctx.moveTo(i, 0);
    ctx.lineTo(i, size);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, i);
    ctx.lineTo(size, i);
    ctx.stroke();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  return texture;
}

export function createNumberedGridTexture(size = 512, gridSize = 32): THREE.Texture {
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d')!;

  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(0, 0, size, size);

  ctx.strokeStyle = '#CCCCCC';
  ctx.lineWidth = 1;
  for (let i = 0; i <= size; i += gridSize) {
    ctx.beginPath();
    ctx.moveTo(i, 0);
    ctx.lineTo(i, size);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(0, i);
    ctx.lineTo(size, i);
    ctx.stroke();
  }

  ctx.fillStyle = '#000000';
  ctx.font = `${gridSize * 0.45}px monospace`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  let number = 0;
  for (let y = gridSize / 2; y < size; y += gridSize) {
    for (let x = gridSize / 2; x < size; x += gridSize) {
      ctx.fillText(String(number++ % 10), x, y);
    }
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  return texture;
}

export type TextureType = 'checkerboard' | 'grid' | 'numbered';

export function createTexture(type: TextureType): THREE.Texture {
  switch (type) {
    case 'checkerboard':
      return createCheckerboardTexture();
    case 'grid':
      return createGridTexture();
    case 'numbered':
      return createNumberedGridTexture();
  }
}
