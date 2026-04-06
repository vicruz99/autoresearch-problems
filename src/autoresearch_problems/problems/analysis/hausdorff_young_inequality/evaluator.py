# Adapted from google-deepmind/alphaevolve_repository_of_problems (Apache 2.0)
"""Evaluator for the Hausdorff-Young inequality problem.

The candidate solve() function returns a 1-D numpy array of shape (2*J,)
representing the values of a function f on the grid
    xs = np.linspace(-R1, (J-1)*R1/J, 2*J)
with R1=5.0, J=500 by default.

The evaluator:
  1. Computes the L^p norm of f via the piecewise-constant approximation.
  2. Computes the Fourier transform f_hat of the piecewise-constant
     approximation analytically.
  3. Computes the L^q norm of f_hat via composite Gauss-Legendre quadrature.
  4. Returns score = ||f_hat||_{L^q} / ||f||_{L^p}.

The sharp Babenko-Beckner constant for p=3/2 is ≈ 0.9532, achieved by
Gaussians.  Higher scores are better.
"""

import numpy as np
from numpy.polynomial.legendre import leggauss


def _lq_norm_gauss_legendre(f_hat_fn, r2: float, q: float,
                             n_intervals: int = 100, order: int = 5) -> float:
    """Estimate ||f_hat||_{L^q([-r2,r2])} via composite Gauss-Legendre."""
    nodes, weights = leggauss(order)
    grid = np.linspace(-r2, r2, n_intervals + 1)
    diffs = np.diff(grid)  # (n_intervals,)

    # Sample points: shape (n_intervals, order)
    midpoints = 0.5 * (grid[:-1] + grid[1:])
    sample_pts = midpoints[:, np.newaxis] + 0.5 * diffs[:, np.newaxis] * nodes
    quad_weights = 0.5 * diffs[:, np.newaxis] * weights  # (n_intervals, order)

    xi_flat = sample_pts.ravel()
    vals = np.abs(f_hat_fn(xi_flat)) ** q
    vals = vals.reshape(sample_pts.shape)

    integral = float(np.sum(vals * quad_weights))
    return float(integral ** (1.0 / q))


def evaluate(output, p: float = 1.5, r1: float = 5.0,
             j: int = 500, r2: float = 10.0, **kwargs) -> dict:
    """Score a candidate function for the Hausdorff-Young inequality.

    Parameters
    ----------
    output:
        Numpy array of shape (2*j,) with function values on the grid
        xs = np.linspace(-r1, (j-1)*r1/j, 2*j).
    p, r1, j, r2:
        Problem parameters (see spec.yaml).

    Returns
    -------
    dict with keys: score (float), valid (bool), error (str), metrics (dict).
    """
    # Parameter validation
    if not (1 < p <= 2):
        return {"score": 0.0, "valid": False,
                "error": f"p must satisfy 1 < p <= 2, got p={p}", "metrics": {}}
    if r1 <= 0:
        return {"score": 0.0, "valid": False,
                "error": f"r1 must be positive, got r1={r1}", "metrics": {}}
    if not (isinstance(j, int) or (isinstance(j, float) and j == int(j))) or int(j) < 1:
        return {"score": 0.0, "valid": False,
                "error": f"j must be a positive integer, got j={j}", "metrics": {}}
    j = int(j)
    if r2 <= 0:
        return {"score": 0.0, "valid": False,
                "error": f"r2 must be positive, got r2={r2}", "metrics": {}}

    try:
        q = p / (p - 1.0)  # conjugate exponent: 1/p + 1/q = 1

        try:
            f_values = np.asarray(output, dtype=float).ravel()
        except Exception as exc:
            return {"score": 0.0, "valid": False,
                    "error": f"Cannot convert output to array: {exc}",
                    "metrics": {}}

        expected_len = 2 * j
        if f_values.shape != (expected_len,):
            return {"score": 0.0, "valid": False,
                    "error": f"Expected shape ({expected_len},), got {f_values.shape}",
                    "metrics": {}}

        if not np.isfinite(f_values).all():
            return {"score": 0.0, "valid": False,
                    "error": "f_values contains NaN or Inf", "metrics": {}}

        if np.max(np.abs(f_values)) > 1e2:
            return {"score": 0.0, "valid": False,
                    "error": "Function values exceed 100 (too large)", "metrics": {}}

        # Grid: xs[k] = -r1 + k*(r1/j), k=0,...,2j-1
        # Extended grid for interval boundaries: [xs[0], xs[1], ..., xs[2j-1], r1]
        extended_xs = np.linspace(-r1, r1, 2 * j + 1)

        # L^p norm of piecewise-constant approximation
        dx = r1 / j
        lp_norm = float((np.sum(np.abs(f_values) ** p) * dx) ** (1.0 / p))

        if lp_norm < 1e-15:
            return {"score": 0.0, "valid": True,
                    "error": "Function is essentially zero",
                    "metrics": {"lp_norm": 0.0, "lq_norm": 0.0}}

        # Fourier transform of piecewise-constant approximation
        def f_hat(xi_array: np.ndarray) -> np.ndarray:
            xi = np.atleast_1d(np.asarray(xi_array, dtype=float))
            # Avoid division by zero near xi=0
            xi_safe = np.where(np.abs(xi) < 1e-12,
                               np.sign(xi + 1e-15) * 1e-12, xi)
            # exp_next[i,k] = exp(-2πi·xi[i]·extended_xs[k+1])
            exp_next = np.exp(-2j * np.pi * np.outer(xi_safe, extended_xs[1:]))
            exp_curr = np.exp(-2j * np.pi * np.outer(xi_safe, extended_xs[:-1]))
            # Analytic integral of exp(-2πi·xi·t) over [x_k, x_{k+1}]
            factor = (exp_next - exp_curr) / (-2j * np.pi * xi_safe[:, np.newaxis])
            return np.sum(f_values[np.newaxis, :] * factor, axis=1)

        # Sanity check: f_hat should not be too large
        test_xi = np.linspace(-15.0, 15.0, 50)
        if np.max(np.abs(f_hat(test_xi))) > 1e2:
            return {"score": 0.0, "valid": False,
                    "error": "Fourier transform exceeds 100 (too large)",
                    "metrics": {}}

        # L^q norm of f_hat over [-r2, r2]
        lq_norm = _lq_norm_gauss_legendre(f_hat, r2, q)

        ratio = float(lq_norm / lp_norm)

        return {
            "score": ratio,
            "valid": True,
            "error": "",
            "metrics": {
                "lp_norm": float(lp_norm),
                "lq_norm": float(lq_norm),
                "ratio": ratio,
            },
        }

    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
