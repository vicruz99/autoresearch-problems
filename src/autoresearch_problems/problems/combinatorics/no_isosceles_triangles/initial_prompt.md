# No Isosceles Triangles in a Grid

## Problem Description

Find the **largest subset** of the `64 × 64` integer grid `{0, 1, ..., 63}²` such that **no three points form an isosceles triangle**.

Three distinct points `a`, `b`, `c` form an isosceles triangle (with `b` as apex) if `dist(a,b) = dist(b,c)`. We check **all ordered triples** `(a, b, c)` — so `b` can be any of the three points.

The **score** is `num_points / 64` (normalized by grid side length). More points = higher score.

## Function Signature

```python
def solve() -> list:
    """
    Returns:
        list: sequence of (x, y) pairs, each an integer tuple.
              x and y must be in {0, 1, ..., 63}.
    """
```

## Evaluation

1. All points must be in the `64×64` grid
2. No duplicate points allowed
3. For every ordered triple `(a, b, c)` from the set: `dist(a,b)² ≠ dist(b,c)²`
4. `score = len(points) / 64` if valid, else `0`

**Warning**: The evaluator is `O(m³)` in the number of points `m`. Keep the set reasonably small (< 100 points) for fast evaluation.

## Tips

- An isosceles triple `(a, b, c)` means `b` is equidistant from `a` and `c`.
- The constraint is strong: most large subsets will contain isosceles triples.
- Think about sets with distinct pairwise distances (Sidon-like conditions).
- Points on a 1D grid (e.g., `y=0`) with all distinct pairwise squared distances (B₂ set) avoid isosceles triangles: `{0, 1, 3, 7, 12, 20, ...}` (Sidon sets).
- Extending a Sidon set to 2D with careful point placement can help.
