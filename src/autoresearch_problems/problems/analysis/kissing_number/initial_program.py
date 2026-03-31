"""Initial program for the Kissing Number problem (d=3).

Places 12 unit spheres touching a central unit sphere using the vertices of a
regular icosahedron scaled to the sphere of radius 2.

The known kissing number in 3D is exactly 12.
"""

import numpy as np


def solve():
    """Return a (12, 3) array of kissing-sphere centres for d=3.

    Each centre is at distance 2 from the origin (touching the central sphere)
    and at distance >= 2 from every other centre (non-overlapping).
    """
    phi = (1.0 + np.sqrt(5.0)) / 2.0  # golden ratio

    # 12 vertices of a regular icosahedron (un-normalised)
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

    # Normalise to the sphere of radius 2
    norms = np.linalg.norm(vertices, axis=1, keepdims=True)
    centres = 2.0 * vertices / norms
    return centres
