# Prime Number Theorem Optimization

## Problem Description

Find a **partial function** `f: ℤ⁺ → ℝ` (represented as a Python `dict` mapping positive integers to floats) to **maximize**:

```
a(f) = -∑_{k in domain(f)}  f(k) · log(k) / k
```

subject to the **constraint** that for all real `x ≥ 1`:

```
∑_{k in domain(f)}  f(k) · ⌊x/k⌋  ≤  1
```

This is related to explicit formulas in analytic number theory, where the constraint resembles a Dirichlet series condition.

## Function Signature

```python
def solve() -> dict:
    """
    Returns:
        dict: mapping positive integers (keys) to real values (floats).
              Example: {1: 3.47, 2: -1.0, 3: -1.0, 5: -1.0, 30: 1.0}
    """
```

## Evaluation

1. The function is normalized: `f(1)` is adjusted so that `∑ f(k)/k = 0`
2. The constraint is checked at `num_samples=100000` random `x` values in `[1, 10·max_key]`
3. If the constraint is violated: `score = -inf` (invalid)
4. Otherwise: `score = a(f) = -∑ f(k)·log(k)/k`

## Tips

- The Möbius function `μ(n)` is a natural starting point (related to `1/ζ(s)` in the Dirichlet series sense).
- Smaller support (fewer keys) makes the constraint easier to satisfy.
- The value `f(1)` is auto-adjusted by the evaluator for normalization.
- A higher score means the function "extracts more" from the prime distribution.
