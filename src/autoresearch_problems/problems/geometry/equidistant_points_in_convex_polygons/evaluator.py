"""Evaluator for the Equidistant Points in Convex Polygons problem.

The problem asks: does every convex polygon have at least one vertex v with
no 4 other vertices equidistant from v?  The goal is to find a convex polygon
that is a counterexample, i.e. every vertex has (approximately) 4 equidistant
neighbours.

solve() must return a 2-D float array of shape (num_vertex, 2) giving the
vertices of the candidate polygon in order.

Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0).
"""

import math

import numpy as np


# ---------------------------------------------------------------------------
# Convexity check
# ---------------------------------------------------------------------------

def _is_convex_polygon(polygon: list) -> bool:
    """Return True iff the sequence of 2-D points forms a strictly convex polygon."""
    try:
        n = len(polygon)
        if n < 3:
            return False
        if len(set(tuple(p) for p in polygon)) != n:
            return False  # duplicate vertices

        pts = [tuple(p) for p in polygon]
        old_x, old_y = pts[-2]
        new_x, new_y = pts[-1]
        new_dir = math.atan2(new_y - old_y, new_x - old_x)
        angle_sum = 0.0
        orientation = 0.0

        for idx, (px, py) in enumerate(pts):
            old_x, old_y, old_dir = new_x, new_y, new_dir
            new_x, new_y = px, py
            new_dir = math.atan2(new_y - old_y, new_x - old_x)

            if old_x == new_x and old_y == new_y:
                return False  # zero-length side

            angle = new_dir - old_dir
            if angle <= -math.pi:
                angle += 2 * math.pi
            elif angle > math.pi:
                angle -= 2 * math.pi

            if angle == 0.0:
                return False  # collinear vertices

            if idx == 0:
                orientation = 1.0 if angle > 0.0 else -1.0
            elif orientation * angle <= 0.0:
                return False  # inconsistent turning direction

            angle_sum += angle

        return abs(round(angle_sum / (2 * math.pi))) == 1
    except (ArithmeticError, TypeError, ValueError, IndexError):
        return False


# ---------------------------------------------------------------------------
# Per-vertex score
# ---------------------------------------------------------------------------

def _vertex_score(vertex_idx: int, pts: list) -> float:
    """Score for a single vertex: how close is it to having 4 equidistant neighbours.

    Returns a value in [0, 1].  Returns 0 if the configuration is degenerate.
    Returns -1 as an error sentinel.
    """
    n = len(pts)
    if n < 5:
        return 0.0

    v = np.array(pts[vertex_idx], dtype=float)
    dists = []
    for i, p in enumerate(pts):
        if i == vertex_idx:
            continue
        d = float(np.linalg.norm(v - np.array(p, dtype=float)))
        if d < 5e-2:
            return 0.0  # overlapping point
        dists.append(d)

    if len(dists) != n - 1:
        return -1.0

    dists.sort()
    nd = len(dists)

    # Find the minimum gap between consecutive distances
    min_gap = float('inf')
    min_k = -1
    for k in range(nd - 1):
        gap = dists[k + 1] - dists[k]
        if gap < min_gap:
            min_gap = gap
            min_k = k

    if min_k == -1:
        return 0.0

    d_k = dists[min_k]
    d_k1 = dists[min_k + 1]
    D_v = (d_k + d_k1) / 2.0
    if D_v < 1e-1:
        return 0.0

    # Pick 4 indices centred around the minimum gap
    k = min_k
    if k == 0:
        sel = [0, 1, 2, 3]
    elif k == nd - 2:
        sel = [nd - 4, nd - 3, nd - 2, nd - 1]
    else:
        sel = [k - 1, k, k + 1, k + 2]

    sel = [i for i in sel if 0 <= i < nd]
    if len(sel) < 4:
        # Fallback: centre as best we can
        start = max(0, min(k - 1, nd - 4))
        sel = list(range(start, start + 4))
    if len(sel) < 4:
        return 0.0

    try:
        d0, d1, d2, d3 = dists[sel[0]], dists[sel[1]], dists[sel[2]], dists[sel[3]]
    except IndexError:
        return 0.0

    if d0 < 1e-2 or d1 < 1e-2:
        return 0.0

    def _ratio(a: float, b: float) -> float:
        return max(a / b, b / a) if b > 1e-12 else float('inf')

    raw = (_ratio(d0, D_v) + _ratio(d1, D_v) + _ratio(d2, D_v) + _ratio(d3, D_v)) / 4.0
    if raw < 1e-2:
        return 0.0

    return max(0.0, min(1.0, 1.0 / raw))


# ---------------------------------------------------------------------------
# Public entry-point
# ---------------------------------------------------------------------------

def evaluate(output, num_vertex: int = 10, **kwargs) -> dict:
    """Score a candidate convex polygon for the equidistant-vertices problem.

    Parameters
    ----------
    output:
        Array-like of shape (num_vertex, 2) giving polygon vertices in order.
    num_vertex:
        Expected number of vertices.

    Returns
    -------
    dict
        score  : minimum per-vertex equidistance score in [0, 1].
        valid  : True iff the polygon is strictly convex and well-formed.
        error  : description of the first error, or ''.
        metrics: dict with per-vertex scores and additional info.
    """
    if not (isinstance(num_vertex, int) or (isinstance(num_vertex, float) and num_vertex == int(num_vertex))) or int(num_vertex) < 3:
        return {"score": 0.0, "valid": False,
                "error": f"num_vertex must be a positive integer >= 3, got num_vertex={num_vertex}",
                "metrics": {}}
    num_vertex = int(num_vertex)

    try:
        coords = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False,
                "error": f"Cannot convert output to array: {exc}", "metrics": {}}

    if coords.ndim != 2 or coords.shape != (num_vertex, 2):
        return {"score": 0.0, "valid": False,
                "error": f"Expected shape ({num_vertex}, 2), got {coords.shape}",
                "metrics": {}}

    if not np.isfinite(coords).all():
        return {"score": 0.0, "valid": False,
                "error": "Array contains NaN or Inf", "metrics": {}}

    # Normalise: centre and scale so average distance to centroid == 1
    centroid = coords.mean(axis=0)
    centered = coords - centroid
    avg_dist = float(np.linalg.norm(centered, axis=1).mean())
    if avg_dist < 1e-3:
        return {"score": 0.0, "valid": False,
                "error": "Polygon has near-zero extent", "metrics": {}}
    scaled = centered / avg_dist

    pts = [tuple(row) for row in scaled]

    if not _is_convex_polygon(pts):
        return {"score": 0.0, "valid": False,
                "error": "Polygon is not strictly convex", "metrics": {}}

    if num_vertex < 5:
        return {"score": 0.0, "valid": False,
                "error": "num_vertex must be >= 5", "metrics": {}}

    vertex_scores = []
    for i in range(num_vertex):
        vs = _vertex_score(i, pts)
        if vs < 0:
            return {"score": 0.0, "valid": False,
                    "error": f"Error computing score for vertex {i}", "metrics": {}}
        vertex_scores.append(vs)

    min_score = float(min(vertex_scores))
    return {
        "score": min_score,
        "valid": True,
        "error": "",
        "metrics": {
            "min_vertex_score": min_score,
            "mean_vertex_score": float(np.mean(vertex_scores)),
            "vertex_scores": vertex_scores,
        },
    }
