# IMO 2025 Problem 6: Grid Tiling

## Problem Statement

Consider an **n × n grid** of unit squares. Place non-overlapping rectangular
tiles on this grid (sides aligned with grid lines) such that:

- Every **row** has exactly **one** unit square that is **not** covered by any tile.
- Every **column** has exactly **one** unit square that is **not** covered by any tile.
- The number of tiles is **minimized**.

## What to Implement

Implement `solve(n: int) -> list[tuple[int, int, int, int]]` returning a list
of tiles. Each tile is `(row, col, height, width)` — all non-negative integers
with `row + height <= n` and `col + width <= n`.

```python
def solve(n: int = 10) -> list[tuple[int, int, int, int]]:
    # Return a list of (row, col, height, width) tiles.
    # Minimize len(tiles) subject to:
    #   - No overlapping tiles
    #   - Each row has exactly 1 uncovered square
    #   - Each column has exactly 1 uncovered square
    ...
```

## Scoring

- **Score = −(num_tiles / reference)** where reference = n*(n-1)//2.
- Higher (less negative) is better. Score **−1.0** matches the baseline.
- Solutions violating constraints receive heavy penalties.

## Hints

- The set of uncovered squares must be a **permutation matrix** (one per row,
  one per column).
- A key insight: for a given permutation of uncovered squares, the remaining
  (n² − n) covered cells can be tiled greedily.
- The number of tiles depends strongly on which permutation you choose.
- Try permutations p(i) = k*i mod n for various k coprime to n.
- The known optimal is approximately n + 2√n − 3 tiles for large n.
- You have 30 seconds to find the best tiling.
