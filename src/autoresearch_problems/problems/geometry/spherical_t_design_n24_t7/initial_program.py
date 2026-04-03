"""Initial solution for Spherical t-design: random points on sphere."""
import numpy as np


def solve() -> np.ndarray:
    """Return 24 random points on the unit sphere as initial t-design candidate."""
    # EVOLVE-BLOCK-START
    n = 24
    rng = np.random.default_rng(42)
    pts = rng.standard_normal((n, 3))
    pts /= np.linalg.norm(pts, axis=1, keepdims=True)
    return pts
    # EVOLVE-BLOCK-END
