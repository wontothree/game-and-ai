class Simulator:
    def __init__(self):
        # State: [number of missionaries on the right bank, number of cannibals on the right bank, boat position]
        self.state = [3, 3, 1]  # Initial state: 3 missionaries, 3 cannibals, boat on the right bank
        self.goal_state = [0, 0, 0]  # Goal state: all on the left bank

    def print_state(self):
        """
        Print the current state
        """
        right_missionaries, right_cannibals, boat = self.state
        left_missionaries = 3 - right_missionaries
        left_cannibals = 3 - right_cannibals

        print("\n")
        print("------------------------------------------------------------")
        print("Right Bank                                         Left Bank")
        print(f"|# of Missionaries|{left_missionaries}|                  |# of Missionaries|{right_missionaries}|")
        print(f"|# of Cannibals   |{left_cannibals}|                  |# of Cannibals   |{right_cannibals}|")
        print(f"|# of Boat        |{1 - boat}|                  |# of Boat        |{boat}|")
        print("------------------------------------------------------------")

    def is_success(self):
        """
        Check if the game has successfully ended
        """
        return self.state == self.goal_state

    def is_failure(self):
        """
        Check if the game has failed
        """
        right_missionaries, right_cannibals = self.state[0], self.state[1]
        left_missionaries = 3 - right_missionaries
        left_cannibals = 3 - right_cannibals

        return (0 < left_missionaries < left_cannibals) or (0 < right_missionaries < right_cannibals)
    
    def is_valid_action(self, action):
        """
        Check if the action is valid
        """
        return 1 <= action[0] + action[1] <= 2
    
    def is_valid_state(self, state):
        """
        Check if the state is valid
        """
        right_missionaries = state[0]
        right_cannibals = state[1]
        left_missionaries = 3 - right_missionaries
        left_cannibals = 3 - right_cannibals

        # Valid state if no more cannibals than missionaries on either bank
        return 0 <= right_missionaries <= 3 and 0 <= right_cannibals <= 3 and \
                0 <= left_missionaries <= 3 and 0 <= left_cannibals <= 3

    def act(self, action):
        """
        Perform the given action and update the state
        """
        right_missionaries, right_cannibals, boat = self.state

        # Determine the new state based on boat position
        if action[2] == 1:  # Boat is on the right bank
            new_state = [right_missionaries - action[0], right_cannibals - action[1], 0]
        elif action[2] == 0:  # Boat is on the left bank
            new_state = [right_missionaries + action[0], right_cannibals + action[1], 1]

        # inspect validity of action
        if self.is_valid_action(action) and self.is_valid_state(new_state):
            # Update the state
            self.state = new_state
        else:
            print("Invalid action or invalid state.")

    def play(self):
        """
        Main loop to execute the game
        """
        print("The game is starting! Move all missionaries and cannibals safely to the other side of the river.")

        while True:
            try:
                self.print_state()

                if self.is_success():
                    print("Game success! All missionaries and cannibals have safely crossed the river.")
                    break
                if self.is_failure():
                    print("Game failure! Cannibals have eaten the missionaries.")
                    break

                missionary = int(input("The number of missionaries to move: "))
                cannibal = int(input("The number of cannibals to move: "))

                if self.state[2] == 1:
                    boat = 1
                    print("The number of boat to move in right bank: 1")
                elif self.state[2] == 0:
                    boat = 0
                    print("The number of boat in left bank: 1")
                
                action = [missionary, cannibal, boat]
                self.act(action)
            
            except ValueError:
                print("Invalid input. Please enter a number.")

if __name__ == '__main__':
    simulator = Simulator()
    simulator.play()
