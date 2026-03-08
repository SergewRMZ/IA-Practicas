import random
from typing import Iterable, List, Tuple

Cell = Tuple[int, int]

def generate_maze(n: int, wall_prob: float = 0.28, seed: int | None = None) -> List[List[int]]:
    rng = random.Random(seed)
    grid = [[0 for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            if (r, c) in [(0, 0), (n - 1, n - 1)]:
                continue
            grid[r][c] = 1 if rng.random() < wall_prob else 0
    return grid

def maze_neighbors(grid: List[List[int]], cell: Cell) -> Iterable[Cell]:
    n = len(grid)
    r, c = cell
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
            yield (nr, nc)