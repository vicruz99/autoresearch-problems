# Agent Guide — Finite Field Kakeya d=5

## Goal

Return a dict `{p: array}` for p ∈ {3,5} where each array has shape `(k, 5)` with entries in `{0,...,p-1}`, representing a Kakeya set in F_p^5; maximize average −|K(p)|/reference.

## Strategy hints

- p=3: 3^5 = 243 points; combinatorial search may be feasible.
- p=5: 5^5 = 3125 points; only algebraic constructions are feasible in 600s.
- Generalize d=3 or d=4 constructions: add extra coordinates f(x₁,...,x_{d-1}).
- The Saraf-Sudan construction: K = {x ∈ F_p^d : P(x) = 0} for a specific low-degree polynomial P.
- Try cross-product constructions: K₅ = K₂ × K₃ (Cartesian product of lower-d Kakeya sets).

## Output format

Return a Python `dict` mapping each prime `p` to a `np.ndarray` of shape `(k, 5)` with integer entries in `{0,...,p-1}`.

```python
import numpy as np

def solve(d: int = 5, primes: list = [3, 5]) -> dict:
    result = {}
    for p in primes:
        # Saraf-Sudan-style: take half of all points
        pts = []
        for x in range(p):
            for x1 in range(p):
                for x2 in range(p):
                    for x3 in range(p):
                        for x4 in range(p):
                            # Include if meets some criterion
                            pts.append([x, x1, x2, x3, x4])
        result[p] = np.array(pts[:p**d // 2 + p**3], dtype=int)
    return result
```

## Pitfalls

- The 600-second timeout must accommodate construction time — precompute offline and hardcode if needed.
- p=5, d=5 has (5^5−1)/(5−1) = 781 directions — verifying all is expensive.
- The trivial all-points construction always works but scores −1.0.

## Baseline

All p^5 points: score = −1.0. Saraf-Sudan fraction (≈ p^5/2): score ≈ −0.5.
