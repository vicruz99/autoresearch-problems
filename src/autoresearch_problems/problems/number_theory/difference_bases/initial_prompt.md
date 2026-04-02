## Difference Bases

Act as a specialist in combinatorics and number theory.

### Problem

Find a small set **B** of non-negative integers such that its set of
*differences*

$$B - B = \{b_i - b_j \mid b_i, b_j \in B,\; b_i > b_j\}$$

covers all integers in the interval **{1, 2, ..., k}** for as large a value
of k as possible.  Such a set is called a *difference basis* for [0, k].

### Scoring

```
score = k / n²
```

where **n = |B|** and **k** is the largest integer such that every integer
in {1, ..., k} is representable as a difference of two elements of B.
**Higher scores are better** (maximise k relative to n²).

The **Rohrbach bound** says that n ~ √(2k) asymptotically, giving
k/n² → 0.5 as k → ∞.

### Your Task

Implement `solve() -> List[int]` that returns the candidate set B.

Useful constructions to explore:
- **Singer difference sets**: cyclic perfect difference sets derived from
  finite projective planes (q² + q + 1 elements in Z_{q²+q+1}).
- **Leech construction**: combine a difference basis A for {0,...,a} with a
  cyclic difference set B mod m using L = {a·m + b : a∈A, b∈B}.
- **Greedy search** augmented with local optimisation.

### Example (known good construction)

```python
A = [0, 1, 4, 6]          # covers differences 1..6
# B = Singer set mod m = 89²+89+1 = 8011
# L = {a*8011 + b : a in A, b in B}
```

### Constraints

- All elements must be non-negative integers.
- Set size ≤ 10,000 elements.

```python
from typing import List

def solve() -> List[int]:
    # EVOLVE-BLOCK-START
    basis = list(range(10))
    # EVOLVE-BLOCK-END
    return basis
```
