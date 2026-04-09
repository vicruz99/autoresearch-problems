# Agent Guide — No 5 on Sphere

## Goal

Return a numpy array of shape `(k, 3)` with k unit vectors in R³ such that no 5 are coplanar with the origin; maximize k ≤ 50.

## Strategy hints

- 5 points are coplanar with the origin iff they lie on a common 2D plane through 0, i.e., they all lie on a great circle (plane through origin).
- A great circle is defined by a unit normal n; all points on it satisfy p·n = 0.
- Check: for any 3 non-collinear sphere points, they define a unique great circle; ensure no 2 others lie on it.
- Random points on a sphere are unlikely to be 5-coplanar; start random and greedily remove violating points.
- Perturb any configuration slightly to break near-coplanar quintuples.

## Output format

Return a `np.ndarray` of shape `(k, 3)` with k rows of 3D unit vectors (or vectors that will be normalized).

```python
import numpy as np

def solve(n: int = 50) -> np.ndarray:
    rng = np.random.default_rng(42)
    pts = rng.standard_normal((n, 3))
    pts /= np.linalg.norm(pts, axis=1, keepdims=True)
    return pts
```

## Pitfalls

- Antipodal pairs (p and −p) lie on every great circle — avoid or handle carefully.
- The coplanarity check is floating-point sensitive; add small perturbations to avoid near-ties.
- Starting with polar-coordinate distributions (equal latitude spacing) creates many coplanar quintuples.

## Baseline

50 random points on the sphere: most sets of 5 will not be coplanar; expect score close to 50 for truly random configurations.
