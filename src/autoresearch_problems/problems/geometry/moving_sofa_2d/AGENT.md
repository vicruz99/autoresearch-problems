# Agent Guide — Moving Sofa 2D

## Goal

Return a numpy array of shape `(20, 3)` representing 20 poses `[x, y, θ]` for moving the sofa; maximize the area of the intersection region; target area > 2.2.

## Strategy hints

- Each pose is `[x, y, θ]` where (x, y) is the translation and θ is the rotation angle.
- The sofa must fit within the L-shaped corridor at every pose.
- Start from the Hammersley sofa path: θ goes from 0 to π/2, x = sin(θ), y = 1 − cos(θ).
- Discretize this smooth path into 20 evenly spaced angle values.
- Gerver's optimal sofa has a more complex curved path — parameterize with 20 points along it.
- The area is evaluated approximately (50×50 grid); finer parameterization improves score but the grid is fixed.

## Output format

Return a `np.ndarray` of shape `(20, 3)` where each row is `[x_translation, y_translation, rotation_angle]`.

```python
import numpy as np

def solve(n_poses: int = 20, n_grid: int = 50) -> np.ndarray:
    # Hammersley sofa path
    thetas = np.linspace(0, np.pi/2, n_poses)
    poses = np.column_stack([
        np.sin(thetas),         # x translation
        1 - np.cos(thetas),     # y translation
        thetas                  # rotation angle
    ])
    return poses
```

## Pitfalls

- If the sofa exits the corridor at any pose, the intersection becomes empty or very small.
- The 50×50 grid gives only ≈ 2 decimal places of accuracy — small improvements may not be detected.
- Ensure the path is continuous (no abrupt jumps in angle or position).

## Baseline

Hammersley path gives area ≈ 2.207. A semicircular sofa (radius 0.5) gives area ≈ 0.785 — much worse.
