from map import map0, map1, map2, map3
from astar import astar
from dijksta import dijkstra

def visualize_path(map_lines, path):
    display_map = [list(row) for row in map_lines]
    for x, y in path:
        if display_map[x][y] != '#':  # 벽이 아니면
            display_map[x][y] = '\033[91m*\033[0m'
    for line in display_map:
        print(''.join(line))

# if __name__ == '__main__':
#     selected_map = map3
#     map_lines = selected_map.strip().splitlines()

#     height = len(map_lines)
#     width = len(map_lines[0])

#     grid = [[False for _ in range(width)] for _ in range(height)]
#     room_cells = {}
#     start_pos = None

#     for i, line in enumerate(map_lines):
#         for j, c in enumerate(line):
#             if c == '#':
#                 grid[i][j] = True
#             elif c == 'S':
#                 start_pos = (i, j)
#                 room_cells.setdefault('S', []).append((i, j))  # S도 구역으로 포함
#             elif c.isalpha():  # 알파벳 방
#                 room_cells.setdefault(c.upper(), []).append((i, j))
#             elif c.isdigit():  # 숫자 방
#                 room_cells.setdefault(c, []).append((i, j))

#     # 사용자 입력
#     start_room = input("시작 방 입력: ").upper()  
#     goal_room = input("목표 방 입력: ").upper()

#     if start_room not in room_cells or goal_room not in room_cells:
#         print("⚠️ 해당 방 번호가 맵에 없음")
#         exit()

#     # 방 중앙 좌표 계산
#     sx = sum(x for x, y in room_cells[start_room]) // len(room_cells[start_room])
#     sy = sum(y for x, y in room_cells[start_room]) // len(room_cells[start_room])
#     gx = sum(x for x, y in room_cells[goal_room]) // len(room_cells[goal_room])
#     gy = sum(y for x, y in room_cells[goal_room]) // len(room_cells[goal_room])

#     start_pos = (sx, sy)
#     goal_pos = (gx, gy)

#     # Dijkstra 또는 A* 경로 탐색
#     path = dijkstra(grid, start_pos, goal_pos)
#     # path = astar(grid, start_pos, goal_pos)

#     if path:
#         visualize_path(map_lines, path)
#     else:
#         print("❌ 경로를 찾을 수 없음")


if __name__ == '__main__':
    selected_map = map3
    map_lines = selected_map.strip().splitlines()

    height = len(map_lines)
    width = len(map_lines[0])

    grid = [[False for _ in range(width)] for _ in range(height)]
    room_cells = {}
    start_pos = None

    # 맵에서 방 위치와 시작점 수집
    for i, line in enumerate(map_lines):
        for j, c in enumerate(line):
            if c == '#':
                grid[i][j] = True
            elif c == 'S':
                start_pos = (i, j)
                room_cells.setdefault('S', []).append((i, j))
            elif c.isalpha():  # 알파벳 방
                room_cells.setdefault(c.upper(), []).append((i, j))
            elif c.isdigit():  # 숫자 방
                room_cells.setdefault(c, []).append((i, j))

    if 'S' not in room_cells:
        print("⚠️ 시작점 S가 맵에 없음")
        exit()

    start_pos = room_cells['S'][0]

    # 모든 경로를 한 맵에 표시
    display_map = [list(row) for row in map_lines]

    for room_id, cells in room_cells.items():
        if room_id == 'S':
            continue  # S 자신은 스킵

        # 방 중앙 좌표 계산
        gx = sum(x for x, y in cells) // len(cells)
        gy = sum(y for x, y in cells) // len(cells)
        goal_pos = (gx, gy)

        # 경로 탐색
        path = dijkstra(grid, start_pos, goal_pos)
        if path:
            for x, y in path:
                if display_map[x][y] not in ['#', 'S']:
                    display_map[x][y] = '\033[91m*\033[0m'

    # 한 번에 시각화
    for line in display_map:
        print(''.join(line))
