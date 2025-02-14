"""
 -------------------------------------
 15_puzzle.py
 
 -------------------------------------
 Hamad Sultan, 169022428, sult2428@mylaurier.ca
 
 -------------------------------------
"""

import heapq
import random

# Goal state for the 15-puzzle (4x4 grid)
GOAL_STATE = ((1,  2,  3,  4), (5,  6,  7,  8), (9, 10, 11, 12), (13, 14, 15, 0))  # 0 represents the blank tile

# Possible moves for the blank tile
MOVES = {
    (0, -1),  # Left
    (0, 1),   # Right
    (-1, 0),  # Up
    (1, 0)    # Down
}

class Puzzle:
    def __init__(self, state, parent=None, move=None, cost=0):
        """
        Represents a 15-puzzle state.
        state (tuple): A tuple representing the current 4x4 puzzle configuration.
        parent (Puzzle, optional): Reference to the parent state.
        move (tuple, optional): The move taken to reach this state.
        cost (int, optional): g(n) - cost from start to this state.
        """
        self.state = state # Stores the current puzzle state as a tuple
        self.parent = parent # Reference to the parent state (used for path reconstruction)
        self.move = move # The move taken to reach this state
        self.cost = cost  # g(n): cost from the start state to this state
        self.blank_pos = self.find_blank() # Locate the blank tile (0)
    
    def find_blank(self):
        """
        Finds the blank position in the puzzle.
        Returns:
            blank_pos (tuple or None): Position of the blank tile (0), or None if not found.
        """
        for r, row in enumerate(self.state):
            for c, val in enumerate(row):
                if val == 0:
                    return (r, c) # Return location of index of blank space
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
            if 0 <= new_r < 4 and 0 <= new_c < 4:  # Ensure move is within bounds
                new_state = [list(row) for row in self.state]  # Convert tuple to list
                new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]  # Swap blank
                children.append(Puzzle(tuple(tuple(row) for row in new_state), self, (dr, dc), self.cost + 1))
        
        return children

    def __eq__(self, other):
        return self.state == other.state  # Check if two puzzle states are identical
    
    def __hash__(self):
        return hash(self.state)  # Enables storing state in sets

    def __lt__(self, other):
        # Compare total cost
        return (self.cost + h2_manhattan_distance(self.state)) < (other.cost + h2_manhattan_distance(other.state))

def h1_misplaced_tiles(state):
    """
    Counts the number of misplaced tiles compared to the goal state.
    Args:
        state (tuple): The current puzzle state.
    
    Returns:
        misplaced_count (int): Number of tiles not in their goal positions.
    """
    return sum(1 for r in range(4) for c in range(4) if state[r][c] and state[r][c] != GOAL_STATE[r][c])

def h2_manhattan_distance(state):
    """
    Calculates Manhattan distance heuristic.
    Args:
        state (tuple): The current puzzle state.
    Returns:
        dist (int): The sum of the Manhattan distances of all tiles from their goal positions.
    """
    dist = 0
    for r in range(4): # Iterate through each row
        for c in range(4): # Iterate through each column
            val = state[r][c]
            if val != 0: # Ignore blank tile
                goal_r, goal_c = (val - 1) // 4, (val - 1) % 4
                dist += abs(goal_r - r) + abs(goal_c - c) # Compute Manhattan distance
    return dist

def linear_conflict(state):
    """
    The linear conflict heuristic is better than the Manhattan distance in that it includes a penalty for when two tiles block 
    each other from moving into their correct positions.

    There is a conflict when:
    Two tiles are within the same column or row that they belong to.
    They are exchanged (in the wrong positions), so one tile has to move before the other can go to its destination.
    As the solution to this conflict always has at least 2 more moves, we add +2 per conflict so that the heuristic is more accurate.

    Args:
        state (tuple): The current puzzle state.

    Returns:
        heuristic_value (int): The computed heuristic value (Manhattan + conflict penalties).
    """
    conflict = 0
    size = 4 # Grid is 4 x 4

    # Row Conflicts:
    for i in range(size): # Iterate through each row
        for j in range(size): # Iterate through each column in row
            tile1 = state[i][j]  # Current tile
            # Check if the tile is in the correct row but might be out of order
            if tile1 != 0 and (tile1 - 1) // size == i:
                for k in range(j + 1, size):
                    tile2 = state[i][k]
                    if tile2 != 0 and (tile2 - 1) // size == i: # Tile2 is also in correct row
                        if (tile1 - 1) % size > (tile2 - 1) % size: # If tiles are in reverse order
                            conflict += 1

    # Checking for column conflicts, same logic as before
    for j in range(size):
        for i in range(size):
            tile1 = state[i][j]
            if tile1 != 0 and (tile1 - 1) % size == j:
                for k in range(i + 1, size):
                    tile2 = state[k][j]
                    if tile2 != 0 and (tile2 - 1) % size == j:
                        if (tile1 - 1) // size > (tile2 - 1) // size:
                            conflict += 1
    return conflict * 2 # Each conflict adds a penalty of 2 to the heuristic

def h3_manhattan_linear(state):
    # Manhattan distance plus linear conflict (new heuristic)
    return h2_manhattan_distance(state) + linear_conflict(state)

def a_star_search(start_state, heuristic):
    """    
    Performs A* search to solve the 15-puzzle using the given heuristic.
    Args:
        start_state (Puzzle): The initial puzzle state.
        heuristic (function): The heuristic function to evaluate states.
    Returns:
        steps (int): Number of steps taken to reach the goal.
        nodes_expanded (int): Number of nodes expanded during the search.
    """
    open_set = []
    heapq.heappush(open_set, (start_state.cost + heuristic(start_state.state), start_state)) # Initialize priority queue
    visited = {start_state.state: start_state.cost}
    steps = 0
    nodes_expanded = 0
    
    while open_set: # Process nodes in priority queue
        _, current = heapq.heappop(open_set)
        steps += 1
        if current.state == GOAL_STATE:
            return steps, nodes_expanded
        for child in current.possible_moves(): # create child nodes
            nodes_expanded += 1
            g = child.cost
            if child.state not in visited or g < visited[child.state]:
                visited[child.state] = g
                heapq.heappush(open_set, (g + heuristic(child.state), child))
    return None

def create_reachable_states(n=100, moves=10):
    """
    Creates n solvable random 15-puzzle states.
    Args:
        n (int, optional): The number of states to generate. Defaults to 100.
    Returns:
        states_list (list): List of solvable 15-puzzle states.
    """
    states = set()
    while len(states) < n:
        current = Puzzle(GOAL_STATE)
        for _ in range(moves):
            neighbors = current.possible_moves()
            current = random.choice(neighbors)
        states.add(current.state)
    return list(states)

reachable_states = create_reachable_states() # Generate 100 reachable states

print("Puzzle Type | Heuristic | Average Steps to Solution | Average Nodes Expanded")
print("============|===========|===========================|=======================")
for state in reachable_states:
    puzzle = Puzzle(state)
    steps_h1, nodes_h1 = a_star_search(puzzle, h1_misplaced_tiles)
    steps_h2, nodes_h2 = a_star_search(puzzle, h2_manhattan_distance)
    steps_h3, nodes_h3 = a_star_search(puzzle, h3_manhattan_linear)
    print(f"15-puzzle   | h1        | {steps_h1:<25,} | {nodes_h1:,}") # Output for h1 
    print(f"15-puzzle   | h2        | {steps_h2:<25,} | {nodes_h2:,}") # Output for h2
    print(f"15-puzzle   | h3        | {steps_h3:<25,} | {nodes_h3:,}") # Output for h3
    print("            |           |                           |")

print("============================================================================")