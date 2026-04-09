# Agent Guide — Kissing Number 7D

## Goal

Return a numpy array of shape `(k, 7)` with k ≥ 126 valid kissing vectors in R⁷; target k = 126 (E₇ lattice), potentially improve toward 134 (upper bound).

## Strategy hints

- E₇ root system has 126 minimal vectors of length √2.
- E₇ can be constructed as: {x ∈ Z⁷ : Σxᵢ ≡ 0 mod 2, Σxᵢ² = 2} ∪ {x + (1/2)·1 : ...}.
- Starting from E₇ vectors and running angular optimization can occasionally find 127.
- Represent vectors as points on S⁶ and use energy minimization.
- Look up the Gram matrix of E₇ to construct the lattice.

## Output format

Return a `np.ndarray` of shape `(k, 7)`.

```python
import numpy as np

def solve(dimension: int = 7) -> np.ndarray:
    # E7 lattice: 126 minimal vectors
    # Generate ±e_i ± e_j combinations (42 vectors) and other roots
    verts = []
    for i in range(7):
        for j in range(i+1, 7):
            for si in [1, -1]:
                for sj in [1, -1]:
                    v = [0]*7
                    v[i] = si; v[j] = sj
                    verts.append(v)
    # This gives 84 vectors; add E7-specific vectors to reach 126
    # Full E7 construction requires the 8-dimensional E8 lattice
    return np.array(verts, dtype=float)
```

## Pitfalls

- The E₇ root system is not just ±eᵢ±eⱼ; look up the full construction.
- Approximate configurations may fail the strict pairwise distance check.
- Normalizing to unit vectors before returning is recommended.

## Baseline

±eᵢ±eⱼ gives 84 vectors but not all are E₇ kissing vectors. The full E₇ system gives 126.
