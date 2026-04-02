# Ovals Problem (Minimize Rayleigh Quotient)

## Problem Description

Find a **convex closed planar curve** and a function **φ** defined on it to **minimize** the Rayleigh quotient:

```
R(φ) = ∫(φ'² + κ²·φ²) dt / ∫ φ² dt
```

where `κ` is the curvature of the curve and the integrals are over the parameter `t ∈ [0, 2π]`.

The **score** is `-R` (negative Rayleigh quotient), so **maximizing** score corresponds to **minimizing** R.

## Function Signature

```python
def solve() -> list:
    """
    Returns:
        list: [x, y, phi] where each is a numpy array of length n=100.
              - x[i], y[i]: B-spline control points for the curve parametrization
              - phi[i]: values of the function phi at n uniformly spaced parameter values
    """
```

## Evaluation

1. A periodic B-spline of degree 4 is fitted to `(x, y)` and `phi` control points
2. The curve must have positive speed everywhere (non-degenerate)
3. The curve must be **convex** (positive signed curvature `x'·y'' - x''·y' > 0` everywhere)
4. Rayleigh quotient `R = ∫(φ'² + κ²φ²)dt / ∫φ²dt` is computed numerically
5. Returns `score = -R`

## Tips

- For a **unit circle**, the curvature κ = 1, so R = (∫φ'²dt + ∫φ²dt) / ∫φ²dt ≥ 1.
- The minimum for the circle over all φ is achieved when φ is a Fourier mode: φ(t) = sin(t) gives R = 1 + 1 = 2.
- Non-circular convex curves may have lower minimum Rayleigh quotient.
- Scale the curve so that the curvature is as small as possible (larger curves have smaller κ).
