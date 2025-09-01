import numpy as np
import heapq

from inflate_map import inflate_map0, inflate_map1, inflate_map2, inflate_map3

class Node:
    def __init__(self, x, y, theta, g=0, f=0, parent=None):
        self.x = x  # 아래 방향
        self.y = y  # 오른쪽 방향
        self.theta = theta
        self.g = g
        self.f = f
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

def differential_drive_step(node, v, omega, dt=1.0):
    x_new = node.x + v * np.cos(node.theta) * dt
    y_new = node.y + v * np.sin(node.theta) * dt
    theta_new = node.theta + omega * dt
    return Node(x_new, y_new, theta_new)

def heuristic(node, goal):
    pos_dist = np.hypot(node.x - goal[0], node.y - goal[1])
    theta_dist = abs(node.theta - goal[2])
    return pos_dist + theta_dist

def hybrid_astar(start_pose, goal_pose, grid, v_list, omega_list, dt=1.0):
    """
    Output: Grid Coordinate
    """
    open_list = []
    start_node = Node(*start_pose)
    start_node.f = heuristic(start_node, goal_pose)
    
    counter = 0
    heapq.heappush(open_list, (start_node.f, counter, start_node))
    counter += 1
    
    visited = set()
    
    while open_list:
        _, _, current = heapq.heappop(open_list)
        key = (int(current.x*10), int(current.y*10), int(current.theta*10))
        if key in visited:
            continue
        visited.add(key)
        
        if np.hypot(current.x - goal_pose[0], current.y - goal_pose[1]) < 1.0:
            path = []
            while current:
                path.append((float(round(current.x,1)), float(round(current.y,1))))
                current = current.parent
            path.reverse()
            return path
        
        for v in v_list:
            for omega in omega_list:
                neighbor = differential_drive_step(current, v, omega, dt)
                # 맵 좌표로 변환
                row = int(neighbor.x + grid.shape[0]//2)
                col = int(neighbor.y + grid.shape[1]//2)
                if row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or grid[row, col]:
                    continue
                neighbor.g = current.g + dt
                neighbor.f = neighbor.g + heuristic(neighbor, goal_pose)
                neighbor.parent = current
                heapq.heappush(open_list, (neighbor.f, counter, neighbor))
                counter += 1
    return None

def plan_path(map_str, start_symbol, goal_symbol):
    map_lines = map_str.strip().splitlines()
    height, width = len(map_lines), len(map_lines[0])

    grid = np.zeros((height, width), dtype=bool)
    start_pos = goal_pos = None
    for i, line in enumerate(map_lines):
        for j, c in enumerate(line):
            if c in ('#','~'):
                grid[i,j] = True
            elif c == start_symbol:
                start_pos = (i,j)
            elif c == goal_symbol:
                goal_pos = (i,j)

    if start_pos is None or goal_pos is None:
        print("Start or goal symbol not found!")
        return None, map_lines

    cx, cy = width // 2, height // 2

    v_list = [0.5, 1.0]
    omega_list = [-0.4,0,0.4]
    dt = 0.5

    # 중앙 기준 좌표: x=아래, y=오른쪽
    start_pose = (start_pos[0]-cy, start_pos[1]-cx, np.pi/2)
    goal_pose  = (goal_pos[0]-cy, goal_pos[1]-cx, np.pi/2)

    # Grid coordinate
    path = hybrid_astar(start_pose, goal_pose, grid, v_list, omega_list, dt)

    grid_size = 0.2
    scaled_path = [(round(x * grid_size, 2), round(y * grid_size, 2)) for x, y in path]

    # 시각화
    display_map = [list(row) for row in map_lines]
    if scaled_path:
        for x, y in path:
            row = int(x + cy)
            col = int(y + cx)
            if 0<=row<height and 0<=col<width and display_map[row][col]=='.':
                display_map[row][col]='\033[91m*\033[0m'

    return scaled_path, display_map

if __name__=="__main__":
    from inflate_map import inflate_map0

    path, display_map = plan_path(inflate_map0, 'S', '1')
    if path:
        print(f"Found path with {len(path)} steps")
        for line in display_map:
            print(''.join(line))
    else:
        print("No path found")

    print(path)

"""
def hybrid_astar(start_pose, goal_pose, grid, v_list, omega_list, dt=1.0):
    open_list = []
    start_node = Node(*start_pose)
    start_node.f = heuristic(start_node, goal_pose)
    
    counter = 0
    heapq.heappush(open_list, (start_node.f, counter, start_node))
    counter += 1
    
    visited = set()
    
    while open_list:
        _, _, current = heapq.heappop(open_list)
        key = (int(current.x*10), int(current.y*10), int(current.theta*10))
        if key in visited:
            continue
        visited.add(key)
        
        if np.hypot(current.x - goal_pose[0], current.y - goal_pose[1]) < 1.0:
            path = []
            while current:
                path.append((float(round(current.x,1)), float(round(current.y,1))))
                current = current.parent
            path.reverse()
            return path
        
        for v in v_list:
            for omega in omega_list:
                neighbor = differential_drive_step(current, v, omega, dt)
                # 맵 좌표로 변환
                row = int(neighbor.x + grid.shape[0]//2)
                col = int(neighbor.y + grid.shape[1]//2)
                if row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or grid[row, col]:
                    continue
                neighbor.g = current.g + dt
                neighbor.f = neighbor.g + heuristic(neighbor, goal_pose)
                neighbor.parent = current
                heapq.heappush(open_list, (neighbor.f, counter, neighbor))
                counter += 1
    return None
"""