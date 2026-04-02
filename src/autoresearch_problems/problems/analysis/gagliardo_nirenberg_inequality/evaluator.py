# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the Gagliardo-Nirenberg inequality problem.

The candidate solve() function returns a 1-D numpy array of shape (2*J+1,)
representing the values of a function f on the symmetric grid
    xs = np.linspace(-R1, R1, 2*J+1)
with R1=15.0, J=500 by default.

The evaluator computes the Gagliardo-Nirenberg quotient:
    Q(f) = ||f||_p^{4p} / (||f||_2^{2(p+2)} * ||f'||_2^{2(p-2)})
using the trapezoidal rule for L^p norms and central finite differences for
the derivative. Higher scores are better.

For p=4, the optimal function is f(x) = 1/cosh(x) = sech(x), which gives
Q(sech) = 1/9 ≈ 0.1111.
"""

import numpy as np


def evaluate(output, p: float = 4.0, r1: float = 15.0,
             j: int = 500, **kwargs) -> dict:
    """Score a candidate function for the Gagliardo-Nirenberg inequality.

    Parameters
    ----------
    output:
        Numpy array of shape (2*j+1,) with function values on the grid
        xs = np.linspace(-r1, r1, 2*j+1).
    p, r1, j:
        Problem parameters (see spec.yaml).

    Returns
    -------
    dict with keys: score (float), valid (bool), error (str), metrics (dict).
    """
    try:
        try:
            f_values = np.asarray(output, dtype=float).ravel()
        except Exception as exc:
            return {"score": 0.0, "valid": False,
                    "error": f"Cannot convert output to array: {exc}",
                    "metrics": {}}

        expected_len = 2 * j + 1
        if f_values.shape != (expected_len,):
            return {"score": 0.0, "valid": False,
                    "error": f"Expected shape ({expected_len},), got {f_values.shape}",
                    "metrics": {}}

        if not np.isfinite(f_values).all():
            return {"score": 0.0, "valid": False,
                    "error": "f_values contains NaN or Inf", "metrics": {}}

        if np.max(np.abs(f_values)) > 1e5:
            return {"score": 0.0, "valid": False,
                    "error": "Function values exceed 1e5 (too large)", "metrics": {}}

        xs = np.linspace(-r1, r1, 2 * j + 1)
        dx = xs[1] - xs[0]

        # Derivative via central finite differences (numpy gradient)
        df_values = np.gradient(f_values, dx)

        # L^p norm (trapezoidal rule; np.trapezoid is the np>=2.0 name)
        _trapz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
        lp_norm = float(_trapz(np.abs(f_values) ** p, xs) ** (1.0 / p))

        # L^2 norms of f and f'
        l2_norm_f = float(_trapz(f_values ** 2, xs) ** 0.5)
        l2_norm_df = float(_trapz(df_values ** 2, xs) ** 0.5)

        if l2_norm_f < 1e-8:
            return {"score": 0.0, "valid": True,
                    "error": "Function is essentially zero",
                    "metrics": {"lp_norm": lp_norm, "l2_norm_f": 0.0,
                                "l2_norm_df": float(l2_norm_df)}}

        if l2_norm_df < 1e-8:
            return {"score": 0.0, "valid": True,
                    "error": "Derivative is essentially zero (constant function)",
                    "metrics": {"lp_norm": lp_norm, "l2_norm_f": float(l2_norm_f),
                                "l2_norm_df": 0.0}}

        # Q(f) = ||f||_p^{4p} / (||f||_2^{2(p+2)} * ||f'||_2^{2(p-2)})
        numerator = lp_norm ** (4.0 * p)
        denominator = (l2_norm_f ** (2.0 * (p + 2.0))) * (l2_norm_df ** (2.0 * (p - 2.0)))

        if denominator == 0.0:
            return {"score": 0.0, "valid": False,
                    "error": "Denominator is zero", "metrics": {}}

        score = float(numerator / denominator)

        return {
            "score": score,
            "valid": True,
            "error": "",
            "metrics": {
                "lp_norm": float(lp_norm),
                "l2_norm_f": float(l2_norm_f),
                "l2_norm_df": float(l2_norm_df),
                "score": score,
            },
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
