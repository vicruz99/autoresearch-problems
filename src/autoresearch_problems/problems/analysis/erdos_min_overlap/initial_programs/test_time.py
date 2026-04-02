import numpy as np


def solve():
    """Construct step-function h with low C5 bound."""
    rng = np.random.default_rng()
    n_points = rng.integers(40, 100)
    h_values = np.full(n_points, rng.random())
    # Normalize so sum(h) * dx == 1, i.e. sum(h) == n_points / 2
    h_values = h_values * (n_points / 2.0 / np.sum(h_values))
    h_values = np.clip(h_values, 0.0, 1.0)
    return h_values
