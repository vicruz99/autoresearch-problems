# Agent Guide — Difference Bases

## Goal

Return a list of distinct non-negative integers B such that {b_i − b_j : b_i > b_j, b_i,b_j ∈ B} covers {1, 2, ..., k} consecutively; maximize k/|B|²; target ≥ 0.45.

## Strategy hints

- Start with {0, 1, 2, 4, 8, ...} (powers of 2) — covers many differences with few elements.
- Greedy: start from {0} and add each element that covers the most new differences.
- Perfect difference sets (from finite geometry) achieve ratio ≈ 0.5: B = {0, 1, 3, 7} covers {1,2,3,4,5,6,7} with |B|=4, ratio = 7/16 ≈ 0.44.
- Sidon sets (B₂ sets) achieve k ≈ n² differences uniquely, approaching ratio 0.5.
- Try B based on quadratic residues mod prime p: {i² mod p : i = 0,...,(p-1)/2}.

## Output format

Return a Python `list` of distinct non-negative integers.

```python
def solve() -> list:
    # Perfect difference set for prime p=7: {0, 1, 3, 7}
    B = [0, 1, 3, 7]
    # Check: diffs = {1,2,3,4,6,7} — covers 1,2,3 consecutively (k=3) — not ideal
    # Better: {0,1,3,6,10,15} as a near-Sidon set
    return [0, 1, 3, 6, 10, 15, 21, 28]
```

## Pitfalls

- Duplicate integers are counted as one element — all elements must be distinct.
- B must be a set of non-negative integers; negative values may be rejected.
- Maximizing n (set size) at the expense of coverage k can reduce score if k grows slower than n².

## Baseline

B = {0, 1, 3, 7}: covers 1,2,3 (k=3), |B|=4, score = 3/16 ≈ 0.19. B = {0,1,3,6,10,15}: k≈18, |B|=6, score≈18/36=0.5.
