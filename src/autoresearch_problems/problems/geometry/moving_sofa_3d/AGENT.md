# Agent Guide — Moving Sofa 3D

## Goal

Return a numpy array representing 20 3D poses (translation + rotation) for a solid moving through an L-shaped corridor; maximize the intersection volume.

## Strategy hints

- Each pose needs a 3D translation and 3D rotation (e.g., as a 6-vector or quaternion).
- The 2D Hammersley path extended to 3D: keep z=0 and add a zero z-rotation.
- Solids that are thin in the dimension perpendicular to the bend (z-axis) can have larger cross-sections in x-y.
- Try the path from the 2D solution extended into 3D with an extra dimension of freedom.
- A cylinder with axis along z, radius 0.5, can always pass through; maximize the cylinder length.

## Output format

Return a `np.ndarray` of shape `(20, 6)` where each row is `[x, y, z, rx, ry, rz]` (translation + Euler angles).

```python
import numpy as np

def solve(n_poses: int = 20, n_grid: int = 20) -> np.ndarray:
    # Extend 2D Hammersley path to 3D
    thetas = np.linspace(0, np.pi/2, n_poses)
    poses = np.zeros((n_poses, 6))
    poses[:, 0] = np.sin(thetas)     # x translation
    poses[:, 1] = 1 - np.cos(thetas) # y translation
    poses[:, 5] = thetas             # z-rotation angle
    return poses
```

## Pitfalls

- The 3D rotation parameterization must match what the evaluator expects (check evaluator.py).
- Low grid resolution (20³=8000 samples) means scores have limited precision.
- Paths that cause the solid to leave the corridor reduce volume to near-zero.

## Baseline

The 2D Hammersley path extended to 3D gives the cross-sectional area times some height. Volume depends on the z-extent of the corridor.
