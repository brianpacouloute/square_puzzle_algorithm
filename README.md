# A* Algorithm Implementation for Square Puzzles
Calculates the average steps to solution and nodes expanded using the A* algorithm given 3 distinct heuristics for the solving of 8 and 15-puzzles. 

## Heuristics
The algorithm will use the following heuristic logic for calculating distances:
- `h1`: Simple misplaced tiles count comparison to goal state.
- `h2`: Manhattan distance heuristic.
- `h3`: Pattern database heuristic (for 8-Puzzle)/Manhattan Linear conflict heuristic (for 15-Puzzle)

## Setup and Install
To run the code, you must install [Git](https://git-scm.com/downloads) and [Python](https://www.python.org/).

1. Clone the repository:
```bash
git clone https://github.com/brianpacouloute/square_puzzle_algorithm
```

2. Change to directory:
```bash
cd square_puzzle_algorithm
```

### Running the 8-Puzzle Calculations

3. a) Run the Python script via Python installed from python.org:
```bash
py 8puzzle.py
```

3. b) Run the Python script via Python installed from Microsoft Store:
```bash
python 8puzzle.py
```

### Running the 15-Puzzle Calculations

4. a) Run the Python script via Python installed from python.org:
```bash
py 15puzzle.py
```

4. b) Run the Python script via Python installed from Microsoft Store:
```bash
python 15puzzle.py
```
