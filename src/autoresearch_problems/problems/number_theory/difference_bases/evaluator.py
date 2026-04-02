# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the difference bases problem.

The candidate solve() function returns a list (or array) of non-negative
integers B such that every positive integer up to k can be expressed as a
difference b_i - b_j (b_i > b_j) for some b_i, b_j in B.

Score = k / n²  where n = |B| and k is the largest integer consecutively
covered by differences of B.  Higher scores mean better efficiency.

The theoretical bound (Rohrbach) says n²/k → 2 as k → ∞, so k/n² ≤ 0.5
asymptotically.
"""

import numpy as np


def evaluate(output, **kwargs) -> dict:
    """Score a difference-basis candidate.

    Parameters
    ----------
    output:
        An iterable of non-negative integers forming the candidate set B.
        0 is added automatically if not present.

    Returns
    -------
    dict with keys: score (float), valid (bool), error (str), metrics (dict).
    """
    try:
        # Convert to a sorted list of unique non-negative ints
        raw: list[int] = []
        for x in output:
            try:
                val = int(x)
            except (TypeError, ValueError) as exc:
                return {"score": 0.0, "valid": False,
                        "error": f"Invalid element {x!r}: {exc}", "metrics": {}}
            if np.isnan(float(val)) or np.isinf(float(val)):
                return {"score": 0.0, "valid": False,
                        "error": f"Non-finite element: {x}", "metrics": {}}
            raw.append(val)

        b_list = sorted(set(raw))

        if not b_list:
            return {"score": 0.0, "valid": False,
                    "error": "Empty set", "metrics": {}}

        if min(b_list) < 0:
            return {"score": 0.0, "valid": False,
                    "error": "Set contains negative integers", "metrics": {}}

        if len(b_list) > 10_000:
            return {"score": 0.0, "valid": False,
                    "error": f"Set too large: {len(b_list)} > 10,000",
                    "metrics": {}}

        n = len(b_list)

        if n < 2:
            return {"score": 0.0, "valid": True,
                    "error": "Need at least 2 elements to form differences",
                    "metrics": {"n": n, "k": 0, "score": 0.0}}

        # Compute all positive pairwise differences
        differences: set[int] = set()
        for i in range(n):
            for j in range(i + 1, n):
                differences.add(b_list[j] - b_list[i])

        if not differences:
            return {"score": 0.0, "valid": True,
                    "error": "No differences computed", "metrics": {"n": n, "k": 0}}

        max_diff = max(differences)

        # Find k = largest integer such that {1, 2, ..., k} ⊆ differences
        k = 0
        for v in range(1, max_diff + 2):
            if v not in differences:
                k = v - 1
                break
        else:
            k = max_diff

        if k == 0:
            # 1 is not representable as a difference
            return {
                "score": 0.0,
                "valid": True,
                "error": "Difference 1 is not achievable",
                "metrics": {"n": n, "k": 0, "score": 0.0},
            }

        score = float(k) / float(n * n)

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {
                "n": n,
                "k": k,
                "n_sq_over_k": float(n * n) / float(k),
                "score": score,
            },
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
