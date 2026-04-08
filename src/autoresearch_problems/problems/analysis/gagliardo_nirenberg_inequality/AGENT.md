# Agent Guide — Gagliardo-Nirenberg Inequality

## Goal

Return a 500-element array representing f on [−15, 15] that maximizes Q(f) = ‖f‖_4^{16} / (‖f‖_2^{12} · ‖f'‖_2^4); the theoretical maximum is 1/9 ≈ 0.1111.

## Strategy hints

- The optimal function is sech(x) = 1/cosh(x) — sample it on the grid as a perfect baseline.
- The quotient is scale-invariant, so only the shape matters.
- Translating the peak or adding small perturbations to sech barely changes the score.
- Try parameterized families: sech^α(βx) for varying α and β.
- Any even function (f(x) = f(−x)) with a single peak at 0 will score close to optimal.

## Output format

Return a 1D `np.ndarray` of shape `(500,)` representing f values on [−15, 15].

```python
import numpy as np

def solve(p: float = 4.0, r1: float = 15.0, j: int = 500) -> np.ndarray:
    x = np.linspace(-r1, r1, j)
    return 1.0 / np.cosh(x)  # sech(x) — the optimal function
```

## Pitfalls

- If f is identically zero, the evaluator will divide by zero (invalid).
- Very broad functions (support much larger than [−5, 5]) lose mass outside the grid, distorting the norms.
- The derivative ‖f'‖_2 is computed numerically — discontinuous or spiky functions will inflate it.

## Baseline

sech(x) achieves the theoretical maximum Q ≈ 0.1111. A Gaussian achieves Q ≈ 0.108.
