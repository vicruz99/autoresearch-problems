# Agent Guide — Thomson Problem n=32

## Goal

Return a numpy array of shape `(32, 3)` representing 32 points on the unit sphere that minimize Thomson energy E = Σ 1/rᵢⱼ; maximize score = −E.

## Strategy hints

- Start from published Thomson configurations for n=32 (available in Sloane's database).
- Use gradient descent: ∂E/∂xᵢ = −Σⱼ (xᵢ − xⱼ) / |xᵢ − xⱼ|³ (project onto sphere).
- The Riesz s-energy for large s converges to the Tammes problem — start with s=1 (Thomson).
- scipy.optimize.minimize with L-BFGS-B on the spherical coordinates is efficient.
- Multiple random restarts are needed; use best of 10 restarts.

## Output format

Return a `np.ndarray` of shape `(32, 3)` — values will be normalized to unit sphere.

```python
import numpy as np
from scipy.spatial.distance import pdist

def solve(n: int = 32) -> np.ndarray:
    rng = np.random.default_rng(42)
    # Random initialization on sphere
    pts = rng.standard_normal((n, 3))
    pts /= np.linalg.norm(pts, axis=1, keepdims=True)
    return pts
```

## Pitfalls

- Points coinciding (rᵢⱼ = 0) cause infinite energy; ensure all points are distinct.
- The energy gradient diverges near degenerate configurations.
- Local minima are abundant; always try multiple initializations.

## Baseline

Random unit sphere points typically give E ≈ −200 to −210 for n=32. Best known: E ≈ −214.7.
