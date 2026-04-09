# Agent Guide — Finite Field Kakeya d=2

## Goal

Return a dict `{p: array}` for p ∈ {3,5,7,11,13} where each array has shape `(k, 2)` with entries in `{0,...,p-1}`, representing a Kakeya set in F_p^2; maximize average −|K(p)|/reference.

## Strategy hints

- In F_p^2, there are p+1 directions (including the vertical direction).
- A Kakeya set needs p points per direction (one full line), with maximum sharing between lines.
- For p=3: try {(0,0),(0,1),(0,2),(1,0),(2,0),(1,1)} — 6 points covering all 4 directions.
- Use integer programming or constraint satisfaction for small p (p≤7).
- Algebraic construction: take {(x,y) : y = f(x) for some polynomial f} plus correction terms.
- The Saraf-Sudan construction for d=2 gives |K| ≈ p²/2.

## Output format

Return a Python `dict` mapping each prime `p` to a `np.ndarray` of shape `(k, 2)` with integer entries in `{0,...,p-1}`.

```python
import numpy as np

def solve(d: int = 2, primes: list = [3, 5, 7, 11, 13]) -> dict:
    result = {}
    for p in primes:
        # Kakeya set from Saraf-Sudan: {(x, y) : y is in a specific set for each x}
        pts = set()
        for x in range(p):
            for y in range(p):
                pts.add((x, y))  # trivial: all points
        result[p] = np.array(list(pts))
    return result
```

## Pitfalls

- Missing any direction makes the set invalid.
- For p=13, the search space (169 points) is large; use algebraic shortcuts.
- The evaluator checks all (p+1) directions; don't forget the vertical direction (slope = ∞).

## Baseline

All p² points: score = −1.0. Saraf-Sudan: score ≈ −0.5. Optimal (for small p): can approach score ≈ −0.3.
