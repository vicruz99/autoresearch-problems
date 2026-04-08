"""Initial program for the Kissing Number problem (d=3).

Returns the 12 vertices of a regular icosahedron.  These already satisfy the
set-C lemma since all vertices have equal norm and the minimum pairwise distance
equals the edge length, which equals the norm.

The known kissing number in 3D is exactly 12 (proved 1953).
"""

import numpy as np


def solve(dimension: int = 3) -> np.ndarray:
    """Return a (12, 3) array certifying a kissing number of 12 for d=3.

    The returned points satisfy: min_{x≠y} ||x-y|| >= max_x ||x||.
    """
    phi = (1.0 + np.sqrt(5.0)) / 2.0  # golden ratio

    # 12 vertices of a regular icosahedron (un-normalised)
    # All vertices have norm sqrt(1 + phi^2) = sqrt(1 + phi^2)
    # Edge length equals norm, so the set-C lemma is satisfied with margin = 0.
    vertices = np.array([
        [ 0,  1,  phi],
        [ 0, -1,  phi],
        [ 0,  1, -phi],
        [ 0, -1, -phi],
        [ 1,  phi,  0],
        [-1,  phi,  0],
        [ 1, -phi,  0],
        [-1, -phi,  0],
        [ phi,  0,  1],
        [-phi,  0,  1],
        [ phi,  0, -1],
        [-phi,  0, -1],
    ], dtype=float)

    return vertices
