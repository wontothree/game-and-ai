class Simulator:
    def __init__(self):
        # State: [number of missionaries on the right bank, number of cannibals on the right bank, boat position]
        self.state = [3, 3, 1]
        self.goal_state = [0, 0, 0]

    def print_current_state(self):
        """
        Print the current state
        """
        print("------------------------------------------------------------")
        print("Right Bank                                         Left Bank")
        print(f"|# of Missionaries|{3 - self.state[0]}|                  |# of Missionaries|{self.state[0]}|")
        print(f"|# of Cannibals   |{3 - self.state[1]}|                  |# of Cannibals   |{self.state[1]}|")
        print(f"|# of Boat        |{1 - self.state[2]}|                  |# of Boat        |{self.state[2]}|")
        print("------------------------------------------------------------")

    def is_valid_state(self, state):
        """
        Check if the state is valid
        """
        right_missionaries, right_cannibals, _ = state
        left_missionaries = 3 - right_missionaries
        left_cannibals = 3 - right_cannibals

        if (right_missionaries < 0 or right_missionaries > 3 or 
            left_missionaries < 0 or left_cannibals < 0 or left_cannibals > 3):
            return False # failure
        
        return True # success

    def is_valid_action(self, missionary, cannibal):
        """
        Check if the action is valid
        """
        if missionary + cannibal > 2 or missionary + cannibal < 1:
            return False
        return True
    
    def is_success(self):
        """
        Check if the game has successfully ended
        """
        return self.state == self.goal_state

    def is_failure(self):
        """
        Check if the game has failed
        """
        right_missionaries, right_cannibals, _ = self.state
        left_missionaries = 3 - right_missionaries
        left_cannibals = 3 - right_cannibals

        if right_missionaries > 0 and right_missionaries < right_cannibals:
            return True
        if left_missionaries > 0 and left_missionaries < left_cannibals:
            return True
        
        return False

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
