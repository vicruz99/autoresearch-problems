# Finite Field Sum-Product Problem

Act as a research mathematician specialising in additive combinatorics.

## Problem Statement

The **sum-product conjecture** (Erdős–Szemerédi, extended to finite fields)
states that for any set X in a field, at least one of the sum set X+X or the
product set X·X must be large.  Your task is to *challenge* this conjecture by
constructing a set that keeps *both* sets small.

Given a prime `p` (≈ 10^3), construct a set X ⊆ F_p of size exactly
⌊√p⌋ that minimises  **max(|X+X|, |X·X|)**  where

    X + X = {(a + b) mod p : a, b ∈ X}
    X · X = {(a × b) mod p : a, b ∈ X}

## Function Signature

```python
def solve(p: int = 1009) -> np.ndarray:
    """Return floor(sqrt(p)) distinct elements of {0,...,p-1}.

    Returns a 1-D int64 array of shape (k,), k = floor(sqrt(p)).
    """
```

## Evaluation

Score = max(|X+X|, |X·X|).  **Lower is better.**

- An arithmetic progression {0,1,…,k−1} gives |X+X| = 2k−1 but |X·X| ≈ k².
- A geometric progression {1,g,g²,…} gives |X·X| = 2k−1 but |X+X| ≈ k².
- **Target:** max(|X+X|, |X·X|) ≪ k² ≈ p.

## Benchmarks

| Construction | Score (p=1009, k=31) |
|---|---|
| Arithmetic progression | ~900 |
| AP ∩ GP intersection | ~170 |
| AlphaEvolve best (AP∩GP) | ~120 |

## Hints

- **AP ∩ GP:** Intersect {1,…,L} with {g^0, g^1, …, g^{L-1}} mod p for a
  well-chosen generator g. The smallest L giving ≥k elements minimises 2L−1.
  Try g = a/b for small integers a, b.
- **Centered AP:** Intersect {−(L−1)/2, …, L/2} (mod p) with a GP; can yield
  a smaller L for some generators.
- **Gaussian integers mod p:** Represent elements as a+bi (mod p) where i²=−1
  (possible when p ≡ 1 mod 4). Sort candidates (a,b) by the largest prime
  factor of a²+b²; smooth norms give structured sets.
- **Cubic roots:** For p ≡ 2 mod 3, generators from cubic roots of small
  integers can work.
- You may use any search procedure; the function must return within
  `timeout_seconds` of the spec.

## Initial Implementation

```python
import math, numpy as np

def solve(p: int = 1009) -> np.ndarray:
    k = int(math.sqrt(p))
    return np.arange(k, dtype=np.int64)  # simple AP baseline
```
