# Agent Guide — Kissing Number 10D

## Goal

Return a numpy array of shape `(k, 10)` with k ≥ 500 valid kissing vectors in R¹⁰; target k = 500 (AlphaEvolve result), potentially improve toward 554 (upper bound).

## Strategy hints

- This was a major AlphaEvolve result — improving from 336 to 500 is a significant jump.
- The construction likely involves lattice constructions from 10D sphere packings.
- P₁₀ and related lattices provide good starting points.
- Combine multiple lattice shells: take vectors of lengths r₁ and r₂ from a lattice.
- Run energy minimization on 500 unit vectors on S⁹ to verify and refine.
- To attempt 501+, start from the 500-vector configuration and run angular optimization.

## Output format

Return a `np.ndarray` of shape `(k, 10)`.

```python
import numpy as np

def solve(dimension: int = 10) -> np.ndarray:
    # D10 lattice as a starting point (180 minimal vectors)
    verts = []
    for i in range(10):
        for j in range(i+1, 10):
            for si in [1, -1]:
                for sj in [1, -1]:
                    v = [0]*10
                    v[i] = si; v[j] = sj
                    verts.append(v)
    return np.array(verts, dtype=float)
```

## Pitfalls

- D₁₀ gives only 180 vectors; reaching 500 requires more sophisticated constructions.
- The timeout (120s) limits optimization iterations significantly.
- Pairwise distance checking for 500+ vectors is O(k²) — use matrix operations.

## Baseline

D₁₀: 180 vectors. Previous best: 336. AlphaEvolve found 500.
