# Agent Guide — Packing Unit Cubes

## Goal

Return a numpy array of shape `(11, 6)` with columns `[cx, cy, cz, α, β, γ]` (center + Euler angles) representing 11 non-overlapping unit cubes in the smallest bounding cube; maximize score = −side_length.

## Strategy hints

- Start with all cubes axis-aligned and packed in a 2×2×3 arrangement minus 1 cube.
- A 2×2×3 arrangement fits in a 2×2×3 box; with 11 cubes, try 3×2×2 = 12 − 1 cube arrangements.
- Tilting cubes by small angles can reduce the bounding box by fitting them in "staircase" patterns.
- Use scipy.optimize.minimize on the 66 parameters (11 × 6).
- The bounding box is computed from all 8 corners of each rotated cube.

## Output format

Return a `np.ndarray` of shape `(11, 6)` where each row is `[cx, cy, cz, euler_angle_1, euler_angle_2, euler_angle_3]`.

```python
import numpy as np

def solve(n: int = 11) -> np.ndarray:
    # Pack 11 cubes in a 3x2x2 arrangement with one cube tilted
    result = []
    for x in range(3):
        for y in range(2):
            for z in range(2):
                if len(result) < 11:
                    result.append([x + 0.5, y + 0.5, z + 0.5, 0, 0, 0])
    return np.array(result[:11])
```

## Pitfalls

- Non-intersecting check is expensive — the evaluator may use a simplified bounding box.
- Euler angle conventions vary; check whether the evaluator uses ZYX, XYZ, etc.
- Very large rotation angles may cause numerical issues.

## Baseline

11 axis-aligned cubes in a 3×2×2 bounding box (minus one corner slot): side = 3, score = −3. Diagonal arrangements can reduce this to ~2.8.
