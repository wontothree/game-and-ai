from collections import deque
from missionaries_and_cannibals_simulator import Simulator

class BFS:
    def __init__(self):
        self.simulator = Simulator()
        self.initial_state = self.simulator.state[:]
        self.goal_state = self.simulator.goal_state[:]
        self.visited_states = set()

    def generate_valid_states(self, state):
        """
        Generate all valid states from the current state and add them to the queue
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

    def bfs_search(self):
        """
        Perform BFS to find a solution
        """
        queue = deque([(self.initial_state, [])])  # (current state, path to this state)
        self.visited_states.add(tuple(self.initial_state))  # Add initial state to visited

        while queue:
            current_state, path = queue.popleft()
            
            # Check if current state is the goal state
            if current_state == self.goal_state:
                return path + [current_state]  # Return the path including the goal state
            
            # Generate valid states from the current state
            for next_state in self.generate_valid_states(current_state):
                if tuple(next_state) not in self.visited_states:
                    self.visited_states.add(tuple(next_state))
                    queue.append((next_state, path + [current_state]))  # Append new state and path

        return None  # No solution found

if __name__ == '__main__':
    bfs = BFS()
    solution = bfs.bfs_search()

    if solution is not None:
        print("Solution found!")
        for step in solution:
            print(step)
    else:
        print("No solution found.")
