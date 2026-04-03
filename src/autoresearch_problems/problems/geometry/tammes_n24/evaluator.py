"""Evaluator for the Tammes problem with n=24 points."""
import numpy as np


def evaluate(output: object, n: int = 24, **kwargs) -> dict:
    try:
        pts = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": f"Cannot convert output to array: {exc}", "metrics": {}}
    if pts.ndim != 2 or pts.shape != (n, 3):
        return {"score": 0.0, "valid": False, "error": f"Expected shape ({n}, 3), got {pts.shape}", "metrics": {}}
    norms = np.linalg.norm(pts, axis=1, keepdims=True)
    if np.any(norms < 1e-10):
        return {"score": 0.0, "valid": False, "error": "Some points are near the origin", "metrics": {}}
    pts = pts / norms
    diff = pts[:, None, :] - pts[None, :, :]
    dist = np.sqrt((diff ** 2).sum(axis=-1))
    np.fill_diagonal(dist, np.inf)
    min_dist = float(dist.min())
    return {"score": min_dist, "valid": True, "error": "", "metrics": {"min_pairwise_distance": min_dist}}
