"""Naive greedy seed solution for the Cap Set problem in F_3^8."""

import itertools

import numpy as np


def solve() -> np.ndarray:
    """Greedy cap-set construction in F_3^8.

    Iterates over all 3^8 = 6561 vectors and greedily adds each one to the
    set if it does not create a three-term arithmetic progression with any
    two existing elements.
    """
    n = 8
    q = 3
    cap: list[tuple[int, ...]] = []
    cap_set: set[tuple[int, ...]] = set()

    for vec in itertools.product(range(q), repeat=n):
        # Check if adding vec creates a progression with any pair in cap_set
        ok = True
        for existing in cap:
            # third element z such that existing + vec + z ≡ 0 (mod q)
            z = tuple((-(existing[d] + vec[d])) % q for d in range(n))
            if z in cap_set:
                ok = False
                break
        if ok:
            cap.append(vec)
            cap_set.add(vec)

    return np.array(cap, dtype=int)
