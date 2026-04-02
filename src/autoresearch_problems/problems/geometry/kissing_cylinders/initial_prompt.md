# Kissing Cylinders Problem

## Problem Description

Find **7 unit-radius infinite cylinders** that all **touch** a central cylinder aligned with the Z-axis (passing through the origin with direction `(0, 0, 1)`).

Two cylinders of unit radius touch (are tangent) when the distance between their axes equals **2** (sum of radii). The score penalizes deviations from this tangency condition.

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: shape (7, 6)
                    Each row: [px, py, pz, vx, vy, vz]
                    - (px, py, pz): a point on the cylinder axis
                    - (vx, vy, vz): direction vector of the axis (will be normalized)
    """
```

## Evaluation

For each of the 7 outer cylinders, the evaluator:
1. Normalizes the direction vector
2. Computes axis-to-axis distance to the central cylinder (Z-axis through origin) using the line-distance formula
3. Returns `score = -sum((dist_i - 2.0)^2)`

**Score = 0.0** is optimal (all cylinders exactly touching). A score close to 0 is best.

## Distance Between Lines

For two infinite lines with point `p1`, direction `v1` and point `p2`, direction `v2`:
- If not parallel: `d = |dot(p2-p1, cross(v1,v2))| / |cross(v1,v2)|`
- If parallel: `d = |cross(p2-p1, v1)|`

## Tips

- The central cylinder has position `(0,0,0)` and direction `(0,0,1)`.
- Start with cylinders at XY-distance 2 from the Z-axis and optimize directions.
- The maximum kissing number for cylinders is known to be related to circle packing in 2D.
- Try tilted configurations—cylinders don't need to be parallel to the Z-axis.
