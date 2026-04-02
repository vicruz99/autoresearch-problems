"""Evaluator for the No 5 on a Sphere problem."""
import numpy as np
from itertools import combinations


def evaluate(output: object, n: int = 50, **kwargs) -> dict:
    try:
        pts = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
    if pts.ndim != 2 or pts.shape[1] != 3:
        return {"score": 0.0, "valid": False,
                "error": f"Expected shape (m, 3), got {pts.shape}", "metrics": {}}

    # Project to unit sphere
    norms = np.linalg.norm(pts, axis=1, keepdims=True)
    if np.any(norms < 1e-10):
        return {"score": 0.0, "valid": False, "error": "Some points are near the origin", "metrics": {}}
    pts = pts / norms
    num_pts = len(pts)

    # Check no 5 points lie on a common great circle (i.e., coplanar with origin = rank <= 2)
    for combo in combinations(range(num_pts), 5):
        sub = pts[list(combo)]  # 5x3
        sv = np.linalg.svd(sub, compute_uv=False)
        if sv[2] < 1e-6:  # 3rd singular value near 0 -> rank <= 2 -> coplanar with origin
            return {"score": 0.0, "valid": False,
                    "error": f"5 points on a common great circle: indices {combo}", "metrics": {}}

    score = float(num_pts)
    return {"score": score, "valid": True, "error": "",
            "metrics": {"num_points": num_pts}}
