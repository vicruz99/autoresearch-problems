# Agent Guide — Kissing Number 5D

## Goal

Return a numpy array of shape `(k, 5)` with k vectors in R⁵ (all at equal distance from origin, all pairwise separated by angle ≥ 60°); maximize k; target k ≥ 40.

## Strategy hints

- Known constructions achieving 40: take the 40 shortest vectors of the D₅ lattice.
- D₅ lattice vectors: all permutations of (±1, ±1, 0, 0, 0) give 40 vectors of length √2.
- Check that min pairwise distance ≥ length of vectors (angle ≥ 60°).
- To potentially beat 40, use gradient-based optimization on 41 or more unit vectors.
- Represent as unit vectors on S⁴ and minimize the Riesz s-energy for s → ∞.

## Output format

Return a `np.ndarray` of shape `(k, 5)` with k rows of 5D vectors.

```python
import numpy as np
from itertools import combinations

def solve(dimension: int = 5) -> np.ndarray:
    # D5 lattice: all (±1, ±1, 0, 0, 0) permutations — 40 vectors
    verts = []
    for i in range(5):
        for j in range(i+1, 5):
            for si in [1, -1]:
                for sj in [1, -1]:
                    v = [0]*5
                    v[i] = si; v[j] = sj
                    verts.append(v)
    return np.array(verts, dtype=float)
```

## Pitfalls

- The D₅ lattice vectors are length √2 — ensure the evaluator normalizes or uses consistent length.
- Pairwise dot product > 0.5 (after normalization) violates the kissing condition.
- Trying to fit 45+ vectors rarely succeeds within timeout.

## Baseline

D₅ lattice gives 40 kissing vectors. The empty set gives 0.
