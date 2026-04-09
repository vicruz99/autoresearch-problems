# Agent Guide — Ovals Problem

## Goal

Return a list representing a convex curve (n=100 parametric points) and a function φ that minimizes the Rayleigh quotient R = ∫(φ'² + κ²φ²)/∫φ²; score = −R, maximize toward 0.

## Strategy hints

- The minimum of R over φ (for fixed curve) is the smallest eigenvalue of −d²/ds² + κ².
- For a fixed curve, compute the optimal φ as the eigenfunction corresponding to the smallest eigenvalue.
- Then optimize over the curve shape (varying curvature distribution κ(s)).
- A circle has constant curvature κ = 1/r — try elongated ellipses.
- Parameterize the curve as r(θ) in polar coordinates and optimize r(·).

## Output format

Check the evaluator to understand the exact list format. It likely expects either `[x_coords, y_coords]` or a flat list of 2n floats, or `[curve_x, curve_y, phi_values]`.

```python
import numpy as np

def solve(n: int = 100) -> list:
    # Circle of radius 1
    theta = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = np.cos(theta)
    y = np.sin(theta)
    phi = np.ones(n)  # constant eigenfunction for circle
    return [x.tolist(), y.tolist(), phi.tolist()]
```

## Pitfalls

- Non-convex curves may be rejected by the evaluator.
- The curve must close (endpoint connects to start).
- Very elongated ellipses may have high curvature at the tips, increasing R.

## Baseline

A unit circle with φ = 1 gives a moderate R. Ellipses with aspect ratio 2 can improve on this.
