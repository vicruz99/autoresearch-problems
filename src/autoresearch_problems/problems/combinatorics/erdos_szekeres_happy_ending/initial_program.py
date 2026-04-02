"""Seed solution for the Erdős–Szekeres Happy Ending problem."""

import numpy as np


def solve(n: int = 6) -> np.ndarray:
    """Return 2^(n-2)+1 points in convex position as a baseline.

    Points in convex position (e.g. on a circle) maximise the number of
    convex n-gons (every n-subset forms a convex n-gon), so this scores
    very poorly.  A good solution would cluster points to avoid forming
    convex n-gons.
    """
    required = 2 ** (n - 2) + 1

    # EVOLVE-BLOCK-START
    # Arrange points in a regular polygon (convex position).
    # This gives many convex n-gons but is always in general position.
    angles = np.linspace(0, 2 * np.pi, required, endpoint=False)
    # Add a small perturbation so no three points are collinear.
    rng = np.random.default_rng(42)
    radii = 1.0 + rng.uniform(-1e-4, 1e-4, size=required)
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    points = np.column_stack([x, y])
    # EVOLVE-BLOCK-END
    return points
