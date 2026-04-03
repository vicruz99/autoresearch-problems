"""Evaluator for the Spherical t-design problem (n=24, t=7).

Matches spherical_t_designs.ipynb Cell 1: calculate_design_score.

Score = -total_error where total_error = sum_k dim_k * sum_{ij} C_k(p_i·p_j) / denom_k
"""
import numpy as np

try:
    from scipy.special import gegenbauer, eval_gegenbauer
    from scipy.special import comb as binom
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def _get_dim_k(k: int, d: int) -> float:
    """Dimension of space of spherical harmonics of degree k on S^d."""
    return binom(d + k, k) - binom(d + k - 2, k - 2)


def evaluate(output: object, n: int = 24, t: int = 7, d: int = 2, **kwargs) -> dict:
    """Score a candidate spherical t-design.

    Parameters
    ----------
    output : array-like of shape (n, d+1)
        Points on the unit sphere S^d.
    n, t, d : int
        Number of points, design degree, sphere dimension (S^d in R^{d+1}).

    Returns
    -------
    dict with keys: score, valid, error, metrics.
        score = -total_error (0 is perfect design, negative otherwise).
    """
    if not HAS_SCIPY:
        return {"score": 0.0, "valid": False, "error": "scipy required", "metrics": {}}
    try:
        pts = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
    if pts.ndim != 2 or pts.shape != (n, d + 1):
        return {"score": 0.0, "valid": False,
                "error": f"Expected ({n}, {d+1}), got {pts.shape}", "metrics": {}}

    if np.any(np.isnan(pts)) or np.any(np.isinf(pts)):
        return {"score": 0.0, "valid": False, "error": "Non-finite values", "metrics": {}}

    # Normalize to unit sphere
    norms = np.linalg.norm(pts, axis=1, keepdims=True)
    if np.any(norms < 1e-9):
        return {"score": 0.0, "valid": False, "error": "Some points near origin", "metrics": {}}
    pts = pts / norms

    dot_products = np.clip(pts @ pts.T, -1.0, 1.0)

    total_error = 0.0
    errors_by_degree = {}

    for k in range(1, t + 1):
        dim_k = _get_dim_k(k, d)
        if abs(dim_k) < 1e-9:
            continue

        # Gegenbauer polynomial with lambda = (d-1)/2
        lam = (d - 1) / 2.0
        gegen_poly = gegenbauer(k, lam)

        # Denominator C_k(1) = binom(k + d - 2, k)
        denom = binom(k + d - 2, k)
        if abs(denom) < 1e-9:
            continue

        poly_vals = gegen_poly(dot_products)
        error_k = float(np.sum(poly_vals))
        errors_by_degree[k] = error_k
        total_error += dim_k * error_k / denom

    score = -total_error
    return {"score": float(score), "valid": True, "error": "",
            "metrics": {"total_error": total_error,
                        "errors_by_degree": errors_by_degree}}
