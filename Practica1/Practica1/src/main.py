from src.core.search import bfs, dfs
from src.core.metrics import measure
from src.problems.maze import generate_maze, maze_neighbors
from src.gui.maze_view import animate_maze
from src.problems.water_jug import jug_neighbors, goal_state
from src.problems.puzzle8 import puzzle_neighbors, is_goal

def main():
    n = 10
    grid = generate_maze(n, wall_prob=0.15, seed=3)
    start = (0, 0)
    goal = (n - 1, n - 1)

    bfs_perf = measure(lambda: bfs(
        start=start,
        is_goal=lambda s: s == goal,
        neighbors=lambda s: maze_neighbors(grid, s),
    ))

    dfs_perf = measure(lambda: dfs(
        start=start,
        is_goal=lambda s: s == goal,
        neighbors=lambda s: maze_neighbors(grid, s),
        depth_limit=500
    ))

    print("=== LABERINTO 10x10 ===")
    print(f"BFS -> found={bfs_perf.result.found} time={bfs_perf.seconds:.6f}s peak={bfs_perf.peak_kb:.1f}KB "
          f"expanded={bfs_perf.result.expanded} visited={bfs_perf.result.visited_count} "
          f"frontierMax={bfs_perf.result.frontier_max} pathLen={len(bfs_perf.result.path)}")

    print(f"DFS -> found={dfs_perf.result.found} time={dfs_perf.seconds:.6f}s peak={dfs_perf.peak_kb:.1f}KB "
          f"expanded={dfs_perf.result.expanded} visited={dfs_perf.result.visited_count} "
          f"frontierMax={dfs_perf.result.frontier_max} pathLen={len(dfs_perf.result.path)}")


    animate_maze(grid, bfs_perf.result.exploration, bfs_perf.result.path)
    print("\n=== PROBLEMA DE LAS JARRAS ===")

a_cap = 3
b_cap = 5
target = 4

start = (0, 0)

bfs_jug = measure(lambda: bfs(
    start=start,
    is_goal=lambda s: goal_state(target, s),
    neighbors=lambda s: jug_neighbors(a_cap, b_cap, s)
))

dfs_jug = measure(lambda: dfs(
    start=start,
    is_goal=lambda s: goal_state(target, s),
    neighbors=lambda s: jug_neighbors(a_cap, b_cap, s)
))

print("BFS Jarras:", bfs_jug.result.path)
print("DFS Jarras:", dfs_jug.result.path)

print("\n=== 8 PUZZLE ===")

start_puzzle = (
    1, 2, 3,
    4, 5, 6,
    0, 7, 8
)

bfs_puzzle = measure(lambda: bfs(
    start=start_puzzle,
    is_goal=is_goal,
    neighbors=puzzle_neighbors
))

dfs_puzzle = measure(lambda: dfs(
    start=start_puzzle,
    is_goal=is_goal,
    neighbors=puzzle_neighbors,
    depth_limit=20
))

print("BFS Puzzle:", bfs_puzzle.result.path)
print("DFS Puzzle:", dfs_puzzle.result.path)
    
if __name__ == "__main__":
    main()