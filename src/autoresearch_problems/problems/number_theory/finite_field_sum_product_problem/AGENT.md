# Agent Guide — Finite Field Sum-Product Problem

## Goal

Return a dict `{p: array}` for p in `[101, 257, 1009]` where each array is a subset X ⊆ F_p of size ⌊√p⌋ minimizing log(max(|X+X|,|X·X|))/log(|X|); lower is better.

## Strategy hints

- An arithmetic progression X = {a, a+d, ..., a+(k-1)d} gives |X+X| = 2k−1 ≈ 2k but |X·X| can be large.
- A geometric progression X = {a, ar, ar², ...} gives small |X·X| but large |X+X|.
- AlphaEvolve's AP∩GP idea: take X = (AP) ∩ (GP) to balance both quantities.
- For p=101, |X| = 10; try all 10-element subsets of AP or GP.
- For p=1009, |X| = 31; optimize over parameterized families.
- Target: max(|X+X|,|X·X|) ≈ |X|^{1.5} to achieve ratio ≈ 1.5.

## Output format

Return a Python `dict` mapping each prime `p` to a `np.ndarray` of shape `(k,)` with integer entries in `{0,...,p-1}` (or a 1D array of ⌊√p⌋ elements).

```python
import numpy as np

def solve(primes: list = [101, 257, 1009]) -> dict:
    result = {}
    for p in primes:
        k = int(p**0.5)
        # Arithmetic progression: {0, 1, 2, ..., k-1}
        X = np.arange(k, dtype=int) % p
        result[p] = X
    return result
```

## Pitfalls

- X must be a subset of F_p = {0, 1, ..., p-1}.
- Size must be exactly ⌊√p⌋ for the score to be computed correctly.
- Including 0 in X can make |X·X| = {0} ∪ X·X\{0}, which complicates things.

## Baseline

Arithmetic progression {1,2,...,k}: |X+X| ≈ 2k, |X·X| ≈ k(k-1)/2, ratio ≈ 1.5. Geometric progression: |X+X| can be as large as k²/2.
