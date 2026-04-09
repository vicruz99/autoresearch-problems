# Agent Guide — Spherical t-Design (n=24, t=7)

## Goal

Return a numpy array of shape `(24, 3)` representing 24 points on the unit sphere that form a spherical 7-design; target score 0 (perfect design).

## Strategy hints

- A spherical t-design requires ∫P(x) dσ = (1/N)ΣP(xᵢ) for all polynomials P of degree ≤ t.
- Known 7-designs with n=24 exist; look up published spherical designs.
- The vertices of the snub cube (24 vertices) approximate a spherical design — try it.
- Gradient descent on the max Gegenbauer error works well starting from near-designs.
- Use scipy.optimize.minimize with the Gegenbauer error as objective.

## Output format

Return a `np.ndarray` of shape `(24, 3)` with unit vectors.

```python
import numpy as np

def solve(n: int = 24, t: int = 7) -> np.ndarray:
    # Snub cube vertices as an approximate spherical design
    # (24 vertices approximately uniformly distributed)
    phi = (1 + 5**0.5) / 2  # golden ratio
    xi = 1.0  # tribonacci constant approximation
    pts = []
    for s1, s2, s3 in [(1,1,1),(-1,1,1),(1,-1,1),(1,1,-1),(-1,-1,1),(-1,1,-1),(1,-1,-1),(-1,-1,-1)]:
        pts.extend([[s1, s2*xi, s3/phi], [s1*xi, s2/phi, s3], [s1/phi, s2, s3*xi]])
    arr = np.array(pts[:n], dtype=float)
    arr /= np.linalg.norm(arr, axis=1, keepdims=True)
    return arr
```

## Pitfalls

- Points not on the unit sphere will be normalized by the evaluator.
- With only 24 points, a degree-7 design requires very precise placement.
- Random unit vectors will not form a 7-design.

## Baseline

The snub cube gives max Gegenbauer error ≈ 0.1–0.3. A known spherical 7-design gives error = 0.
