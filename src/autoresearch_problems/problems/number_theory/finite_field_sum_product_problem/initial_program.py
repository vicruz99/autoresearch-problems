# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
import math
import numpy as np


def solve(p: int = 1009) -> np.ndarray:
    """Construct a set X ⊆ F_p of size ⌊√p⌋ minimising max(|X+X|, |X·X|).

    Returns
    -------
    np.ndarray of shape (k,) with k = floor(sqrt(p)), dtype int64,
    containing k distinct elements from {0, …, p-1}.
    """
    # EVOLVE-BLOCK-START
    size = int(math.sqrt(p))
    # Baseline: arithmetic progression {0, 1, …, k-1}
    # This has small sum set (|X+X| = 2k-1) but large product set.
    # The challenge is to keep BOTH sum and product sets small.
    x = np.arange(size, dtype=np.int64)
    # EVOLVE-BLOCK-END

    return x
