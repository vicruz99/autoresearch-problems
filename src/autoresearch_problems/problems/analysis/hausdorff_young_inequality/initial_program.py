import numpy as np


def solve(r1: float = 5.0, j: int = 500, **kwargs) -> np.ndarray:
    """Return function values on grid xs = np.linspace(-r1, (j-1)*r1/j, 2*j).

    The evaluator computes the Hausdorff-Young quotient
        Q(f) = ||f_hat||_{L^q} / ||f||_{L^p}  (p=1.5, q=3)
    from these values.  The optimal function is a Gaussian.

    Returns
    -------
    np.ndarray of shape (2*j,)
    """
    j = int(j)
    xs = np.linspace(-r1, (j - 1) * r1 / j, 2 * j)

    # EVOLVE-BLOCK-START
    # Double-exponential (Laplace) function — not optimal.
    # The optimal function for the Hausdorff-Young inequality is a Gaussian.
    f_values = np.exp(-np.abs(xs))
    # EVOLVE-BLOCK-END

    return f_values
