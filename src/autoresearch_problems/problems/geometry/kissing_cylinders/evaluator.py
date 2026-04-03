"""Evaluator for the Kissing Cylinders problem."""
import numpy as np


def _dist_between_lines(p1, v1, p2, v2):
    """Distance between two infinite lines."""
    cross = np.cross(v1, v2)
    norm_cross = np.linalg.norm(cross)
    if norm_cross < 1e-9:  # parallel
        return float(np.linalg.norm(np.cross(p2 - p1, v1)))
    return float(abs(np.dot(p2 - p1, cross)) / norm_cross)


def evaluate(output: object, n_cylinders: int = 7, **kwargs) -> dict:
    try:
        arr = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
    if arr.ndim != 2 or arr.shape != (n_cylinders, 6):
        return {"score": 0.0, "valid": False,
                "error": f"Expected ({n_cylinders}, 6), got {arr.shape}", "metrics": {}}

    # Central cylinder: along Z axis through origin
    p0 = np.array([0.0, 0.0, 0.0])
    v0 = np.array([0.0, 0.0, 1.0])

    total_penalty = 0.0
    dists = []
    for i in range(n_cylinders):
        p = arr[i, :3]
        v = arr[i, 3:]
        v_norm = np.linalg.norm(v)
        if v_norm < 1e-10:
            return {"score": 0.0, "valid": False,
                    "error": f"Cylinder {i} has zero direction vector", "metrics": {}}
        v = v / v_norm
        d = _dist_between_lines(p0, v0, p, v)
        dists.append(d)
        total_penalty += (d - 2.0) ** 2

    score = -total_penalty
    return {"score": score, "valid": True, "error": "",
            "metrics": {"distances_to_central": dists, "penalty": total_penalty}}
