# No 5 on a Sphere (Great Circle)

## Problem Description

Place as many points as possible on the unit sphere in ℝ³ such that **no 5 points lie on any common great circle**.

A **great circle** is the intersection of the unit sphere with any plane passing through the origin. Five points lie on a common great circle if and only if they all lie in a 2-dimensional subspace through the origin (i.e., they are coplanar with the origin).

The **score** equals the number of points in the output — more points is better.

## Constraint

For every subset of 5 points from your output, the 5×3 matrix formed by the unit vectors must have **rank ≥ 3** (not coplanar with origin). The evaluator checks this via singular value decomposition: if the 3rd singular value is less than 1e-6, the 5 points are considered coplanar.

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: shape (m, 3) for any m >= 1.
                    Points will be projected to the unit sphere.
                    Score = m if no 5 points are on a great circle, else 0.
    """
```

## Evaluation

1. Points are projected to the unit sphere
2. All C(m, 5) subsets of 5 points are checked for coplanarity with origin
3. If any 5 are coplanar: `score = 0` (invalid)
4. Otherwise: `score = m` (number of points)

## Tips

- Generic random points on the sphere are very unlikely to have 5 coplanar ones—but as m grows, accidental near-coplanarity becomes an issue.
- Consider using algebraically independent directions or points from a construction with provable properties.
- The evaluator is O(m^5) in the number of points, so do not return very large sets.
