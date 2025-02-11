import heapq
import random
import itertools

# Goal state for 8 puzzle
GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))  # 0 represents the blank space

# Possible moves
MOVES = {
    (0, -1),  # Left
    (0, 1),   # Right
    (-1, 0),  # Up
    (1, 0)    # Down
}

class Puzzle:
    """Represents an 8-puzzle state with methods for movement and heuristic calculations. """
    def __init__(self, state, parent=None, move=None, cost=0):
        self.state = state  # Stores the current puzzle state as a tuple
        self.parent = parent  # Reference to the parent state (used for path reconstruction)
        self.move = move  # The move taken to reach this state
        self.cost = cost  # g(n): cost from the start state to this state
        self.blank_pos = self.find_blank()  # Locate the blank tile (0)
    
    def find_blank(self):
        """Finds blank position in puzzle"""
        for r, row in enumerate(self.state):
            for c, val in enumerate(row):
                if val == 0:
                    return (r, c)  # Return location of index of blank space
        return None
    
    def possible_moves(self):
        """Possible puzzle states """
        r, c = self.blank_pos
        children = []
        
        for dr, dc in MOVES:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < 3 and 0 <= new_c < 3:  # Ensure move is within bounds
                new_state = [list(row) for row in self.state]
                new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]  # Swap blank
                children.append(Puzzle(tuple(tuple(row) for row in new_state), self, (dr, dc), self.cost + 1))
        
        return children

def generate_reachable_states(n=100):
    """Generates n solvable random 8-puzzle states."""
    states = set()
    while len(states) < n:
        shuffled = list(range(9))
        random.shuffle(shuffled)
        state = tuple(tuple(shuffled[i:i + 3]) for i in range(0, 9, 3))
        if is_solvable(state):
            states.add(state)
    return list(states)

def is_solvable(state):
    """Checks if given 8-puzzle state is solvable."""
    flat_list = [num for row in state for num in row if num != 0]
    inversions = sum(1 for i in range(len(flat_list)) for j in range(i + 1, len(flat_list)) if flat_list[i] > flat_list[j])
    return inversions % 2 == 0  # puzzle is solvable if the number of inversions is even

# Generate 100 reachable states
reachable_states = generate_reachable_states()
