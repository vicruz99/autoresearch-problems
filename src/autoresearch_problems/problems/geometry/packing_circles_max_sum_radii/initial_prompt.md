# Circle Packing: Maximize Sum of Radii

## Problem Description

Pack **26 non-overlapping circles** inside the unit square `[0,1]²` to **maximize the sum of their radii**.

Unlike the classic circle packing problem (which packs equal-radius circles), here circles may have **different radii**. The objective is to maximize the total coverage `∑ rᵢ`.

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: shape (26, 3)
                    Each row: [cx, cy, r]
                    - cx, cy: center of the circle
                    - r: radius (must be positive)
    """
```

## Constraints

1. All radii must be **positive**: `r > 0`
2. Each circle must be **inside the unit square**: `cx - r ≥ 0`, `cx + r ≤ 1`, `cy - r ≥ 0`, `cy + r ≤ 1`
3. No two circles may **overlap**: `dist(cᵢ, cⱼ) ≥ rᵢ + rⱼ` for all `i ≠ j`

## Evaluation

- If any constraint is violated: `score = 0`
- Otherwise: `score = sum(r)`

## Tips

- The optimal solution may have **one large circle** and many small ones filling the gaps.
- Consider using different sizes: one large circle near the center, then progressively smaller circles in the corners and gaps.
- The Apollonian gasket gives a mathematically optimal packing for the infinite case.
- For n=26, the sum of radii is bounded above by `√(26/π)/2 ≈ 1.44` (area packing bound).
