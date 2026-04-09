# Agent Guide — Third Autocorrelation Inequality

## Goal

Return a list of floats (possibly negative) representing f on [−¼, ¼] that minimizes C₃ = 2n·max|f*f|/(Σ|f|)²; target C₃ < 1.4556.

## Strategy hints

- Unlike C₁ and C₂, f can take negative values — exploit this degree of freedom.
- Anti-symmetric functions (f(−t) = −f(t)) can give flatter convolutions.
- Alternating-sign patterns in the step function tend to reduce max|f*f|.
- The score is scale-invariant (Σ|f| in denominator), so only shape matters.
- Try combining a symmetric positive part with an anti-symmetric correction.

## Output format

Return a Python `list` of floats (may be negative).

```python
import numpy as np

def solve() -> list:
    n = 600
    x = np.linspace(-0.25, 0.25, n)
    # Alternating sign function as a starting point
    f = np.sign(np.sin(20 * np.pi * x))
    return f.tolist()
```

## Pitfalls

- All-positive functions perform worse than mixed-sign functions for C₃.
- Very spiky functions (few non-zero elements) inflate max|f*f| relative to (Σ|f|)².
- Lists of length < 100 may not have sufficient resolution.

## Baseline

All-ones function (triangular convolution) gives C₃ ≈ 2.0. Simple alternating signs can reach C₃ ≈ 1.6.
