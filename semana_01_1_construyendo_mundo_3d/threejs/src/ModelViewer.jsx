import React, { useMemo, useEffect, useState } from 'react'
import { Edges } from '@react-three/drei'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader'
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader'

export default function ModelViewer({ src = '/models/scene.obj', mode = 'solid', onLoaded }) {
  const [meshes, setMeshes] = useState(null)

  useEffect(() => {
    let mounted = true
    const ext = (src.split('.').pop() || '').toLowerCase()

    const ensureIndex = (geom) => {
      if (!geom.index) {
        const count = geom.attributes.position ? geom.attributes.position.count : 0
        const idx = new (count > 65535 ? Uint32Array : Uint16Array)(count)
        for (let i = 0; i < count; i++) idx[i] = i
        geom.setIndex(new THREE.BufferAttribute(idx, 1))
      }
    }

    if (ext === 'glb' || ext === 'gltf') {
      const loader = new GLTFLoader()
      loader.load(
        src,
        (gltf) => {
          if (!mounted) return
          const list = []
          gltf.scene.traverse((child) => {
            if (child.isMesh) {
              const geom = child.geometry.clone()
              ensureIndex(geom)
              list.push({ name: child.name || 'mesh', geometry: geom })
            }
          })
          setMeshes(list)
        },
        undefined,
        (err) => console.error('GLTF load error', err)
      )
    } else if (ext === 'obj') {
      const loader = new OBJLoader()
      loader.load(
        src,
        (obj) => {
          if (!mounted) return
          const list = []
          obj.traverse((child) => {
            if (child.isMesh) {
              const geom = child.geometry.clone()
              ensureIndex(geom)
              list.push({ name: child.name || 'mesh', geometry: geom })
            }
          })
          setMeshes(list)
        },
        undefined,
        (err) => console.error('OBJ load error', err)
      )
    } else if (ext === 'stl') {
      const loader = new STLLoader()
      loader.load(
        src,
        (geometry) => {
          if (!mounted) return
          const geom = geometry.isBufferGeometry ? geometry.clone() : new THREE.BufferGeometry().fromGeometry(geometry)
          ensureIndex(geom)
          setMeshes([{ name: 'stl', geometry: geom }])
        },
        undefined,
        (err) => console.error('STL load error', err)
      )
    } else {
      setMeshes(null)
    }

    return () => {
      mounted = false
    }
  }, [src])

  useEffect(() => {
    if (!meshes) return
    let vertices = 0
    let faces = 0
    let meshesCount = 0
    meshes.forEach((m) => {
      const pos = m.geometry.attributes.position
      vertices += pos ? pos.count : 0
      faces += m.geometry.index ? m.geometry.index.count / 3 : pos ? pos.count / 3 : 0
      meshesCount++
    })
    onLoaded && onLoaded({ vertices, faces, meshes: meshesCount })
  }, [meshes, onLoaded])

  if (!meshes || meshes.length === 0) {
    return (
      <mesh>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial color="#8aa" />
      </mesh>
    )
  }

  return (
    <group>
      {meshes.map((m, idx) => {
        if (mode === 'points') {
          return (
            <points key={idx} geometry={m.geometry}>
              <pointsMaterial size={0.02} color={'orange'} />
            </points>
          )
        }

        return (
          <mesh key={idx} geometry={m.geometry} castShadow receiveShadow>
            <meshStandardMaterial color={'#c0c0c0'} wireframe={mode === 'wireframe'} />
            {mode === 'edges' && <Edges threshold={15} />}
          </mesh>
        )
      })}
    </group>
  )
}
