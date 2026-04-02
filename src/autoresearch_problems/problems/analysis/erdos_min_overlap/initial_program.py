import numpy as np


def solve():
    """Construct a step function h that minimizes the Erdős C5 overlap constant.

    Returns a 1-D numpy array of n values in [0, 1] with sum * (2/n) ≈ 1.
    """
    rng = np.random.default_rng()
    n_points = rng.integers(40, 100)
    h_values = np.full(n_points, rng.random())
    # Normalize so integral == 1: sum(h) * dx == 1, dx = 2/n → sum(h) == n/2
    h_values = h_values * (n_points / 2.0 / np.sum(h_values))
    h_values = np.clip(h_values, 0.0, 1.0)
    return h_values
