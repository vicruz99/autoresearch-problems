"""Evaluator for the Erdős–Szekeres Happy Ending Problem.

The Erdős–Szekeres theorem states that any set of 2^(n-2)+1 points in general
position (no three collinear) in the plane must contain a convex n-gon.

The goal is to find a configuration of exactly 2^(n-2)+1 points that minimises
the total count of convex n-gons among them.  Score = -(total_ngons); higher
is better (score 0 would be a counterexample to the theorem, which is
impossible — but scores close to 0 are configurations with very few n-gons).

solve() must return a 2-D float array of shape (2^(n-2)+1, 2).

Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0).
"""

import math

import numpy as np

_COLLINEARITY_THRESHOLD = 1e-9  # |2*signed_area| below this → collinear
_PROXIMITY_THRESHOLD = 1e-12    # squared distance below this → overlapping


def _count_convex_ngons(points: np.ndarray, n: int) -> int:
    """Count the number of convex n-gons in *points* using a DP approach.

    The algorithm:
    - Sort points lexicographically.
    - For each pivot P[i], sort the remaining points by angle around P[i].
    - Build a DP table dp[length][j][k] counting convex chains of `length`
      vertices ending with edges Q[k]→Q[j], starting from pivot.
    - Close the polygon and accumulate the count.

    Time complexity: O(N^2 * N^(n-2)) which is manageable for small n and N.
    """
    pts = sorted(map(tuple, points))
    num_pts = len(pts)
    total = 0

    def orient(p, q, r):
        """Signed orientation: >0 left turn, <0 right turn, 0 collinear."""
        return (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])

    for i in range(num_pts):
        pivot = pts[i]
        rest = [pts[j] for j in range(i + 1, num_pts)]
        if len(rest) < n - 1:
            continue

        rest_sorted = sorted(rest,
                             key=lambda p: math.atan2(p[1] - pivot[1],
                                                      p[0] - pivot[0]))
        M = len(rest_sorted)

        # dp[k][j] = number of convex chains of length k ending at index j
        # (the "previous" vertex is implicitly tracked via prev arrays)
        # We use a dict-based DP: dp[length] is a 2D array dp[k, j]
        # encoding chains. But for counting (not reconstruction) we can use
        # dp[length][prev_k][j] as in the notebook.
        dp = np.zeros((n + 1, M, M), dtype=np.int64)

        # Initialise length-3 chains: pivot → Q[k] → Q[j] with left turn
        for j in range(M):
            for k in range(j):
                if orient(pivot, rest_sorted[k], rest_sorted[j]) > 0:
                    dp[3, k, j] = 1

        # Extend to longer chains
        for length in range(4, n + 1):
            for j in range(M):
                for k in range(j):
                    if not np.any(dp[length - 1, :k, k]):
                        continue
                    for pk in range(k):
                        if (dp[length - 1, pk, k] > 0 and
                                orient(rest_sorted[pk],
                                       rest_sorted[k],
                                       rest_sorted[j]) > 0):
                            dp[length, k, j] += dp[length - 1, pk, k]

        # Close the polygon: check the final turn back to pivot
        for j in range(M):
            for k in range(j):
                if (dp[n, k, j] > 0 and
                        orient(rest_sorted[k], rest_sorted[j], pivot) > 0):
                    total += dp[n, k, j]

    return total


def evaluate(output, n: int = 6, **kwargs) -> dict:
    """Score a candidate point configuration for the Happy Ending problem.

    Parameters
    ----------
    output:
        Float array of shape (2^(n-2)+1, 2).
    n:
        Target convex polygon size (default 6).

    Returns
    -------
    dict
        score   : -(number of convex n-gons); higher is better.
        valid   : True iff the configuration is well-formed and in general position.
        error   : description of the first error, or ''.
        metrics : dict with num_points, num_ngons, etc.
    """
    if not (isinstance(n, int) or (isinstance(n, float) and n == int(n))) or int(n) < 3:
        return {"score": 0.0, "valid": False,
                "error": f"n must be a positive integer >= 3, got n={n}", "metrics": {}}
    n = int(n)

    try:
        required = 2 ** (n - 2) + 1

        try:
            pts = np.asarray(output, dtype=float)
        except Exception as exc:
            return {"score": 0.0, "valid": False,
                    "error": f"Cannot convert output to array: {exc}",
                    "metrics": {}}

        if pts.ndim != 2 or pts.shape[1] != 2:
            return {"score": 0.0, "valid": False,
                    "error": f"Expected shape ({required}, 2), got {pts.shape}",
                    "metrics": {}}

        if pts.shape[0] != required:
            return {"score": 0.0, "valid": False,
                    "error": f"Expected {required} points for n={n}, got {pts.shape[0]}",
                    "metrics": {}}

        if not np.isfinite(pts).all():
            return {"score": 0.0, "valid": False,
                    "error": "Array contains NaN or Inf", "metrics": {}}

        num_pts = required

        # Proximity check
        for i in range(num_pts):
            for j in range(i + 1, num_pts):
                dx = pts[i, 0] - pts[j, 0]
                dy = pts[i, 1] - pts[j, 1]
                if dx * dx + dy * dy < _PROXIMITY_THRESHOLD:
                    return {"score": float(-1e15), "valid": False,
                            "error": f"Points {i} and {j} are too close",
                            "metrics": {}}

        # Collinearity check (all triples)
        for i in range(num_pts):
            for j in range(i + 1, num_pts):
                for k in range(j + 1, num_pts):
                    area2 = (pts[i, 0] * (pts[j, 1] - pts[k, 1]) +
                             pts[j, 0] * (pts[k, 1] - pts[i, 1]) +
                             pts[k, 0] * (pts[i, 1] - pts[j, 1]))
                    if abs(area2) < _COLLINEARITY_THRESHOLD:
                        return {"score": float(-1e15), "valid": False,
                                "error": (f"Points {i}, {j}, {k} are nearly "
                                          f"collinear (|2*area|={abs(area2):.2e})"),
                                "metrics": {}}

        ngon_count = _count_convex_ngons(pts, n)
        score = float(-ngon_count)

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {
                "num_points": num_pts,
                "n": n,
                "num_ngons": ngon_count,
            },
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
