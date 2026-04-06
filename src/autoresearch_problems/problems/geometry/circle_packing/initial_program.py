"""Naive grid seed solution for the Circle Packing problem."""

import numpy as np


def solve(n: int = 26, **kwargs) -> np.ndarray:
    """Place n circles on a near-square grid inside [0, 1]^2."""
    n = int(n)
    cols = int(np.ceil(np.sqrt(n)))
    rows = int(np.ceil(n / cols))

    xs = np.linspace(0.0, 1.0, cols)
    ys = np.linspace(0.0, 1.0, rows)
    grid = np.array([[x, y] for y in ys for x in xs])

    # Take only the first n points
    return grid[:n].astype(float)
