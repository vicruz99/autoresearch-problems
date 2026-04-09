# Agent Guide — Tammes n=24

## Goal

Return a numpy array of shape `(24, 3)` representing 24 points on the unit sphere maximizing min pairwise distance; target > 0.57.

## Strategy hints

- The snub cube (24 vertices of a snub cube projected onto a sphere) is a natural starting point.
- Thomson energy minimization converges to near-Tammes configurations.
- Use scipy.optimize.minimize with the (negative) soft minimum of pairwise distances.
- Initialize from the known 24-point spherical t-design (same problem as spherical_t_design_n24_t7).
- Perturb the snub cube vertices and optimize.

## Output format

Return a `np.ndarray` of shape `(24, 3)`.

```python
import numpy as np

def solve(n: int = 24) -> np.ndarray:
    # Random initialization on sphere
    rng = np.random.default_rng(0)
    pts = rng.standard_normal((n, 3))
    pts /= np.linalg.norm(pts, axis=1, keepdims=True)
    return pts
```

## Pitfalls

- Random initialization typically gives min distance ≈ 0.3–0.4; optimization is essential.
- The problem has many symmetrically equivalent optimal solutions.
- Use pdist from scipy for O(n²) pairwise distances efficiently.

## Baseline

Random unit sphere points: min distance ≈ 0.35. Snub cube: ≈ 0.57. Best known: ≈ 0.5765.
