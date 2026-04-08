# Agent Guide — Kissing Number 9D

## Goal

Return a numpy array of shape `(k, 9)` with k ≥ 306 valid kissing vectors in R⁹; target k = 306 (known lower bound), potentially improve.

## Strategy hints

- The D₉ and Λ₉ lattice constructions achieve 306.
- D₉ has 144 minimal vectors (all ±eᵢ±eⱼ); augmented lattice constructions reach 306.
- Use the Leech lattice cross-sections or known 9D sphere packing constructions as starting points.
- Energy minimization (Thomson problem on S⁸) converges near kissing configurations.
- From 306 vectors, gradient search for a 307th is computationally expensive but worth attempting.

## Output format

Return a `np.ndarray` of shape `(k, 9)`.

```python
import numpy as np

def solve(dimension: int = 9) -> np.ndarray:
    # D9 lattice as starting point (144 minimal vectors)
    verts = []
    for i in range(9):
        for j in range(i+1, 9):
            for si in [1, -1]:
                for sj in [1, -1]:
                    v = [0]*9
                    v[i] = si; v[j] = sj
                    verts.append(v)
    return np.array(verts, dtype=float)
```

## Pitfalls

- D₉ only gives 144 vectors; additional lattice vectors are needed to reach 306.
- The evaluator may have a specific format requirement for the array.
- Finding 307+ vectors requires sophisticated lattice theory.

## Baseline

D₉ lattice: 144 vectors. Full 9D construction: 306. Empty set: 0.
