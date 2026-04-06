# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
import math
import numpy as np


def solve(primes=None) -> dict:
    """Construct sets X ⊆ F_p of size ⌊√p⌋ minimising max(|X+X|, |X·X|).

    Parameters
    ----------
    primes:
        List of prime integers.  Defaults to [101, 257, 1009].

    Returns
    -------
    dict
        Maps each prime p to a 1-D int64 array of length floor(sqrt(p)) with
        distinct elements from {0, …, p-1}.
    """
    if primes is None:
        primes = [101, 257, 1009]

    # EVOLVE-BLOCK-START
    result = {}
    for p in primes:
        size = int(math.sqrt(p))
        # Baseline: arithmetic progression {0, 1, …, k-1}
        # This has small sum set (|X+X| = 2k-1) but large product set.
        # The challenge is to keep BOTH sum and product sets small.
        result[p] = np.arange(size, dtype=np.int64)
    # EVOLVE-BLOCK-END

    return result
