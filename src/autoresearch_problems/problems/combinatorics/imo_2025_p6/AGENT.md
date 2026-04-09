# Agent Guide — IMO 2025 Problem 6

## Goal

Return a list of tile specifications for an n=10 grid such that each row and column has exactly one uncovered cell, using as few tiles as possible; score = −num_tiles/45, maximize toward 0.

## Strategy hints

- Think of the uncovered cells as defining a permutation matrix (one per row, one per column).
- For a given placement of uncovered cells, greedily merge adjacent covered cells into maximal rectangles.
- A Latin square of size n gives a valid uncovering pattern; then tile the remaining cells.
- Aim to use large tiles (spanning many rows/columns) to minimize tile count.
- The minimum tile count is related to the number of "rectangles" needed to cover all cells except a permutation.

## Output format

Return a Python `list` of tile records. Each tile is likely a tuple/list `(row_start, col_start, row_end, col_end)` representing an axis-aligned rectangle. Check the evaluator for exact format.

```python
def solve(n: int = 10) -> list:
    # Diagonal uncovered cells: (i, i) for i in 0..9
    # Cover remaining cells with row-by-row tiles
    tiles = []
    for row in range(n):
        uncovered_col = row
        if uncovered_col > 0:
            tiles.append((row, 0, row, uncovered_col - 1))
        if uncovered_col < n - 1:
            tiles.append((row, uncovered_col + 1, row, n - 1))
    return tiles
```

## Pitfalls

- If any row or column has 0 or ≥2 uncovered cells, the solution is invalid.
- Overlapping tiles are not allowed.
- Merging tiles incorrectly can leave gaps (uncovered cells) that violate constraints.

## Baseline

The diagonal uncovered pattern with 2 tiles per row gives 2×10 = 20 tiles (score ≈ −0.44). Smarter merging can reduce this to ~10 tiles.
