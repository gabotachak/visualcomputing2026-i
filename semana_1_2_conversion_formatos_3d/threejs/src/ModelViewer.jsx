import React, { useMemo, useEffect, useState } from 'react';
import { useLoader } from '@react-three/fiber';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';
import { STLLoader } from 'three/examples/jsm/loaders/STLLoader';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import * as THREE from 'three';

export function ModelViewer({ format, url, onLoadedStats }) {
    const [model, setModel] = useState(null);

    useEffect(() => {
        let loader;
        if (format === 'OBJ') loader = new OBJLoader();
        else if (format === 'STL') loader = new STLLoader();
        else if (format === 'GLTF') loader = new GLTFLoader();

        if (!loader) return;

        loader.load(
            url,
            (object) => {
                let sceneObj = null;
                let vCount = 0;
                let pCount = 0;

                // Process based on format
                if (format === 'GLTF') {
                    sceneObj = object.scene;
                } else if (format === 'STL') {
                    // STL loads a geometry directly
                    const material = new THREE.MeshStandardMaterial({
                        color: '#3b82f6',
                        roughness: 0.4,
                        metalness: 0.6
                    });
                    sceneObj = new THREE.Mesh(object, material);
                } else {
                    // OBJ loads a Group
                    sceneObj = object;
                    sceneObj.traverse((child) => {
                        if (child.isMesh) {
                            child.material = new THREE.MeshStandardMaterial({
                                color: '#4ade80',
                                roughness: 0.5,
                                metalness: 0.2
                            });
                        }
                    });
                }

                // Calculate stats
                sceneObj.traverse((child) => {
                    if (child.isMesh) {
                        vCount += child.geometry.attributes.position.count;
                        if (child.geometry.index) {
                            pCount += child.geometry.index.count / 3;
                        } else {
                            pCount += child.geometry.attributes.position.count / 3;
                        }
                    }
                });

                // Center the model properly
                const box = new THREE.Box3().setFromObject(sceneObj);
                const center = box.getCenter(new THREE.Vector3());
                sceneObj.position.x += (sceneObj.position.x - center.x);
                sceneObj.position.y += (sceneObj.position.y - center.y);
                sceneObj.position.z += (sceneObj.position.z - center.z);

                setModel(sceneObj);
                onLoadedStats({ vertices: vCount, polygons: pCount });
            },
            undefined,
            (error) => {
                console.error('An error happened', error);
            }
        );
    }, [format, url, onLoadedStats]);

    if (!model) return null;

    return <primitive object={model} scale={1.5} />;
}
