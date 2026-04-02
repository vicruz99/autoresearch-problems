# Tammes Problem (n=14)

## Problem Description

Place **14 points** on the surface of the unit sphere in ℝ³ such that the **minimum pairwise Euclidean distance** between any two points is **maximized**.

This is the Tammes problem for n=14, also known as the spherical packing problem. The goal is to distribute 14 points as evenly as possible on the unit sphere.

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: shape (14, 3), each row is a 3D point.
                    Points need not be on the unit sphere—they will be
                    projected to the unit sphere before evaluation.
    """
```

## Evaluation

The evaluator:
1. Projects each point onto the unit sphere: `p /= ||p||`
2. Computes all pairwise Euclidean distances
3. Returns `score = min(pairwise distances)`

A higher score means the points are more evenly spread.

## Tips

- The theoretical maximum min-distance for n=14 on the unit sphere is approximately 0.9191.
- Fibonacci sphere sampling gives a good initial distribution.
- Gradient-based repulsion (treating points as charged particles) can improve results.
- The score is invariant to overall rotation of the configuration.
