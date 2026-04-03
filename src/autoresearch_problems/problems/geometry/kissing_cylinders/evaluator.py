"""Evaluator for the Kissing Cylinders problem.

Matches kissing_cylinders.ipynb Cell 1: calculate_arrangement_score_numba.

The score is -sum_{i<j} (dist(axis_i, axis_j) - 2.0)^2 for all pairs.
Input: (n_cylinders, 6) array where each row is [p0, p1, p2, v0, v1, v2]
(point on axis closest to origin, and unit direction vector).
"""
import numpy as np


def _dist_between_lines(p1, v1, p2, v2):
    """Shortest distance between two infinite lines."""
    cross = np.cross(v1, v2)
    norm_cross = np.linalg.norm(cross)
    if norm_cross < 1e-9:  # parallel lines
        return float(np.linalg.norm(np.cross(p2 - p1, v1)))
    return float(abs(np.dot(p2 - p1, cross)) / norm_cross)


def evaluate(output: object, n_cylinders: int = 7, target_dist: float = 2.0,
             contact_box_limit: float = 100.0, **kwargs) -> dict:
    """Score a candidate cylinder arrangement.

    Parameters
    ----------
    output : array-like of shape (n_cylinders, 6)
        Each row is [p0, p1, p2, v0, v1, v2] — point on axis (closest to origin)
        and direction vector.
    n_cylinders : int
        Expected number of cylinders (default 7).
    target_dist : float
        Target axis-to-axis distance for tangency (default 2.0 for unit cylinders).
    contact_box_limit : float
        Midpoints of closest approach must lie within this box (default 100.0).

    Returns
    -------
    dict with keys: score, valid, error, metrics.
        score = -sum_{i<j} (d_{ij} - target_dist)^2  (0 is perfect, negative otherwise).
    """
    try:
        arr = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": -np.inf, "valid": False, "error": str(exc), "metrics": {}}
    if arr.ndim != 2 or arr.shape != (n_cylinders, 6):
        return {"score": -np.inf, "valid": False,
                "error": f"Expected ({n_cylinders}, 6), got {arr.shape}", "metrics": {}}

    if not np.all(np.isfinite(arr)):
        return {"score": -np.inf, "valid": False,
                "error": "Non-finite values in input", "metrics": {}}

    # Extract and validate cylinders
    ps = []
    vs = []
    for i in range(n_cylinders):
        p = arr[i, :3]
        v = arr[i, 3:]
        v_norm = np.linalg.norm(v)
        if v_norm < 1e-10:
            return {"score": -np.inf, "valid": False,
                    "error": f"Cylinder {i} has zero direction vector", "metrics": {}}
        v = v / v_norm
        # Standardize p to be the point on the axis closest to origin
        p = p - np.dot(p, v) * v
        ps.append(p)
        vs.append(v)

    # Compute pairwise penalties (all pairs)
    total_penalty = 0.0
    pairwise_dists = []
    for i in range(n_cylinders):
        for j in range(i + 1, n_cylinders):
            d = _dist_between_lines(ps[i], vs[i], ps[j], vs[j])
            pairwise_dists.append(d)
            total_penalty += (d - target_dist) ** 2

            # Check contact point constraint (midpoint of closest approach)
            p1, v1 = ps[i], vs[i]
            p2, v2 = ps[j], vs[j]
            dp = p1 - p2
            v1_dot_v2 = np.dot(v1, v2)
            if abs(abs(v1_dot_v2) - 1.0) < 1e-7:
                # Parallel: midpoint of standardized points
                mid = (p1 + p2) / 2.0
                m = mid - np.dot(mid, v1) * v1
            else:
                denom = 1.0 - v1_dot_v2 ** 2
                dp_dot_v1 = np.dot(dp, v1)
                dp_dot_v2 = np.dot(dp, v2)
                t_c = (v1_dot_v2 * (-dp_dot_v2) - (-dp_dot_v1)) / denom
                s_c = ((-dp_dot_v2) - v1_dot_v2 * (-dp_dot_v1)) / denom
                c1 = p1 + t_c * v1
                c2 = p2 + s_c * v2
                m = (c1 + c2) / 2.0
            if np.any(np.abs(m) > contact_box_limit):
                return {"score": -np.inf, "valid": False,
                        "error": f"Contact point ({i},{j}) outside box", "metrics": {}}

    score = -total_penalty
    return {"score": float(score), "valid": True, "error": "",
            "metrics": {"pairwise_distances": pairwise_dists, "penalty": float(total_penalty)}}
