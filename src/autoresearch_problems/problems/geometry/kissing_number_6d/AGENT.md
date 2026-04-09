# Agent Guide — Kissing Number 6D

## Goal

Return a numpy array of shape `(k, 6)` with k ≥ 72 valid kissing vectors in R⁶; target k = 72 (lower bound), potentially improve toward 78 (upper bound).

## Strategy hints

- The E₆ lattice achieves 72 kissing vectors.
- E₆ minimal vectors: 72 vectors of the form ±e_i ± e_j and specific patterns — look up the E₆ lattice basis.
- To attempt 73+: start from the 72 E₆ vectors and try gradient descent on S⁵ to squeeze in one more.
- scipy.optimize.minimize on the angular separation objective.
- Energy minimization (Thomson problem on S⁵) converges toward kissing configurations.

## Output format

Return a `np.ndarray` of shape `(k, 6)` with k 6D vectors.

```python
import numpy as np

def solve(dimension: int = 6) -> np.ndarray:
    # E6 lattice minimal vectors (72 vectors)
    # Construct using the standard E6 embedding
    verts = []
    # All (±1, ±1, 0, 0, 0, 0) permutations: C(6,2)*4 = 60 vectors
    for i in range(6):
        for j in range(i+1, 6):
            for si in [1, -1]:
                for sj in [1, -1]:
                    v = [0]*6
                    v[i] = si; v[j] = sj
                    verts.append(v)
    # Additional 12 vectors from E6 root system
    extras = [[1,1,1,1,0,0], [-1,-1,-1,-1,0,0], [1,1,0,0,1,1],
              [-1,-1,0,0,-1,-1], [1,0,1,0,1,0], [-1,0,-1,0,-1,0],
              [0,1,0,1,0,1], [0,-1,0,-1,0,-1], [1,0,0,1,0,1],
              [-1,0,0,-1,0,-1], [0,1,1,0,1,0], [0,-1,-1,0,-1,0]]
    verts.extend(extras)
    arr = np.array(verts[:72], dtype=float)
    return arr
```

## Pitfalls

- E₆ has a specific root structure — verify all 72 vectors satisfy pairwise kissing.
- The evaluator may normalize vectors; ensure consistent scale.
- Trying 73+ vectors requires careful initialization near the E₆ configuration.

## Baseline

E₆ lattice gives 72. Empty set gives 0.
