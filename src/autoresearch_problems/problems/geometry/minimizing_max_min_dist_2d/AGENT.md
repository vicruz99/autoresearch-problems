# Agent Guide — Minimizing Max-Min Distance 2D

## Goal

Return a numpy array of shape `(16, 2)` representing 16 points in 2D that maximize (dmin/dmax)²; target score ≥ 1.0 (match or beat benchmark).

## Strategy hints

- Points should be as uniformly distributed as possible — think of spreading 16 points on a 2D grid.
- The optimal arrangement is likely related to a hexagonal or triangular lattice.
- Use scipy.optimize.minimize to directly maximize the ratio.
- Lloyd's relaxation (Voronoi centroid iteration) converges to uniform distributions.
- Try starting from a hexagonal arrangement of 16 points (4×4 hex grid).

## Output format

Return a `np.ndarray` of shape `(16, 2)` — no bounding box constraint mentioned, so points can be anywhere in the plane.

```python
import numpy as np

def solve(n: int = 16, d: int = 2) -> np.ndarray:
    # Hexagonal grid as a starting point
    pts = []
    for r in range(4):
        for c in range(4):
            x = c + (0.5 if r % 2 else 0)
            y = r * np.sqrt(3)/2
            pts.append([x, y])
    return np.array(pts[:n])
```

## Pitfalls

- Points that are collinear or all identical will give dmin = 0 (score = 0).
- The ratio dmin/dmax is scale-invariant — absolute coordinates don't matter.
- Adding jitter to regular grids can improve the ratio slightly.

## Baseline

A 4×4 square grid has dmin=1 and dmax=3√2≈4.24, giving ratio ≈ 0.236. Hexagonal grids do better.
