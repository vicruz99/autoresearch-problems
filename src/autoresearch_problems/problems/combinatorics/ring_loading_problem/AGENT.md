# Agent Guide — Ring Loading Problem

## Goal

Return a list of 15 pairs (u_i, v_i) with u_i + v_i ≤ 1 that maximizes alpha = min over sign choices of max circular imbalance.

## Strategy hints

- Start with uniform pairs: all u_i = v_i = 0.5.
- The maximum alpha is bounded above by 0.5 (when all pairs have u_i + v_i = 1 and equal split).
- Try pairs where u_i and v_i vary smoothly to maximize the minimum imbalance.
- Consider pairs arranged in decreasing order of u_i − v_i to probe different sign-choice landscapes.
- Simulated annealing on the 30 values (15 × 2) works well.

## Output format

Return a Python `list` of 15 pairs, either as a flat list of 30 floats or a list of 15 [u, v] pairs. Check the evaluator for exact format.

```python
def solve(m: int = 15) -> list:
    # Uniform pairs as baseline
    pairs = []
    for i in range(m):
        pairs.append([0.5, 0.5])
    return pairs
```

## Pitfalls

- u_i or v_i negative is invalid.
- u_i + v_i > 1 is invalid.
- Very small pairs (u_i ≈ v_i ≈ 0) contribute little to imbalance.

## Baseline

All-equal pairs (0.5, 0.5) give a moderate alpha. Random valid pairs typically give alpha ≈ 0.1–0.3.
