# Agent Guide — Erdős-Szekeres Happy Ending

## Goal

Return a numpy array of shape `(17, 2)` representing 17 points in the plane (no 3 collinear) that minimize the number of convex 6-gons; score = −count, so maximize toward 0.

## Strategy hints

- Start from a convex configuration (all 17 points on a circle) — this maximizes convex 6-gons and is the worst case for score.
- Move points inward to "break" convex subsets; one point strictly inside the convex hull of the others eliminates many convex 6-gons.
- Use small perturbations around configurations with known few convex polygons.
- Avoid collinear triples — add small random noise to prevent this.
- The score is piecewise constant (integer-valued); gradient-free optimization is essential.

## Output format

Return a `np.ndarray` of shape `(17, 2)` representing 2D coordinates.

```python
import numpy as np

def solve(n: int = 6) -> np.ndarray:
    # 17 points: 16 on a circle + 1 at center
    num_points = 2**(n-2) + 1  # = 17
    angles = np.linspace(0, 2*np.pi, num_points-1, endpoint=False)
    pts = np.column_stack([np.cos(angles), np.sin(angles)])
    center = np.array([[0.0, 0.0]])
    return np.vstack([pts, center])
```

## Pitfalls

- Collinear triples make the configuration invalid; add small perturbations.
- Returning fewer than 17 points will cause an evaluation error.
- Coordinates outside a reasonable range (e.g., |x|, |y| > 1000) may cause numerical issues.

## Baseline

All 17 points on a circle maximizes convex hexagons (score very negative). Adding 1 interior point reduces the count significantly.
