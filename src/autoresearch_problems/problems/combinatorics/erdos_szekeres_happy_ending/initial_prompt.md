# Erdős–Szekeres Happy Ending Problem

## Problem

The **Erdős–Szekeres theorem** states that any set of 2^(n−2)+1 points in the
plane in *general position* (no three collinear) must contain the vertices of a
convex n-gon.

Your goal is to find a configuration of **exactly 2^(n−2)+1 points** in general
position that **minimises the total number of convex n-gons** among them.

## What to implement

Implement `solve(n: int) -> np.ndarray` that returns a float array of shape
`(2^(n-2)+1, 2)`.

```python
import numpy as np

def solve(n: int = 6) -> np.ndarray:
    # Return shape (2^(n-2)+1, 2): a point configuration in general position
    # that minimises the number of convex n-gons.
    ...
```

For `n=6` you need **17 points**; for `n=7` you need **33 points**.

## Scoring

- **Score = −(number of convex n-gons)**.  Higher (less negative) is better.
- Score 0 would mean zero convex n-gons — a counterexample to Erdős–Szekeres.
- If any **three points are collinear** (|2·signed_area| < 1e-9) the score is
  −10^15 (heavy penalty).
- If any **two points overlap** (squared distance < 1e-12) the score is also
  penalised heavily.
- The evaluator returns the exact count using a dynamic-programming approach.

## Notes

- The Erdős–Szekeres theorem guarantees at least one convex n-gon, so a
  perfect score of 0 is **impossible**.  The competition is to minimise the count.
- Points in convex position (e.g. a regular polygon) maximise the count —
  every n-subset is a convex n-gon.
- Clustering points to avoid convex subsets, while maintaining general position,
  is the key challenge.
