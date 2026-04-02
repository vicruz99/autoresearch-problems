import numpy as np


def solve() -> np.ndarray:
    """Place 16 points in 2D to maximize the ratio of minimum to maximum distance.

    Returns
    -------
    np.ndarray of shape (16, 2)
    """
    n = 16
    d = 2
    np.random.seed(42)
    points = np.random.randn(n, d)
    return points
