"""
 -------------------------------------
 8_puzzle.py
 
 -------------------------------------
 Edan Phillips, 190778550, phil7855@mylaurier.ca
 
 -------------------------------------
"""

import heapq
import random
import itertools

# Goal state of the 8-puzzle problem
GOAL_STATE = ((1, 2, 3), (4, 5, 6), (7, 8, 0))  # 0 represents the blank space

# Possible moves
MOVES = {
    (0, -1),  # Left
    (0, 1),   # Right
    (-1, 0),  # Up
    (1, 0)    # Down
}

class Puzzle:
    def __init__(self, state, parent=None, move=None, cost=0):
        """
        Represents an 8-puzzle state with methods for movement and heuristic calculations
        state (tuple): A tuple representing the current puzzle configuration
        parent (Puzzle, optional): Reference to the parent state for path reconstruction
        move (tuple, optional): The move taken to reach this state
        cost (int, optional): The g(n) cost from the start state to this state
        """
        self.state = state  # Stores the current puzzle state as a tuple
        self.parent = parent  # Reference to the parent state (used for path reconstruction)
        self.move = move  # The move taken to reach this state
        self.cost = cost  # g(n): cost from the start state to this state
        self.blank_pos = self.find_blank()  # Locate the blank tile (0)
    
    def find_blank(self):
        """
        Finds the blank position in the puzzle.
        Returns:
            blank_pos (tuple or None): Position of the blank tile (0), or None if not found.
        """
        for r, row in enumerate(self.state):
            for c, val in enumerate(row):
                if val == 0:
                    return (r, c)  # Return location of index of blank space
        return None # Return none if blank tile is not found
    
    def possible_moves(self):
        """
        Creates new puzzle states by moving the blank tile.
        Returns:
            children (list): A list of new puzzle instances showing valid moves.
        """
        r, c = self.blank_pos
        children = []
        
        for dr, dc in MOVES:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < 3 and 0 <= new_c < 3:  # Ensure move is within bounds
                new_state = [list(row) for row in self.state] # Convert tuple to list 
                new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]  # Swap blank
                children.append(Puzzle(tuple(tuple(row) for row in new_state), self, (dr, dc), self.cost + 1)) # Create a new Puzzle instance and add it to the list of children
        
        return children

    def __eq__(self, other):
        return self.state == other.state  # Check if two puzzle states are identical
    
    def __lt__(self, other):
        return False  # Required for heapq operations but not used in comparison
    
    def __hash__(self):
        return hash(self.state)  # Allows puzzle state to be stored in sets

def h1_misplaced_tiles(state):
    """
    Counts the number of misplaced tiles compared to the goal state.
    Args:
        state (tuple): The current puzzle state.
    
    Returns:
        misplaced_count (int): Number of tiles not in their goal positions.
    """
    return sum(1 for r in range(3) for c in range(3) if state[r][c] and state[r][c] != GOAL_STATE[r][c])

def h2_manhattan_distance(state):
    """
    Calculates Manhattan distance heuristic.
    Args:
        state (tuple): The current puzzle state.
    Returns:
        dist (int): The sum of the Manhattan distances of all tiles from their goal positions.
    """
    dist = 0
    for r in range(3): # Iterate through each row
        for c in range(3): # Iterate through each column
            val = state[r][c]
            if val != 0:  # Ignore blank tile
                goal_r, goal_c = (val - 1) // 3, (val - 1) % 3
                dist += abs(goal_r - r) + abs(goal_c - c)  # Compute Manhattan distance
    return dist

def h3_pattern_database(state):
    """
    Pattern Database heuristic by referencing calculated distances for a subset of tiles.
    Args:
        state (tuple): The current puzzle state.
    Returns:
        heuristic_value (int): A heuristic value based on calculated tile distances.
    """
    pattern_goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0)
    }
    heuristic_value = 0
    for r in range(3): # Iterate through each row
        for c in range(3): # Iterate through each column
            val = state[r][c]
            if val in pattern_goal_positions:
                goal_r, goal_c = pattern_goal_positions[val]
                heuristic_value += abs(goal_r - r) + abs(goal_c - c) # Compute Manhattan distance for subset
    return heuristic_value

def a_star_search(start_state, heuristic):
    """    
    Performs A* search to solve the 8-puzzle using the given heuristic.
    Args:
        start_state (Puzzle): The initial puzzle state.
        heuristic (function): The heuristic function to evaluate states.
    Returns:
        steps (int): Number of steps taken to reach the goal.
        nodes_expanded (int): Number of nodes expanded during the search.
    """
    open_set = []
    heapq.heappush(open_set, (0, start_state)) # Initialize priority queue
    visited = set()
    steps = 0
    nodes_expanded = 0
    while open_set: # Process nodes in priority queue
        _, current = heapq.heappop(open_set)
        steps += 1
        if current.state == GOAL_STATE:
            return steps, nodes_expanded
        visited.add(current.state)
        for child in current.possible_moves(): # create child nodes
            if child.state not in visited:
                f_cost = child.cost + heuristic(child.state)
                heapq.heappush(open_set, (f_cost, child))
                nodes_expanded += 1
    return None

def create_reachable_states(n=100):
    """
Creates n solvable random 8-puzzle states.
    Args:
        n (int, optional): The number of states to generate. Defaults to 100.
    Returns:
        states_list (list): List of solvable 8-puzzle states.
    """
    states = set()
    while len(states) < n:
        shuffled = list(range(9)) # Create a list containing numbers 0 to 8
        random.shuffle(shuffled)  # Randomly shuffle the numbers to create a new puzzle state
        state = tuple(tuple(shuffled[i:i + 3]) for i in range(0, 9, 3)) # Turn shuffled list into a 3x3 tuple representation of the puzzle
        if is_solvable(state):
            states.add(state)
    return list(states) # Turn set to list before returning

def is_solvable(state):
    """
        Checks if the given 8-puzzle state is solvable.
    Args:
        state (tuple): The current puzzle state.
    Returns:
        solvable (bool): True if solvable, False otherwise.
    """
    flat_list = [num for row in state for num in row if num != 0]
    inversions = sum(1 for i in range(len(flat_list)) for j in range(i + 1, len(flat_list)) if flat_list[i] > flat_list[j])
    return inversions % 2 == 0

reachable_states = create_reachable_states() # Generate 100 reachable states


print("Puzzle Type | Heuristic | Average Steps to Solution | Average Nodes Expanded")
for state in reachable_states:
    puzzle = Puzzle(state)
    steps_h1, nodes_h1 = a_star_search(puzzle, h1_misplaced_tiles)
    steps_h2, nodes_h2 = a_star_search(puzzle, h2_manhattan_distance)
    steps_h3, nodes_h3 = a_star_search(puzzle, h3_pattern_database)
    print(f"8-puzzle | h1 | {steps_h1} | {nodes_h1}") # Output for h1 
    print(f"8-puzzle | h2 | {steps_h2} | {nodes_h2}") # Output for h2
    print(f"8-puzzle | h3 | {steps_h3} | {nodes_h3}") # Output for h3
