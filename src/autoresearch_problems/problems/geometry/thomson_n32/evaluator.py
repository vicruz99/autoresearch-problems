"""Evaluator for the Thomson problem with n=32 points on the unit sphere."""
import numpy as np


def evaluate(output: object, n: int = 32, **kwargs) -> dict:
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
    # Thomson energy: sum of 1/r_ij for all pairs i < j
    energy = float(np.sum(1.0 / dist) / 2.0)
    score = -energy
    return {"score": score, "valid": True, "error": "", "metrics": {"energy": energy}}
