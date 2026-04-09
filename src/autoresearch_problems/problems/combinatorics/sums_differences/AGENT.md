# Agent Guide — Sums and Differences

## Goal

Return a list of distinct integers A that maximizes log|A−A|/log|A+A|; higher ratio means the difference set is much larger relative to the sumset.

## Strategy hints

- To maximize the ratio, you want |A−A| to be large and |A+A| to be small.
- Arithmetic progressions minimize both — avoid them.
- Sets with additive structure (like Sidon sets) have |A+A| ≈ |A|² but also large |A−A|.
- Consider sets based on geometric progressions perturbed by small additive noise.
- Sets of size 10–100 are computationally tractable.

## Output format

Return a Python `list` of distinct integers.

```python
def solve() -> list:
    # B_2 (Sidon) set: no two pairs with equal sum
    # The squares {1, 4, 9, 16, 25, ...} give a near-Sidon set
    return [i**2 for i in range(1, 20)]
```

## Pitfalls

- Duplicate elements are invalid (all must be distinct).
- |A+A| = 1 (all sums equal) means A has at most 1 element — degenerate.
- Very large sets slow down the evaluator quadratically.

## Baseline

Arithmetic progression {0,1,...,19} gives ratio ≈ 1.0. Squares {1,4,9,...,361} give ratio closer to 1.5–1.8.
