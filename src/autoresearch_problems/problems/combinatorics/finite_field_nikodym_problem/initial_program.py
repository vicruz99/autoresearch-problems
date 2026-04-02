# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
import itertools
import numpy as np


def _find_non_square(p: int) -> int:
    for k in range(2, p):
        if pow(k, (p - 1) // 2, p) == p - 1:
            return k
    raise ValueError(f"No non-square for p={p}")


def solve(p: int = 5, d: int = 2) -> np.ndarray:
    """Construct a Nikodym set in F_{p^2}^2 and return it as shape (k,2,2).

    Returns
    -------
    np.ndarray of shape (k, 2, 2), dtype int64
        Each row [[xa,xb],[ya,yb]] is a point in F_{p^2}^2.
    """
    # EVOLVE-BLOCK-START
    if d != 2:
        return np.zeros((0, d, 2), dtype=np.int64)

    # Find a non-square element w for F_q = F_{p^2} = F_p[α]/(α²−w)
    w = _find_non_square(p)

    class Fq:
        """Element of F_q = F_p[α] / (α² − w)."""
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

    # All elements of F_q
    all_fq = [Fq(a, b) for a in range(p) for b in range(p)]

    # Build Unital U: {(x,y) ∈ F_q^2 : Trace(x) + Norm(y) = 0}
    unital = set()
    for x in all_fq:
        for y in all_fq:
            if (trace(x) + norm(y)).is_zero():
                unital.add((x, y))

    # Build Y_special: {u^2 + v·α : u,v ∈ F_p}
    alpha = Fq(0, 1)
    Y_special = set()
    for u in range(p):
        for v in range(p):
            Y_special.add(Fq(pow(u, 2, p), v))

    # Blocking set B ⊆ U: points whose y-coordinate is in Y_special
    blocking = {(x, y) for x, y in unital if y in Y_special}

    # Excluded set S = U \ B;  Nikodym set N = all_points \ S
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
    # EVOLVE-BLOCK-END

    return result
