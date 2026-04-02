# Finite Field Kakeya Problem

## Problem

A **Kakeya set** in F_p^d (the d-dimensional vector space over the finite field
of prime order p) is a subset K ⊆ F_p^d that contains a complete line in every
direction.  Formally, for every non-zero vector v ∈ F_p^d there must exist a
base point x ∈ K such that the line

  { x + t·v  mod p  :  t ∈ F_p } ⊆ K.

**Goal**: find a Kakeya set K of minimum cardinality |K|.

## What to implement

Implement `solve(p: int, d: int) -> np.ndarray` that returns an integer array
of shape `(k, d)` with entries in `{0, …, p-1}` representing the set K.

```python
import numpy as np

def solve(p: int = 3, d: int = 3) -> np.ndarray:
    # Return shape (k, d): a Kakeya set in F_p^d, entries in {0,...,p-1}.
    # Minimise k while ensuring the Kakeya property.
    ...
```

## Scoring

- **Score = −(|K| / |reference|)** where the reference is the Saraf–Sudan
  construction of size ≈ p^d / 2.  Higher (less negative) is better.
- Score −1.0 = matches the Saraf–Sudan reference.
- Score > −1.0 = smaller than the reference (improvement).
- If K is **not** a valid Kakeya set the score is −10^6 (heavy penalty).
- Duplicate points are silently removed before scoring.

## Notes

- The Dvir (2009) lower bound gives |K| ≥ p^d / d!.  For d=3, p=3 that is
  3^3 / 6 = 4.5, so |K| ≥ 5.
- The best known constructions have size ≈ (1/2) p^d + lower-order terms.
- The Saraf–Sudan construction (the baseline) achieves size ≈ p^d / 2.
- Directions are equivalence classes of non-zero vectors under scalar
  multiplication: the number of distinct directions in F_p^d is
  (p^d − 1)/(p − 1).
