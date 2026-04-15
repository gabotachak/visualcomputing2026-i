import React from 'react';

const SPEED_OPTIONS = [0.5, 1, 1.5, 2];

const AnimationController = ({
  animations,
  activeAnimation,
  isPlaying,
  speed,
  onAnimationChange,
  onPlayPause,
  onSpeedChange,
}) => {
  return (
    <div className="controller-panel">
      <h2 className="panel-title">Animation Controller</h2>

      <div className="control-group">
        <label className="control-label">Animation</label>
        <select
          className="anim-select"
          value={activeAnimation}
          onChange={e => onAnimationChange(e.target.value)}
        >
          {animations.length === 0 ? (
            <option value="Idle">Idle (loading...)</option>
          ) : (
            animations.map(name => (
              <option key={name} value={name}>
                {name}
              </option>
            ))
          )}
        </select>
      </div>

      <div className="control-group btn-row">
        <button
          className={`btn ${isPlaying ? 'btn-active' : ''}`}
          onClick={() => onPlayPause(true)}
        >
          ▶ Play
        </button>
        <button
          className={`btn ${!isPlaying ? 'btn-active' : ''}`}
          onClick={() => onPlayPause(false)}
        >
          ⏸ Pause
        </button>
      </div>

      <div className="control-group">
        <label className="control-label">Speed</label>
        <div className="speed-options">
          {SPEED_OPTIONS.map(val => (
            <label key={val} className="speed-option">
              <input
                type="radio"
                name="speed"
                value={val}
                checked={speed === val}
                onChange={() => onSpeedChange(val)}
              />
              {val}x
            </label>
          ))}
        </div>
      </div>

      <div className="status-bar">
        Status: {isPlaying ? 'Playing' : 'Paused'} — {activeAnimation}
      </div>
    </div>
  );
};

export default AnimationController;
