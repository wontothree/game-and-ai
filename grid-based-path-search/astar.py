import heapq
import math

def heuristic(a, b, method="squared_euclidean"):
    if method == "zero":
        return 0
    elif method == "manhattan":
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
    elif method == "chebyshev":
        return max(abs(a[0]-b[0]), abs(a[1]-b[1]))
    elif method == "squared_euclidean":
        return (a[0]-b[0])**2 + (a[1]-b[1])**2
    elif method == "euclidean":
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    elif method == "diagonal":
        dx = abs(a[0]-b[0])
        dy = abs(a[1]-b[1])
        return dx + dy + (math.sqrt(2) - 2) * min(dx, dy)
    elif method == "octile":
        dx = abs(a[0]-b[0])
        dy = abs(a[1]-b[1])
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)
    elif method == "weighted_manhattan":
        return 1.5 * (abs(a[0]-b[0]) + abs(a[1]-b[1]))
    elif method == "cosine":
        dx1, dy1 = a[0]-b[0], a[1]-b[1]
        dx2, dy2 = 1, 0
        dot = dx1*dx2 + dy1*dy2
        norm1 = math.sqrt(dx1**2 + dy1**2)
        norm2 = math.sqrt(dx2**2 + dy2**2)
        return 1 - dot/(norm1*norm2+1e-9)
    else:
        raise ValueError(f"Unknown heuristic method: {method}")

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
            x, y = neighbor
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                if grid[x][y]:
                    continue
                tentative_g_score = gscore[current] + 1
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                if tentative_g_score < gscore.get(neighbor, float('inf')) or neighbor not in [i[1] for i in open_heap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_heap, (fscore[neighbor], neighbor))
    return None

map0 = """
########################################
########################################
##......................#.............##
##..11111111..........................##
##..11111111..........................##
##..11111111..........................##
##..11111111..........................##
##..11111111..........................##
##..11111111..........................##
##..11111111..........................##
##..11111111..........................##
##....................................##
##......................#.............##
#########################.............##
##....................................##
##....................................##
##....................................##
##....................................##
##..........................00000000..##
##..........................00000000..##
##..........................00000000..##
##...S......................00000000..##
##..........................00000000..##
##..........................00000000..##
##..........................00000000..##
##..........................00000000..##
##....................................##
##....................................##
########################################
########################################
"""

if __name__ == '__main__':
    from map import map0

    map_lines = map0.strip().splitlines()
    height = len(map_lines)
    width = len(map_lines[0])

    grid = [[False for _ in range(width)] for _ in range(height)]
    room_cells = {}
    start_pos = None

    for i, line in enumerate(map_lines):
        for j, c in enumerate(line):
            if c == '#':
                grid[i][j] = True
            elif c == 'S':
                start_pos = (i, j)
            elif c.isdigit():
                room_id = int(c)
                room_cells.setdefault(room_id, []).append((i, j))

    display_map = [list(row) for row in map_lines]

    for room_id, cells in room_cells.items():
        xs = [x for x, y in cells]
        ys = [y for x, y in cells]
        goal = (sum(xs)//len(xs), sum(ys)//len(ys))

        path = astar(grid, start_pos, goal)
        if path:
            for x, y in path:
                if display_map[x][y] != 'S':
                    display_map[x][y] = '\033[91m*\033[0m'

    for line in display_map:
        print(''.join(line))