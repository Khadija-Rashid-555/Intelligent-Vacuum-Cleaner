import time
from collections import deque
import heapq

# Grid setup
ROWS, COLS = 6, 6

def create_grid():
    return [
        [0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0],
    ]
# 0 = dirty, 1 = obstacle

DIRECTIONS = [(-1,0),(1,0),(0,-1),(0,1)]

def get_neighbors(grid, pos):
    r, c = pos
    neighbors = []
    for dr, dc in DIRECTIONS:
        nr, nc = r+dr, c+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] != 1:
            neighbors.append((nr, nc))
    return neighbors

def get_dirty_cells(grid):
    return [(r, c) for r in range(ROWS) for c in range(COLS) if grid[r][c] == 0]

# ───── BFS ─────
def bfs(grid, start):
    dirty = set(get_dirty_cells(grid))
    visited_order = []
    visited = set()
    queue = deque([(start, [start])])
    visited.add(start)
    steps = 0

    while queue and dirty:
        pos, path = queue.popleft()
        steps += 1
        if pos in dirty:
            dirty.remove(pos)
            visited_order.append(pos)
        for neighbor in get_neighbors(grid, pos):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return visited_order, steps

# ───── DFS ─────
def dfs(grid, start):
    dirty = set(get_dirty_cells(grid))
    visited_order = []
    visited = set()
    stack = [(start, [start])]
    steps = 0

    while stack and dirty:
        pos, path = stack.pop()
        if pos in visited:
            continue
        visited.add(pos)
        steps += 1
        if pos in dirty:
            dirty.remove(pos)
            visited_order.append(pos)
        for neighbor in get_neighbors(grid, pos):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))

    return visited_order, steps

# ───── Heuristic (A* style greedy) ─────
def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def heuristic_search(grid, start):
    dirty = set(get_dirty_cells(grid))
    visited_order = []
    visited = set()
    pos = start
    steps = 0

    while dirty:
        visited.add(pos)
        if pos in dirty:
            dirty.remove(pos)
            visited_order.append(pos)
        steps += 1

        neighbors = get_neighbors(grid, pos)
        unvisited = [n for n in neighbors if n not in visited]

        if not unvisited:
            # find nearest dirty cell via heap
            if dirty:
                heap = [(manhattan(pos, d), d) for d in dirty]
                heapq.heapify(heap)
                _, pos = heapq.heappop(heap)
            else:
                break
        else:
            if dirty:
                pos = min(unvisited, key=lambda n: min(manhattan(n, d) for d in dirty))
            else:
                break

    return visited_order, steps

# ───── Run & Compare ─────
def run_comparison():
    print("=" * 55)
    print("       SMART VACUUM CLEANER - ALGORITHM COMPARISON")
    print("=" * 55)

    grid = create_grid()
    start = (0, 0)
    total_dirty = len(get_dirty_cells(grid))

    print(f"\nGrid size : {ROWS}x{COLS}")
    print(f"Start pos : {start}")
    print(f"Dirty cells: {total_dirty}")
    print(f"Obstacles  : {sum(row.count(1) for row in grid)}")
    print("\nGrid (0=dirty, 1=obstacle, S=start):")
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            if (r,c) == start:
                row_str += "S "
            elif grid[r][c] == 1:
                row_str += "# "
            else:
                row_str += ". "
        print(" ", row_str)

    algorithms = [
        ("BFS (Breadth-First Search)", bfs),
        ("DFS (Depth-First Search)",   dfs),
        ("Heuristic Search (Greedy)",  heuristic_search),
    ]

    results = []
    print("\n" + "-" * 55)
    for name, algo in algorithms:
        start_time = time.perf_counter()
        cleaned, steps = algo(create_grid(), start)
        elapsed = (time.perf_counter() - start_time) * 1000

        results.append((name, len(cleaned), steps, elapsed))
        print(f"\n{name}")
        print(f"  Cells cleaned : {len(cleaned)} / {total_dirty}")
        print(f"  Steps taken   : {steps}")
        print(f"  Time (ms)     : {elapsed:.4f}")
        print(f"  Clean order   : {cleaned}")

    print("\n" + "=" * 55)
    print("  PERFORMANCE SUMMARY")
    print("=" * 55)
    print(f"{'Algorithm':<30} {'Cleaned':>7} {'Steps':>6} {'Time(ms)':>10}")
    print("-" * 55)
    for name, cleaned, steps, t in results:
        short = name.split("(")[0].strip()
        print(f"{short:<30} {cleaned:>7} {steps:>6} {t:>10.4f}")

    best_steps = min(results, key=lambda x: x[2])
    best_time  = min(results, key=lambda x: x[3])
    print("\n  Winner (fewest steps) :", best_steps[0].split("(")[0].strip())
    print("  Winner (fastest time) :", best_time[0].split("(")[0].strip())
    print("=" * 55)

if __name__ == "__main__":
    run_comparison()