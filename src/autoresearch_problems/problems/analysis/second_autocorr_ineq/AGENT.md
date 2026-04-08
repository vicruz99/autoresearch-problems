# Agent Guide — Second Autocorrelation Inequality

## Goal

Return a list of non-negative floats representing a step function f that maximizes C₂ = ‖f*f‖₂² / (‖f*f‖₁ · ‖f*f‖∞); target C₂ > 0.8963.

## Strategy hints

- A perfectly flat autocorrelation A = f*f gives C₂ = 1 (theoretical max); aim for flat A.
- Functions related to Golay complementary pairs or Barker codes tend to have flat autocorrelations.
- Try step functions with values in {0, 1} or {0, 1, 2}; the score is scale-invariant.
- Optimizing the Fourier magnitude |F(ω)|² (which equals the power spectrum of f) is equivalent to optimizing A = f*f.
- A list of length 100–1000 gives good results.

## Output format

Return a Python `list` of non-negative floats.

```python
import numpy as np

def solve() -> list:
    n = 256
    f = np.random.choice([0, 1], size=n).astype(float)
    return f.tolist()
```

## Pitfalls

- Negative values are invalid for a step function; ensure all values are ≥ 0.
- A constant function gives a triangular autocorrelation (not flat), scoring around 0.75.
- Very short lists (< 50 elements) may not converge to near-optimal.

## Baseline

Random binary sequences score C₂ ≈ 0.82–0.87. The constant function scores ≈ 0.75. AlphaEvolve's construction scores ≈ 0.8963.
