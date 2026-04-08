# IMO 2025 Problem 6

**Category:** combinatorics  
**Optimize:** Maximize `score` (minimize tiles)  
**Known best:** open

## Problem Statement

IMO 2025 Problem 6: Given an n×n grid (n=10), place non-overlapping rectangular tiles (sides aligned with the grid) such that every row and every column has exactly one uncovered unit square. Minimize the number of tiles used.

Score = −(num_tiles / reference_tiles) where reference = n×(n−1)/2 = 45. Higher (less negative) is better. Score −1.0 matches the reference.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `list` |
| Parameters | `n: 10` |

## Scoring

The evaluator:
1. Verifies that every row has exactly 1 uncovered cell and every column has exactly 1 uncovered cell.
2. Verifies tiles are non-overlapping and axis-aligned.
3. Returns score = −(num_tiles / 45).

## Known Results

- Minimum number of tiles for a 10×10 grid is conjectured to be around n−1 = 9 (one tile per pair of rows/columns).
- This was IMO 2025 Problem 6, making it a very recent competition problem.
- The reference score of 45 = n(n−1)/2 corresponds to using a triangular number of tiles.

## Source

[AlphaEvolve repository of problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems)
