# Agent Guide — Sphere Packing Uncertainty Principle

## Goal

Return a numpy array of m=10 positive real values (root positions z₁, ..., z_m) that maximize the largest sign change of the Laguerre combination g(x) with double zeros at those positions.

## Strategy hints

- The roots should be spread out over a reasonable range (roughly [0.1, 50] for n_dim=25).
- Start with roughly equally spaced roots on a logarithmic scale.
- The roots z_i must be distinct and positive; the evaluator may reject degenerate configurations.
- Local optimization of root positions (e.g., scipy.optimize.minimize) starting from a good initial arrangement works well.
- Aim for roots that balance the oscillation of g between zeros.

## Output format

Return a 1D `np.ndarray` of shape `(10,)` with strictly positive values.

```python
import numpy as np

def solve(m: int = 10, n_dim: int = 25) -> np.ndarray:
    # Spread roots logarithmically between 0.5 and 40
    return np.logspace(np.log10(0.5), np.log10(40), m)
```

## Pitfalls

- Non-positive or zero roots are invalid (Laguerre polynomials require positive argument).
- Roots that are too close together cause near-degenerate double zeros.
- Roots larger than ~100 may be outside the meaningful support of the Laguerre functions.

## Baseline

Equally spaced roots on [1, 20] give a moderate sign change. Logarithmically spaced roots usually improve on this.
