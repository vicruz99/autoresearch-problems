"""Evaluator for the Circle Packing problem.

Given n centres in the unit square [0,1]^2, the score is the minimum pairwise
Euclidean distance between any two centres.  All centres must lie strictly
inside [0,1]^2 (boundary inclusive).

This file is standalone and library-agnostic — it does NOT import from
autoresearch_problems.  The only dependency is numpy.
"""

import numpy as np


def evaluate(output: object, n: int = 26, **kwargs) -> dict:
    """Score a candidate circle packing.

    Parameters
    ----------
    output:
        A 2-D array-like of shape ``(n, 2)`` with float entries in ``[0, 1]``.
    n:
        Expected number of circles.

    Returns
    -------
    dict
        ``score`` = minimum pairwise distance (higher is better).
        ``valid`` = True iff all centres are in [0,1]^2 and count == n.
        ``error`` = description of the first error found, or empty string.
        ``metrics`` = dict with extra info (e.g. ``min_pairwise_distance``).
    """
    try:
        centres = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": f"Cannot convert output to array: {exc}", "metrics": {}}

    if centres.ndim != 2 or centres.shape != (n, 2):
        return {
            "score": 0.0,
            "valid": False,
            "error": f"Expected shape ({n}, 2), got {centres.shape}",
            "metrics": {},
        }

    if np.any(centres < 0.0) or np.any(centres > 1.0):
        return {
            "score": 0.0,
            "valid": False,
            "error": "All centres must be in [0, 1]^2",
            "metrics": {},
        }

    # Compute all pairwise distances
    diff = centres[:, None, :] - centres[None, :, :]  # (n, n, 2)
    dist = np.sqrt((diff ** 2).sum(axis=-1))           # (n, n)

    # Mask diagonal (distance to self = 0)
    np.fill_diagonal(dist, np.inf)
    min_dist = float(dist.min())

    return {
        "score": min_dist,
        "valid": True,
        "error": "",
        "metrics": {"min_pairwise_distance": min_dist},
    }
