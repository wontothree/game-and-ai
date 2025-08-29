import heapq

def dijkstra(grid, start, goal):
    neighbors = [
        (0, 1),  (1, 0),  (0, -1), (-1, 0),   # 상하좌우
        (1, 1),  (1, -1), (-1, 1), (-1, -1)   # 대각선
    ]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    open_heap = [(gscore[start], start)]
    
    while open_heap:
        cost, current = heapq.heappop(open_heap)
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
                tentative_g_score = gscore[current] + 1  # 모든 이동 비용 1
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                if tentative_g_score < gscore.get(neighbor, float('inf')) or neighbor not in [i[1] for i in open_heap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    heapq.heappush(open_heap, (gscore[neighbor], neighbor))
    return None


if __name__ == '__main__':
    from map import map1 as map
    
    map_lines = map.strip().splitlines()
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

        path = dijkstra(grid, start_pos, goal)
        if path:
            for x, y in path:
                if display_map[x][y] != 'S':
                    display_map[x][y] = '\033[91m*\033[0m'  # 빨간색 표시

    for line in display_map:
        print(''.join(line))
