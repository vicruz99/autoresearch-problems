"""Evaluator for the Spherical t-design problem (n=24, t=7)."""
import numpy as np

try:
    from scipy.special import eval_gegenbauer
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def evaluate(output: object, n: int = 24, t: int = 7, **kwargs) -> dict:
    if not HAS_SCIPY:
        return {"score": 0.0, "valid": False, "error": "scipy required", "metrics": {}}
    try:
        pts = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
    if pts.ndim != 2 or pts.shape != (n, 3):
        return {"score": 0.0, "valid": False,
                "error": f"Expected ({n}, 3), got {pts.shape}", "metrics": {}}

    # Project to unit sphere
    norms = np.linalg.norm(pts, axis=1, keepdims=True)
    if np.any(norms < 1e-10):
        return {"score": 0.0, "valid": False, "error": "Some points near origin", "metrics": {}}
    pts = pts / norms

    # Check t-design: for each degree k=1..t, the empirical average of
    # Gegenbauer polynomial C_k^(1/2)(p_i · p_j) over all pairs (including i=j) should be 0
    max_error = 0.0
    gegenbauer_errors = {}
    dots = pts @ pts.T  # (n, n)
    np.clip(dots, -1.0, 1.0, out=dots)

    for k in range(1, t + 1):
        vals = eval_gegenbauer(k, 0.5, dots.flatten())
        avg = float(np.mean(vals))
        gegenbauer_errors[k] = abs(avg)
        max_error = max(max_error, abs(avg))

    score = -max_error
    return {"score": score, "valid": True, "error": "",
            "metrics": {"max_gegenbauer_error": max_error,
                        "errors_by_degree": gegenbauer_errors}}
