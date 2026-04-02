"""Random initialization for Thomson problem with n=32."""
import numpy as np


def solve() -> np.ndarray:
    """Place 32 points randomly on the unit sphere."""
    # EVOLVE-BLOCK-START
    n = 32
    rng = np.random.default_rng(42)
    pts = rng.standard_normal((n, 3))
    pts /= np.linalg.norm(pts, axis=1, keepdims=True)
    return pts
    # EVOLVE-BLOCK-END
