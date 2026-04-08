# Agent Guide — Equidistant Points in Convex Polygons

## Goal

Return a numpy array of shape `(10, 2)` representing 10 vertices of a convex polygon where every vertex has ≥4 equidistant neighbors; target score 1.0.

## Strategy hints

- A regular polygon has every vertex equidistant from all others — try a regular 10-gon as baseline.
- For a regular n-gon with n vertices, each vertex has exactly 2 equidistant neighbors at each distance level.
- Perturb the regular polygon to try to equalize more distance levels.
- The polygon must be convex — maintain convexity throughout optimization.
- Parameterize as r(θ) deviations from a circle.

## Output format

Return a `np.ndarray` of shape `(10, 2)` representing 2D convex polygon vertices (in order, either CW or CCW).

```python
import numpy as np

def solve(num_vertex: int = 10) -> np.ndarray:
    # Regular polygon as a starting point
    angles = np.linspace(0, 2*np.pi, num_vertex, endpoint=False)
    return np.column_stack([np.cos(angles), np.sin(angles)])
```

## Pitfalls

- Non-convex vertex orderings are invalid; ensure vertices are in convex position.
- Degenerate configurations (3+ collinear vertices) may be rejected.
- The equidistance check has numerical tolerance — avoid nearly-equal but not-equal distances.

## Baseline

A regular 10-gon gives each vertex 2 equidistant neighbors at each chord length; score will be low. Careful perturbation can improve this.
