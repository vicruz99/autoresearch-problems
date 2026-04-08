# Agent Guide — Kakeya Needle 2D

## Goal

Return a numpy array of shape `(32,)` representing x-offsets for 32 triangles that minimize total union area; score = −area/reference, maximize toward 0.

## Strategy hints

- The key insight: triangles should overlap as much as possible.
- The Besicovitch construction: organize triangles so they share a large common region.
- A known good strategy is to arrange triangle bases to cluster around a few x-positions rather than spreading them out.
- Gradient information is not directly available (area is computed by polygon union); use random search or evolutionary strategies.
- Start from the Keich construction (evenly spaced offsets) and then optimize.

## Output format

Return a 1D `np.ndarray` of shape `(32,)` representing x-coordinates of triangle base offsets.

```python
import numpy as np

def solve(n: int = 32) -> np.ndarray:
    # Keich construction: positions folded toward center
    x = np.zeros(n)
    for i in range(n):
        x[i] = -i / (2 * n)  # fold triangles leftward
    return x
```

## Pitfalls

- Very large x-values spread the triangles out, maximizing area (worst score).
- The union area computation via Shapely can be slow for n=32 — keep calls to a minimum.
- The score is relative to a reference, not absolute area.

## Baseline

Uniformly spaced x-offsets (x_i = i/n) give area close to the reference (score ≈ −1.0). Compressing offsets toward 0 reduces area significantly.
