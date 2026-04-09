# Agent Guide — Tammes n=14

## Goal

Return a numpy array of shape `(14, 3)` representing 14 points on the unit sphere that maximize the minimum pairwise distance; target > 0.81.

## Strategy hints

- Start from the 14-point Tammes configuration: points at vertices of a rhombic dodecahedron-like arrangement.
- Or start from 14 random unit vectors and apply Thomson energy minimization.
- Thomson energy (minimize Σ 1/rᵢⱼ) concentrates on near-Tammes configurations.
- Gradient descent with the soft minimum (log-sum-exp approximation) works well.
- Known configurations: cuboctahedron (12) + 2 poles ≈ a good starting point for 14.

## Output format

Return a `np.ndarray` of shape `(14, 3)` — values will be normalized to unit sphere.

```python
import numpy as np

def solve(n: int = 14) -> np.ndarray:
    # Cuboctahedron (12 vertices) + 2 poles as a starting point
    pts = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                if abs(i) + abs(j) + abs(k) == 2:
                    pts.append([i, j, k])
    pts.extend([[0, 0, 1], [0, 0, -1]])
    arr = np.array(pts[:n], dtype=float)
    arr /= np.linalg.norm(arr, axis=1, keepdims=True)
    return arr
```

## Pitfalls

- Points must be on the unit sphere — use normalization.
- Local minima are abundant; run multiple random initializations.
- The minimum distance is non-differentiable at ties — use softmin for gradient methods.

## Baseline

Cuboctahedron + 2 poles gives min distance ≈ 0.78. Best known Tammes-14 configuration ≈ 0.816.
