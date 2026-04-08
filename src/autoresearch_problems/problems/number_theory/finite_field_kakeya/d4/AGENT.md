# Agent Guide — Finite Field Kakeya d=4

## Goal

Return a dict `{p: array}` for p ∈ {3,5,7} where each array has shape `(k, 4)` with entries in `{0,...,p-1}`, representing a Kakeya set in F_p^4; maximize average −|K(p)|/reference.

## Strategy hints

- In F_p^4, there are (p^4−1)/(p−1) = p³+p²+p+1 directions.
- AlphaEvolve's d=4 construction linked to elliptic curves: try defining K using the equation of an elliptic curve over F_p.
- For p=3 (81 points): exhaustive search with constraint propagation is feasible.
- For p=7 (2401 points): use algebraic constructions only; exhaustive search is too slow.
- Try: K = {(x₁,x₂,x₃,x₄) : x₄ = f(x₁,x₂,x₃)} for a carefully chosen f.
- Extend d=3 constructions by adding a fourth coordinate derived from the others.

## Output format

Return a Python `dict` mapping each prime `p` to a `np.ndarray` of shape `(k, 4)` with integer entries in `{0,...,p-1}`.

```python
import numpy as np

def solve(d: int = 4, primes: list = [3, 5, 7]) -> dict:
    result = {}
    for p in primes:
        pts = np.array([[x1, x2, x3, x4]
                        for x1 in range(p) for x2 in range(p)
                        for x3 in range(p) for x4 in range(p)],
                       dtype=int)
        result[p] = pts  # trivial: all points
    return result
```

## Pitfalls

- The timeout is 300 seconds — use precomputed/algebraic constructions, not dynamic search.
- p=7 has 2401 points; numpy operations should be vectorized.
- The number of directions (p³+p²+p+1) is large; use batch-verification.

## Baseline

All p^4 points: score = −1.0. Any algebraic construction reducing the set by 30% reaches score ≈ −0.7.
