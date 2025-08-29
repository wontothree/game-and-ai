# Missionaries and Cannibals

    missionaries_and_cannibals/
    │
    ├── main.py                       # 실행 스크립트
    ├── simulator.py                  # 문제 환경 시뮬레이터 (환경, 상태/행동 검증)
    ├── solver.py                     

    ├── strategies/
    │   ├── base_solver.py            # 공통 인터페이스 정의 (BaseSolver)
    │   ├── bfs_solver.py             # BFS 기반 솔버 (BfsSolver)
    │   └── rl_solver.py              # RL 기반 솔버 (RLSolver)

## SImulation

```bash
The game is starting! Move all missionaries and cannibals safely to the other side of the river.


------------------------------------------------------------
Right Bank                                         Left Bank
|# of Missionaries|0|                  |# of Missionaries|3|
|# of Cannibals   |0|                  |# of Cannibals   |3|
|# of Boat        |0|                  |# of Boat        |1|
------------------------------------------------------------
The number of missionaries to move: 0
The number of cannibals to move: 2
The number of boat to move in right bank: 1

...

------------------------------------------------------------
Right Bank                                         Left Bank
|# of Missionaries|3|                  |# of Missionaries|0|
|# of Cannibals   |3|                  |# of Cannibals   |0|
|# of Boat        |1|                  |# of Boat        |0|
------------------------------------------------------------
Game success! All missionaries and cannibals have safely crossed the river.
```

## Search Algorithm

- Breath-First Search
