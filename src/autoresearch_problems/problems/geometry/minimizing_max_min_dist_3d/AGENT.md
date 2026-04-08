# Agent Guide — Minimizing Max-Min Distance 3D

## Goal

Return a numpy array of shape `(14, 3)` representing 14 points in 3D that maximize (dmin/dmax)²; target score ≥ 1.0.

## Strategy hints

- 14 points in 3D: try face-centered cubic (FCC) or body-centered cubic (BCC) lattice arrangements.
- The optimal packing of 14 points in 3D is not the same as sphere packing — there's no bounding container.
- Use BFGS on the ratio objective: minimize −(dmin/dmax)².
- Computing (dmin/dmax)² is differentiable everywhere except at ties; use sub-gradient methods.
- Initialize with 14 random unit-sphere points and run gradient descent.

## Output format

Return a `np.ndarray` of shape `(14, 3)`.

```python
import numpy as np

def solve(n: int = 14, d: int = 3) -> np.ndarray:
    # FCC lattice as starting point
    pts = []
    for x in range(3):
        for y in range(3):
            for z in range(3):
                pts.append([x, y, z])
                if len(pts) == n:
                    break
    return np.array(pts[:n], dtype=float)
```

## Pitfalls

- Degenerate configurations (all in a plane or on a line) give low scores.
- The ratio is scale-invariant; only the shape of the configuration matters.
- Use cdist from scipy for efficient pairwise distances.

## Baseline

A 3×3×2 rectangular grid (with some adjustments) gives moderate ratios. The benchmark was found by ShinkaEvolve/AlphaEvolve optimization.
