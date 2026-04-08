# Agent Guide — Kissing Number 11D

## Goal

Return a numpy array of shape `(k, 11)` with k ≥ 593 valid kissing vectors in R¹¹; target k = 593 (current best), potentially improve to 594+.

## Strategy hints

- This requires reproducing or improving AlphaEvolve's construction.
- Start with 592 known vectors from lattice constructions (D₁₁ + extra shells).
- AlphaEvolve likely used evolutionary search over lattice codes to find the 593rd vector.
- Parameterize as angles in S¹⁰ and use simulated annealing.
- Pairwise dot products of unit vectors must be ≤ 0.5 for all pairs.
- Use scipy.optimize.minimize with penalty for dot products > 0.5.

## Output format

Return a `np.ndarray` of shape `(k, 11)` with k 11D unit vectors.

```python
import numpy as np

def solve(dimension: int = 11) -> np.ndarray:
    # D11 lattice as a starting point
    verts = []
    for i in range(11):
        for j in range(i+1, 11):
            for si in [1, -1]:
                for sj in [1, -1]:
                    v = [0]*11
                    v[i] = si; v[j] = sj
                    verts.append(v)
    return np.array(verts, dtype=float)
```

## Pitfalls

- D₁₁ gives 220 vectors; reaching 593 requires extensive optimization.
- The 120s timeout is tight for this high-dimensional problem.
- Use `scipy.spatial.distance.pdist` for fast pairwise distance computation.

## Baseline

D₁₁: 220 vectors. Previous best: 592. AlphaEvolve: 593.
