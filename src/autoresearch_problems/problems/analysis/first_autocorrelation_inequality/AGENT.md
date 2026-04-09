# Agent Guide — First Autocorrelation Inequality

## Goal

Return a list of 600 non-negative floats representing f on [−¼, ¼] that minimizes C₁ = max(f*f)(t)/(∫f)²; target C₁ < 1.5053.

## Strategy hints

- The function should be symmetric around 0 for best results (f(−t) = f(t)).
- Unimodal functions (single peak at 0) often outperform multimodal ones.
- Try optimizing a small number of Fourier cosine coefficients (≤ 20) rather than all 600 values.
- The score is scale-invariant (divides by (∫f)²), so absolute magnitudes don't matter — only shape.
- Gradient descent on the 600 values using numerical finite differences works but is slow; parameterize with fewer degrees of freedom first.

## Output format

Return a Python `list` of 600 non-negative floats.

```python
import numpy as np

def solve(num_intervals: int = 600) -> list:
    x = np.linspace(-0.25, 0.25, num_intervals)
    f = np.maximum(0, 1 - np.abs(x) / 0.25)  # triangular
    return f.tolist()
```

## Pitfalls

- Negative values in the list will be clipped or cause `valid=False`.
- Returning all zeros gives undefined C₁ (division by zero).
- Very peaked or spiky functions inflate the max convolution value.

## Baseline

Uniform f = 1 gives C₁ ≈ 1.5. Triangular function gives C₁ ≈ 1.53. Gaussian-shaped gives C₁ ≈ 1.51.
