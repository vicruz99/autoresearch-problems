"""Evaluator for the Circle Packing problem.

Given n centres in the unit square [0,1]^2, the score is the minimum pairwise
Euclidean distance between any two centres.  All centres must lie strictly
inside [0,1]^2 (boundary inclusive).
"""

from __future__ import annotations

import numpy as np

from autoresearch_problems.core.result import EvalResult


def evaluate(output: object, *, n: int = 26) -> EvalResult:
    """Score a candidate circle packing.

    Parameters
    ----------
    output:
        A 2-D array-like of shape ``(n, 2)`` with float entries in ``[0, 1]``.
    n:
        Expected number of circles.

    Returns
    -------
    EvalResult
        ``score`` = minimum pairwise distance (higher is better).
        ``valid`` = True iff all centres are in [0,1]^2 and count == n.
    """
    try:
        centres = np.asarray(output, dtype=float)
    except Exception as exc:
        return EvalResult(score=0.0, valid=False, error=f"Cannot convert output to array: {exc}")

    if centres.ndim != 2 or centres.shape != (n, 2):
        return EvalResult(
            score=0.0,
            valid=False,
            error=f"Expected shape ({n}, 2), got {centres.shape}",
        )

    if np.any(centres < 0.0) or np.any(centres > 1.0):
        return EvalResult(
            score=0.0,
            valid=False,
            error="All centres must be in [0, 1]^2",
        )

    # Compute all pairwise distances
    diff = centres[:, None, :] - centres[None, :, :]  # (n, n, 2)
    dist = np.sqrt((diff ** 2).sum(axis=-1))           # (n, n)

    # Mask diagonal (distance to self = 0)
    np.fill_diagonal(dist, np.inf)
    min_dist = float(dist.min())

    return EvalResult(
        score=min_dist,
        valid=True,
        metrics={"min_pairwise_distance": min_dist},
    )
