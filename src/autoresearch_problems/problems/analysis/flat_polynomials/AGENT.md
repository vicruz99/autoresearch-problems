# Agent Guide — Flat Polynomials

## Goal

Return an array of 64 values in {−1, +1} for polynomial coefficients that minimizes max|g(z)|/√(n+1) on the unit circle; target < 1.384.

## Strategy hints

- The output is binarized: any positive value becomes +1, any non-positive becomes −1. So you can return a continuous array and let the evaluator snap it.
- Exhaustive search is infeasible (2^64 combinations); use local search starting from known good sequences (Rudin-Shapiro, Golay pairs, etc.).
- Simulated annealing with random single-bit flips converges well; start hot and cool slowly.
- Evaluate polynomials using FFT (np.fft) for speed — evaluate at 2^k points simultaneously.
- The score is invariant to overall sign flip and to the reversal c_i → c_{n+1−i}.

## Output format

Return a 1D `np.ndarray` of shape `(64,)`. Values are snapped to ±1 by the evaluator, so floats are fine.

```python
import numpy as np

def solve(n: int = 64) -> np.ndarray:
    # Rudin-Shapiro sequence as a baseline
    c = np.ones(n)
    for i in range(n):
        count = bin(i & (i >> 1)).count('1')
        c[i] = 1.0 if count % 2 == 0 else -1.0
    return c
```

## Pitfalls

- Returning a constant array (+1 or −1 throughout) gives the worst possible score (the DFT of a constant is a spike).
- The score function is non-convex with many local minima — do not rely on gradient descent alone.
- Using a grid too coarse to evaluate the polynomial will miss the true maximum.

## Baseline

Rudin-Shapiro sequence achieves score ≈ √2 ≈ 1.414. Random ±1 sequences typically score 1.5–2.0.
