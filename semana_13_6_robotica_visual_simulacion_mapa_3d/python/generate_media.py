#!/usr/bin/env python3
"""Semana 13_6: Robot navigation simulation in 3D map."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import os, io

os.makedirs('../media', exist_ok=True)
np.random.seed(42)

# Grid map for robot navigation (0=free, 1=obstacle)
GRID_SIZE = 20
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
# Add obstacles
for ox, oy, w, h in [(3,3,3,2),(10,5,2,5),(5,12,4,2),(15,8,2,4),(7,7,1,1),(12,2,3,1)]:
    grid[oy:oy+h, ox:ox+w] = 1

# BFS pathfinding
from collections import deque
def bfs(grid, start, goal):
    H, W = grid.shape
    queue = deque([start])
    visited = {start: None}
    while queue:
        node = queue.popleft()
        if node == goal:
            break
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx, ny = node[0]+dx, node[1]+dy
            if 0<=nx<W and 0<=ny<H and grid[ny,nx]==0 and (nx,ny) not in visited:
                visited[(nx,ny)] = node
                queue.append((nx,ny))
    path = []
    node = goal
    while node:
        path.append(node)
        node = visited.get(node)
    return list(reversed(path))

start = (1, 1)
goal = (18, 18)
path = bfs(grid, start, goal)

# Robot sensors (raycasting simulation)
def raycast(grid, pos, angle, max_range=8):
    x, y = pos
    dx, dy = np.cos(angle), np.sin(angle)
    for r in np.linspace(0, max_range, 50):
        nx, ny = int(x + dx*r), int(y + dy*r)
        if nx < 0 or nx >= GRID_SIZE or ny < 0 or ny >= GRID_SIZE:
            return r
        if grid[ny, nx] == 1:
            return r
    return max_range

# Plot 1: Navigation simulation frames
frames = []
for step in range(0, len(path), max(1, len(path)//12)):
    robot_pos = path[step]
    robot_angle = np.pi/4  # fixed heading for sim

    fig_f, ax_f = plt.subplots(figsize=(6, 6), facecolor='#0a0a1a')
    ax_f.set_facecolor('#111')

    # Draw grid
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y, x] == 1:
                ax_f.add_patch(plt.Rectangle((x, y), 1, 1, color='#555'))

    # Draw path
    if len(path) > 1:
        px, py = zip(*path)
        ax_f.plot(np.array(px)+0.5, np.array(py)+0.5, color='#4af', linewidth=1.5, alpha=0.5, linestyle='--')

    # Draw raycasts from robot
    angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
    for a in angles:
        r = raycast(grid, (robot_pos[0]+0.5, robot_pos[1]+0.5), a)
        ex = robot_pos[0]+0.5 + np.cos(a)*r
        ey = robot_pos[1]+0.5 + np.sin(a)*r
        ax_f.plot([robot_pos[0]+0.5, ex], [robot_pos[1]+0.5, ey], color='#f84', linewidth=0.5, alpha=0.4)

    # Draw start and goal
    ax_f.add_patch(plt.Circle((start[0]+0.5, start[1]+0.5), 0.4, color='#4e4'))
    ax_f.add_patch(plt.Circle((goal[0]+0.5, goal[1]+0.5), 0.4, color='#e44'))

    # Draw robot
    ax_f.add_patch(plt.Circle((robot_pos[0]+0.5, robot_pos[1]+0.5), 0.5, color='#4af'))
    ax_f.text(robot_pos[0]+0.5, robot_pos[1]+0.5, 'R', ha='center', va='center', color='white', fontsize=10, fontweight='bold')

    ax_f.set_xlim(0, GRID_SIZE); ax_f.set_ylim(0, GRID_SIZE)
    ax_f.set_title(f'Robot en ({robot_pos[0]},{robot_pos[1]}) — Paso {step}/{len(path)-1}', color='white', fontsize=10)
    ax_f.axis('off')

    buf = io.BytesIO()
    fig_f.savefig(buf, format='png', dpi=80, bbox_inches='tight', facecolor=fig_f.get_facecolor())
    plt.close(fig_f)
    buf.seek(0)
    frames.append(Image.open(buf).copy())

frames[0].save('../media/robot_navigation.gif', save_all=True,
               append_images=frames[1:], duration=200, loop=0)
print("Saved: robot_navigation.gif")

# Plot 2: 3D environment visualization
fig2 = plt.figure(figsize=(14, 6), facecolor='#0a0a1a')
fig2.suptitle('Entorno 3D de Robótica Visual — Mapa y Trayectoria', color='white', fontsize=12, fontweight='bold')

ax2d = fig2.add_subplot(121)
ax2d.set_facecolor('#111')
ax2d.imshow(grid, cmap='gray_r', origin='lower', vmin=0, vmax=1.5)
if path:
    px, py = zip(*path)
    ax2d.plot(px, py, color='#4af', linewidth=2, label='Trayectoria BFS')
ax2d.plot(*start, 'g*', markersize=15, label='Inicio')
ax2d.plot(*goal, 'r*', markersize=15, label='Meta')
ax2d.set_title('Mapa 2D + Trayectoria (BFS)', color='white')
ax2d.legend(facecolor='#0a0a1a', labelcolor='white', fontsize=9)

ax3d2 = fig2.add_subplot(122, projection='3d')
ax3d2.set_facecolor('#0d0d2a')
# Obstacles as 3D boxes
for y in range(GRID_SIZE):
    for x in range(GRID_SIZE):
        if grid[y,x] == 1:
            ax3d2.bar3d(x, y, 0, 1, 1, 1, color='#555', alpha=0.8)
# Path as 3D line
if path:
    px3, py3 = zip(*path)
    ax3d2.plot(px3, py3, [0.1]*len(path), color='#4af', linewidth=2)
ax3d2.set_title('Entorno 3D (obstáculos = muros)', color='white')
ax3d2.tick_params(colors='gray', labelsize=6)

plt.tight_layout()
fig2.savefig('../media/robot_3d_environment.png', dpi=150, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close()
print("Saved: robot_3d_environment.png")
print("All media generated for semana_13_6")
