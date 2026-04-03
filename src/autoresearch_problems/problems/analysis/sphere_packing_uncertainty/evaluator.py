"""Evaluator for the Sphere Packing Uncertainty Principle problem."""
import numpy as np

try:
    from scipy.special import eval_genlaguerre
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def _build_laguerre_combination(m, n_dim, zs):
    """Build a function g as a combination of Laguerre polynomials with double zeros at zs."""
    alpha = n_dim / 2.0 - 1.0
    # Use odd-degree Laguerre polynomials L_{2k+1}^alpha, k=0,1,...
    num_terms = 2 * m + 2
    degrees = [2 * k + 1 for k in range(num_terms)]

    # Build constraints: g(0)=0, g'(0)=1, and g(z_i)=0, g'(z_i)=0 for each z_i
    num_eq = 2 + 2 * m
    A = np.zeros((num_eq, num_terms))
    b = np.zeros(num_eq)
    b[1] = 1.0  # g'(0) = 1

    for j, d in enumerate(degrees):
        # g(0) = L_d^alpha(0)
        A[0, j] = eval_genlaguerre(d, alpha, 0.0)
        # g'(0) = -L_{d-1}^{alpha+1}(0) (derivative formula)
        A[1, j] = -eval_genlaguerre(d - 1, alpha + 1, 0.0)

    for i, z in enumerate(zs):
        for j, d in enumerate(degrees):
            A[2 + 2 * i, j] = eval_genlaguerre(d, alpha, z)
            A[2 + 2 * i + 1, j] = -eval_genlaguerre(d - 1, alpha + 1, z)

    coeffs, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

    def g(x_vals):
        x_vals = np.asarray(x_vals)
        result = np.zeros_like(x_vals, dtype=float)
        for j, d in enumerate(degrees):
            result += coeffs[j] * eval_genlaguerre(d, alpha, x_vals)
        return result

    return g


def evaluate(output: object, m: int = 10, n_dim: int = 25, **kwargs) -> dict:
    if not HAS_SCIPY:
        return {"score": 0.0, "valid": False, "error": "scipy required", "metrics": {}}
    try:
        zs = np.asarray(output, dtype=float).flatten()
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
    if len(zs) != m:
        return {"score": 0.0, "valid": False,
                "error": f"Expected {m} roots, got {len(zs)}", "metrics": {}}
    if np.any(zs <= 0) or np.any(zs > 300):
        return {"score": 0.0, "valid": False,
                "error": "Roots must be in (0, 300]", "metrics": {}}
    if len(zs) != len(np.unique(zs)):
        return {"score": 0.0, "valid": False, "error": "Roots must be distinct", "metrics": {}}

    try:
        zs_sorted = np.sort(zs)
        g = _build_laguerre_combination(m, n_dim, zs_sorted)

        x_vals = np.linspace(0.01, float(zs_sorted[-1]) * 2, 3000)
        g_vals = g(x_vals)

        # Find sign changes (zeros)
        sign_diff = np.diff(np.sign(g_vals))
        sign_change_idx = np.where(sign_diff != 0)[0]
        if len(sign_change_idx) == 0:
            return {"score": 0.0, "valid": True, "error": "No sign changes found",
                    "metrics": {"num_sign_changes": 0}}

        largest_sc = float(x_vals[sign_change_idx[-1] + 1])
        return {"score": largest_sc, "valid": True, "error": "",
                "metrics": {"largest_sign_change": largest_sc,
                             "num_sign_changes": len(sign_change_idx)}}
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
