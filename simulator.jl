struct Simulator
    state::Vector{Int}  # State: [number of missionaries on the right bank, number of cannibals on the right bank, boat position]
    goal_state::Vector{Int}

    function Simulator()
        new([3, 3, 1], [0, 0, 0])  # Initial state and goal state
    end

    function print_current_state(sim::Simulator)
        println("------------------------------------------------------------")
        println("Right Bank                                         Left Bank")
        println("|# of Missionaries| ", 3 - sim.state[1], " |                  |# of Missionaries| ", sim.state[1], " |")
        println("|# of Cannibals   | ", 3 - sim.state[2], " |                  |# of Cannibals   | ", sim.state[2], " |")
        println("|# of Boat        | ", 1 - sim.state[3], " |                  |# of Boat        | ", sim.state[3], " |")
        println("------------------------------------------------------------")
    end

    function is_valid_state(state::Vector{Int})
        right_missionaries, right_cannibals, _ = state
        left_missionaries = 3 - right_missionaries
        left_cannibals = 3 - right_cannibals

        return !(right_missionaries < 0 || right_missionaries > 3 || 
                 left_missionaries < 0 || left_cannibals < 0 || left_cannibals > 3)
    end

    function is_valid_action(missionary::Int, cannibal::Int)
        if missionary + cannibal > 2 || missionary + cannibal < 1
            println("You can move at least 1 and at most 2 people at a time.")
            return false
        end
        return true
    end

    function is_success(sim::Simulator)
        return sim.state == sim.goal_state
    end

    function is_failure(sim::Simulator)
        right_missionaries, right_cannibals, _ = sim.state
        left_missionaries = 3 - right_missionaries
        left_cannibals = 3 - right_cannibals

        return (right_missionaries > 0 && right_missionaries < right_cannibals) ||
               (left_missionaries > 0 && left_missionaries < left_cannibals)
    end

    function act(sim::Simulator, missionary::Int, cannibal::Int)
        if sim.state[3] == 1  # Boat is on the right bank
            new_state = [sim.state[1] - missionary, sim.state[2] - cannibal, 0]
        else  # Boat is on the left bank
            new_state = [sim.state[1] + missionary, sim.state[2] + cannibal, 1]
        end

        if is_valid_action(missionary, cannibal) && is_valid_state(new_state)
            sim.state = new_state
            print_current_state(sim)

            if is_success(sim)
                return true  # End successfully
            elseif is_failure(sim)
                return true  # End in failure
            end
        else
            println("The action is invalid. State remains unchanged.")
        end
        return false
    end
end

function play(sim::Simulator)
    println("The game is starting! Move all missionaries and cannibals safely to the other side of the river.")
    while true
        try
            print("Enter the number of missionaries to move: ")
            missionary_input = readline()
            println("Received missionary input: ", missionary_input)  # 디버그 출력
            missionary = parse(Int, missionary_input)

            print("Enter the number of cannibals to move: ")
            cannibal_input = readline()
            println("Received cannibal input: ", cannibal_input)  # 디버그 출력
            cannibal = parse(Int, cannibal_input)

            if Simulator.act(sim, missionary, cannibal)  # sim 객체를 통해 메서드 호출
                break  # Exit loop on success or failure
            end
        catch e
            println("Invalid input. Please enter a number.")
            println("Error message: ", e)  # 오류 메시지 출력
        end
    end

    # Print game end message
    if is_success(sim)
 