# Agent Guide — Hausdorff-Young Inequality

## Goal

Return a 500-element array representing f on [−5, 5] that maximizes Q(f) = ‖f̂‖_{L^3} / ‖f‖_{L^{1.5}}; the theoretical maximum is the Babenko-Beckner constant ≈ 0.9532.

## Strategy hints

- The optimal function is a Gaussian: f(x) = exp(−αx²) for any α > 0.
- The quotient is scale-invariant in the function value but width matters — tune the Gaussian width.
- Try f(x) = exp(−π x²) as the canonical choice.
- Any even, bell-shaped function with no oscillations will score near optimal.
- Verify that the Fourier transform is well-captured by the grid (function should decay to near zero at x = ±5).

## Output format

Return a 1D `np.ndarray` of shape `(500,)` representing f values on [−5, 5].

```python
import numpy as np

def solve(p: float = 1.5, r1: float = 5.0, j: int = 500, r2: float = 10.0) -> np.ndarray:
    x = np.linspace(-r1, r1, j)
    return np.exp(-np.pi * x**2)  # Gaussian — the optimal function
```

## Pitfalls

- Functions that don't decay to zero at ±r1 will have truncation error in the Fourier transform.
- Non-positive functions or functions with negative values may not be valid inputs.
- Very sharp functions (small σ) may be undersampled on the 500-point grid.

## Baseline

Gaussian exp(−πx²) achieves the theoretical maximum ≈ 0.9532. A triangular pulse scores ≈ 0.90.
