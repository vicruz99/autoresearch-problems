# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the Flat Polynomials / Golay's conjecture problem.

The candidate program's solve() function should return a 1-D array-like of
length n containing ±1 coefficients  [c_1, c_2, …, c_n]  for the polynomial
    g(z) = c_1·z + c_2·z² + … + c_n·z^n.

The objective is to MINIMISE
    score = max_{|z|=1} |g(z)| / √(n+1)
where the maximum is approximated by sampling 100 000 equally-spaced points
on the unit circle.

This file is standalone — it does NOT import from autoresearch_problems.
"""

import numpy as np

_DEFAULT_N = 64
_NUM_SAMPLE_POINTS = 100_000


def _c_plus_score(coefficients: np.ndarray) -> float:
    """Return max|g(z)| / sqrt(n+1) sampled over the unit circle."""
    n = len(coefficients)
    zs = np.exp(1j * np.linspace(0, 2 * np.pi, _NUM_SAMPLE_POINTS, endpoint=False))
    # g(z) = sum_{k=1}^{n} c_k * z^k  — evaluate via Horner-like numpy poly
    # np.poly1d expects highest-degree coefficient first; our array is [c_1,...,c_n]
    # g(z) = z * (c_1 + z*(c_2 + ... + z*c_n)) = np.polyval([c_n,...,c_1,0], z)
    poly_coeffs = np.concatenate([coefficients[::-1], [0.0]])  # [c_n,...,c_1,0]
    vals = np.polyval(poly_coeffs, zs)
    return float(np.max(np.abs(vals))) / np.sqrt(n + 1)


def evaluate(output, n: int = _DEFAULT_N, **kwargs) -> dict:
    """Score a candidate coefficient sequence.

    Parameters
    ----------
    output:
        A 1-D array-like of length *n* with entries in {+1, −1}.
    n:
        Expected number of coefficients (from spec parameters).

    Returns
    -------
    dict
        score   : max|g(z)|/√(n+1)  – **lower is better**
        valid   : True iff the array has the right shape and ±1 entries
        error   : "" on success, description of first problem otherwise
        metrics : dict with raw_max_abs, n_used
    """
    try:
        try:
            coeffs = np.asarray(output, dtype=float)
        except Exception as exc:
            return {
                "score": float("inf"),
                "valid": False,
                "error": f"Cannot convert output to array: {exc}",
                "metrics": {},
            }

        coeffs = coeffs.ravel()

        if coeffs.shape[0] != n:
            return {
                "score": float("inf"),
                "valid": False,
                "error": f"Expected {n} coefficients, got {coeffs.shape[0]}",
                "metrics": {},
            }

        if not np.isfinite(coeffs).all():
            return {
                "score": float("inf"),
                "valid": False,
                "error": "Coefficients contain NaN or Inf",
                "metrics": {},
            }

        # Coefficients must be ±1 (allow a small tolerance for float representations)
        if not np.allclose(np.abs(coeffs), 1.0, atol=1e-6):
            return {
                "score": float("inf"),
                "valid": False,
                "error": "Coefficients must all be +1 or -1",
                "metrics": {},
            }

        # Snap to exact ±1
        coeffs = np.sign(coeffs)

        raw_score = _c_plus_score(coeffs)
        raw_max_abs = raw_score * np.sqrt(n + 1)

        return {
            "score": raw_score,
            "valid": True,
            "error": "",
            "metrics": {
                "raw_max_abs": raw_max_abs,
                "n_used": n,
            },
        }

    except Exception as exc:
        return {
            "score": float("inf"),
            "valid": False,
            "error": f"Unexpected error: {exc}",
            "metrics": {},
        }
