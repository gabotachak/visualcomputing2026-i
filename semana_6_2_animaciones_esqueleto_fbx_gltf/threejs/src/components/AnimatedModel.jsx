import React, { useRef, useEffect } from 'react';
import { useGLTF, useAnimations } from '@react-three/drei';
import { getAnimationName } from '../utils.js';

const AnimatedModel = ({ activeAnimation, isPlaying, speed, onAnimationsLoaded }) => {
  const group = useRef();
  const { scene, animations } = useGLTF('/models/character.glb');
  const { actions, mixer } = useAnimations(animations, group);

  // Tracks the active action key so the play/pause effect can find it without
  // including activeAnimation in its deps (which would cause unnecessary resets).
  const activeKeyRef = useRef(null);
  // Reads isPlaying without making the animation-change effect depend on it.
  const isPlayingRef = useRef(isPlaying);
  isPlayingRef.current = isPlaying;

  // Expose animation list to parent on mount
  useEffect(() => {
    if (animations.length > 0) {
      const names = animations.map(a => getAnimationName(a.name));
      onAnimationsLoaded(names);
    }
  }, [animations, onAnimationsLoaded]);

  // Animation change → fade out others, reset + fade in new clip.
  // Does NOT run when isPlaying toggles, so resume never restarts the clip.
  useEffect(() => {
    if (!actions || !activeAnimation) return;
    const key = Object.keys(actions).find(
      k => getAnimationName(k) === activeAnimation || k === activeAnimation
    );
    if (!key) return;
    activeKeyRef.current = key;

    Object.keys(actions).forEach(k => {
      if (k !== key) actions[k].fadeOut(0.5);
    });

    actions[key].reset().fadeIn(0.5).play();
    // Apply current play state immediately after starting
    actions[key].paused = !isPlayingRef.current;
  }, [activeAnimation, actions]);

  // Play/pause toggle → only flip paused, never reset position.
  useEffect(() => {
    const key = activeKeyRef.current;
    if (!actions || !key || !actions[key]) return;
    actions[key].paused = !isPlaying;
  }, [isPlaying, actions]);

  // Speed control via mixer.timeScale
  useEffect(() => {
    if (mixer) mixer.timeScale = speed;
  }, [speed, mixer]);

  return (
    <group ref={group}>
      <primitive object={scene} />
    </group>
  );
};

useGLTF.preload('/models/character.glb');

export default AnimatedModel;
