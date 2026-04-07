# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
import itertools
import numpy as np


def _find_non_square(p: int) -> int:
    for k in range(2, p):
        if pow(k, (p - 1) // 2, p) == p - 1:
            return k
    raise ValueError(f"No non-square for p={p}")


def _construct_nikodym(p: int) -> np.ndarray:
    """Build a Nikodym set in F_{p^2}^2 using the Unital-minus-BlockingSet method."""
    w = _find_non_square(p)

    class Fq:
        __slots__ = ("a", "b")

        def __init__(self, a, b):
            self.a = int(a) % p
            self.b = int(b) % p

        def __add__(self, o):
            return Fq(self.a + o.a, self.b + o.b)

        def __mul__(self, o):
            return Fq(self.a * o.a + self.b * o.b * w,
                      self.a * o.b + self.b * o.a)

        def __eq__(self, o):
            return self.a == o.a and self.b == o.b

        def __hash__(self):
            return hash((self.a, self.b))

        def is_zero(self):
            return self.a == 0 and self.b == 0

    def trace(x: Fq) -> Fq:
        return Fq(2 * x.a, 0)

    def norm(x: Fq) -> Fq:
        return Fq(x.a * x.a - x.b * x.b * w, 0)

    all_fq = [Fq(a, b) for a in range(p) for b in range(p)]

    unital = set()
    for x in all_fq:
        for y in all_fq:
            if (trace(x) + norm(y)).is_zero():
                unital.add((x, y))

    alpha = Fq(0, 1)
    Y_special = set()
    for u in range(p):
        for v in range(p):
            Y_special.add(Fq(pow(u, 2, p), v))

    blocking = {(x, y) for x, y in unital if y in Y_special}
    excluded = unital - blocking
    all_points = set(itertools.product(all_fq, repeat=2))
    nikodym = all_points - excluded

    k = len(nikodym)
    result = np.zeros((k, 2, 2), dtype=np.int64)
    for i, (x, y) in enumerate(nikodym):
        result[i, 0, 0] = x.a
        result[i, 0, 1] = x.b
        result[i, 1, 0] = y.a
        result[i, 1, 1] = y.b
    return result


def solve(d: int = 2, primes=None) -> dict:
    """Return Nikodym sets in F_{p^2}^2 for each prime in *primes*.

    Parameters
    ----------
    d:
        Dimension (must be 2).
    primes:
        List of prime integers.  Defaults to [3, 5].

    Returns
    -------
    dict
        Maps each prime p to a 3-D int64 array of shape (k, 2, 2) with values
        in {0, …, p-1} representing a valid Nikodym set for F_{p^2}^2.
    """
    if primes is None:
        primes = [3, 5]

    # EVOLVE-BLOCK-START
    result = {}
    for p in primes:
        result[p] = _construct_nikodym(p)
    # EVOLVE-BLOCK-END

    return result
