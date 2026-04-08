# Agent Guide — Edges vs. Triangles

## Goal

Return a numpy array of shape `(20, 20)` (20 probability vectors of length 20) that traces the theoretical (edge_density, triangle_density) boundary; target score 1.0.

## Strategy hints

- Each row is a probability vector (non-negative, sums to 1); use softmax to parameterize.
- Space the 20 vectors to cover a range of edge densities evenly (0 to 1).
- The Kruskal-Katona boundary at edge density p is triangle density ≥ p^(3/2) — aim to trace exactly this curve.
- Sort vectors by implied edge density to minimize max_gap.
- The Turán graph and its fractional relaxations provide good initial points.

## Output format

Return a `np.ndarray` of shape `(20, 20)` where each row is a probability vector (non-negative, sums to 1).

```python
import numpy as np

def solve(n: int = 20) -> np.ndarray:
    # Uniform probability vectors equally spaced
    result = np.zeros((n, n))
    for i in range(n):
        result[i, i] = 1.0  # one-hot vectors as a baseline
    return result
```

## Pitfalls

- Rows that don't sum to 1 or have negative entries may be invalid.
- All identical vectors give max_gap ≈ 1, which dominates the score.
- Not sorting by edge density produces large gaps in the coverage curve.

## Baseline

One-hot probability vectors (identity matrix) score poorly due to large gaps. Evenly spaced interpolations score around 0.4–0.6.
