from map import map0, map1, map2, map3

def inflate_walls(map_str):
    lines = map_str.strip("\n").split("\n")
    h, w = len(lines), len(lines[0])

    grid = [list(row) for row in lines]
    new_grid = [row[:] for row in grid]  # deepcopy

    # 8방향 + 자기 자신
    directions = [(-1,-1), (-1,0), (-1,1),
                (0,-1),  (0,0),  (0,1),
                (1,-1),  (1,0),  (1,1)]

    for y in range(h):
        for x in range(w):
            if grid[y][x] == "#" or grid[y][x] == 'X':
                for dy, dx in directions:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        # 빈 칸만 채우기 (다른 문자 보호)
                        if new_grid[ny][nx] == ".":
                            new_grid[ny][nx] = "~"

    return "\n".join("".join(row) for row in new_grid)


# 예시 실행
print(inflate_walls(map0))
