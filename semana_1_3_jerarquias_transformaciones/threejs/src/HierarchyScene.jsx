import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useControls, folder } from 'leva';
import { Text } from '@react-three/drei';

export default function HierarchyScene() {
    const childRef = useRef();
    const grandchildRef = useRef();

    // Leva controls for the Parent
    const { positionX, positionY, positionZ, rotX, rotY, rotZ, scale } = useControls('Nivel 1: Padre (Cubo)', {
        Posición: folder({
            positionX: { value: 0, min: -5, max: 5, step: 0.1 },
            positionY: { value: 0, min: -5, max: 5, step: 0.1 },
            positionZ: { value: 0, min: -5, max: 5, step: 0.1 },
        }),
        Rotación: folder({
            rotX: { value: 0, min: -Math.PI, max: Math.PI, step: 0.1 },
            rotY: { value: 0, min: -Math.PI, max: Math.PI, step: 0.1 },
            rotZ: { value: 0, min: -Math.PI, max: Math.PI, step: 0.1 },
        }),
        Escala: folder({
            scale: { value: 1, min: 0.1, max: 3, step: 0.1 },
        })
    });

    const { childRotY, childScale } = useControls('Nivel 2: Hijo (Esfera)', {
        childRotY: { value: 0, min: -Math.PI, max: Math.PI, step: 0.1, label: 'Rotación Y Local' },
        childScale: { value: 1, min: 0.5, max: 2, step: 0.1, label: 'Escala Local' }
    });

    const { grandchildRotX } = useControls('Nivel 3: Nieto (Toroide)', {
        grandchildRotX: { value: 0, min: -Math.PI, max: Math.PI, step: 0.1, label: 'Rotación X Local' }
    });

    const { bindAxis, animateChild } = useControls('Visualización', {
        bindAxis: { value: true, label: 'Mostrar ejes' },
        animateChild: { value: true, label: 'Rotación automática (Hijo/Nieto)' }
    });

    useFrame((state, delta) => {
        if (animateChild) {
            if (childRef.current) {
                childRef.current.rotation.y += delta * 0.5;
            }
            if (grandchildRef.current) {
                grandchildRef.current.rotation.x += delta;
            }
        } else {
            if (childRef.current) {
                childRef.current.rotation.y = childRotY;
            }
            if (grandchildRef.current) {
                grandchildRef.current.rotation.x = grandchildRotX;
            }
        }
    });

    return (
        <>
            {/* Contenedor principal del padre */}
            <group
                position={[positionX, positionY, positionZ]}
                rotation={[rotX, rotY, rotZ]}
                scale={[scale, scale, scale]}
                dispose={null}
            >
                {/* PARENT NODE */}
                <mesh>
                    <boxGeometry args={[1.5, 1.5, 1.5]} />
                    <meshStandardMaterial color="#3b82f6" transparent opacity={0.6} />
                </mesh>

                <mesh>
                    <sphereGeometry args={[0.15, 16, 16]} />
                    <meshBasicMaterial color="#ffffff" />
                </mesh>

                <Text position={[0, 1.2, 0]} fontSize={0.3} color="white" anchorX="center" anchorY="bottom" outlineWidth={0.02} outlineColor="#000000">
                    Nivel 1: Padre
                </Text>

                {bindAxis && <axesHelper args={[2]} />}

                {/* Connection from Parent to Child */}
                <mesh position={[1.5, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
                    <cylinderGeometry args={[0.02, 0.02, 3, 8]} />
                    <meshStandardMaterial color="#94a3b8" />
                </mesh>

                {/* CHILD NODE (Relative position to parent) */}
                <group position={[3, 0, 0]} scale={[childScale, childScale, childScale]}>

                    <group ref={childRef}>
                        <mesh>
                            <sphereGeometry args={[0.6, 32, 32]} />
                            <meshStandardMaterial color="#ef4444" roughness={0.3} metalness={0.8} />
                        </mesh>

                        <Text position={[0, 0.9, 0]} fontSize={0.25} color="white" anchorX="center" anchorY="bottom" outlineWidth={0.02} outlineColor="#000000">
                            Nivel 2: Hijo
                        </Text>

                        {bindAxis && <axesHelper args={[1.2]} />}

                        {/* Connection from Child to Grandchild */}
                        <mesh position={[0, 1, 0]} rotation={[0, 0, 0]}>
                            <cylinderGeometry args={[0.015, 0.015, 2, 8]} />
                            <meshStandardMaterial color="#94a3b8" />
                        </mesh>

                        {/* GRANDCHILD NODE (Relative position to child) */}
                        <group position={[0, 2, 0]}>
                            <group ref={grandchildRef}>
                                <mesh>
                                    <torusGeometry args={[0.3, 0.08, 16, 32]} />
                                    <meshStandardMaterial color="#eab308" roughness={0.1} metalness={0.9} />
                                </mesh>

                                <Text position={[0, 0.6, 0]} fontSize={0.2} color="white" anchorX="center" anchorY="bottom" outlineWidth={0.02} outlineColor="#000000">
                                    Nivel 3: Nieto
                                </Text>

                                {bindAxis && <axesHelper args={[0.8]} />}
                            </group>
                        </group>
                    </group>

                </group>
            </group>
        </>
    );
}
