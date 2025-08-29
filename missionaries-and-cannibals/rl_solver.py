import random
from simulator import Simulator

class Solver:
    def __init__(self):
        self.simulator = Simulator()
        self.initial_state = self.simulator.state[:]
        self.goal_state = self.simulator.goal_state[:]
        self.visited_states = set()

        # Q-learning 파라미터
        self.alpha = 0.1  # 학습률
        self.gamma = 0.9  # 할인율
        self.epsilon = 0.1  # 탐색률 (epsilon-greedy)
        self.q_table = {}  # Q-테이블 초기화

    def generate_valid_states(self, state):
        """
        Generate all valid states from the current state.
        """
        valid_states = []
        right_missionaries, right_cannibals, boat_position = state

        # Determine possible actions (moving missionaries and cannibals)
        for missionary in range(0, 3):  # 0 to 2 missionaries
            for cannibal in range(0, 3):  # 0 to 2 cannibals
                # is valid action
                if self.simulator.is_valid_action([missionary, cannibal, boat_position]):
                    if boat_position == 1:  # Boat is on the right bank
                        new_state = [right_missionaries - missionary, right_cannibals - cannibal, 0]
                    else:  # Boat is on the left bank
                        new_state = [right_missionaries + missionary, right_cannibals + cannibal, 1]

                    # is valid state
                    if self.simulator.is_valid_state(new_state):
                        valid_states.append(new_state)

        return valid_states

    def get_q_value(self, state, action):
        """
        Q 테이블에서 주어진 상태와 행동에 대한 Q 값을 가져옵니다.
        """
        state_tuple = tuple(state)
        
        # Q-테이블에 상태가 없다면 초기화
        if state_tuple not in self.q_table:
            # 상태에 대해 가능한 모든 행동을 얻어와서 Q-테이블을 초기화
            self.q_table[state_tuple] = {tuple(action): 0 for action in self.generate_valid_states(state)}

        # 해당 상태와 행동에 대한 Q값을 반환
        return self.q_table[state_tuple].get(tuple(action), 0)

    def update_q_value(self, state, action, reward, next_state):
        """
        Q 값 업데이트 (Q-learning의 Bellman 방정식 적용)
        """
        current_q_value = self.get_q_value(state, action)

        # next_state가 Q 테이블에 없으면 초기화
        next_state_tuple = tuple(next_state)
        if next_state_tuple not in self.q_table:
            self.q_table[next_state_tuple] = {tuple(action): 0 for action in self.generate_valid_states(next_state)}

        # 다음 상태에서 가능한 Q값 중 가장 큰 값
        max_next_q_value = max(self.q_table[next_state_tuple].values()) if next_state else 0
        
        # 새로운 Q값 계산
        new_q_value = current_q_value + self.alpha * (reward + self.gamma * max_next_q_value - current_q_value)

        state_tuple = tuple(state)
        # 새로운 Q값을 테이블에 업데이트
        self.q_table[state_tuple][tuple(action)] = new_q_value

    def epsilon_greedy(self, state):
        """
        epsilon-greedy 방식으로 행동을 선택합니다.
        """
        if random.random() < self.epsilon:
            # 무작위로 행동 선택 (탐색)
            return random.choice(self.generate_valid_states(state))
        else:
            # Q 값이 가장 큰 행동 선택 (활용)
            state_tuple = tuple(state)
            q_values = self.q_table.get(state_tuple, {})
            if not q_values:
                return random.choice(self.generate_valid_states(state))
            max_q_value = max(q_values, key=q_values.get)
            return list(max_q_value)

    def rl_search(self, episodes=1000):
        """
        Q-learning을 사용하여 목표 상태를 찾습니다.
        """
        for episode in range(episodes):
            state = self.initial_state
            path = [state]
            while state != self.goal_state:
                action = self.epsilon_greedy(state)
                next_state = action
                reward = 1 if next_state == self.goal_state else 0  # 목표 상태에 도달하면 보상 1, 아니면 0
                self.update_q_value(state, action, reward, next_state)
                state = next_state
                path.append(state)

                if reward == 1:  # 목표 상태에 도달하면 종료
                    break

            if state == self.goal_state:
                return path  # 목표 상태에 도달한 경로 반환

        return None  # 목표 상태에 도달하지 못한 경우

if __name__ == '__main__':
    solver = Solver()
    solution = solver.rl_search(episodes=1000)  # 1000번의 에피소드 동안 학습

    if solution is not None:
        print("Solution found using RL!")
        for step in solution:
            print(step)
    else:
        print("No solution found using RL.")
