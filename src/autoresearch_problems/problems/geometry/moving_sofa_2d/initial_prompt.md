# 2D Moving Sofa Problem

## Problem Description

Find the **largest-area 2D shape** (a "sofa") that can be moved around a **right-angle corner** in an L-shaped corridor of **unit width**.

The sofa shape is implicitly defined as the set of all points that remain inside the corridor throughout the entire path. Your task is to specify the **path of poses** — the sequence of (translation_x, translation_y, rotation_degrees) — and the evaluator computes the sofa area by point sampling.

## Corridor Definition

The L-shaped corridor consists of:
- **Horizontal arm**: `y ∈ [0, 1]`, extends to the left (`x ≤ 1`)
- **Vertical arm**: `x ∈ [0, 1]`, extends upward (`y ≥ 0`)
- The corner region `x ∈ [0,1], y ∈ [0,1]` is shared

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: shape (m, 3) — a sequence of poses
                    Each row: [tx, ty, theta_deg]
                    - tx, ty: translation of the sofa reference point
                    - theta_deg: rotation angle in degrees
    """
```

## Evaluation

1. A grid of candidate points is generated in the horizontal corridor region
2. For each pose `(tx, ty, θ)`, each candidate point is rotated by `θ` and translated by `(tx, ty)`
3. Points that fall outside the corridor at any pose are eliminated
4. `score = (number of surviving points) × (cell area)` ≈ sofa area

## Tips

- The **Gerver sofa** (area ≈ 2.2195) is the conjectured optimum — try to approach it.
- The path must smoothly rotate the sofa from pointing along the x-axis to the y-axis (0° to 90°).
- More poses (larger `m`) gives more accurate sofa shape but slower evaluation.
- The translation path should sweep through the corner region `[0,1]²`.
- Symmetric paths around `(0.5, 0.5)` often give good results.
