import numpy as np
import heapq

import numpy as np
import heapq

class Node:
    def __init__(self, x, y, theta, g=0, f=0, parent=None):
        self.x = x
        self.y = y
        self.theta = theta
        self.g = g
        self.f = f
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f  # heapq에서 f 값 기준으로 정렬

def differential_drive_step(node, v, omega, dt=1.0):
    x_new = node.x + v * np.cos(node.theta) * dt
    y_new = node.y + v * np.sin(node.theta) * dt
    theta_new = node.theta + omega * dt
    return Node(x_new, y_new, theta_new)

def heuristic(node, goal):
    pos_dist = np.hypot(node.x - goal[0], node.y - goal[1])
    theta_dist = abs(node.theta - goal[2])
    return pos_dist + theta_dist

def hybrid_astar(start, goal, grid, v_list, omega_list, dt=1.0):
    open_list = []
    start_node = Node(*start)
    start_node.f = heuristic(start_node, goal)
    
    counter = 0  # tie-breaker
    heapq.heappush(open_list, (start_node.f, counter, start_node))
    counter += 1
    
    visited = set()
    
    while open_list:
        _, _, current = heapq.heappop(open_list)
        key = (int(current.x*10), int(current.y*10), int(current.theta*10))
        if key in visited:
            continue
        visited.add(key)
        
        if np.hypot(current.x - goal[0], current.y - goal[1]) < 1.0:
            path = []
            while current:
                path.append((int(current.x), int(current.y)))
                current = current.parent
            path.reverse()
            return path
        
        for v in v_list:
            for omega in omega_list:
                neighbor = differential_drive_step(current, v, omega, dt)
                xi, yi = int(neighbor.x), int(neighbor.y)
                if xi<0 or xi>=grid.shape[0] or yi<0 or yi>=grid.shape[1] or grid[xi,yi]:
                    continue
                neighbor.g = current.g + dt
                neighbor.f = neighbor.g + heuristic(neighbor, goal)
                neighbor.parent = current
                heapq.heappush(open_list, (neighbor.f, counter, neighbor))
                counter += 1
    
    return None


# ----------------------------
# 맵 정의
# ----------------------------
map_lines = [
"########################################",
"########################################",
"##......................#.............##",
"##..11111111..........................##",
"##..11111111..........................##",
"##..11111111..........................##",
"##..11111111..........................##",
"##..11111111..........................##",
"##..11111111..........................##",
"##..11111111..........................##",
"##..11111111..........................##",
"##..11111111..........................##",
"##....................................##",
"##......................#.............##",
"#########################.............##",
"##....................................##",
"##....................................##",
"##....................................##",
"##..........................00000000..##",
"##..........................00000000..##",
"##..........................00000000..##",
"##...S......................00000000..##",
"##..........................00000000..##",
"##..........................00000000..##",
"##..........................00000000..##",
"##..........................00000000..##",
"##....................................##",
"##....................................##",
"########################################",
"########################################"
]

height = len(map_lines)
width = len(map_lines[0])

grid = np.zeros((height, width), dtype=bool)
room_cells = {}
start_pos = None

for i, line in enumerate(map_lines):
    for j, c in enumerate(line):
        if c == '#':
            grid[i,j] = True
        elif c == 'S':
            start_pos = (i,j)
        elif c.isdigit():
            room_id = int(c)
            room_cells.setdefault(room_id, []).append((i,j))

# ----------------------------
# 방 중앙값 계산
# ----------------------------
def room_center(cells):
    xs = [x for x, y in cells]
    ys = [y for x, y in cells]
    return (int(np.mean(xs)), int(np.mean(ys)))

# ----------------------------
# Hybrid A*로 경로 계산
# ----------------------------
v_list = [0.5, 1.0]        # 선속도 후보
omega_list = [-0.5, 0, 0.5] # 각속도 후보
dt = 1.0

paths = {}
for room_id, cells in room_cells.items():
    goal_pos = room_center(cells)
    start_state = start_pos + (0,)       # 시작 방향 theta=0
    goal_state = goal_pos + (0,)         # 목표 방향 theta=0
    path = hybrid_astar(start_state, goal_state, grid, v_list, omega_list, dt)
    if path:
        paths[room_id] = path

# ----------------------------
# 맵 시각화
# ----------------------------
display_map = [list(row) for row in map_lines]

for room_id, path in paths.items():
    for x, y in path:
        if display_map[x][y] in ('.',):
            display_map[x][y] = '*'

for line in display_map:
    print(''.join(line))
