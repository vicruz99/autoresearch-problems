"""Evaluator for the Kissing Number problem.

The kissing number K(d) is the maximum number of non-overlapping unit spheres
that can simultaneously touch a central unit sphere in d-dimensional Euclidean
space.  Known values: K(1)=2, K(2)=6, K(3)=12, K(4)=24, K(8)=240, K(24)=196560.

Each candidate kissing sphere is represented by its centre vector, which must
be at distance exactly 2 from the origin (unit radius + unit radius = touching)
and at distance >= 2 from every other candidate centre (non-overlapping).

We allow a small tolerance (1e-6) for floating-point precision.

This file is standalone and library-agnostic — it does NOT import from
autoresearch_problems.  The only dependency is numpy.
"""

import numpy as np

# Tolerance for distance checks
_TOL = 1e-6


def evaluate(output: object, d: int = 3, **kwargs) -> dict:
    """Score a candidate kissing number configuration.

    Parameters
    ----------
    output:
        A 2-D array-like of shape ``(k, d)`` where each row is the centre of a
        candidate kissing sphere.  Each centre must be at distance 2 from the
        origin and at pairwise distance >= 2 from all other centres.
    d:
        Dimension of the space.

    Returns
    -------
    dict
        ``score``   = number of valid kissing spheres (higher is better).
        ``valid``   = True iff all distance constraints are satisfied.
        ``error``   = description of the first violation found, or "".
        ``metrics`` = dict with ``num_spheres``, ``min_pairwise_dist``,
                      ``max_origin_dist_error``.
    """
    try:
        centres = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": f"Cannot convert output to array: {exc}", "metrics": {}}

    if centres.ndim != 2 or centres.shape[1] != d:
        return {
            "score": 0.0,
            "valid": False,
            "error": f"Expected shape (k, {d}), got {getattr(centres, 'shape', '?')}",
            "metrics": {},
        }

    k = centres.shape[0]
    if k == 0:
        return {"score": 0.0, "valid": True, "error": "", "metrics": {"num_spheres": 0}}

    # Check that each centre is at distance 2 from the origin
    origin_dists = np.sqrt((centres ** 2).sum(axis=1))
    dist_errors = np.abs(origin_dists - 2.0)
    max_dist_error = float(dist_errors.max())
    if max_dist_error > _TOL:
        worst = int(np.argmax(dist_errors))
        return {
            "score": 0.0,
            "valid": False,
            "error": (
                f"Centre {worst} is at distance {origin_dists[worst]:.6f} from origin "
                f"(expected 2.0 ± {_TOL})"
            ),
            "metrics": {"max_origin_dist_error": max_dist_error},
        }

    # Check pairwise distances >= 2 (non-overlapping)
    if k > 1:
        diff = centres[:, None, :] - centres[None, :, :]  # (k, k, d)
        pairwise = np.sqrt((diff ** 2).sum(axis=-1))       # (k, k)
        np.fill_diagonal(pairwise, np.inf)
        min_pairwise = float(pairwise.min())

        if min_pairwise < 2.0 - _TOL:
            idx = np.unravel_index(np.argmin(pairwise), pairwise.shape)
            return {
                "score": 0.0,
                "valid": False,
                "error": (
                    f"Spheres {idx[0]} and {idx[1]} overlap: "
                    f"centre distance {min_pairwise:.6f} < 2.0"
                ),
                "metrics": {"min_pairwise_dist": min_pairwise},
            }
    else:
        min_pairwise = float("inf")

    return {
        "score": float(k),
        "valid": True,
        "error": "",
        "metrics": {
            "num_spheres": k,
            "min_pairwise_dist": min_pairwise,
            "max_origin_dist_error": max_dist_error,
        },
    }
