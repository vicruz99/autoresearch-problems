"""Evaluator for the Kissing Number problem in dimension 3.

The kissing number C(n) is the maximum number of non-overlapping unit spheres
that can simultaneously touch a central unit sphere in n-dimensional space.

Equivalently (by a standard lemma), a valid kissing configuration of size |C|
is certified by a set C ⊂ R^n with 0 ∉ C satisfying:
    min_{x ≠ y ∈ C} ||x - y||  ≥  max_{x ∈ C} ||x||.

The score is the number of valid points |C|.  Higher is better.

The exact value K(3) = 12 was proved in 1953.

Adapted from the AlphaEvolve "Mathematical Exploration and Discovery at Scale"
paper (Problem 6.8, Section 6.4) and the google-deepmind/alphaevolve_repository_of_problems.
"""
import math
import numpy as np
import scipy.spatial.distance as spdist

# Known upper bound for dimension 3 (exact: K(3) = 12)
_UPPER_BOUND = 12


def evaluate(output: object, dimension: int = 3, **kwargs) -> dict:
    """Score a candidate kissing number configuration.

    Parameters
    ----------
    output : array-like of shape (n, dimension)
        A set C of n points in R^dimension.  Each row is a point.
        May be integer or float dtype.
    dimension : int
        The dimension of the space (default 3).

    Returns
    -------
    dict with keys: score, valid, error, metrics.
        score = |C| if the configuration is valid, else 0.
    """
    try:
        points = np.asarray(output)
    except Exception as exc:
        return {"score": 0.0, "valid": False,
                "error": f"Cannot convert output to array: {exc}",
                "metrics": {}}

    # --- Shape validation ---
    if points.ndim != 2 or points.shape[1] != dimension:
        return {"score": 0.0, "valid": False,
                "error": f"Expected shape (n, {dimension}), got {points.shape}",
                "metrics": {}}

    n = points.shape[0]
    if n < 2:
        return {"score": 0.0, "valid": False,
                "error": "Need at least 2 points",
                "metrics": {}}

    if not np.all(np.isfinite(points)):
        return {"score": 0.0, "valid": False,
                "error": "Non-finite values in input",
                "metrics": {}}

    # Reject configurations exceeding the known upper bound
    if n > _UPPER_BOUND:
        return {"score": 0.0, "valid": False,
                "error": f"Number of points ({n}) exceeds known upper bound ({_UPPER_BOUND})",
                "metrics": {}}

    # --- Check 0 ∉ C (no zero vectors) ---
    norms_raw = np.linalg.norm(points.astype(float), axis=1)
    if np.any(norms_raw == 0.0):
        return {"score": 0.0, "valid": False,
                "error": "Zero vector present in C (0 must not be in C)",
                "metrics": {}}

    # --- Check kissing constraint ---
    is_int = np.issubdtype(points.dtype, np.integer)

    if is_int:
        # Exact integer arithmetic path: compare squared quantities as Python ints
        P = points.astype(object)
        max_norm_sq = 0
        for i in range(n):
            n2 = int(np.dot(P[i], P[i]))
            if n2 == 0:
                return {"score": 0.0, "valid": False,
                        "error": "Zero vector present in C",
                        "metrics": {}}
            if n2 > max_norm_sq:
                max_norm_sq = n2

        min_dist_sq = None
        for i in range(n - 1):
            vi = P[i]
            for j in range(i + 1, n):
                diff = vi - P[j]
                d2 = int(np.dot(diff, diff))
                if min_dist_sq is None or d2 < min_dist_sq:
                    min_dist_sq = d2

        if min_dist_sq is None or min_dist_sq < max_norm_sq:
            return {"score": 0.0, "valid": False,
                    "error": ("Kissing constraint violated (integer-exact): "
                              f"min_dist²={min_dist_sq}, max_norm²={max_norm_sq}"),
                    "metrics": {
                        "mode": "integer-exact",
                        "min_pairwise_distance_squared": int(min_dist_sq) if min_dist_sq else 0,
                        "max_norm_squared": int(max_norm_sq),
                    }}

        min_dist = math.sqrt(float(min_dist_sq))
        max_norm = math.sqrt(float(max_norm_sq))
        margin = float(min_dist - max_norm)
        extra = {
            "mode": "integer-exact",
            "min_pairwise_distance_squared": int(min_dist_sq),
            "max_norm_squared": int(max_norm_sq),
            "margin_squared": int(min_dist_sq - max_norm_sq),
        }
    else:
        # Floating-point path using scipy for efficiency
        pts_f = points.astype(float)
        dists = spdist.pdist(pts_f)
        norms = np.linalg.norm(pts_f, axis=1)

        min_dist = float(dists.min())
        max_norm = float(norms.max())
        margin = min_dist - max_norm

        # Use a small tolerance for floating point
        if margin < -1e-9:
            return {"score": 0.0, "valid": False,
                    "error": ("Kissing constraint violated (float): "
                              f"min_dist={min_dist:.12f}, max_norm={max_norm:.12f}, "
                              f"margin={margin:.2e}"),
                    "metrics": {
                        "mode": "float",
                        "min_pairwise_distance": min_dist,
                        "max_norm": max_norm,
                        "margin": margin,
                    }}

        extra = {"mode": "float"}

    kissing_count = n
    return {
        "score": float(kissing_count),
        "valid": True,
        "error": "",
        "metrics": {
            "kissing_count": kissing_count,
            "dimension": dimension,
            "min_pairwise_distance": float(min_dist),
            "max_norm": float(max_norm),
            "margin": float(margin),
            **extra,
        },
    }
