# Agent Guide — Finite Field Kakeya (Parent, d=3)

## Goal

Return a dict `{p: array}` for each prime p in `[3,5,7,11]` where each array has shape `(k, 3)` with entries in `{0,...,p-1}`, representing a Kakeya set in F_p^3; maximize the average −|K(p)|/reference over primes.

## Strategy hints

- A Kakeya set must contain a full line in every direction.
- The number of directions in F_p^d is (p^d − 1) / (p − 1).
- Algebraic constructions: take the Saraf-Sudan polynomial construction as a baseline.
- AlphaEvolve's d=3 construction: involve polynomial maps over F_p^3.
- For small p (p=3,5), exhaustive search or SAT-based methods can find smaller Kakeya sets.
- Try Kakeya sets of the form {x ∈ F_p^3 : f(x) = 0} for some polynomial f.

## Output format

Return a Python `dict` mapping each prime `p` to a `np.ndarray` of shape `(k, 3)` with integer entries in `{0,...,p-1}`.

```python
import numpy as np

def solve(d: int = 3, primes: list = [3, 5, 7, 11]) -> dict:
    result = {}
    for p in primes:
        # Trivial: include all points (valid but large Kakeya set)
        pts = np.array([[i, j, k] for i in range(p) for j in range(p) for k in range(p)])
        result[p] = pts
    return result
```

## Pitfalls

- A Kakeya set that misses any direction is invalid.
- Including all p^d points is always valid but gives the worst score.
- Verify the Kakeya property: for each direction v ≠ 0, all p translates of line through v must be covered.

## Baseline

All-points Kakeya set gives score ≈ −1.0 (matches reference). Saraf-Sudan gives score ≈ −0.5. AlphaEvolve constructions improve further.
