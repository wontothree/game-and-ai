import numpy as np
import heapq

from inflate_map import inflate_map0, inflate_map1, inflate_map2, inflate_map3

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
                if xi < 0 or xi >= grid.shape[0] or yi < 0 or yi >= grid.shape[1] or grid[xi, yi]:
                    continue
                neighbor.g = current.g + dt
                neighbor.f = neighbor.g + heuristic(neighbor, goal)
                neighbor.parent = current
                heapq.heappush(open_list, (neighbor.f, counter, neighbor))
                counter += 1
    return None

def plan_path(map_str, start_symbol, goal_symbol):
    """
    map_str : 맵 문자열
    start_symbol : 출발 심볼
    goal_symbol : 도착 심볼
    return : path ([(x,y),...]), display_map (시각화된 맵)
    """
    map_lines = map_str.strip().splitlines()
    height, width = len(map_lines), len(map_lines[0])

    grid = np.zeros((height, width), dtype=bool)
    start_pos = None
    goal_pos = None

    for i, line in enumerate(map_lines):
        for j, c in enumerate(line):
            if c == '#' or c == '~':  # 지나갈 수 없는 지역
                grid[i, j] = True
            elif c == start_symbol:
                start_pos = (i, j)
            elif c == goal_symbol:
                goal_pos = (i, j)

    if start_pos is None or goal_pos is None:
        print("Start or goal symbol not found!")
        return None, map_lines

    v_list = [0.5, 1.0]
    omega_list = [-0.5, 0, 0.5]
    dt = 1.0

    # Start pose
    start_state = start_pos + (np.pi / 2,)
    goal_state = goal_pos + (0,)

    path = hybrid_astar(start_state, goal_state, grid, v_list, omega_list, dt)

    display_map = [list(row) for row in map_lines]
    if path:
        for x, y in path:
            if display_map[x][y] == '.':
                display_map[x][y] = '\033[91m*\033[0m'

    return path, display_map

if __name__ == "__main__":
    from inflate_map import inflate_map0

    path, display_map = plan_path(inflate_map0, 'S', '1')
    if path:
        print(f"Found path with {len(path)} steps")
        for line in display_map:
            print(''.join(line))
    else:
        print("No path found")

    print(path)