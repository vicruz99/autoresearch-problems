"""Evaluator for the minimizing max/min distance problem in 2D with 16 points.

The candidate program's solve() function should return a numpy array of shape
(16, 2) containing the (x, y) coordinates of 16 points in 2D space.

The objective is to MAXIMIZE:
  (dmin / dmax)²
where dmin is the minimum pairwise distance and dmax is the maximum pairwise
distance between all point pairs.

Score: (dmin/dmax)² / BENCHMARK  (higher is better; > 1 means a new record)
BENCHMARK = 1 / 12.889266112  (found by AlphaEvolve)

Some of the code in this file is adapted from:
google-deepmind/alphaevolve_results (Apache License v2.0).

This file is standalone — it does NOT import from autoresearch_problems.
"""

import numpy as np

try:
    import scipy.spatial.distance as _spdist
    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False

NUM_POINTS = 16
DIMENSION = 2
BENCHMARK = 1.0 / 12.889266112


def _pdist(points: np.ndarray) -> np.ndarray:
    """Return pairwise distances; uses scipy if available, else pure numpy."""
    if _HAS_SCIPY:
        return _spdist.pdist(points)
    n = len(points)
    dists = []
    for i in range(n):
        for j in range(i + 1, n):
            dists.append(float(np.linalg.norm(points[i] - points[j])))
    return np.array(dists)


def evaluate(output, n: int = NUM_POINTS, d: int = DIMENSION, **kwargs) -> dict:
    """Score a candidate point arrangement.

    Parameters
    ----------
    output:
        A 2-D array-like of shape ``(n, d)`` with float entries.
    n:
        Expected number of points.
    d:
        Expected dimensionality.

    Returns
    -------
    dict
        score  : (dmin/dmax)² / BENCHMARK  (higher is better)
        valid  : True iff shape is correct and distances are finite
        error  : "" on success, description of first error otherwise
        metrics: dict with min_dist, max_dist, ratio_squared
    """
    try:
        try:
            points = np.asarray(output, dtype=float)
        except Exception as exc:
            return {"score": 0.0, "valid": False, "error": f"Cannot convert output to array: {exc}", "metrics": {}}

        if points.ndim != 2 or points.shape != (n, d):
            return {
                "score": 0.0,
                "valid": False,
                "error": f"Expected shape ({n}, {d}), got {points.shape}",
                "metrics": {},
            }

        if not np.isfinite(points).all():
            return {"score": 0.0, "valid": False, "error": "Points contain NaN or Inf values", "metrics": {}}

        pairwise_distances = _pdist(points)

        if len(pairwise_distances) == 0:
            return {"score": 0.0, "valid": False, "error": "No pairwise distances computed", "metrics": {}}

        min_distance = float(np.min(pairwise_distances))
        max_distance = float(np.max(pairwise_distances))

        if max_distance <= 0:
            inv_ratio_squared = 0.0
        else:
            inv_ratio_squared = (min_distance / max_distance) ** 2

        score = inv_ratio_squared / BENCHMARK if BENCHMARK > 0 else 0.0

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {
                "min_dist": min_distance,
                "max_dist": max_distance,
                "ratio_squared": inv_ratio_squared,
            },
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": f"Unexpected error: {exc}", "metrics": {}}
