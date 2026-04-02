"""Evaluator for the Ovals problem (minimize Rayleigh quotient of a convex curve)."""
import numpy as np

try:
    import scipy.interpolate
    import scipy.integrate
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def _make_periodic_spline(vals, n_pts):
    xs = np.linspace(0, 2 * np.pi, n_pts + 1)
    vals_periodic = list(vals) + [vals[0]]
    return scipy.interpolate.make_interp_spline(xs, vals_periodic, k=4, bc_type="periodic")


def evaluate(output: object, n: int = 100, **kwargs) -> dict:
    if not HAS_SCIPY:
        return {"score": 0.0, "valid": False, "error": "scipy not available", "metrics": {}}
    try:
        output = list(output)
        if len(output) != 3:
            return {"score": 0.0, "valid": False, "error": "Output must be [x, y, phi]", "metrics": {}}
        x, y, phi = [np.asarray(v, dtype=float) for v in output]
        if len(x) != n or len(y) != n or len(phi) != n:
            return {"score": 0.0, "valid": False,
                    "error": f"Each array must have length {n}", "metrics": {}}
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}

    try:
        x_fn = _make_periodic_spline(x, n)
        y_fn = _make_periodic_spline(y, n)
        phi_fn = _make_periodic_spline(phi, n)

        dx1 = x_fn.derivative(1)
        dx2 = y_fn.derivative(1)

        ts = np.linspace(0, 2 * np.pi, 10000, endpoint=False)
        speed = np.sqrt(dx1(ts) ** 2 + dx2(ts) ** 2)
        if np.min(speed) < 1e-4:
            return {"score": 0.0, "valid": False,
                    "error": "Curve speed is degenerate (near zero)", "metrics": {}}

        phi_l2, _ = scipy.integrate.quad(
            lambda t: float(phi_fn(t)) ** 2, 0, 2 * np.pi, limit=500)
        if phi_l2 < 1e-6:
            return {"score": 0.0, "valid": False,
                    "error": "phi is degenerate (near zero L2 norm)", "metrics": {}}

        d2x1 = x_fn.derivative(2)
        d2x2 = y_fn.derivative(2)
        d1phi = phi_fn.derivative(1)

        # Check convexity: signed curvature must be positive everywhere
        signed_kappa_vals = dx1(ts) * d2x2(ts) - d2x1(ts) * dx2(ts)
        if np.any(signed_kappa_vals < -1e-6):
            return {"score": 0.0, "valid": False,
                    "error": "Curve is not convex (signed curvature is negative)", "metrics": {}}

        def kappa(t):
            d1 = float(dx1(t)); d2 = float(dx2(t))
            dd1 = float(d2x1(t)); dd2 = float(d2x2(t))
            spd = np.sqrt(d1 ** 2 + d2 ** 2)
            return abs(d1 * dd2 - dd1 * d2) / spd ** 3

        numerator, _ = scipy.integrate.quad(
            lambda t: float(d1phi(t)) ** 2 + (kappa(t) * float(phi_fn(t))) ** 2,
            0, 2 * np.pi, limit=500)

        rayleigh = numerator / phi_l2
        return {"score": -rayleigh, "valid": True, "error": "",
                "metrics": {"rayleigh_quotient": rayleigh}}
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
