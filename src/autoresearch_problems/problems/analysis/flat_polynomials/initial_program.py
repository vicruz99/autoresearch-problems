# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
import time
import numpy as np


def _c_plus_score(coefficients: np.ndarray) -> float:
    """Return max|g(z)| / sqrt(n+1) sampled over 100 000 unit-circle points."""
    n = len(coefficients)
    zs = np.exp(1j * np.linspace(0, 2 * np.pi, 100_000, endpoint=False))
    poly_coeffs = np.concatenate([coefficients[::-1], [0.0]])
    vals = np.polyval(poly_coeffs, zs)
    return float(np.max(np.abs(vals))) / np.sqrt(n + 1)


def solve(n: int = 64) -> np.ndarray:
    """Return n ±1 coefficients minimising max|g(z)|/√(n+1).

    Returns
    -------
    np.ndarray of shape (n,) with entries in {+1, -1}
    """
    # EVOLVE-BLOCK-START
    best_coefficients = np.ones(n)
    curr_coefficients = best_coefficients.copy()
    best_score = _c_plus_score(best_coefficients)

    start_time = time.time()
    while time.time() - start_time < 55:
        random_index = np.random.randint(0, n)
        curr_coefficients[random_index:] *= -1
        curr_score = _c_plus_score(curr_coefficients)
        if curr_score < best_score:
            best_score = curr_score
            best_coefficients = curr_coefficients.copy()
    # EVOLVE-BLOCK-END

    return best_coefficients
