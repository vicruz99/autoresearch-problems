# Packing Unit Cubes

## Problem Description

Pack **11 unit cubes** (side length 1) into the **smallest possible axis-aligned bounding cube**. Cubes may be **rotated arbitrarily**.

The **score** is the **negative of the bounding box side length** (`score = -side`), so maximizing score corresponds to minimizing the bounding cube.

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: shape (11, 6)
                    Each row: [cx, cy, cz, rx, ry, rz]
                    - cx, cy, cz: center of the cube
                    - rx, ry, rz: Euler rotation angles in degrees (ZYX convention)
    """
```

## Evaluation

1. Rotation matrices are computed using ZYX Euler angles: `R = Rz(rz) @ Ry(ry) @ Rx(rx)`
2. The 8 vertices of each cube are computed in world coordinates
3. **Separating Axis Theorem (SAT)** checks for intersection between all pairs of cubes
4. If any two cubes intersect: `score = 0` (invalid)
5. Otherwise: `score = -max(bounding_box_span_x, span_y, span_z)`

## Tips

- 11 axis-aligned unit cubes arranged in a grid pattern require a bounding box with the smallest side of at least 3 (e.g. a 2×2×3 arrangement).
- Rotating cubes by 45° can reduce bounding box in some configurations.
- The theoretical minimum for 11 cubes is approximately 2.73 (with rotations).
- Start with a 3×4 or 4×3 grid and then optimize rotations.
- A cube rotated 45° around one axis fits in a bounding box of `1 × √2 × √2` — sometimes useful for interlocking.
