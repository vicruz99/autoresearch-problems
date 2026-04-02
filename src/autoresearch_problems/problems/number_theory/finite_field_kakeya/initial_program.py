"""Seed solution for the Finite Field Kakeya problem."""

import itertools

import numpy as np


def solve(p: int = 3, d: int = 3) -> np.ndarray:
    """Return a Saraf-Sudan-style Kakeya set in F_p^d as the baseline.

    The Saraf-Sudan / Dvir construction is:
      K = { (a_1, …, a_{d-1}, beta) | a_i + beta^2 is a quadratic residue }
          ∪ { F_p^(d-1) × {0} }

    This is a valid Kakeya set of size roughly p^d / 2 for odd p.
    """
    # EVOLVE-BLOCK-START
    if p % 2 == 0:
        # Fallback for even p: return the full space
        pts = list(itertools.product(range(p), repeat=d))
        return np.array(pts, dtype=np.int64)

    squares = {pow(i, 2, p) for i in range(p)}
    final_set: set = set()

    for beta in range(p):
        beta_sq = (beta * beta) % p
        for s_tuple in itertools.product(squares, repeat=d - 1):
            point = tuple((s - beta_sq) % p for s in s_tuple) + (beta,)
            final_set.add(point)

    # Add the hyperplane F_p^(d-1) × {0}
    for coords in itertools.product(range(p), repeat=d - 1):
        final_set.add(coords + (0,))

    # EVOLVE-BLOCK-END
    return np.array(sorted(final_set), dtype=np.int64)
