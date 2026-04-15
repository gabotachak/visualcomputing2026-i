import { useState, useCallback } from 'react';
import { getAnimationName } from '../utils.js';

/**
 * Custom hook: wraps useAnimations with fade/transition logic.
 * Returns animation controls that can be used in App or AnimatedModel.
 */
export const useSkeletalAnimation = (animations, actions) => {
  const [activeAnimation, setActiveAnimation] = useState(null);
  const [isPlaying, setIsPlaying] = useState(true);
  const [speed, setSpeed] = useState(1);

  // Fade to a new animation by display name (handles "Armature|Idle" → "Idle")
  const playAnimation = useCallback((name, fadeDuration = 0.5) => {
    if (!actions) return;
    const key = Object.keys(actions).find(
      k => getAnimationName(k) === name || k === name
    );
    if (!key) return;

    Object.keys(actions).forEach(k => {
      if (k !== key) actions[k].fadeOut(fadeDuration);
    });

    actions[key].reset().fadeIn(fadeDuration).play();
    setActiveAnimation(name);
    setIsPlaying(true);
  }, [actions]);

  const pauseAnimation = useCallback(() => {
    if (!actions || !activeAnimation) return;
    const key = Object.keys(actions).find(
      k => getAnimationName(k) === activeAnimation || k === activeAnimation
    );
    if (key && actions[key]) actions[key].paused = true;
    setIsPlaying(false);
  }, [actions, activeAnimation]);

  const resumeAnimation = useCallback(() => {
    if (!actions || !activeAnimation) return;
    const key = Object.keys(actions).find(
      k => getAnimationName(k) === activeAnimation || k === activeAnimation
    );
    if (key && actions[key]) actions[key].paused = false;
    setIsPlaying(true);
  }, [actions, activeAnimation]);

  return {
    activeAnimation,
    isPlaying,
    speed,
    playAnimation,
    pauseAnimation,
    resumeAnimation,
    setSpeed,
    animationList: animations?.map(a => getAnimationName(a.name)) ?? [],
  };
};
