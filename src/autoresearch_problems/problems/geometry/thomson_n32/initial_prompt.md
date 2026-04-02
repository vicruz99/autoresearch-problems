# Thomson Problem (n=32)

## Problem Description

Place **32 unit charges** on the surface of the unit sphere in ℝ³ to **minimize the total electrostatic (Thomson) energy**:

```
E = sum_{i < j} 1 / ||p_i - p_j||
```

The score returned is **negative energy** (`score = -E`), so **maximizing** the score corresponds to **minimizing** the energy.

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: shape (32, 3), each row is a 3D point.
                    Points will be projected to the unit sphere before evaluation.
    """
```

## Evaluation

The evaluator:
1. Projects each point onto the unit sphere: `p /= ||p||`
2. Computes all pairwise distances
3. Returns `score = -sum_{i<j} 1/dist(i,j)`

A higher (less negative) score means lower energy = better configuration.

## Tips

- Start with a good initial placement (e.g., Fibonacci sphere or icosahedral arrangement).
- Gradient descent with the Coulomb repulsion force is effective: move each point away from others along the sphere tangent.
- The optimal configuration for n=32 is not analytically known; numerical optimization is required.
- The energy for Fibonacci sphere initialization is a reasonable baseline to beat.
