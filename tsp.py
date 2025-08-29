import itertools
import math

# 노드 정의
nodes = {
    "DockingStation": (39, 4),
    "Bathroom": (8, 17),
    "LivingRoom": (27, 13),
    "Bedroom1": (13, 39),
    "Bedroom2": (29, 42),
    "Balcony": (45, 39)
}

# 두 점 사이의 유클리드 거리
def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# 방문해야 할 노드들 (DockingStation 제외)
visit_nodes = [node for node in nodes if node != "DockingStation"]

all_paths = []

# 모든 경우 탐색
for perm in itertools.permutations(visit_nodes):
    path = ["DockingStation"] + list(perm) + ["DockingStation"]
    
    # 비용 계산
    cost = 0
    for i in range(len(path) - 1):
        cost += euclidean_distance(nodes[path[i]], nodes[path[i+1]])
    
    # 저장
    all_paths.append((path, cost))

# 모든 경로와 비용 출력 (인덱스 포함)
for idx, (path, cost) in enumerate(all_paths, start=1):
    print(f"[{idx}] 경로: {path}, 비용: {cost:.2f}")

# 최소 비용 경로 찾기
min_index, (min_path, min_cost) = min(enumerate(all_paths, start=1), key=lambda x: x[1][1])

print("\n총 경우의 수:", len(all_paths))
print(f"최소 비용 경로 (index {min_index}): {min_path}")
print("최소 비용:", round(min_cost, 2))
