import numpy as np
import heapq

from map import map0, map1, map2, map3

# ----------------------------
# A* 
# ----------------------------
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])  # Manhattan 거리

def astar(grid, start, goal):
    neighbors = [(0,1),(1,0),(0,-1),(-1,0)]
    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    open_heap = [(fscore[start], start)]
    
    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        close_set.add(current)
        for dx, dy in neighbors:
            neighbor = (current[0]+dx, current[1]+dy)
            if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1]:
                if grid[neighbor]:
                    continue  # 벽
                tentative_g_score = gscore[current] + 1
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                if tentative_g_score < gscore.get(neighbor, float('inf')) or neighbor not in [i[1] for i in open_heap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_heap, (fscore[neighbor], neighbor))
    return None

map_lines = map1.strip().splitlines()

height = len(map_lines)
width = len(map_lines[0])

grid = np.zeros((height, width), dtype=bool)
room_cells = {}  # 방 ID별 위치
start_pos = None

for i, line in enumerate(map_lines):
    for j, c in enumerate(line):
        if c == '#':
            grid[i,j] = True
        elif c == 'S':
            start_pos = (i,j)
        elif c.isdigit():  # 방 ID
            room_id = int(c)
            room_cells.setdefault(room_id, []).append((i,j))

# ----------------------------
# 방 중앙값 계산
# ----------------------------
def room_center(cells):
    xs = [x for x, y in cells]
    ys = [y for x, y in cells]
    return (int(np.mean(xs)), int(np.mean(ys)))

paths = {}
for room_id, cells in room_cells.items():
    goal = room_center(cells)
    path = astar(grid, start_pos, goal)
    if path:
        paths[room_id] = path

# ----------------------------
# 맵 시각화
# ----------------------------
display_map = [list(row) for row in map_lines]

for room_id, path in paths.items():
    for x,y in path:
        display_map[x][y] = '*'

# 출력
for line in display_map:
    print(''.join(line))
