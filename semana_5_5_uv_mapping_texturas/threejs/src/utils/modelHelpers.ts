import * as THREE from 'three';

export function createBoxCorrectUV(): THREE.BufferGeometry {
  // BoxGeometry already has correct UVs by default.
  // Each face occupies a rectangular region in UV space.
  const geometry = new THREE.BoxGeometry(2, 2, 2);
  return geometry;
}

export function createBoxStretchedUV(): THREE.BufferGeometry {
  const geometry = new THREE.BoxGeometry(2, 2, 2);
  const uvAttribute = geometry.getAttribute('uv');
  const uvArray = uvAttribute.array as Float32Array;

  // Multiply all U coordinates by 2 to stretch the texture horizontally.
  for (let i = 0; i < uvArray.length; i += 2) {
    uvArray[i] *= 2.0;
  }

  uvAttribute.needsUpdate = true;
  return geometry;
}

export function createSphereOverlappingUV(): THREE.BufferGeometry {
  const geometry = new THREE.SphereGeometry(1, 32, 32);
  const uvAttribute = geometry.getAttribute('uv');
  const uvArray = uvAttribute.array as Float32Array;

  // Map to only 1/4 of UV space — causes the texture to tile 4x,
  // making seams and overlapping regions clearly visible.
  for (let i = 0; i < uvArray.length; i += 2) {
    uvArray[i] *= 0.5;
    uvArray[i + 1] *= 0.5;
  }

  uvAttribute.needsUpdate = true;
  return geometry;
}
