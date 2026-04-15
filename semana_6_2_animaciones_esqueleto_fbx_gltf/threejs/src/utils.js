// Normalize Mixamo-style names: "Armature|Idle" → "Idle"
export const getAnimationName = (clipName) => {
  return clipName.split('|').pop();
};

// Format a list of clips for display
export const formatClipList = (clips) => {
  return clips.map(c => getAnimationName(c.name));
};
