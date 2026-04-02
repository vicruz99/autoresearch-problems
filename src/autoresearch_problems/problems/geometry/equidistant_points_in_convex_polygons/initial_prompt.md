# Equidistant Points in Convex Polygons

## Problem

There is a conjecture in combinatorial geometry:

> **Every convex polygon has at least one vertex v such that no 4 other vertices are equidistant from v.**

Your goal is to **find a counterexample** — a convex polygon where *every* vertex has (at least) 4 approximately equidistant neighbours — or get as close as possible.

## What to implement

Implement `solve(num_vertex: int) -> np.ndarray` that returns a convex polygon
as a 2-D float array of shape `(num_vertex, 2)`.  The vertices should be given
in order (either clockwise or counterclockwise).

```python
import numpy as np

def solve(num_vertex: int = 10) -> np.ndarray:
    # Return shape (num_vertex, 2): polygon vertices in order
    ...
```

## Scoring

The evaluator:
1. Normalises the polygon (centres it and scales the average vertex distance to 1).
2. Checks it is **strictly convex**.
3. For each vertex v, sorts the distances to the other `num_vertex - 1` vertices,
   finds the pair of consecutive distances with the **smallest gap**, defines a
   target distance `D_v` as the midpoint of that gap, and selects the 4 distances
   nearest to that gap.
4. Per-vertex score = `1 / mean(max(d/D_v, D_v/d) for the 4 chosen distances)`.
   This equals 1 when those 4 distances equal `D_v` exactly.
5. **Final score = minimum per-vertex score** (in [0, 1]).

A score of **1.0** would be a perfect counterexample.  A regular polygon scores
near 0 (only 2 equidistant neighbours per vertex, not 4).

## Notes

- You are free to choose any `num_vertex`; the evaluator uses the same value you pass in.
- The polygon **must** be strictly convex after normalisation (non-convex polygons receive score 0).
- Scores are in [0, 1]; higher is better.
- Hint: polygons with high rotational symmetry and carefully chosen vertex spacings tend to score well.
