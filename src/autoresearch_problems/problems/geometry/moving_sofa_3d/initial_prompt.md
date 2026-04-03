# 3D Moving Sofa Problem

## Problem Description

Find the **largest-volume 3D solid** that can be moved through an **L-shaped 3D corridor** of unit width. The solid's shape is implicitly defined as the intersection of the corridor over all poses along the path.

## Corridor Definition

The 3D L-shaped corridor has width `W=1` and consists of three arms:
1. **Entry arm**: `x ≤ 0`, `y ∈ [0, 1]`, `z ∈ [0, 1]` (extends in -x direction)
2. **Middle arm**: `x ∈ [0, 1]`, `y ∈ [0, 5]`, `z ∈ [0, 1]` (length 4 + 1)
3. **Exit arm**: `x ∈ [0, 1]`, `y ∈ [5, 6]`, `z ≥ 0` (extends upward in z)

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: shape (m, 6) — a sequence of 3D poses
                    Each row: [tx, ty, tz, yaw_deg, pitch_deg, roll_deg]
                    - tx, ty, tz: translation of the solid's reference point
                    - yaw, pitch, roll: ZYX Euler angles in degrees
    """
```

## Evaluation

1. A 3D grid of candidate points is sampled in the entry arm region (`x ∈ [-4,0]`, `y,z ∈ [0,1]`)
2. For each pose, candidate points are rotated (ZYX Euler) and translated
3. Points outside the corridor at any pose are eliminated
4. `score ≈ (surviving points) × (cell volume)` = approximate solid volume

## Tips

- The path must navigate the solid from the **entry arm** (along x) to the **exit arm** (along z).
- This requires two 90° turns in different planes.
- Start with a simple rectangular box path and optimize.
- The solid must fit within the unit-width corridor cross-section at all times.
- The 2D Gerver sofa (area ≈ 2.22) gives an upper bound for the cross-sectional area.
