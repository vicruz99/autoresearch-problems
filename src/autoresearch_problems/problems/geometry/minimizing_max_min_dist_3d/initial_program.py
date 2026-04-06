import numpy as np


def solve(n: int = 14, d: int = 3, **kwargs) -> np.ndarray:
    """Place n points in d-dimensional space to maximize the ratio of minimum to maximum distance.

    Returns
    -------
    np.ndarray of shape (n, d)
    """
    n = int(n)
    d = int(d)
    np.random.seed(42)
    points = np.random.randn(n, d)
    return points
