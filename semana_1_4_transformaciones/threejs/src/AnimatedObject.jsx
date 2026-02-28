import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { useControls } from 'leva'
import * as THREE from 'three'

export function AnimatedObject() {
    const meshRef = useRef()

    // Controles UI usando Leva
    const { speed, scaleAmount, enableAnimation } = useControls('Controles de Animación', {
        enableAnimation: { value: true, label: 'Animar' },
        speed: { value: 1.0, min: 0.1, max: 3.0, step: 0.1, label: 'Velocidad' },
        scaleAmount: { value: 0.5, min: 0.1, max: 1.5, step: 0.1, label: 'Cantidad Escala' }
    })

    // useFrame se ejecuta en cada iteración del renderizador (frame)
    useFrame((state) => {
        if (!meshRef.current || !enableAnimation) return

        // Obtener el tiempo transcurrido
        // Nota: usando state.clock.elapsedTime como recomienda react-three-fiber en v9+
        const t = state.clock.elapsedTime * speed

        /**
         * 1. TRASLACIÓN
         * Trayectoria senoidal / circular en el plano XY
         */
        meshRef.current.position.x = Math.sin(t) * 2.5
        meshRef.current.position.y = Math.cos(t * 1.5) * 1.5
        // Movimiento leve en Z para dar profundidad
        meshRef.current.position.z = Math.sin(t * 0.5) * 1.0

        /**
         * 2. ROTACIÓN
         * Rotación continua sobre sus propios ejes
         */
        meshRef.current.rotation.x = t * 1.2
        meshRef.current.rotation.y = t * 0.8
        meshRef.current.rotation.z = t * 0.5

        /**
         * 3. ESCALA
         * Efecto de latido o "respiración" suave
         */
        const scale = 1.0 + Math.sin(t * 2) * scaleAmount
        meshRef.current.scale.set(scale, scale, scale)
    })

    return (
        <mesh ref={meshRef}>
            {/* Geometría de un Icosaedro para que se vea bien la rotación */}
            <icosahedronGeometry args={[1, 0]} />
            {/* Material wireframe brillante */}
            <meshStandardMaterial
                color="#00d2ff"
                wireframe={true}
                emissive="#0055ff"
                emissiveIntensity={0.5}
            />

            {/* Añadimos ejes locales para visualizar mejor la rotación individual */}
            <axesHelper args={[2]} />
        </mesh>
    )
}
