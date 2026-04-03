# Tammes Problem (n=24)

## Problem Description

Place **24 points** on the surface of the unit sphere in ℝ³ such that the **minimum pairwise Euclidean distance** between any two points is **maximized**.

This is the Tammes problem for n=24, also known as the spherical packing problem. The goal is to distribute 24 points as evenly as possible on the unit sphere.

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: shape (24, 3), each row is a 3D point.
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

- The 24-cell (vertices of a 24-cell projected to 3D) may provide useful inspiration.
- Fibonacci sphere sampling gives a good initial distribution.
- Gradient-based repulsion (treating points as charged particles) can improve results.
- The snub cube has 24 vertices on a sphere and may be near-optimal.
- The score is invariant to overall rotation of the configuration.
