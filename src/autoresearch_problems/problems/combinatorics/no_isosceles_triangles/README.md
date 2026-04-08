# No Isosceles Triangles

**Category:** combinatorics  
**Optimize:** Maximize `score`  
**Known best:** open

## Problem Statement

Find the largest subset of the n×n integer grid (n=64) such that no three points form an isosceles triangle. Formally, no ordered triple (a, b, c) satisfies dist(a, b) = dist(b, c) where dist is Euclidean distance.

Score = num_points / n. Higher is better.

## Input / Output

| Field | Value |
|---|---|
| Function name | `solve` |
| Output type | `list` |
| Parameters | `n: 64` |

## Scoring

The evaluator:
1. Checks that all returned points are distinct integer grid points in [0, n)².
2. Verifies no three points form an isosceles triangle.
3. Returns score = len(points) / n.

## Known Results

- For small grids the maximum is known exactly; for n=64 it is open.
- Random sets of ~n points tend to contain isosceles triangles; careful construction is needed.
- AlphaEvolve explored this problem as a combinatorial extremal problem.

## Source

Google DeepMind / AlphaEvolve (Apache 2.0)
