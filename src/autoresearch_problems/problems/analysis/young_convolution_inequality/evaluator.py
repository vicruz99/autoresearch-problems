# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for Young's convolution inequality problem.

The candidate solve() function returns a 2-D numpy array of shape (2, 2*J)
where row 0 contains values of f and row 1 contains values of g on the grid
    xs = np.linspace(-R1, (J-1)*R1/J, 2*J)
with R1=10.0, J=500 by default.

The evaluator computes Young's convolution quotient:
    Q(f, g) = ||f * g||_{L^r} / (||f||_{L^p} * ||g||_{L^q})
where p=4/3, q=7/5 and 1/r = 1/p + 1/q - 1 (so r = 28/13 ≈ 2.154).

The L^p norms are computed from the piecewise-constant approximation.
The convolution uses numpy's 'same' mode with the same grid spacing.
Higher scores are better; the optimum (Gaussians) achieves a value ≈ 1.
"""

import numpy as np


def evaluate(output, p: float = 4.0 / 3.0, q: float = 1.4,
             r1: float = 10.0, j: int = 500, **kwargs) -> dict:
    """Score candidate functions f, g for Young's convolution inequality.

    Parameters
    ----------
    output:
        Numpy array of shape (2, 2*j) where row 0 = f values, row 1 = g values
        on the grid xs = np.linspace(-r1, (j-1)*r1/j, 2*j).
    p, q, r1, j:
        Problem parameters (see spec.yaml).

    Returns
    -------
    dict with keys: score (float), valid (bool), error (str), metrics (dict).
    """
    # Parameter validation
    if p <= 1:
        return {"score": 0.0, "valid": False,
                "error": f"p must be > 1, got p={p}", "metrics": {}}
    if q <= 1:
        return {"score": 0.0, "valid": False,
                "error": f"q must be > 1, got q={q}", "metrics": {}}
    if 1.0 / p + 1.0 / q < 1.0 - 1e-12:
        return {"score": 0.0, "valid": False,
                "error": f"Young's convolution requires 1/p + 1/q >= 1, got {1.0/p + 1.0/q:.6f}",
                "metrics": {}}
    if r1 <= 0:
        return {"score": 0.0, "valid": False,
                "error": f"r1 must be positive, got r1={r1}", "metrics": {}}
    if not (isinstance(j, int) or (isinstance(j, float) and j == int(j))) or int(j) < 1:
        return {"score": 0.0, "valid": False,
                "error": f"j must be a positive integer, got j={j}", "metrics": {}}
    j = int(j)

    try:
        r = 1.0 / (1.0 / p + 1.0 / q - 1.0)  # r = 28/13 ≈ 2.154

        try:
            arr = np.asarray(output, dtype=float)
        except Exception as exc:
            return {"score": 0.0, "valid": False,
                    "error": f"Cannot convert output to array: {exc}",
                    "metrics": {}}

        expected_shape = (2, 2 * j)
        if arr.shape != expected_shape:
            return {"score": 0.0, "valid": False,
                    "error": f"Expected shape {expected_shape}, got {arr.shape}",
                    "metrics": {}}

        if not np.isfinite(arr).all():
            return {"score": 0.0, "valid": False,
                    "error": "Array contains NaN or Inf", "metrics": {}}

        if np.max(np.abs(arr)) > 1e3:
            return {"score": 0.0, "valid": False,
                    "error": "Values exceed 1e3 (too large)", "metrics": {}}

        f_values = arr[0]
        g_values = arr[1]

        dx = r1 / j  # grid spacing

        # L^p, L^q norms via piecewise-constant approximation
        lp_norm = float((np.sum(np.abs(f_values) ** p) * dx) ** (1.0 / p))
        lq_norm = float((np.sum(np.abs(g_values) ** q) * dx) ** (1.0 / q))

        if lp_norm < 1e-8:
            return {"score": 0.0, "valid": True,
                    "error": "f is essentially zero",
                    "metrics": {"lp_norm": 0.0, "lq_norm": float(lq_norm)}}

        if lq_norm < 1e-8:
            return {"score": 0.0, "valid": True,
                    "error": "g is essentially zero",
                    "metrics": {"lp_norm": float(lp_norm), "lq_norm": 0.0}}

        # Discrete convolution (f * g)(x) ≈ sum_k f(x - x_k) g(x_k) * dx
        conv = np.convolve(f_values, g_values, mode="same") * dx

        # L^r norm of convolution
        lr_norm = float((np.sum(np.abs(conv) ** r) * dx) ** (1.0 / r))

        ratio = float(lr_norm / (lp_norm * lq_norm))

        return {
            "score": ratio,
            "valid": True,
            "error": "",
            "metrics": {
                "lp_norm": float(lp_norm),
                "lq_norm": float(lq_norm),
                "lr_norm_conv": float(lr_norm),
                "ratio": ratio,
                "r": float(r),
            },
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
