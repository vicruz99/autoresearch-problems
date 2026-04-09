# Agent Guide — Finite Field Kakeya d=3

## Goal

Return a dict `{p: array}` for p ∈ {3,5,7,11} where each array has shape `(k, 3)` with entries in `{0,...,p-1}`, representing a Kakeya set in F_p^3; maximize average −|K(p)|/reference.

## Strategy hints

- In F_p^3, there are (p³−1)/(p−1) = p²+p+1 directions.
- AlphaEvolve's construction likely involves polynomial constructions over F_p^3.
- Try: K = {(x, y, f(x, y)) : x,y ∈ F_p} ∪ corrections for specific directions.
- Graph constructions: represent the Kakeya problem as a hypergraph covering problem and use greedy set cover.
- For p=3 (27 points total), exact minimum is achievable by exhaustive search.
- Read AlphaEvolve's paper for hints about the d=3 algebraic construction.

## Output format

Return a Python `dict` mapping each prime `p` to a `np.ndarray` of shape `(k, 3)` with integer entries in `{0,...,p-1}`.

```python
import numpy as np

def solve(d: int = 3, primes: list = [3, 5, 7, 11]) -> dict:
    result = {}
    for p in primes:
        # Graph-based construction: for each direction, include a canonical line
        pts = set()
        for a in range(p):
            for b in range(p):
                # Line in direction (1, 0, a): {(t, 0, a*t) : t ∈ F_p}
                for t in range(p):
                    pts.add((t % p, 0, (a*t) % p))
                # Add more directions...
        for x in range(p):
            for y in range(p):
                pts.add((x, y, 0))
        result[p] = np.array(list(pts))
    return result
```

## Pitfalls

- The d=3 Kakeya problem has p²+p+1 directions — ensure all are covered.
- For p=11, checking all directions is expensive; vectorize using numpy modular arithmetic.
- Constructions that work for p=3 may not generalize to p=11.

## Baseline

All p³ points: score = −1.0. Saraf-Sudan: score ≈ −0.5. AlphaEvolve improved on this.
