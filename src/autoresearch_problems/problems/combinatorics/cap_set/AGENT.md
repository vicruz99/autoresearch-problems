# Agent Guide — Cap Set

## Goal

Return a numpy array of shape `(k, 8)` with entries in {0, 1, 2} representing k vectors in F_3^8 such that no three form a 3-AP (x + y + z ≡ 0 mod 3); maximize k.

## Strategy hints

- Start from a greedy algorithm: add vectors one by one, checking the cap set property before each addition.
- Use the algebraic structure: cap sets in F_3^n can be constructed by taking combinatorial products of small cap sets.
- A known large cap set in F_3^4 has 20 elements; try tensor products to scale to n=8.
- Represent elements as integers in base 3 for faster computation.
- Evolutionary search starting from known constructions works better than random search.

## Output format

Return a `np.ndarray` of shape `(k, 8)` with dtype int, values in {0, 1, 2}.

```python
import numpy as np

def solve(n: int = 8, q: int = 3) -> np.ndarray:
    # Greedy cap set construction
    cap = []
    cap_set_ints = set()
    for x in range(3**n):
        v = np.array([(x // 3**i) % 3 for i in range(n)])
        valid = True
        for a in cap:
            for b in cap:
                if np.all((v + a + b) % 3 == 0):
                    valid = False
                    break
            if not valid:
                break
        if valid:
            cap.append(v)
    return np.array(cap) if cap else np.zeros((0, n), dtype=int)
```

## Pitfalls

- The greedy check is O(k²) per insertion — memoize or use vectorized modular arithmetic for speed.
- Returning duplicate vectors is invalid.
- Vectors must have entries strictly in {0, 1, 2} — not {−1, 0, 1} or {1, 2, 3}.

## Baseline

A greedy algorithm typically finds cap sets of size ~100–200. The known best for F_3^8 is 496. A trivial baseline (return a single element) scores 1.
