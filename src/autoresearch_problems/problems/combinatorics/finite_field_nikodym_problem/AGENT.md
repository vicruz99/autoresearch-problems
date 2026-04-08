# Agent Guide — Finite Field Nikodym Problem

## Goal

Return a dict `{p: array}` for each prime p in `primes=[3,5]` where each array has shape `(k, 2, 2)` with values in `{0,...,p-1}`, representing a Nikodym set in F_{p²}^2; maximize the average complement fraction.

## Strategy hints

- A Nikodym set must contain a full punctured line in every direction through every point.
- Start with a construction that works for small p and generalize.
- For p=3: F_{9}^2 has 81 points; a Nikodym set using ~55–70 points gives complement fraction ~0.14–0.32.
- Use algebraic constructions based on polynomial maps over F_{p²}.
- The complement set (points NOT in N) is small; try to find which points can safely be excluded.

## Output format

Return a Python `dict` mapping each prime `p` to a `np.ndarray` of shape `(k, 2, 2)` with integer entries in `{0,...,p-1}`. Each `array[i]` is a 2×2 matrix representing a point in F_{p²}^2.

```python
import numpy as np

def solve(d: int = 2, primes: list = [3, 5]) -> dict:
    result = {}
    for p in primes:
        # Include all points as a valid (but non-optimal) Nikodym set
        q = p * p
        pts = []
        for a in range(q):
            for b in range(q):
                pts.append([[a // p, a % p], [b // p, b % p]])
        result[p] = np.array(pts)
    return result
```

## Pitfalls

- The all-points set is always a valid Nikodym set but scores 0 (no complement).
- Missing a single required punctured line will make the set invalid.
- The array shape must be `(k, 2, 2)` — not `(k, 4)` or other shapes.

## Baseline

Returning all points of F_{p²}^2 gives score 0.0. The best known constructions achieve ~3–14% complement fraction depending on p.
