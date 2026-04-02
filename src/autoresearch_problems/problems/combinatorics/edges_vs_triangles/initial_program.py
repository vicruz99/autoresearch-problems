import numpy as np

N = 20  # vector length (must match evaluator parameter n)


def solve() -> np.ndarray:
    """Return a set of probability vectors tracing the edges-vs-triangles curve.

    Each row of the returned array is a non-negative vector of length N=20.
    Rows are normalised to sum to 1 before scoring.

    For a vector v the edge density = sum_{i<j} v_i*v_j and the triangle
    density = sum_{i<j<k} v_i*v_j*v_k.  The goal is to find rows whose
    (edge, triangle) pairs densely cover the theoretical boundary curve,
    minimising area + 10 * max_gap.

    Score = (5/6) / (area + 10 * max_gap); higher is better.

    Returns
    -------
    np.ndarray of shape (M, N) with M ≥ 1.
    """
    # EVOLVE-BLOCK-START
    # Use k equal-weight elements for k = 1, ..., N.
    # Edge density for k equal weights: (k-1)/(2k).
    # This covers the range 0 to ~0.475 but gaps are large for small k.
    solutions = []
    for k in range(1, N + 1):
        v = np.zeros(N, dtype=float)
        v[:k] = 1.0 / k
        solutions.append(v)
    # EVOLVE-BLOCK-END

    return np.array(solutions)
