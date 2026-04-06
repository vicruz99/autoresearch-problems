"""Seed solution for the Finite Field Kakeya problem."""

import itertools

import numpy as np


def _saraf_sudan_construction(p: int, d: int) -> np.ndarray:
    """Return the Saraf-Sudan Kakeya set in F_p^d as an integer array."""
    if p == 2:
        pts = list(itertools.product(range(p), repeat=d))
        return np.array(pts, dtype=np.int64)

    squares = {pow(i, 2, p) for i in range(p)}
    final_set: set = set()

    for beta in range(p):
        beta_sq = (beta * beta) % p
        for s_tuple in itertools.product(squares, repeat=d - 1):
            point = tuple((s - beta_sq) % p for s in s_tuple) + (beta,)
            final_set.add(point)

    for coords in itertools.product(range(p), repeat=d - 1):
        final_set.add(coords + (0,))

    return np.array(sorted(final_set), dtype=np.int64)


def solve(d: int = 3, primes=None) -> dict:
    """Return Saraf-Sudan Kakeya sets for each prime in *primes*.

    Parameters
    ----------
    d:
        Dimension of F_p^d.
    primes:
        List of prime integers to construct sets for.  Defaults to [3, 5, 7, 11].

    Returns
    -------
    dict
        Maps each prime p to a 2-D int64 array of shape (k, d) with entries in
        {0, …, p-1} representing a valid Kakeya set for F_p^d.
    """
    if primes is None:
        primes = [3, 5, 7, 11]

    # EVOLVE-BLOCK-START
    result = {}
    for p in primes:
        result[p] = _saraf_sudan_construction(p, d)
    # EVOLVE-BLOCK-END

    return result
