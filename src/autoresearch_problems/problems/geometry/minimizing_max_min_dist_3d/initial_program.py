import numpy as np


def solve() -> np.ndarray:
    """Place 14 points in 3D to maximize the ratio of minimum to maximum distance.

    Returns
    -------
    np.ndarray of shape (14, 3)
    """
    n = 14
    d = 3
    np.random.seed(42)
    points = np.random.randn(n, d)
    return points
