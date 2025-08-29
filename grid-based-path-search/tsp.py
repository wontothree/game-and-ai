import itertools
import math
from dijksta import dijkstra
from map import map3

def visualize_path_with_indices(map_lines, path):
    display_map = [list(row) for row in map_lines]
    for idx, (x, y) in enumerate(path):
        if display_map[x][y] != '#':  # 벽과 시작점 제외
            display_map[x][y] = '\033[91m*\033[0m'
    for line in display_map:
        print(''.join(line))
    print(f"\n총 이동 개수: {len(path)-1}")

def compute_distance(grid, pos1, pos2):
    path = dijkstra(grid, pos1, pos2)
    if path:
        return len(path) - 1  # 이동 비용
    else:
        return math.inf

if __name__ == '__main__':
    selected_map = map3
    map_lines = selected_map.strip().splitlines()
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
                room_cells.setdefault('S', []).append((i, j))
            elif c.isalpha() or c.isdigit():
                room_cells.setdefault(c.upper(), []).append((i, j))

    rooms_to_visit = input("방 이름들을 ,로 구분하여 입력 (예: A,B,C): ").upper().split(',')
    rooms_to_visit = [r.strip() for r in rooms_to_visit]

    all_rooms = ['S'] + rooms_to_visit

    room_centers = {}
    for r in all_rooms:
        xs = [x for x, y in room_cells[r]]
        ys = [y for x, y in room_cells[r]]
        room_centers[r] = (sum(xs)//len(xs), sum(ys)//len(ys))

    cost_matrix = {}
    for r1 in all_rooms:
        cost_matrix[r1] = {}
        for r2 in all_rooms:
            if r1 == r2:
                cost_matrix[r1][r2] = 0
            else:
                cost_matrix[r1][r2] = compute_distance(grid, room_centers[r1], room_centers[r2])

    # 모든 순열과 비용 출력
    min_cost = math.inf
    best_order = None
    print("\n모든 순열과 비용:")
    index = 1
    for perm in itertools.permutations(rooms_to_visit):
        order = ['S'] + list(perm) + ['S']
        cost = sum(cost_matrix[order[i]][order[i+1]] for i in range(len(order)-1))
        print(f"[{index}] {order} -> 비용: {cost}")
        index += 1
        if cost < min_cost:
            min_cost = cost
            best_order = order

    print(f"\n최적 방문 순서: {best_order}, 최소 비용: {min_cost}")

    # 최적 경로 생성
    full_path = []
    for i in range(len(best_order)-1):
        start = room_centers[best_order[i]]
        goal = room_centers[best_order[i+1]]
        segment = dijkstra(grid, start, goal)
        if segment:
            if i > 0:
                segment = segment[1:]  # 이전 끝점 겹치지 않도록
            full_path += segment

    # 시각화 (인덱스 포함)
    visualize_path_with_indices(map_lines, full_path)

# A, B, 1, 2,9, 0