# Agent Guide — Erdős Minimum Overlap

## Goal

Find a step function h: [0,2] → [0,1] with ∫h = 1 that minimizes C₅ = max_k ∫h(x)(1 − h(x+k)) dx; target C₅ < 0.3809.

## Strategy hints

- Return a 1D numpy array of length ~1000 representing h on a uniform grid over [0, 2]; the evaluator normalizes it.
- Smooth, symmetric functions around x=1 tend to perform well.
- Start from a piecewise-constant approximation to the known near-optimal: h peaks near x=0.5 and x=1.5.
- Gradient-free optimization (e.g., COBYLA, Nelder-Mead) on the array coefficients works well given the convolution scoring.
- Exploit the symmetry h(x) = h(2−x) to reduce the search space by half.

## Output format

Return a 1D `np.ndarray` of non-negative floats of any length; the evaluator clips to [0,1] and normalizes the integral. A length of 500–2000 gives good resolution.

```python
import numpy as np

def solve() -> np.ndarray:
    n = 1000
    x = np.linspace(0, 2, n)
    h = np.exp(-10 * (x - 0.5)**2) + np.exp(-10 * (x - 1.5)**2)
    return h
```

## Pitfalls

- Returning all-zeros or a constant will give a near-worst-case score after normalization.
- Very short arrays (< 100 elements) may have insufficient resolution to approach the optimal.
- Do not return negative values — they get clipped to 0, distorting the integral.

## Baseline

The uniform function h(x) = 0.5 (constant) gives C₅ ≈ 0.25 but violates ∫h = 1 for the [0,2] domain. A simple triangular function centered at x=1 achieves C₅ ≈ 0.39.
