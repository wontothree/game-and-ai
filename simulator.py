class Simulator:
    def __init__(self):
        # State: [number of missionaries on the right bank, number of cannibals on the right bank, boat position]
        self.state = [3, 3, 1]
        self.goal_state = [0, 0, 0]

        self.right_missionaries = self.state[0]
        self.right_cannibals = self.state[1]
        self.right_boat = self.state[2]
        self.left_missionaries = 3 - self.right_missionaries
        self.left_cannibals = 3 - self.right_cannibals
        self.left_boat = 1 - self.state[2]

    def print_current_state(self):
        """
        Print the current state
        """
        print("------------------------------------------------------------")
        print("Right Bank                                         Left Bank")
        print(f"|# of Missionaries|{self.left_missionaries}|                  |# of Missionaries|{self.right_missionaries}|")
        print(f"|# of Cannibals   |{self.left_cannibals}|                  |# of Cannibals   |{self.right_cannibals}|")
        print(f"|# of Boat        |{self.left_boat}|                  |# of Boat        |{self.right_boat}|")
        print("------------------------------------------------------------")

    def is_valid_state(self, state):
        """
        Check if the state is valid
        """

        return (0 <= self.right_missionaries <= 3 and 0 <= self.right_cannibals <= 3 and
                0 <= self.left_missionaries <= 3 and 0 <= self.left_cannibals <= 3)

    def is_valid_action(self, missionary, cannibal):
        """
        Check if the action is valid
        """
        return 1 <= missionary + cannibal <= 2
    
    def is_success(self):
        """
        Check if the game has successfully ended
        """
        return self.state == self.goal_state

    def is_failure(self):
        """
        Check if the game has failed
        """

        return (0 < self.right_cannibals < self.right_missionaries) or (0 < self.left_cannibals < self.left_missionaries)

    def act(self, missionary, cannibal):
        """
        Perform the given action and update the state
        """
        if self.state[2] == 1:  # Boat is on the right bank
            new_state = [self.state[0] - missionary, self.state[1] - cannibal, 0]
        else:  # Boat is on the left bank
            new_state = [self.state[0] + missionary, self.state[1] + cannibal, 1]

        if self.is_valid_action(missionary, cannibal) and self.is_valid_state(new_state):
            self.state = new_state
            self.print_current_state()

            if self.is_success():
                return True  # End successfully
            elif self.is_failure():
                return True  # End in failure
        else:
            print("You can move at least 1 and at most 2 people at a time. The action is invalid. State remains unchanged.")
        return False

    def play(self):
        """
        Main loop to execute the game
        """
        print("The game is starting! Move all missionaries and cannibals safely to the other side of the river.")
        self.print_current_state()

        while True:
            try:
                missionary = int(input("Enter the number of missionaries to move: "))
                cannibal = int(input("Enter the number of cannibals to move: "))
                
                if self.act(missionary, cannibal):
                    break  # Exit loop on success or failure
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Print game end message
        if self.is_success():
            print("Game success! All missionaries and cannibals have safely crossed the river.")
        else:
            print("Game failure! Cannibals have eaten the missionaries.")

if __name__ == '__main__':
    simulator = Simulator()
    simulator.play()
