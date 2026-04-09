# Agent Guide — Kissing Number 3D

## Goal

Return a numpy array of shape `(12, 3)` with 12 vectors in R³ representing kissing sphere centers; achieve the known optimum score of 12.

## Strategy hints

- The 12 kissing spheres in 3D form an icosahedral arrangement.
- Place 12 unit vectors at the vertices of a regular icosahedron.
- The golden ratio φ = (1+√5)/2 appears: vertices at (0, ±1, ±φ) and permutations.
- All pairwise angles should be ≥ 60°.
- This problem is solved — just implement the icosahedral construction.

## Output format

Return a `np.ndarray` of shape `(12, 3)`.

```python
import numpy as np

def solve(dimension: int = 3) -> np.ndarray:
    phi = (1 + 5**0.5) / 2
    # Vertices of regular icosahedron
    verts = np.array([
        [0,  1,  phi], [0, -1,  phi], [0,  1, -phi], [0, -1, -phi],
        [1,  phi, 0], [-1,  phi, 0], [1, -phi, 0], [-1, -phi, 0],
        [phi, 0,  1], [-phi, 0,  1], [phi, 0, -1], [-phi, 0, -1],
    ])
    return verts / np.linalg.norm(verts[0])
```

## Pitfalls

- Vectors must be on the unit sphere (or the evaluator normalizes them).
- Any pair with angular distance < 60° (dot product > 0.5) violates the kissing condition.
- Returning fewer than 12 vectors loses score unnecessarily.

## Baseline

The regular icosahedron gives exactly 12 kissing vectors, achieving the known optimum.
