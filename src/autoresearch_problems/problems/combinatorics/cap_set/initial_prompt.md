# Cap Set Problem

## Task

Find the **largest possible subset** S of F_3^8 (the 8-dimensional vector space over GF(3)) such that **no three elements of S form a three-term arithmetic progression**.

Formally, S must satisfy: for all distinct x, y, z ∈ S, x + y + z ≢ 0 (mod 3).

## What to implement

Implement a function `solve() -> np.ndarray` that returns the cap set as a 2-D NumPy array of shape `(k, 8)` with integer entries in `{0, 1, 2}`.  Each row is a vector in F_3^8.

```python
import numpy as np

def solve() -> np.ndarray:
    # Return a 2-D integer array of shape (k, 8) with entries in {0, 1, 2}.
    # Maximise k while ensuring no three rows sum to 0 (mod 3).
    ...
```

## Scoring

- **Score = k** (the number of vectors in the set).
- A higher score is better.
- The set is invalid (score = 0) if any three-term arithmetic progression exists.

## Notes

- The known upper bound for |S| in F_3^8 is 496 (Croot–Lev–Pach / Ellenberg–Gijswijt bound).
- A simple greedy or random search can find sets of size ~300–400.
- The world-record for F_3^8 is larger; can your program beat the greedy baseline?
