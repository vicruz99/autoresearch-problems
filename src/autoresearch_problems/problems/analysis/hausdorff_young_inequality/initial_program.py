import numpy as np

# Fixed grid parameters (must match evaluator)
R1 = 5.0
J = 500


def solve() -> np.ndarray:
    """Return function values on grid xs = np.linspace(-R1, (J-1)*R1/J, 2*J).

    The evaluator computes the Hausdorff-Young quotient
        Q(f) = ||f_hat||_{L^q} / ||f||_{L^p}  (p=1.5, q=3)
    from these values.  The optimal function is a Gaussian.

    Returns
    -------
    np.ndarray of shape (2*J,) = (1000,)
    """
    xs = np.linspace(-R1, (J - 1) * R1 / J, 2 * J)

    # EVOLVE-BLOCK-START
    # Double-exponential (Laplace) function — not optimal.
    # The optimal function for the Hausdorff-Young inequality is a Gaussian.
    f_values = np.exp(-np.abs(xs))
    # EVOLVE-BLOCK-END

    return f_values
