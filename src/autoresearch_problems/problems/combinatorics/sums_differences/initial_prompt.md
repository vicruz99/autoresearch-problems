# Sums and Differences (Ruzsa's Inequality)

## Problem Description

Find a set `A` of **distinct integers** to **maximize**:

```
score = log|A - A| / log|A + A|
```

where:
- `A + A = {a + b : a, b ∈ A}` (sumset)
- `A - A = {a - b : a, b ∈ A}` (difference set)
- `|·|` denotes cardinality

**Ruzsa's inequality** states that `|A - A| ≤ |A + A|^(3/2) / |A|^(1/2)`, so the ratio `log|A-A| / log|A+A|` is bounded above by `3/2`. Finding sets where the difference set is much larger than the sumset challenges this bound.

## Function Signature

```python
def solve() -> list:
    """
    Returns:
        list: a sequence of distinct integers.
              Example: [0, 1, 2, 4]
    """
```

## Evaluation

1. Duplicates are removed (only unique elements count)
2. `A + A` and `A - A` are computed as sets
3. `score = log(|A - A|) / log(|A + A|)` (using natural or any consistent log base — ratio is same)

## Tips

- **Arithmetic progressions** have `|A - A| = |A + A| - 1 ≈ |A + A|`, giving ratio ≈ 1.
- **Sidon sets** (B₂ sets) have `|A + A| = |A|(|A|+1)/2`, maximizing `|A + A|`, making the denominator large.
- To **maximize** the ratio, we want `|A - A|` to be large relative to `|A + A|`.
- For random sets, `|A - A| ≈ 2|A + A| - 1`, giving ratio slightly above 1.
- The **theoretical maximum** ratio approaches 3/2 as `|A| → ∞` for some constructions.
- Try structured sets like `{0, n, 2n, ...}` (arithmetic) or random integer sets.
