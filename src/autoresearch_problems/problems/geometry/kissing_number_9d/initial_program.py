"""Baseline solver for the Kissing Number problem in dimension 9.

Returns a trivially valid configuration.  The goal is to evolve this into
a construction achieving as many kissing points as possible (best known: 306).
"""
import numpy as np


def solve(dimension: int = 9) -> np.ndarray:
    """Return a set C ⊂ R^dimension certifying a kissing configuration.

    The returned array has shape (n, dimension).  The kissing constraint is:
        min_{x≠y} ||x-y|| >= max_x ||x||
    and 0 ∉ C.  The score is n (the number of points).
    """
    # Trivial valid configuration: two antipodal points along first axis
    # This certifies a kissing number of at least 2.
    points = np.zeros((2, dimension), dtype=int)
    points[0, 0] = 1
    points[1, 0] = -1
    return points
