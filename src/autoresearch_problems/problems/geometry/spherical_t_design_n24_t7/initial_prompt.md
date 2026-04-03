# Spherical t-Design (n=24, t=7)

## Problem Description

Construct a **spherical 7-design** with **24 points** on the unit sphere `S²`. A spherical `t`-design is a finite set of points `{p₁, ..., pₙ}` on the sphere such that:

```
(1/n) ∑ᵢ f(pᵢ) = (1/|S²|) ∫_{S²} f(p) dp
```

for all polynomials `f` of degree ≤ t. The **score** is `-max_error` where `max_error` is the maximum absolute discrepancy in the Gegenbauer polynomial test across degrees 1..7. **Score = 0** is perfect.

## Function Signature

```python
def solve() -> np.ndarray:
    """
    Returns:
        np.ndarray: shape (24, 3), unit sphere points.
                    Points will be projected to the unit sphere.
    """
```

## Evaluation

For each degree `k = 1, ..., 7`:
1. Compute all pairwise dot products `dᵢⱼ = pᵢ · pⱼ`
2. Evaluate Gegenbauer polynomial `C_k^(1/2)(dᵢⱼ)` for all pairs
3. The average should be 0 for a valid t-design
4. `max_error = max_k |mean(C_k^(1/2)(dᵢⱼ))|`
5. `score = -max_error` (closer to 0 = better design)

## Tips

- 24 points is the **minimum** for a spherical 7-design in `S²`.
- The vertices of the **snub cube** (24 vertices) form a near-optimal starting point.
- Gradient descent minimizing the Gegenbauer discrepancy is effective.
- The Fibonacci lattice gives a poor starting point (not symmetric enough for t=7).
- Known exact designs can be found in the literature (Hardin & Sloane tables).
