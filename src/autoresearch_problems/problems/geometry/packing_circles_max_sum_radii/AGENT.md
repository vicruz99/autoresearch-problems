# Agent Guide — Packing Circles Max Sum Radii

## Goal

Return a numpy array of shape `(26, 3)` with columns `[cx, cy, radius]` representing 26 non-overlapping circles inside [0,1]²; maximize Σ radius.

## Strategy hints

- Hierarchical packing: place one large circle, then fill gaps with smaller circles.
- The Apollonius gasket gives optimal circle packings in irregular shapes.
- Greedy approach: place circles from largest to smallest, each as large as possible given existing circles.
- Equal-radius packing of 26 circles gives a baseline; optimizing radii individually can improve sum.
- Boundary constraint: center must be at distance ≥ radius from each wall.

## Output format

Return a `np.ndarray` of shape `(26, 3)` where each row is `[cx, cy, radius]` with cx, cy ∈ [0,1] and radius > 0.

```python
import numpy as np

def solve(n: int = 26) -> np.ndarray:
    # Equal radius packing in a 5x5 hex grid + 1 extra
    r = 0.089  # approximate radius for 26-circle packing
    centers = []
    for row in range(6):
        for col in range(5):
            x = r + col * 2 * r + (r if row % 2 else 0)
            y = r + row * 2 * r * np.sqrt(3)/2 * 0.9
            if 0 < x < 1 and 0 < y < 1:
                centers.append([x, y, r])
    arr = np.array(centers[:n])
    return arr
```

## Pitfalls

- Any circle extending outside [0,1]² (cx − r < 0, etc.) is invalid.
- Two overlapping circles (distance < r_i + r_j) are invalid.
- Setting all radii very small scores poorly (sum ≈ 0 for r ≈ 0).

## Baseline

26 circles with equal radius ≈ 0.089 packed on a hex grid scores ≈ 2.3. A single circle of radius 0.5 scores 0.5.
