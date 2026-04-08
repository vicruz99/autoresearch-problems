# Agent Guide — Kissing Cylinders

## Goal

Return a numpy array representing 7 cylinder axes (direction + position) such that all have axis-to-axis distance exactly 2 from the central Z-axis cylinder; target score = 0.0.

## Strategy hints

- Axis-to-axis distance between two skew lines can be computed as the dot product of their direction cross product with the connecting vector.
- Start with 7 cylinders in the horizontal plane (axes parallel to Z-axis) arranged in a circle of radius 2 — all are tangent to the central cylinder.
- For non-parallel cylinders, the axis-to-axis distance formula is more complex: minimize it analytically.
- Use scipy.optimize.minimize to tune axis directions and positions.
- The perfect solution (score = 0) is achievable by construction.

## Output format

Return a `np.ndarray` of shape `(7, 6)` where each row is [dx, dy, dz, px, py, pz] — the cylinder's direction vector and a point on its axis.

```python
import numpy as np

def solve(n_cylinders: int = 7) -> np.ndarray:
    # 7 cylinders with Z-parallel axes arranged in a circle of radius 2
    result = np.zeros((n_cylinders, 6))
    for i in range(n_cylinders):
        angle = 2 * np.pi * i / n_cylinders
        result[i] = [0, 0, 1, 2*np.cos(angle), 2*np.sin(angle), 0]
    return result
```

## Pitfalls

- Axis direction vectors should be unit vectors (or the evaluator will normalize them).
- Two cylinders at distance < 2 overlap — they are not valid kissing cylinders.
- The output format (shape, column meanings) must match what the evaluator expects.

## Baseline

7 parallel cylinders at radius 2, evenly spaced in angle, gives score = 0.0 (perfect). This is the known optimal.
