# Agent Guide — Young's Convolution Inequality

## Goal

Return a numpy array of shape `(1000,)` where the first 500 elements are f and the last 500 are g on [−10, 10], maximizing Q(f,g) = ‖f*g‖_{L^r} / (‖f‖_{L^p}·‖g‖_{L^q}) with p=4/3, q=7/5.

## Strategy hints

- Both optimal functions are Gaussians: f(x) = g(x) = exp(−αx²) for some α.
- Start with f = g = exp(−πx²) and tune the width parameter.
- The quotient is scale-invariant in each function independently.
- Try asymmetric choices: f and g with different widths.
- The convolution of two Gaussians is another Gaussian — use this analytically to find the optimal α.

## Output format

Return a 1D `np.ndarray` of shape `(1000,)` where output[:500] = f values and output[500:] = g values on [−10, 10].

```python
import numpy as np

def solve(p: float = 4/3, q: float = 1.4, r1: float = 10.0, j: int = 500) -> np.ndarray:
    x = np.linspace(-r1, r1, j)
    f = np.exp(-np.pi * x**2)
    g = np.exp(-np.pi * x**2)
    return np.concatenate([f, g])
```

## Pitfalls

- Returning only j elements instead of 2j will cause an indexing error.
- Functions that don't decay to zero at ±r1 will have truncation artifacts in the convolution.
- Negative values in f or g may be valid mathematically but check the evaluator's assumptions.

## Baseline

Two identical Gaussians exp(−πx²) achieve near-optimal Q. A pair of box functions scores significantly lower.
